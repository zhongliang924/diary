# Node.js

## 简介

Node.js 是一个跨平台的 JavaScript 环境，它构建在为了在服务端运行 JavaScript 代码而设计的 Chrome JavaScript 上，通常用来构建后端应用，是目前非常流行的全栈和前端解决方案。npm 是 node.js 的默认包管理工具，也是世界上最大的软件仓库。

## 安装

### 从 Ubuntu 软件源安装 node.js 和 npm

安装非常简单直接，运行下面命令更新软件包索引，并且安装 Node.js 和 npm：

```
sudo apt update
sudo apt install nodejs npm
```

上面的命令将会安装一系列包，一旦完成，运行下面命令，验证安装过程：

```
$ nodejs --version
v10.19.0

$ npm -v
6.14.4
```

但这种安装方法在 Jetson 设备上运行 `npm install <包名>` 时会报错。

### Jetson 安装 Nodejs

去官网下载 ARMv8 版本的压缩包，下载地址：https://nodejs.org/en/download/

![](../../figs.assets/image-20230722101445259.png)

解压下载的文件，添加软链接并添加进环境变量

```
# 解压
tar -xvf node-v18.17.0-linux-arm64.tar.xz
# 建立软链接
sudo ln -s /home/lzl/lzl/tools/node-v18.17.0-linux-arm64/bin/node /bin/node
sudo ln -s /home/lzl/lzl/tools/node-v18.17.0-linux-arm64/bin/npm /bin/npm
```

验证安装：

```
$ nodejs --version
v18.17.0

$ npm -v
9.6.7
```

## 使用方法

首先安装 websocket 包

```
npm install websocket
```

然后运行 `app.js` 程序：

```
node app.js
```

![](../../figs.assets/image-20230722103346099.png)

这样就把服务端部署到 NX 上了