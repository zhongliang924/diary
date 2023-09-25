# Triton 推理服务入门

## 概述

NVIDIA Triton（前身是 NVIDIA TensorRT Inference Server）是 NVIDIA 推出的一个用于深度学习模型推理的开源推理服务器软件。它的目标是简化和加速深度学习模型部署到生产环境中的过程。

![](../../figs.assets/image-20230103170550670.png)

<center>图 通用推理服务架构</center>

Triton基本功能特性：

1. **多框架支持**：Triton 支持多种深度学习框架，包括 `TensorFlow, Pytorch, TensorRT, ONNX RT, custom backends` 等，这使得用户可以使用它们喜欢的框架来训练和部署模型。
2. **高性能推理**：Triton 利用 NVIDIA 提供的 TensorRT 推理加速库，以及 GPU 硬件强大性能，实现高效的深度学习推理。它适用于对实时性较高的应用，如自动驾驶。
3. **灵活的部署选项**：Triton 支持各种部署选项，包括单机部署、多机部署以及容器化部署。用户可以根据自己的需求选择最合适的应用程序部署方式。
4. **多模型支持**：Triton 允许同时部署多个深度学习模型，并为每个模型提供独立的端点。
5. **RESTful API**：Triton 提供了一个 RESTful API，使得客户端应用程序可以轻松与服务器进行通信，提交推理请求并接收推理结果。
6. **监控和管理**：Triton 提供监控和管理功能，可以让用户跟踪服务器的性能、资源使用情况和模型的状态，并进行必要的管理操作。
7. **开源和社区支持**


## 设计理念

自己设计一个 Triton 该如何设计？

### 推理请求生命周期

- 基于不同框架推理模型都需要支持，backends 的方式实现对不同框架的支持
- 通用功能
  - Backends管理
  - 模型管理
  - 实例管理实现并发，多线程角度
  - 推理服务队列的分发和调度
  - 推理生命周期管理 
    - 推理请求管理  进入
    - 推理响应管理  退出
- GRPC服务相关

### 模型角度

- 单一简单的模型（Stateless model）：Default scheduler均匀分配、Dynamic batch
- 模型的组合  pipeline：模型与模型之间有依赖关系，每个模型可以有自己的调度方式
- 有状态模型（Stateful model）：语言类模型，下一个推理结果的产生依赖于之前的推理结果，采用基于序列的调度方式。Direct：按照原有的队列方式Direct，Oldest动态批处理



Backend可以对推理服务本身进行解耦

## 增值功能

- Model Analyzer：对推理请求全方位的扫描
  - Performance Analysis
  - Memory Analysis

## 上手参考

## 推理引擎比较

- Triton是开源的
  - 社区有很多讨论
  - 核心团队主要来自NV
  - 很多不同公司所构建的backends
  - 新特性，提问题
- 支持最多的框架
- 被很多公司所采用并上线部署
- 通过backends的方式实现解耦合
- 支持多实例、GRPC和CUDA优化
- Metrics支持，监控整个推理服务的状况
