# Triton_Backend详解

## 概述

### 主要场景

有些客户有自己的深度学习框架：Tencent-TNN; Baidu-Paddle; Nvidia-HugeCTR

在 Triton 深度学习框架运行定制化模块：前处理、后处理、未部署到主流 DL 框架

### 部署什么

TRITONBackend_Backend：ONNX、Pytorch、Tensorflow（后端）

TRITONBACKEND_Model：yolov、VGG、RNN（模型）

TRITONBACKEND_ModelInstance：可以在 GPU0、GPU1上跑（设备）

这三个类代码已经实现了，Triton 需要与这三个类交互，需要实现七个接口函数（C语言编写），TritonBACKEND 将对象传到接口函数里面，包括 Initialize 和 Finalize，关键部分：ModelInstanceExecute，调这个接口执行推理

![](../../figs.assets/image-20230614111953084.png)

Triton 设计了两个状态类，**ModelState** 和 **ModelInstanceState**，推理执行的代码是写在这两个类里面，

![](../../figs.assets/image-20230614112122034.png)

**维护状态 -> ModelState**：模型名称、模型输入输出信息，batch_size；ModelInstance：在哪个设备上运行

**模型推理 -> ModelState、ModelInstanceState**：其中 ModelState  实现了成员函数 loadModel；ModelInstanceState 实现成员函数：SetInputTensors、Execute、ReadOutputTensors

![](../../figs.assets/image-20230614112407527.png)

> 定义三个预定义类的目的：
>
> **Triton 对于不同的 Backends 用统一的方式进行管理**，Predefined Class 是躯壳类。
>
> 
>
> 定义 ModelState 和 ModelInstanceState 的目的：
>
> 七个接口不是**面向对象的编程**，使用两个 Modle 对象，在不同的 Instance 里面执行推理，属于两个状态类，不同 Instance 之间的推理是独立安全的。
>
> 
>
> 为什么不在三个类里面进行实例化：
>
> 这么设计主要是解耦 backend 和 triton 之间的主流程，不需要编译整个 Triton，Backend 之间的开发更高效。

## 代码

以 Pytorch 为例，Tensorflow 和 ONNXRuntime 类似：

七个关键接口

- Backend_Initialize：读取版本号
- ModelInitialize：获取 model 的名称和版本，创建一个 Modle_State 类
- ModelFinalize：销毁 Model_State
- ModelInstanceInitiallize：操作 instance 对象
- ModelInstanceFinalize：释放 instance 对象
- ModelInstanceExecute：拿到推理的 instance 以及送进来的 requests，送入 ProcessRequest 推理

ModelState：

- 使用 Create() 创建，补全 Config，将 Config 写进 json
- LoadModel：生成 Pytorch 模型路径，开始读取模型，`torch::jit:load` 方法读取，

ModelInstanceState：通过 ModelState 的 LoadModel 方法读取模型

- 继承了 BackendModelInstance 类，维护 Instance 类型 和 ID
- 实际执行模型推理：ProcessRequest 函数实现，顺序执行三个成员方法：准备数据 -> 模型推理 -> 汇总推理结果
- 执行推理使用 ProcessRequest 函数，第一步检查 max_batch_size，为每个 request 创建一个 response 对象
  - SetInputTensor：获取 InputTensor 变量
  - Execute：调用 torch_model_ 对象的 forward 函数，拿到模型推理的结果
  - ReadOutputTensors：把 batch 的内容拆分 request 对应的 response

## 注意事项

1、注意 device id

2、batching 的工作需要 backend 自己实现

3、注意 Request 对象的管理，Request 在 backend 外面创建，但是在 backend 里面销毁，如果 Request 发生严重问题，需要及时终止整个推理流程并释放掉推理对象

4、Response 对象在 backend 里面创建，而不负责销毁，当推理发生错误时，立即返回 Error Response

