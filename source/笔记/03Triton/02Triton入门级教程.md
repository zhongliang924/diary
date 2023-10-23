# Triton入门级教程

## 模型并行推理逻辑

假设具有**两个模型**（模型 0 和模型 1），Triton 当前没有任何处理任务请求，当两个请求同时到达 Triton 服务，每个模型一个请求，Triton 立即将它们调度到 GPU 上，GPU 的硬件调度程序开始并行处理这两个计算。在系统 CPU 上执行的模型由 Triton 进行类似处理。

默认情况下，如果**同一个模型的多个请求**同时到达，Triton 将通过在 GPU 上一次只调度一个来序列化它们的执行。

Triton 提供了一个名为 `instance-group` 的选项，它允许每个模型指定该模型的**并行执行数**。每个这样启用的并行执行都称为一个实例。默认情况下，Triton 会在系统中每个可用的 GPU 上为每个模型提供一个实例，同时跑多个实例可以提高 GPU 利用率。通过使用模型配置中的 `instance-group` 字段，可以更改模型的执行实例数。

![](../../figs.assets/image-20230107160654931.png)

Triton 支持**多种调度和批处理算法**，可以为每个模型独立配置。

## 模型类型及调度器

Triton 定义了三种模型类型：无状态（Stateless）、有状态（Stateful）和集成（ensemble）模型，同时，Triton 提供了调度器来支持这些模型类型。

### 模型类型

Triton中三种模型类型如下：

- 无状态模型（Stateless models）：简单来说就是应对不同推理请求**没有相互依赖**的情况。平常遇到的大部分模型都属于这一类模型，比如：文本分类、实体抽取、目标检测等。
- 有状态模型（Stateful Models）：当前的**模型输出依赖上一刻的模型的状态**（比如：中间状态或输出）。对于推理服务来说，就是不同推理请求之间有状态依赖，比如：顺序依赖。
- 集成模型（Ensemble model）：表示一个或多个模型组成的工作流(有向无环图)。最常见的使用场景就是：**数据预处理->模型推理->数据后处理**。通过集成模型可以避免传输中间 tensor 的开销，并且可以最小化请求次数。比如：`bert` 实现的文本分类任务，需要在前置处理中对输入文本做 Tokenizer，Tokenizer 输出结果作为模型属性输入。

### 调度器

Triton 提供了以下几种调度策略：

**Default Scheduler**：默认调度策略，将推理请求按比例分配到不同的模型实例执行推理

**Dynamic Batcher**：在应对高吞吐的场景，将一定时间内的请求聚合成一个批次（batch），该调度器用于调度无状态模型。使用 **Dynamic Batcher** 之后客户端将比较小的请求合并成比较大的请求，可以极大提升模型的吞吐。

**Sequence Batcher：**类似于 **Dynamic Batcher**，也是动态聚合推理请求，区别是 **Sequence Batcher** 应用于有状态模型，并且一个序列请求只能路由到同一个模型是咧。

**Ensemble Scheduler：**只能调度集成模型，不能用于其它类型的模型

对于给定的模型，调度策略的选择和配置是通过模型的配置文件完成的。

## 启动 TritonServer

本节对 tritonserver 命令行参数做简要介绍，使用命令 `tritonserver --help` 查看 tritonserver 所有的选项，将 tritonserver 各个参数做分类，相关参数聚集在一起，看着会更加清晰一点。

检查 Server 健康状态：`curl -v <Server IP>:8000/v2/health/ready`

### log 相关

triton 提供四种等级的 Log：info warning error verbose，每一个选项可以分别选择是否打开

```shell
--log-verbose <integer>
--log-info <boolean>
--log-warning <boolean>
--log-error <boolean>
```

### 模型相关

`--model-store` 和 `--model-repository`：指定模型仓库地址

`--backend-directory`：指定 backend 的地址

`--repoagent-directory`：指定 agent 的地址

`--strict-model-config`：配置文件（true 表示一定要配置文件，false 表示可以尝试自动填充）

`--model-control-mode`：none, poll, explicit 三种

`--repository-poll-secs`：轮询时长

`--load-model`：配合 explicit 使用，指定启动的模型

`--backend-config <<string>,<string>=<string>>`：给某个 backend 加上特定的选项

### 服务相关

`-id`：指定服务器标识符

`--strict-readiness`：true 表示服务器和模型启动完毕才能访问 `v2/health/ready`，false 表示服务器启动即可

`--allow-http`：开启 HTTP 服务器

`--allow-grpc`：开启 GRPC 服务器

`--allow-sagemaker`：监听 Sagemaker 的请求

`--allow-metrics`：开启端口提供 prometheus 格式的使用数据

`allow-gpu-metrics`：提供 GPU 相关的数据

上面每一种 allow，都有配套的其它选项，比如 http 可以设置处理线程的数量，grpc 可以设置是否开启 ssl 等，可以使用 `--help` 查看。

### trace 相关

记录一条请求在 triton 中执行的整个过程，记录接受请求、请求处理、排队、计算、发送响应等时间戳。

`--trace-file`：输出的位置

`--trace-level`：输出等级，max 会记录更多信息，比如将计算拆解成输入、输出、推理等部分

`--trace-rate`：输出频率，比如多少个请求采样一次

### cuda 相关

`--pinned-memory-pool-byte-size`：锁页内存的大小，可以加速 host 和 device 的数据传输，默认 256MB

`--cuda-memory-pool-byte-size <<integer>:<integer>>`：第一个数字 gpu 卡号，第二个数字显存大小，默认 64MB。

`--min-supported-compute-capability <float>`：最低的 compute capability，小于这个的就不使用。

### 杂项

`--exit-on-error`：发送错误的时候退出

`--exit-timeout-secs <integer>`：当退出服务器的时候，有的请求还没处理完，这个选项指定了超时时间。

`--rate-limit` 和 `--rate-limit-resource`：用于限制了请求分发到模型实例上，resource 选项用来分配资源，资源满足就执行

`--response-cache-byte-size <integer>`：响应缓存的大小。·

`--buffer-manager-thread-count`：指定线程数量，可以加速在输入输出 tensor 上的操作。

`--host-policy <<string>,<string>=<string>`：NUMA( 多个物理 CPU 共享内存 ) 相关的选项，具体看[文档](https://github.com/triton-inference-server/server/blob/main/docs/optimization.md#numa-optimization)

## 配置集成模型

子模块需要准备好，放在模型仓库里面，创建 **ensemble model**，在语音识别任务中对应着 **attention_rescoring**：

```
name: "attention_rescoring"
platform: "ensemble"
max_batch_size: 64 #MAX_BATCH

input [
  {
    name: "WAV"
    data_type: TYPE_FP32
    dims: [-1]
  },
  {
    name: "WAV_LENS"
    data_type: TYPE_INT32
    dims: [1]
  }
]

output [
  {
    name: "TRANSCRIPTS"
    data_type: TYPE_STRING
    dims: [1]
  }
]

ensemble_scheduling {
 step [
   {
    model_name: "feature_extractor"
    model_version: -1
    input_map {
      key: "wav"
      value: "WAV"
    }
    input_map {
      key: "wav_lens"
      value: "WAV_LENS"
    }
    output_map {
      key: "speech"
      value: "SPEECH"
    }
    output_map {
      key: "speech_lengths"
      value: "SPEECH_LENGTHS"
    }
   },
   {
    model_name: "encoder"
    model_version: -1
    input_map {
      key: "speech"
      value: "SPEECH"
    }
    input_map {
      key: "speech_lengths"
      value: "SPEECH_LENGTHS"
    }
    output_map {
      key: "encoder_out"
      value: "encoder_out"
    }
    output_map {
      key: "encoder_out_lens"
      value: "encoder_out_lens"
    }
    output_map {
        key: "beam_log_probs"
        value: "beam_log_probs"
    }
    output_map {
        key: "beam_log_probs_idx"
        value: "beam_log_probs_idx"
    }
  },
  {
      model_name: "scoring"
      model_version: -1
      input_map {
          key: "encoder_out"
          value: "encoder_out"
      }
      input_map {
          key: "encoder_out_lens"
          value: "encoder_out_lens"
      }
      input_map {
          key: "batch_log_probs"
          value: "beam_log_probs"
      }
      input_map {
          key: "batch_log_probs_idx"
          value: "beam_log_probs_idx"
      }
      output_map {
          key: "OUTPUT0"
          value: "TRANSCRIPTS"
      }
  }
 ]
}
```

接下来定义模块之间的连接关系

- **键（key）**：模型文件本身定义的输入张量和输出张量

- **值（value）**：集成模型中定义的输入张量和输出张量，用于连接不同的模块

每一个子模块有各自的调度器，模块之间的数据传输通过**CPU 内存**。每一个子模型的**模型实例**是解耦的。

**Feature extractor模块**

```
name: "feature_extractor"
backend: "python"
max_batch_size: 64

parameters [
  {
    key: "num_mel_bins",
    value: { string_value: "80"}
  },
  {
    key: "frame_shift_in_ms"
    value: { string_value: "10"}
  },
  {
    key: "frame_length_in_ms"
    value: { string_value: "25"}
  },
  {
    key: "sample_rate"
    value: { string_value: "16000"}
  }

]

input [
  {
    name: "wav"
    data_type: TYPE_FP32
    dims: [-1]
  },
  {
    name: "wav_lens"
    data_type: TYPE_INT32
    dims: [1]
  }
]

output [
  {
    name: "speech"
    data_type: TYPE_FP32
    dims: [-1, 80]  # 80
  },
  {
    name: "speech_lengths"
    data_type: TYPE_INT32
    dims: [1]
  }
]

dynamic_batching {
    preferred_batch_size: [ 16, 32 ]
  }
instance_group [
    {
      count: 2
      kind: KIND_GPU
    }
]
```

**Encoder模块**

```
name: "encoder"
backend: "onnxruntime"
default_model_filename: "encoder.onnx"

max_batch_size: 64
input [
  {
    name: "speech"
    data_type: TYPE_FP32
    dims: [-1, 80] # 80
  },
  {
    name: "speech_lengths"
    data_type: TYPE_INT32
    dims: [1]
    reshape: { shape: [ ] }
  }
]

output [
  {
    name: "encoder_out"
    data_type: TYPE_FP32
    dims: [-1, 256] # [-1, feature_size]
  },
  {
    name: "encoder_out_lens"
    data_type: TYPE_INT32
    dims: [1]
    reshape: { shape: [ ] }
  },
  {
    name: "ctc_log_probs"
    data_type: TYPE_FP32
    dims: [-1, 7029]
  },
  {
    name: "beam_log_probs"
    data_type: TYPE_FP32
    dims: [-1, 10]  # [-1, beam_size]
  },
  {
    name: "beam_log_probs_idx"
    data_type: TYPE_INT64
    dims: [-1, 10] # [-1, beam_size]
  }
]

dynamic_batching {
    preferred_batch_size: [ 16, 32 ]
  }


instance_group [
    {
      count: 2
      kind: KIND_GPU
    }
]

```

**decoder模块**

```
name: "decoder"
backend: "onnxruntime"
default_model_filename: "decoder.onnx"

max_batch_size: 640
input [
  {
    name: "encoder_out"
    data_type: TYPE_FP32
    dims: [-1, 256] # [-1, feature_size]
  },
  {
    name: "encoder_out_lens"
    data_type: TYPE_INT32
    dims: [1]
    reshape: { shape: [ ] }
  },
  {
    name: "hyps_pad_sos_eos"
    data_type: TYPE_INT64
    dims: [10, -1]
  },
 {
    name: "hyps_lens_sos"
    data_type: TYPE_INT32
    dims: [10]
  },
  {
    name: "ctc_score"
    data_type: TYPE_FP32
    dims: [10]
  }
]

output [
   {
    name: "best_index"
    data_type: TYPE_INT64
    dims: [1]
    reshape: { shape: [ ] }
  }
]

dynamic_batching {
    preferred_batch_size: [ 16, 32 ]
  }

instance_group [
    {
      count: 2
      kind: KIND_GPU
    }
]
```

**scoring模块**

```
name: "scoring"
backend: "python"
max_batch_size: 64

parameters [
  {
    key: "vocabulary",
    value: { string_value: "/workspace/speech/onnx_model/units.txt"}
  },
  {
    key: "bidecoder",
    value: { string_value: "0"}
  },
  {
    key: "lm_path",
    value: { string_value: "None"}
  },
  {
   key: "hotwords_path",
   value : { string_value: "None"}
  }
]
input [
  {
    name: "encoder_out"
    data_type: TYPE_FP32
    dims: [-1, 256] # [-1, feature_size]
  },
  {
    name: "encoder_out_lens"
    data_type: TYPE_INT32
    dims: [1]
    reshape: { shape: [ ] }
  },
  {
    name: "batch_log_probs"
    data_type: TYPE_FP32
    dims: [-1, 10] #[-1, beam_size]
  },
  {
    name: "batch_log_probs_idx"
    data_type: TYPE_INT64
    dims: [-1, 10]
  }
]
output [
  {
    name: "OUTPUT0"
    data_type: TYPE_STRING
    dims: [1]
  }
]
dynamic_batching {
    preferred_batch_size: [ 16, 32 ]
  }
instance_group [
    {
      count: 4
      kind: KIND_CPU
    }
  ]
```



## 发送请求

 import tritonclient.grpc as grpcclient

1. 创建client对象：grpcclient.
2. 获取config数据：tritonclient.get_model_metadata
3. 准备输入原始数据
4. 打包到request里面，准备好inputs对象和outputs对象
5. 发送请求执行推理：异步、同步、streaming

当在同一台机器部署server client时，使用shared memory模块，python_backend使用shared memory传输数据。

