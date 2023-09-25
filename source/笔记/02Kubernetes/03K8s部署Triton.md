# K8s 部署 Triton

docker版本：24.0.2

k8s版本：1.21.3

## 创建 K8s 部署

第一步是为 Triton 推理服务器创建**Kubernetes部署**。部署为 Pods 和 ReplicaSet 提供声明性更新。Kubernetes 中的 ReplicaSet 同时启动同一 Pod 的多个实例。

以下文件创建了三个 **replicated Pods**，每个 Pod 运行一个名为 **speech** 的容器，该容器运行 ``10.24.83.22:8080/triton_server:v08.30`` 版本 Triton 推理服务器镜像，与 Triton 端口号相同，容器端口 **8000、8001、8002** 分别为 **HTTP、gRPC和 NVIDIA Triton metrics**。

如果没有共享文件系统，则必须确保将**模型加载到所有工作节点**，以便 Kubernetes 启动的 Pods 可以访问

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: speech
  labels:
    app: speech
spec:
  replicas: 1
  selector:
    matchLabels:
      app: speech
  template:
    metadata:
      labels:
        app: speech
    spec:
      volumes:
      - name: dshm
        emptyDir:
          medium: Memory
          sizeLimit: 2048Mi
      nodeName: node01
      containers:
        - name: speech
          ports:
          - containerPort: 8000
            name: http-triton
          - containerPort: 8001
            name: grpc-triton
          - containerPort: 8002
            name: metrics-triton
          image: 10.24.83.22:8080/triton_server:v08.30
          command: ["/bin/bash", "-c"]
          args: ["cd /workspace/speech; bash scripts/convert_start_server.sh;"]
          volumeMounts:
            - mountPath: /dev/shm
              name: dshm
```

使用字段 ``nodeName: node01`` 指定将服务部署到工作节点上执行推理服务，使用 ``kuberctl apply`` 创建 Kubernetes 部署：

```shell
kubectl apply -f speech-replicas2.yml
```

显示 `deployment.apps/speech created`，则表示 k8s 部署创建成功。

若需要删除之前部署的服务，采用 ``kubectl delete`` 命令删除：

```shell
kubectl delete deployment speech
```



> 当创建单机版 k8s 时，这个时候 master 节点默认不允许调度 pod，解决方案是将 master 标记为可调度即可：

## 创建 K8s 服务

第二步是创建一个 K8s 服务，将 Triton 推理服务器作为网络服务公开。创建服务时，使用 `Type` 字段选择自动创建外部负载均衡选项，其提供了一个外部可访问的IP地址，用于将流量发送到节点上的正确端口：

用于创建 K8s 服务的 YAML 文件 `speech-service.yml` 内容如下：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: speech
  labels:
    app: speech
spec:
  selector:
    app: speech
  ports:
    - protocol: TCP
      port: 8000
      name: http
      targetPort: 8000
    - protocol: TCP
      port: 8001
      name: grpc
      targetPort: 8001
    - protocol: TCP
      port: 8002
      name: metrics
      targetPort: 8002
  type: LoadBalancer 
```

使用如下命令创建 K8s 服务

```shell
kubectl apply -f speech-service.yml
```

验证服务创建成功

```shell
kubectl get svc
```

![](../../figs.assets/image-20230321113857175.png)

现在，Triton 推理服务器已准备好接收来自远程客户端的推理请求，如果客户端发送推理请求，则客户端可以查看语音识别的结果。

![](../../figs.assets/image-20230321122629260.png)

至此，多个 Triton 推理服务器在 K8s 环境中运行，对客户端发送的语音进行推理，可以手动更改服务器的数量。在接下来的部分中，对其进行改进，以便可以根据客户端请求自动调整服务器的数量。

## 安装 Prometheus

Prometheus 的安装过程迁移到 [Prometheus 安装教程](https://notebook-lzl.readthedocs.io/zh/latest/%E7%AC%94%E8%AE%B0/02Kubernetes/04%E6%95%B0%E6%8D%AE%E5%8F%AF%E8%A7%86%E5%8C%96.html#prometheus)

## 缩扩容服务

Prometheus在监视服务器，接下来部署Prometheus适配器，它知道如何与Kubernetes和Prometheus通信，适配器能够使用Prometheus收集的指标作出缩放决策。

### 创建 PodMonitor

Prometheus 主要通过 `Pull` 的方式抓取目标服务暴露出来的监控接口，因此需要配置对应的抓取任务来请求对应的监控数据并写入到 Prometheus 提供的存储中，目前 Prometheus 服务提供了如下几个任务的配置：

- 原生 Job 配置：提供 Prometheus 原生抓取 Job 的配置
- Pod Monitor：在 K8s 生态下，基于 Prometheus Operator 来抓取 Pod 上对应的监控数据
- Service Monitor：在 K8s 生态下，基于 Prometheus Operator 来抓取 Service 对应 Endpoints 上的监控数据

在 `speech-pod-monitor.yml` 文件中，定义一个 **PodMonitor** 来监视服务器的pod，如 **spec.selector** 字段所示，还需要 kube-prometheus，包括prometheus的部署，并抓取链接到Prometheus各种度量端点的目标配置，如 **spec.podMetricsEndpoints** 字段所示，Prometheus每隔 10s 从这些端点抓取NVIDIA Triton指标：

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: kube-prometheus-stack-tritonmetrics
  namespace: monitoring
  labels:
      prometheus: k8s
spec:
   selector:
      matchLabels:
         app: speech
   namespaceSelector:
      matchNames:
         - default
   podMetricsEndpoints:
   - port: metrics-triton
     interval: 10s
     path: /metrics
```

要匹配 **NVIDIA Triton 部署** 的标签，确保`spec.selector.matchLabels`字段为`app: speech`，`spec.namespaceSelector.matchNames`字段为`-default`，两者都应与 **NVIDIA Triton 部署** 位于同一命名空间下。

使用命令创建一个 PodMonitor：

```shell
kubectl apply -f speech-pod-monitor.yml
```

### 创建 ConfigMap

在 K8s 的某些场景下，Pod 需要依赖各种配置及配置文件，这些配置无法写死在镜像中，否则会影响到镜像的扩展性，`ConfigMap` 可以将环境变量配置信息和容器镜像解耦，便于应用配置修改。 `ConfigMap` 和 `Secret` 是 K8s 系统上两种特殊类型的存储卷，`ComfigMap` 对象用来将非机密性的数据保存到键值对中，

首先需要告诉 Prometheus 如何收集特定的度量，在 `ConfigMap` 中自定义平均等待时间 `avg_time_queue_us` 度量，`nv_inference_request_success[30]`定义了过去30s成功推理请求数目，`nv_inference_quene_duration_us`定义了以微秒为单位的累计排队持续时间。

自定义度量指过去30s每个推理请求的平均队列时间，**HPA** 根据该时间决定是否改变 **replicas** 数目。

度量需要有一个 endpoint，未编址的度量无法从度量API查询，添加 `.overrides` 字段，强制 pod 和 namespaces 之后在 API 中分开

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: adapter-config
  namespace: monitoring
data:
  triton-adapter-config.yml: |
    rules:
    - seriesQuery: 'nv_inference_queue_duration_us{namespace="default",pod!=""}'
      resources:
        overrides:
          namespace:
            resource: "namespace"
          pod:
            resource: "pod"
      name:
        matches: "nv_inference_queue_duration_us"
        as: "avg_time_queue_us"
      metricsQuery: 'avg(delta(nv_inference_queue_duration_us[30s])/(1+delta(nv_inference_request_success[30s]))) by (<<.GroupBy>>)'
```

执行创建一个用于自定义度量的 `ConfigMap`：

```shell
kubectl apply -f custom-metrics-server-config.yml
```

### 创建 Prometheus 适配器

Prometheus 可以采集自定义指标，但 Prometheus 采集到的指标并不能直接给 K8s 用，因为两者数据格式不兼容，因此还需要另外一个组件 `Prometheus-Adapter`，将 Prometheus 的指标数据转换为 K8s API 接口能识别的格式。由于 `Prometheus-adapter` 是自定义 `API Service`，所以还需要使用 `Kubernetes aggregator` 在主 API 服务器中注册，以便直接通过 `/apis` 来访问。

首先在 K8s 集群中创建一个 `ClusterRoleBinding` 对象，将 `cluster-admin` 角色分配给指定的用户和组，以便它们可以拥有完全的集群管理权限。请谨慎使用 `cluster-admin` 角色，因为它具有非常高的权限，只应该分配给受信任的用户和服务。

```shell
kubectl create clusterrolebinding permissive-binding --clusterrole=cluster-admin --user=admin --user=kubelet --group=system:serviceaccounts 
```

为了使 HPA 对这个自定义度量做出反应，必须为 `Prometheus Adapter` 创建 **Deployment、Service、APIService**。

**Deployment：**

以下是部署文件 `custom-metrics-server-Deployment.yml` 的内容，其使用 `ConfigMap` 告诉适配器收集自定义度量，创建 **Deployment**，`adapter Pod` 提取自定义度量。`containers.config` 字段必须与 `.mountPath` 字段和上一步在 ConfigMap 中创建的文件名 `triton-adapter-config.yml` 匹配。

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: triton-custom-metrics-apiserver
  namespace: monitoring
  labels:
    app: triton-custom-metris-apiserver
spec:
  replicas: 1
  selector:
    matchLabels:
      app: triton-custom-metrics-apiserver
  template:
    metadata:
      labels:
        app: triton-custom-metrics-apiserver
    spec:
      containers:
      - name: custom-metrics-server
        image: quay.io/coreos/k8s-prometheus-adapter-amd64:v0.8.0
        args:
        - --cert-dir=/tmp
        - --prometheus-url=http://10.24.83.40:30503
        - --metrics-relist-interval=30s
        - --v=10
        - --config=/etc/config/triton-adapter-config.yml
        - --secure-port=6443
        ports:
        - name: main-port
          containerPort: 6443
        volumeMounts:
        - name: config-volume
          mountPath: /etc/config
          readOnly: false
      volumes:
      - name: config-volume
        configMap:
          name: adapter-config
```

K8s 版本与 K8s-Prometheus-adapter 版本对应参考：

![](../../figs.assets/image-20230322203935105.png)

**Service：**

接下来创建 `custom-metrics-server-service.yml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: triton-custom-metrics-api
  namespace: monitoring
spec:
  selector:
    app: triton-custom-metrics-apiserver
  ports:
  - port: 443
    targetPort: 6443 
```

**APIService：**

接下来，创建一个 **APIService**，以便 K8s 可以访问 `Prometheus adapter`。

以下是文件 `custom-metrics-server-apiservice.yml` 的内容，其中 `.spec.service` 字段必须与 **Service** 文件的 `.metadata` 字段匹配，为了允许自动缩放器访问自定义度量，需要向 `API aggregator` 注册该 metrics，需要使用的API是 `custom.metrics.k8s.io/v1beta1`。

```yaml
apiVersion: apiregistration.k8s.io/v1beta1
kind: APIService
metadata:
   name: v1beta1.custom.metrics.k8s.io
spec:
   insecureSkipTLSVerify: true
   group: custom.metrics.k8s.io
   groupPriorityMinimum: 100
   versionPriority: 5
   service:
     name: triton-custom-metrics-api
     namespace: monitoring
   version: v1beta1
```

### 查询创建的自定义指标

使用命令 `kubectl apply` 来创建三个前面提到的 **YAML** 文件配置，为 Prometheus 创建 **API Service** 之后，可以看到 `custom metrics`可用：

```shell
kubectl get --raw /apis/custom.metrics.k8s.io/v1beta1 | jq .
```

![](../../figs.assets/image-20230327192343568.png)

还可以检查 `custom metrics` 的当前值，该值为 0 表示没有来自客户端的推理请求，`default namespace` 选择所有 pod，其中部署了 speech-demo：

```shell
kubectl get --raw /apis/custom.metrics.k8s.io/v1beta1/namespaces/default/pods/*/avg_time_queue_us | jq .
```

![](../../figs.assets/image-20230327192704313.png)

## 部署HPA

**Autoscaling**  即弹性伸缩，是 K8s 中一种非常核心的功能，它可以根据给定的指标（例如 CPU 或 内存）自动缩放 Pod 副本，从而可以更好管理和应用计算机资源，提高系统可用性和性能，同时减少开销和成本，弹性收缩可以解决服务负载存在较大波动或资源实际使用与预估之间的差距。**HPA** (Horizotal Pod AutoScaler) 可以根据 Pod 个数实现自动扩/缩容。

现在可以创建一个用于自定义度量的 HPA ，HPA 可以根据观察到的指标自动缩放复制器中 Pods 的数量。HPA 根据监测值和当前值的比率来控制 K8s 中 **replicas Pods** 的数量。
$$
R = ceil(CR \cdot \frac{CV}{DV})
$$
其中 $R$ 表示 K8s 拥有 replicas 的数量；$CR$ 是当前 replicas pod 的数量；$CV$ 是当前的指标，表示来自所有自定义度量的平均值；$DV$ 是所需的度量值。当 $R$ 与 $CR$ 不同时，HPA 可以增加或减少 replicas 的数量。

以下 HPA 文件 `speech-HPA.yml` 可以自动缩放 Triton 推理服务器的部署，使用 `.spec.targetAverageValue` 字段所需的度量值。该字段定期调整 pods 的数量，以使观察到的自定义度量与目标值匹配。

```yaml
apiVersion: autoscaling/v2beta1
kind: HorizontalPodAutoscaler
metadata:
   name: speech-hpa
spec:
   scaleTargetRef:
     apiVersion: apps/v1beta1
     kind: Deployment
     name: speech
   minReplicas: 1
   maxReplicas: 3
   metrics:
   - type: Pods
     pods:
       metricName: avg_time_queue_us
       targetAverageValue: 10000
```

可以查看部署的 HPA 状态：

```shell
kubectl get hpa
```

![](../../figs.assets/image-20230327200937175.png)

如果客户端向服务器发送推理请求，则新的 HPA 可以获取部署的自定义度量，并建立所需 Pods 的数量，当客户端停止发送推理请求时，HPA 将 replicas 数量减少到只有 1。

使用命令可以查看 HPA 的部署变化情况：

```
kubectl describe hpa speech-hpa
```

![](../../figs.assets/image-20230327203412462.png)

## 使用NGINX Plus负载均衡

​	负载均衡是为了在可用的服务器之间以最佳方式分配来自客户端的负载。NGINX Plus作为高级7层负载均衡

​	在该demo中，使用Prometheus，通过autoscaler新添加的Pods无法使用Kubernetes内置的负载均衡器获得工作负载。使用NGINX Plus，它是第七层（应用层）负载均衡器，工作负载均匀分布在所有Pods中，包括新扩展的Pod。

​	首先需要创建一个NGINX镜像，因为Dockerhub无法提供NGINX Plus商业产品。使用Docker Hub中的NGINX开源镜像在Docker容器中创建一个NGINX实例，然后将本地镜像推送到一个专用的Docker注册表中。

​	接下来，要部署NGINX Plus，使用以下命令将要部署NGINX Plus的节点标记为`role=nginxplus`：

```
kubectl label node xmdx role=nginxplus
```

![](../../figs.assets/image-20230403111341595.png)	

​	修改Service将Cluster IP设置为None，暴露并标识所有的replicas端点。创建一个新的Service文件`speech-service-nginx.yml`，并且apply it：

```
apiVersion: v1
kind: Service
metadata:
  name: speech-nginx
  labels:
    app: speech
Spec:
  clusterIP: None 
  selector:
    app: speech
  ports:
    - protocol: TCP
      port: 8000
      name: http
      targetPort: 8000
    - protocol: TCP
      port: 8001
      name: grpc
      targetPort: 8001 
```

​	现在，为NGINX创建一个配置文件，位于`/path/to/nginx/config/nginx.conf`。

```
resolver 10.96.0.10 valid=5s;
upstream backend {
   zone upstream-backend 64k;
   server speech-nginx.default.svc.cluster.local:8000 resolve;
}

upstream backendgrpc {
   zone upstream-backend 64k;
   server speech-nginx.default.svc.cluster.local:8001 resolve;
}
  
server {
   listen 80;
   status_zone backend-servers;
  
   location / {
     proxy_pass http://backend;
     health_check uri=/v2/health/ready;
   }
}
  
server {
        listen 89 http2;
 
        location / {
            grpc_pass grpc://backendgrpc;
        }
}
  
server {
    listen 8080;
    root /usr/share/nginx/html;
    location = /dashboard.html { }
    location = / {
       return 302 /dashboard.html;
    }
    location /api {
      api write=on;
    }
} 
```

​	最后，在`nginxplus-rc.yml`文件中，为NGINX Plus创建一个ReplicationController。要从私有注册表中提取镜像，Kubernetes需要凭据(credentials)。配置文件中的`imagePullSecrets`字段指定Kubernetes应该从名为regcred的Secret中获取凭据。在这个配置文件中，还必须将上一步创建的NGINX配置文件挂载到`/etc/nginx/conf.d`下。

```
 apiVersion: v1
 kind: ReplicationController
 metadata:
   name: nginxplus-rc
 spec:
   replicas: 1
   selector:
     app: nginxplus
   template:
     metadata:
       labels:
         app: nginxplus
     spec:
       nodeSelector:
         role: nginxplus
       imagePullSecrets:
       - name: regcred
       containers:
       - name: nginxplus
         command: [ "/bin/bash", "-c", "--" ]
         args: [ "nginx; while true; do sleep 30; done;" ]
         imagePullPolicy: IfNotPresent
         image: nvcr.io/nvidian/swdl/nginxplus:v1
         ports:
           - name: http
             containerPort: 80
             hostPort: 8085
           - name: grpc
             containerPort: 89
             hostPort: 8087
           - name: http-alt
             containerPort: 8080
             hostPort: 8086
           - name: flower-svc
             containerPort: 8000
             hostPort: 32309
         volumeMounts:
           - mountPath: "/etc/nginx/conf.d"
             name: etc-nginx-confd
       volumes:
         - nfs:
            server: <NFS server IP>
            path: </path/to/nginx/config>
            readOnly: false
           name: etc-nginx-confd 
```

​	使用以下命令创建ReplicationController：

```
kubectl create -f nginxplus-rc.yml  
```

验证Deployment，可以看到NGINX Plus正在运行





现在，当客户端向服务器发送推理请求时，可以看到NGINX Plus Dashboard：

- 自动缩放器的数量从一个逐渐增加到七个
- 工作负载在所有Pod之间均匀分布，如Traffic中所示

还可以通过检查Prometheus中所有Pods的度量值或自定义度量值来确认新添加的Pods处于工作状态

