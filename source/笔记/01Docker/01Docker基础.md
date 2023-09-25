# Docker 基础

Docker 是一个开源项目，基于 Google 公司推出的 Go 语言实现，项目后来加入了 Linux 基金会，遵从 Apache 2.0 协议，项目代码在 Github 上进行维护。

Docker 相比虚拟机，交付速度更快，资源消耗更低，Docker 采用客户端/服务端（C/S）结构，使用远程 API 管理和创建容器，其可以轻松构建一个**轻量级、可移植的、自给自足**的容器，Docker 的三大理念是 **build（构建）、ship（运输）、run（运行）**，通过 **namespace** 及 **cgroup** 等来提供容器的资源隔离与安全保障。

Docker 容器在运行时不需要类似虚拟机（空运行的虚拟机占用物理 6-8% 的性能）的额外性能开销，可以大幅提高资源利用率。总而言之，Docker 是一种用新颖的方式实现的轻量级虚拟机，类似于虚拟机但在原理和应用上和虚拟机差别还是很大的，Docker 的专业用法叫应用容器（**Application Container**）。

- 镜像（Images）：Docker 镜像是用于创建 Docker 容器的模板
- 容器（Containers）：Docker 容器是从 Docker 镜像创建的运行实例
- 挂载（Mounting）：挂载是一种将宿主机的文件或目录在容器内部可见和可访问的方式，这种方式对于数据持久化和容器间数据共享十分重要

## 什么是 Docker 容器

Docker 是一种流行的开源软件平台，可简化创建、管理、运行和分发应用程序的过程。它使用容器打包应用程序及其依赖项，我们也可以将容器视为 Docker 镜像的运行实例。

## Docker 和虚拟机有何不同

Docker 是轻量级的沙盒，在其中运行的只是应用，虚拟机里面还有额外的系统。

## 什么是 DockerFile

Dockerfile 是一个文本文件，其中包含了我们需要运行以构建 Docker 镜像的所有命令，每一条指令构建一层，每一条指令的内容用于描述该层应当如何构建。Docker 使用 Dockerfile 中的指令自动构建镜像。我们可以使用 `docker build` 用来创建按顺序执行多个命令行指令的自动创建。

一些常用的指令：

> FROM：建立基础镜像。在所有有效的 Dockerfile 中，FROM 是第一条指令
>
> LABEL：用于组织项目镜像，模块，许可等。在自动化部署方面 LABEL 也有很大的用途。在 LABEL 中指定一组键值对，可用于程序化配置或部署 Docker
>
> RUN：可在当前层执行任何命令并创建一个新层，用于在镜像中添加新的功能层
>
> CMD：为执行的容器提供默认值，在 Dockerfile 文件中，若添加多个 CMD 指令，只有最后的 CMD 指令运行

## Docker Compose 如何保证容器 A 先于容器 B 运行

> Docker Compose 是一个用来定义和运行复杂应用的 Docker 工具。一个应用通常由多个容器组成，使用 Docker Compose 将不再需要使用脚本来启动容器。Compose 通过一个配置文件来管理多个 Docker 容器。简单理解：Docker Compose 是 docker 的管理工具。

Docker Compose 在继续下一个容器之前不会等待容器准备就绪。为了控制我们的执行顺序，我们可以使用 `depends_on` 条件，使用 `docker-compose up` 命令将按照我们指定的依赖顺序启动和运行服务。

## 一个完整的 Docker 由哪些部分组成

- DockerClient 客户端
- Docker Daemon 守护进程
- DockerImage 镜像
- DockerContainer 容器

## Docker 常用命令

1. 查看本地主机的所用镜像：``docker images``
2. 搜索镜像：``docker search mysql``
3. 下载镜像：``docker pull mysql``，默认下载 latest 镜像
4. 下载指定版本的镜像：``docker pull mysql:5.7``
5. 删除镜像：``docker rmi -f 镜像id 镜像id 镜像id``

## 描述 Docker 容器生命周期

Docker 容器经历以下阶段：

- 创建容器
- 运行容器
- 暂停容器（可选）
- 取消暂停容器（可选）
- 启动容器
- 停止容器
- 重启容器
- 杀死容器
- 销毁容器

## Docker 容器间如何隔离

**NameSpace 和 Cgroups**

Linux 中的 PID、IPC、网络等资源是全局的，而 Linux 的 NameSpace 机制是一种资源隔离方案，在该机制下这些资源将不再是全局的，而是属于某个特定的 NameSpace，各个 NameSpace 下的资源互不干扰。

**NameSpace 实际上修改了应用进程看待整个计算机“视图”，即它的“视线”被操作系统做了限制，只能“看到”某些指定的内容**。对于宿主机来说，这些被“隔离”了的进程跟其它进程并没有区别。

虽然 NameSpace 技术可以实现资源隔离，但是进程还是可以不受控的访问系统资源，比如 CPU、内存、磁盘、网络等，为了控制容器进程对资源的访问，Docker 采用 control groups 技术（也就是 cgrous），有了 `cgroups` 就可以控制容器中进程对资源的访问，比如限制某个容器使用内存的上限、可以在哪些 CPU 上运行等等。

有了这两项技术，容器看起来就真的像是独立的操作系统了