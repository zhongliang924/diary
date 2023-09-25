# NNI WeNet 剪枝

## 剪枝器选择

### L1NormPruner



### MovementPruner



## 遇到的问题

1、RuntimeError: Too many open files. Communication with the workers is no longer possible. Please increase the limit using `ulimit -n` in the shell or change the sharing strategy by calling `torch.multiprocessing.set_sharing_strategy('file_system')` at the beginning of your code



代码的开头添加：

```python
import torch.multiprocessing
torch.multiprocessing.set_sharing_strategy('file_system')
```

2、验证 loss 不断增加

减少 train.yaml 中的 optim_conf: lr 可以避免训练过程中 loss 增加，原来是 0.001(1e-3)，减小为 0.0001(1e-4)。

