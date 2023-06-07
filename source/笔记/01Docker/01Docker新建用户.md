# Docker新建用户

**1、在Ubuntu主机上安装docker**

```
sudo apt-get update
sudo apt-get install docker.io
```

**2、拉取 NVIDIA CUDA 镜像**

```
docker pull 10.24.83.22:8080/nvidia/cuda:11.6.0-devel-ubuntu18.04
```

**3、使用命令创建一个 Docker 容器**

```
# --name 字段指定容器名称，-v 字段指定容器挂载主机文件，-p 字段指定容器与主机的端口映射
user=user
docker run -it --gpus all --name ${user} -v /hdd0:/data -p 4000:22 nvidia/cuda:11.6.0-devel-ubuntu18.04 /bin/bash

# wenet
docker run --gpus all --name wenet_server -it -p 8000:8000 -p 8001:8001 -p 8002:8002 --shm-size=1g --ulimit memlock=-1  wenet_server:22.03 /bin/bash
```

这将创建一个名为“user”的新容器，并将其映射到主机的端口3000，映射机械硬盘 /hdd0 到 /data，需要记住映射的端口号，

**4、容器创建完成后，在容器内依次执行以下命令进行初始化**

```
# user 是容器用户名，123456 是容器 sudo 的密码
user=user
chmod 777 /tmp && \
apt-get update && apt-get upgrade -y && \
apt-get install -y xauth ssh vim sudo && \
adduser ${user} --gecos '' --disabled-password && \
echo "${user}:123456" | chpasswd && \
usermod -aG sudo ${user}
```

**5、开机ssh自启动**

首先，在 /root 目录下新建一个 start_ssh.sh文件，并给予该文件可执行权限。

```
vim /root/start_ssh.sh

chmod +x /root/start_ssh.sh
```

start_ssh.sh 脚本的内容，如下：

```
#!/bin/bash
LOGTIME=$(date "+%Y-%m-%d %H:%M:%S")
echo "[$LOGTIME] startup run..." >>/root/start_ssh.log
service ssh start >>/root/start_ssh.log
#service mysql start >>/root/star_mysql.log
```

将start_ssh.sh脚本添加到启动文件中，在 .bashrc 文件末尾加入如下内容

```
vim /root/.bashrc

# startup run
if [ -f /root/start_ssh.sh ]; then
      /root/start_ssh.sh
fi
```

保存后，等下次重启容器的时候，添加的服务也就跟着重启了。

**6、docker自启动**

以上操作都完成后，按 Ctrl+D 退出容器，使用 `docker ps -a` 发现刚刚创建的容器处于 `Exited()` 状态，首先开启容器：

```
user=user
docker start ${user}
```

user 为容器名称，然后设置 docker 开机自启动

```
docker update --restart=always ${user}
```

用户名和密码是第 4 步设置的





