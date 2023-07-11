# Android GRPC

## 什么是 GRPC

在 gRPC 中，客户端应用程序可以直接调用另一台计算机上服务器应用程序上的方法，这样更容易创建分布式应用程序和服务。与许多 RPC 系统一样，gRPC 基于定义服务的思想，指定可以通过参数和返回类型远程调用的方法。在服务器端，服务器实现了这个接口，并运行一个 gRPC 服务器来处理客户端调用；在客户端，客户端有一个存根 stub（某些语言称为 just），它提供与服务器相同的方法。

![](../../figs.assets/image-20230710144141465.png)

gRPC 客户端和服务器可以在各种环境中运行并相互通信。例如，可以使用 Java 创建 gRPC 服务器，并使用 Go, Python 或 Ruby 作为客户端。此外，最新的谷歌 API 将有 gRPC 版本的接口，可以轻松将谷歌功能构建到应用程序中。

## 核心观念、架构和生命周期

### 服务定义

gRPC 基于定义服务的思想，指定可以远程调用的方法，默认情况下，gRPC 使用 protocol buffers 作为接口定义语言，来描述服务接口和有效负载消息结构，如果需要可以使用其它替代方案

```
service HelloService {
  rpc SayHello (HelloRequest) returns (HelloResponse);
}

message HelloRequest {
  string greeting = 1;
}

message HelloResponse {
  string reply = 1;
}
```

gRPC 允许您定义四种服务方法：

- 一元 RPC：客户端向服务器发送一个请求并得到一个响应，就像正常的函数调用一样：

  ```
  rpc SayHello(HelloRequest) returns (HelloResponse);
  ```

- 服务器流式 RPC：客户端向服务器发送请求获取一个流以读取一系列消息，客户端从返回的流中提取，直到不再有消息为止

  ```
  rpc LotsOfReplies(HelloRequest) returns (stream HelloResponse);
  ```

- 客户端流式 RPC：客户端写入一系列消息，使用提供的流将其发送到服务器，一旦客户端完成消息的编写，它就会等待服务器读取消息并返回响应，gRPC 保证在单个 RPC 调用中的顺序

  ```
  rpc LotsOfGreetings(stream HelloRequest) returns (HelloResponse);
  ```

- 双向流式 RPC：双方使用读写流发送一系列消息，这两个流独立运行，因此客户端和服务器可以按照喜好的顺序进行读写。例如，服务器可以等待收到所有客户端消息后再写响应，或者可以交替地读一条消息然后写一条消息，每个流中消息的顺序会保留下来

  ```
  rpc BidiHello(stream HelloRequest) returns (stream HelloResponse);
  ```

### 使用 API

从 .proto 文件中的服务定义开始，gRPC 提供了协议缓冲区编译器插件，其生成客户端和服务端代码，gRPC 用户通常再客户端调用这些 API，并在服务端实现相应的 API

- 在服务器端，服务器实现服务定义方法，并运行 gRPC 服务器处理客户端调用，gRPC 基础结构对传入请求进行解码，执行服务方法，并对服务响应进行编码

## Quick start





 