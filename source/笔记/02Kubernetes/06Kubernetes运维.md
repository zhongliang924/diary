# K8s 运维

## 结点删除网络配置

重置 kubernetes 服务，重置网络，删除网络配置和 link：

```
kubeadm reset
systemctl stop kubelet
systemctl stop docker
rm -rf /var/lib/cni/
rm -rf /var/lib/kubelet/*
rm -rf /etc/cni/
ifconfig cni0 down
ifconfig flannel.1 down
ifconfig docker0 down
ip link delete cni0
ip link delete flannel.1
```

这样可以完全重置 k8s 节点