# Triton 客户端

项目链接：https://github.com/triton-inference-server/client

为了简化与 Triton 的通信，Triton 项目提供了几个客户端库以及如何使用这些库的示例，提供的客户端库主要如下：

## 一、C++ 和 Python API

可以使用 C++ 或 Python 应用程序与 Triton 进行通信，这些库可以向 Triton 发送 HEEP/REST 或 GRPC 请求，以访问其所有功能：推理、状态和健康、统计和度量、模型仓库管理等

C++ 客户端 API 公开了基于类的接口，commented 接口在 [grpc_client.h](https://github.com/triton-inference-server/client/blob/main/src/c%2B%2B/library/grpc_client.h), [http_client.h](https://github.com/triton-inference-server/client/blob/main/src/c%2B%2B/library/http_client.h), [common.h](https://github.com/triton-inference-server/client/blob/main/src/c%2B%2B/library/common.h) 中可用。

Python 客户端 API 提供了与 C++ API 类似的功能，commented 接口在 [grpc](https://github.com/triton-inference-server/client/blob/main/src/python/library/tritonclient/grpc/__init__.py) 和 [http](https://github.com/triton-inference-server/client/blob/main/src/python/library/tritonclient/http/__init__.py) 中可用。

### HTTP 选项

#### 1. SSL/TLS

客户端库允许使用 HTTPS 协议通过安全通道进行通信，仅仅设置这些 SSL 不能保证通信安全，Triton 服务器应该在 `https://` 代理下（如 nginx）运行。然后客户端可以建立到代理的安全通道，服务器仓库 [qa/L0_https](https://github.com/triton-inference-server/server/blob/main/qa/L0_https/test.sh)解释了如何实现。

对于 C++ 客户端，参考 `HttpSslOptions`，其封装在 [http_client.h](https://github.com/triton-inference-server/client/blob/main/src/c%2B%2B/library/http_client.h)；对于 Python 客户端，参考 [http/\__init__.py](https://github.com/triton-inference-server/client/blob/main/src/python/library/tritonclient/http/__init__.py)

客户端侧如何使用 SSL/TLS 设置的 [C++ ](https://github.com/triton-inference-server/client/blob/main/src/c%2B%2B/examples/simple_http_infer_client.cc)例子 和 [Python](https://github.com/triton-inference-server/client/blob/main/src/python/examples/simple_http_infer_client.py) 例子。

#### 2. 压缩

客户端库支持 HTTP 事务的联机压缩。

参考 [http_client.h](https://github.com/triton-inference-server/client/blob/main/src/c%2B%2B/library/http_client.h)中 `Infer` 和 `AsyncInfer` 函数中的 `request_compression_algorithm` 和 `response_compression_algorithm` 参数，默认情况下参数设置为 `CompressionType::None`；在 Python 下是类似的。

如何使用压缩选项的[C++ ](https://github.com/triton-inference-server/client/blob/main/src/c%2B%2B/examples/simple_http_infer_client.cc)例子 和 [Python](https://github.com/triton-inference-server/client/blob/main/src/python/examples/simple_http_infer_client.py) 例子。

### GRPC 选项

#### 1. SSL/TLS

客户端库允许使用 gRPC 协议通过安全通道进行通信。

对于 C++ 客户端，参考 `SslOptions`，其封装在 [grpc_client.h](https://github.com/triton-inference-server/client/blob/main/src/c%2B%2B/library/grpc_client.h)；对于 Python 客户端，参考 [grpc/\__init__.py](https://github.com/triton-inference-server/client/blob/main/src/python/library/tritonclient/grpc/__init__.py)。

在客户端侧使用 SSL/TLS 设置的 [C++](https://github.com/triton-inference-server/client/blob/main/src/c%2B%2B/examples/simple_grpc_infer_client.cc) 和 [Python](https://github.com/triton-inference-server/client/blob/main/src/python/examples/simple_grpc_infer_client.py) 例子。

#### 2. 压缩

客户端公开了用于 GRPC 事务的联机压缩

参考 [grpc_client.h](https://github.com/triton-inference-server/client/blob/main/src/c%2B%2B/library/grpc_client.h)中 `AsyncInfer` 和 `StartStream` 函数中的 `compression_algorithm`参数，默认情况下参数设置为 `GRPC_COMPRESS_NONE`；在 Python 下是类似的。

如何使用压缩选项的[C++ ](https://github.com/triton-inference-server/client/blob/main/src/c%2B%2B/examples/simple_grpc_infer_client.cc)例子 和 [Python](https://github.com/triton-inference-server/client/blob/main/src/python/examples/simple_grpc_infer_client.py) 例子。

## 二、简单例子应用

本节介绍了几个简单的示例应用程序及其所展示的功能：

### 1. Bytes/String Datatype

### 2. 系统共享内存

### 3. CUDA 共享内存

### 4. Stateful 模型的客户端 API

## 三、图像分类例子





## 四、Java API

由阿里云 PAI 团队提供，可以使用 HTTP/REST 请求从 Java 应用程序中,

Java 客户端 API 提供了与 Python API 类似的功能，具有类似的类和方法，有关更多的信息参考 [Java 客户端目录](https://github.com/triton-inference-server/client/tree/main/src/java)。