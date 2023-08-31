# Chatgpt-Web

项目地址：https://github.com/Chanzhaoyu/chatgpt-web

使用 Express 和 Vue3 搭建 ChatGPT 演示网页

## 获取 ChatGPT API

提供两种 `ChatGPT API` 方法

- 第一种方式：ChatGPTAPI（收费，可靠，相对较笨）

  使用梯子进入 Openai 官网，进入账户的 API 设置[API keys - OpenAI API](https://platform.openai.com/account/api-keys)，可以查看账户已有的 API，对于 Web Key 的 API，其值为 `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`，如果忘记了新建一个即可

  ![](../../figs.assets/image-20230805171803101.png)

  

  如果使用改方式需要付费，具体的我也没试过了，主要尝试第二种方法

  ![](../../figs.assets/image-20230805171922675.png)

- 第二种方式：ChatGPTUnofficialProxyAPI（免费，相对不可靠，聪明）

  打开一个**无痕模式**的浏览器，进入网址 https://chat.openai.com/api/auth/session ，找到 `accessToken` 字段，记录该字符串序列

**警告：**

1. 首先应使用 `API` 方式

2. 使用 `API` 时，如果网络不通，那是国内被墙了，你需要自建代理，绝对不要使用别人的公开代理，那是危险的。

3. 使用 `accessToken` 方式时反向代理将向第三方暴露您的访问令牌，这样做应该不会产生任何不良影响，但在使用这种方法之前请考虑风险。

4. 使用 `accessToken` 时，不管你是国内还是国外的机器，都会使用代理。默认代理为 [pengzhile](https://github.com/pengzhile) 大佬的 https://ai.fakeopen.com/api/conversation ，这不是后门也不是监听，除非你有能力自己翻过 `CF` 验证，用前请知悉。社区代理：https://github.com/transitive-bullshit/chatgpt-api#reverse-proxy

   （注意：只有这两个是推荐，其他第三方来源，请自行甄别）

5. 把项目发布到公共网络时，你应该设置 `AUTH_SECRET_KEY` 变量添加你的密码访问权限，你也应该修改 `index.html` 中的 `title`，防止被关键词搜索到。

## 安装依赖

Node 的 安装可以参考我之前写的文档：[Node.js 安装](https://notebook-lzl.readthedocs.io/zh/latest/%E7%AC%94%E8%AE%B0/06%E5%B0%8F%E5%B7%A5%E5%85%B7/09Nodejs.html#id2)

检查版本：

```
~# node -v
v16.15.1
```

安装 `pnpm`，记住需要添加软链接

```
npm install pnpm -g

ln -s /workspace/node-v16.15.1-linux-x64/bin/pnpm /usr/bin/pnpm
```

接下来需要填写密钥，进入文件 `/service/.env`，如果有 `ChatGPTAPI Key`，则在 `OPENAI_API_KEY=` 下进行编写，我这里没法用这个，所以采用第二种方式，总共有三处需要修改的地方：

- 在 `OPENAI_ACCESS_TOKEN=` 下填写刚才获取的字符串

![](../../figs.assets/image-20230805173537267.png)

- 指定模型名 ` OPENAI_API_MODEL` 为 `gpt-3.5-turbo`
- 指定 API 反向代理 `API_REVERSE_PROXY` 为 `https://ai.fakeopen.com/api/conversation`

 设置完这些后，对于后端，进入文件夹 `/service` 运行以下命令

```
pnpm install
```

对于前端，在根目录下运行以下命令

```
pnpm bootstrap
```

完成初始化工作

## 测试环境运行

对于**后端服务**，进入文件夹 `/service` 运行以下命令：

```
pnpm start
```

对于**前端网页**，在根目录下运行以下命令：

```
pnpm dev
```

## Docker 容器化部署

因为我之前的操作都是在 Ubuntu18.04 容器内进行的，首先使用 `docker commit` 将容器打包成基础镜像 `chatgpt-web:08.05`，然后编写 Dockerfile 文件：

```
FROM chatgpt-web:08.05

WORKDIR /workspace/chatgpt-web

COPY ./chat.sh ./

EXPOSE 1002
EXPOSE 3002

CMD sh chat.sh
```

上面的命令需要将本地的批处理文件复制到容器内并执行，我们需要在容器内执行两个服务，一个前端服务和一个后端服务，使用脚本文件进行批量执行，`chat.sh` 的内容为：

```
#!/bin/bash

pnpm dev &

cd ./service
pnpm start &
```

其中 `&` 表示程序在后台运行以便顺利执行下一个程序。

使用 `docker build` 命令构建镜像，在 `Dockerfile` 目录下执行

```
docker build -t chatgpt-web:v1 .
```

然后构建容器

```
docker run -d --restart=always --name chat-web -p 1002:1002 -p 3002:3002 chatgpt-web:v1
```

然后打开网页 `10.136.10.24:1002` ，IP 需要根据自身网络情况进行确定，端口号固定为 `1002`，就可以使用 ChatGPT 服务了。

![](../../figs.assets/image-20230805183631623.png)

示例：

![](../../figs.assets/image-20230805184140828.png)

