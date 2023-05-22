### Triton Metrics

Triton提供了指示GPU和请求统计信息的Prometheus度量。

#### 1、推理请求Metrics

​	对于不支持批处理的模型，其请求数、推理数和执行数应该是相等的；对于支持批处理的模型，平均批处理大小应为推理数/执行数。

| Category           | Metric              | Metric Name                             | Description                                              | Granularity | Frequency   |
| ------------------ | ------------------- | --------------------------------------- | -------------------------------------------------------- | ----------- | ----------- |
| Count              | Success Count       | `nv_inference_request_success`          | Triton收到的成功推理请求数                               | Per model   | Per request |
|                    | Failure Count       | `nv_inference_request_failure`          | Triton收到的失败推理请求数                               | Per model   | Per request |
|                    | Inference Count     | nv_inference_count                      | 执行的推理数量                                           | Per model   | Per request |
|                    | Execution Count     | nv_inference_exec_count                 | 执行批处理推理数目                                       | Per model   | Per request |
| Latency（count）   | Request Time        | nv_inference_request_duration_us        | 累积端到端推理请求处理时间（包括缓存）                   | Per model   | Per request |
|                    | Queue Time          | nv_inference_queue_duration_us          | 请求在调度队列中等待的累计时间                           | Per model   | Per request |
|                    | Compute Input Time  | nv_inference_compute_input_duration_us  | 处理推理输入请求所花费的累计时间（框架后端，不包含缓存） | Per model   | Per request |
|                    | Compute Time        | nv_inference_compute_infer_duration_us  | 执行推理模型所花费的累计时间（框架后端，不包括缓存）     | Per model   | Per request |
|                    | Compute Output Time | nv_inference_compute_output_duration_us | 处理推理输出所花费的累计时间（框架后端，不包括缓存）     | Per model   | Per request |
| Latency（Summary） | Request Time        | nv_inference_request_summary_us         | 端到端推理请求处理次数总结（包括缓存）                   | Per model   | Per request |
| （默认是禁用的）   | Queue Time          | nv_inference_queue_summary_us           | 请求在调度队列中等待时间摘要（包括缓存）                 | Per model   | Per request |
|                    | Compute Input Time  | nv_inference_compute_input_summary_us   | 请求处理推理输入所花费的时间摘要（框架后端，不包括缓存） | Per model   | Per request |
|                    | Compute Time        | nv_inference_compute_infer_summary_us   | 请求执行推理模型所花费的时间摘要（框架后端，不包括缓存） | Per model   | Per request |
|                    | Compute Output Time | nv_inference_compute_output_summary_us  | 请求处理推理输出所花费的时间摘要（框架后端，不包括缓存） | Per model   | Per request |

#### 2、GPU Metrics

| Category | Metric        | Metric Name               | Description                     | Granularity | Frequency    |
| -------- | ------------- | ------------------------- | ------------------------------- | ----------- | ------------ |
| GPU利用  | 功率使用      | nv_gpu_power_usage        | GPU瞬时功率                     | Per GPU     | Per interval |
|          | 功率限制      | nv_gpu_power_limit        | 最大GPU功率限制                 | Per GPU     | Per interval |
|          | 能量消耗      | nv_energy_consumption     | 自Triton启动以来GPU能耗（焦耳） | Per GPU     | Per interval |
|          | GPU利用率     | nv_gpu_utilization        | GPU利用率（0.0-1.0）            | Per GPU     | Per interval |
| GPU内存  | GPU总内存     | nv_gpu_memory_total_bytes | GPU总内存（字节）               | Per GPU     | Per interval |
|          | GPU已使用内存 | nv_gpu_memory_used_bytes  | 已用GPU内存（字节）             | Per GPU     | Per interval |