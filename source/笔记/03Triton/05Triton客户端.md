# Triton 客户端

项目链接：https://github.com/triton-inference-server/client

为了简化与 Triton 的通信，Triton 项目提供了几个客户端库以及如何使用这些库的示例，提供的客户端库主要如下：

## 一、C++ 和 Python API

可以使用 C++ 或 Python 应用程序与 Triton 进行通信，这些库可以向 Triton 发送 HEEP/REST 或 GRPC 请求，以访问其所有功能：推理、状态和健康、统计和度量、模型仓库管理等

C++ 客户端 API 公开了基于类的接口，commented 接口在 [grpc_client.h](https://github.com/triton-inference-server/client/blob/main/src/c%2B%2B/library/grpc_client.h), [http_client.h](https://github.com/triton-inference-server/client/blob/main/src/c%2B%2B/library/http_client.h), [common.h](https://github.com/triton-inference-server/client/blob/main/src/c%2B%2B/library/common.h) 中可用。

Python 客户端 API 提供了与 C++ API 类似的功能，commented 接口在 [grpc](https://github.com/triton-inference-server/client/blob/main/src/python/library/tritonclient/grpc/__init__.py) 和 [http](https://github.com/triton-inference-server/client/blob/main/src/python/library/tritonclient/http/__init__.py) 中可用。

使用 cmake 来配置 build，需要根据正在使用和想要构建的 Triton Client 组件来调整标志。例如，如果想要构建 C API 的 Perf Analyzer，需要设置 `-DTRITON_ENABLE_PERF_ANALYZER=ON -DTRITON_ENABLE_PERF_ANALYZER_C_API=ON`，也可以使用 `TRITON_ENABLE_PERF_ANALYZER_TFS` 和 `TRITON_ENABLE_PERF_ANALYZER_TS` 标签在性能分析器中启用/禁用对 TensorFlow Serving 和 TorchServer 后端的支持。以下命令演示了如何构建具有所有功能的客户端（在 client 主目录下）：

```
$ mkdir build
$ cd build
$ cmake -DCMAKE_INSTALL_PREFIX=`pwd`/install -DTRITON_ENABLE_CC_HTTP=ON -DTRITON_ENABLE_CC_GRPC=ON -DTRITON_ENABLE_PERF_ANALYZER=ON -DTRITON_ENABLE_PERF_ANALYZER_C_API=ON -DTRITON_ENABLE_PERF_ANALYZER_TFS=ON -DTRITON_ENABLE_PERF_ANALYZER_TS=ON -DTRITON_ENABLE_PYTHON_HTTP=ON -DTRITON_ENABLE_PYTHON_GRPC=ON -DTRITON_ENABLE_JAVA_HTTP=ON -DTRITON_ENABLE_GPU=ON -DTRITON_ENABLE_EXAMPLES=ON -DTRITON_ENABLE_TESTS=ON ..
```

如果在发布分支上进行构建，还必须使用其它 cmake 参数指向客户端构建所依赖的分支。例如，如果正在构建 r21.10 客户端分支，需要附加以下 cmake 标志：

```
-DTRITON_COMMON_REPO_TAG=r21.10
-DTRITON_THIRD_PARTY_REPO_TAG=r21.10
-DTRITON_CORE_REPO_TAG=r21.10
```

然后使用 make 构建客户端和示例：

```
make cc-clients python-clients java-clients -j12
```

整个构建时间较长，构建完成后，可以在安装目录中找到库和示例。

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

一些框架支持张量，其中张量中的每个元素都是可变长度的二进制数据。每个元素可以包含一个字符串或任意的字节序列，在客户端中，数据类型是 BYTES。

Python 客户端库使用 numpy 来表示输入和输出张量，对于 BYTES 张量，numpy 数组的 dtype 应为 `np.object`，为了与之前版本的客户端向后兼容，`np.bytes_`也可用于 BYTES 张量，但是不建议使用`np.bytes_`，因为使用此 dtype 会导致 numpy 从每个数组元素中删除所有尾随的零。因此，以零结尾的二进制序列将无法正确表示。

BYTES 张量在 C++ 示例程序 `simple_http_string_infer_client.cc` 和 `simple_grpc_string_infer_client.cc` 中进行了演示，String 张量在 Python 示例 `simple_http_string_infer_client.py` 和 `simple_grpc_string_infer_client.py` 中演示。

### 2. 系统共享内存

在某些情况下，使用系统共享内存在客户端库和 Triton 之间张量通信可以显著提高性能。

在 C++ 示例应用程序 `simple_http_shm_client.cc` 和 `simple_grpc_shm_client.cc` 中演示了使用系统共享内存；在 Python 示例中 `simple_http_shm_client.py` 和 `simple_grpc_shm_client` 中演示了共享内存如何使用。

Python 没有分配和访问共享内存的标准方法，因此提供了一个[系统共享内存模块](https://github.com/triton-inference-server/client/tree/main/src/python/library/tritonclient/utils/shared_memory)，该模块可以与 Python 客户端一起使用，以创建、设置和销毁系统共享内存。

### 3. CUDA 共享内存

在某些情况下，使用 CUDA 共享内存在客户端和 Triton 之间张量通信可以显著提高性能。

在 C++ 示例应用程序 `simple_http_cudashm_client.cc` 和 `simple_grpc_cudashm_client.cc` 中演示了使用 CUDA 共享内存；在 Python 示例中 `simple_http_cudashm_client.py` 和 `simple_grpc_cudashm_client` 中演示了 CUDA 共享内存如何使用。

Python 没有分配和访问共享内存的标准方法，因此提供了一个[CUDA共享内存模块](https://github.com/triton-inference-server/client/blob/main/src/python/library/tritonclient/utils/cuda_shared_memory)，该模块可以与 Python 客户端一起使用，以创建、设置和销毁 CUDA 共享内存。

### 4. Stateful 模型的客户端 API

当使用 Stateful 模型执行推理时，客户端必须识别哪些推理请求属于同一序列，以及序列何时开始和结束。

每个序列使用序列 ID 来标识，该序列 ID 是做出推理请求时提供的，由客户端创建一个唯一的序列 ID。对于每个序列，第一个推理请求应标记为该序列的开始，最后一个推理请求则应标记为序列的结束。

C++ 示例程序 `simple_http_sequence_stream_infer_client.cc`和`simple_grpc_sequence_stream_infer_client.cc` 演示了序列 ID 开始和结束标识的使用，Python 应用程序对应 `simple_http_sequence_stream_infer_client.py`和`simple_grpc_sequence_stream_infer_client.py`。

## 三、图像分类例子

使用 C++ 客户端进行图像分类的例子位于 `src/c++/examples/image_client.cc`；Python 客户端位于 `src/python/examples/image_client.py`。

要使用 image_client（或 image_client.py），必须拥有一个正在运行的 Triton，该 Triton 为一个或多个图像分类模型提供服务，image_client 应用程序要求模型具有单个图像输入并产生单个分类输出。如果没有包含图像分类模型的模型仓库，参考 [QuickStart](https://github.com/triton-inference-server/server/blob/main/docs/getting_started/quickstart.md)。

运行 Triton 后，可以使用 `image_client` 应用程序发送推理请求，可以指定单个图像或包含图像的目录，使用 `qa/images` 目录的图像向 inception_graphdef 模型发送请求。

- Python 应用程序客户端：

```
$ python examples/image_client.py -m inception_graphdef -s INCEPTION car.jpg
Request 1, batch size 1
    0.823674 (818) = SPORTS CAR
PASS
```

- C++ 客户端：

在 `client/build/cc-clients/examples`目录下有 C++ 编译好的 `image_client` 可执行文件，执行该文件，可以得到图片识别结果：

```
$ ./image_client -m densenet_onnx -c 3 -s INCEPTION /home/lzl/lzl/server/qa/images/mug.jpg
Request 0, batch size 1
Image '/home/lzl/lzl/server/qa/images/mug.jpg':
    15.349566 (504) = COFFEE MUG
    13.227465 (968) = CUP
    10.424895 (505) = COFFEEPOT
```

在 `src/c++/examples` 目录下，模仿 `image_client.cc` 编写自己的 C++ 文件可以对自己的模型进行识别。

## 四、Java API

由阿里云 PAI 团队提供，可以使用 HTTP/REST 请求从 Java 应用程序中,

Java 客户端 API 提供了与 Python API 类似的功能，具有类似的类和方法，有关更多的信息参考 [Java 客户端目录](https://github.com/triton-inference-server/client/tree/main/src/java)。