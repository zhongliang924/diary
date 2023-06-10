# 4-Wenet模型结构

## 1、ASR 模型

模型目录位于`wenet/transformer/asr_model.py-->ASRModel(torch.nn.Module)`：

编码器部分：

```python
encoder_out, encoder_mask = self.encoder(speech, speech_lengths)
encoder_out_lens = encoder_mask.squeeze(1).sum(1)
```

CTC 和注意力损失结合：

```python
loss_att, acc_att = self._calc_att_loss(encoder_out, encoder_mask, text, text_lengths)
loss_ctc = self.ctc(encoder_out, encoder_out_lens, text, text_lengths)
loss = self.ctc_weight * loss_ctc + (1 - self.ctc_weight) * loss_att
```

计算注意力损失的代码：

```python
def _calc_att_loss(self, encoder_out, encoder_mask, ys_pad, ys_pad_lens: torch.Tensor):
    ys_in_pad, ys_out_pad = add_sos_eos(ys_pad, self.sos, self.eos, self.ignore_id)
    ys_in_lens = ys_pad_lens + 1

    # 翻转 seq，用于右到左解码
    r_ys_pad = reverse_pad_list(ys_pad, ys_pad_lens, float(self.ignore_id))
    r_ys_in_pad, r_ys_out_pad = add_sos_eos(r_ys_pad, self.sos, self.eos,
                                            self.ignore_id)
    # 1. 前向解码
    decoder_out, r_decoder_out, _ = self.decoder(encoder_out, encoder_mask,
                                                 ys_in_pad, ys_in_lens,
                                                 r_ys_in_pad,
                                                 self.reverse_weight)
    # 2. 计算注意力损失
    loss_att = self.criterion_att(decoder_out, ys_out_pad)
    r_loss_att = torch.tensor(0.0)
    # 如果有右到左的注意力
    if self.reverse_weight > 0.0:
        r_loss_att = self.criterion_att(r_decoder_out, r_ys_out_pad)
        loss_att = loss_att * (
            1 - self.reverse_weight) + r_loss_att * self.reverse_weight
        acc_att = th_accuracy(
            decoder_out.view(-1, self.vocab_size),
            ys_out_pad,
            ignore_label=self.ignore_id,
        )
return loss_att, acc_att
```

## 2、损失

### 2.1 CTC 损失

模型目录位于`wenet/transformer/ctc.py-->CTC(torch.nn.Module)`：

模型结构

```
(ctc): CTC(
    (ctc_lo): Linear(in_features=256, out_features=7029, bias=True)
    (ctc_loss): CTCLoss()
)
```

代码实现：

```python
# Class CTC(torch.nn.Module)    
def __init__(self, odim, encoder_output_size, dropout_rate, reduce):
    """
    	构建 CTC 模块
    	odim：输出维度
    	encoder_output_size：编码器投影单元的数目
    	reduce：bool 类型，返回 CTC loss 到标量
    """
    super().__init__()
    eprojs = encoder_output_size
    self.dropout_rate = dropout_rate
    self.ctc_lo = torch.nn.Linear(eprojs, odim)
    reduction_type = "sum" if reduce else "none"
    self.ctc_loss = torch.nn.CTCLoss(reduction=reduction_type)


def forward(self, hs_pad, hlens, ys_pad, ys_lens):
    # hs_pad: (B, L, NProj) -> ys_hat: (B, L, Nvocab)
    ys_hat = self.ctc_lo(F.dropout(hs_pad, p=self.dropout_rate))
    # ys_hat: (B, L, D) -> (L, B, D)
    ys_hat = ys_hat.transpose(0, 1)
    ys_hat = ys_hat.log_softmax(2)
    loss = self.ctc_loss(ys_hat, ys_pad, hlens, ys_lens)
    # Batch-size average
    loss = loss / ys_hat.size(1)
    return loss


def log_softmax(self, hs_pad: torch.Tensor) -> torch.Tensor:
    return F.log_softmax(self.ctc_lo(hs_pad), dim=2)


def argmax(self, hs_pad: torch.Tensor) -> torch.Tensor:
    return torch.argmax(self.ctc_lo(hs_pad), dim=2)
```

### 2.2 注意力损失

模型目录位于`wenet/transformer/label_smoothing_loss.py-->LabelSmoothingLoss(torch.nn.Module)`。关于 Label-smoothing loss 可以参考 [5.7 LabelSmoothingLoss](##5.7 LabelSmoothingLoss)。

模型结构：

```
(criterion_att): LabelSmoothingLoss(
    (criterion): KLDivLoss()
)
```

代码实现

```python
# Class LabelSmoothingLoss(torch.nn.Module)
def __init__(self, size, padding_idx, smoothing, normalize_length):
    super(LabelSmoothingLoss, self).__init__()
    self.criterion = nn.KLDivLoss(reduction="none")
    self.padding_idx = padding_idx
    self.confidence = 1.0 - smoothing
    self.smoothing = smoothing
    self.size = size
    self.normalize_length = normalize_length


def forward(self, x, target):
    # 计算模型输出和目标标签之间的损失
    assert x.size(2) == self.size
    batch_size = x.size(0)
    x = x.view(-1, self.size)
    target = target.view(-1)
    # 使用 zeros_like 替代 no_grad()
    true_dist = torch.zeros_like(x)
    true_dist.fill_(self.smoothing / (self.size - 1))
    ignore = target == self.padding_idx
    total = len(target) - ignore.sum().item()
    target = target.masked_fill(ignore, 0)
    true_dist.scatter_(1, target.unsqueeze(1), self.confidence)
    kl = self.criterion(torch.log_softmax(x, dim=1), true_dist)
    denom = total if self.normalize_length else batch_size
    return kl.masked_fill(ignore.unsqueeze(1), 0).sum() / denom
```

## 3、编码器模块实现

模型目录位于 `wenet/transformer/encoder.py-->ConformerEncoder(BaseEncoder)`，继承了 `BaseEncoder` 的方法：

### 3.1 全局归一化

模型结构：

```
(global_cmvn): GlobalCMVN()
```

代码实现：

```python
# global_cmvn (Optional[torch.nn.Module]): Optional GlobalCMVN module
self.global_cmvn = global_cmvn
```

其中 `global_cmvn` 可参考 [CMVN实现](##5.6 CMVN)

> CMVN：倒谱均值方差归一化，提取声学特征后，使得另一个空间下参数符合某种概率分布，压缩特征参数值域的范围，减小训练和测试环境的不匹配，是一种提升模型鲁棒性的归一化操作。

### 3.2 编码器嵌入编码

模型结构：

```
(embed): Conv2dSubsampling4(
    (conv): Sequential(
        (0): Conv2d(1, 256, kernel_size=(3, 3), stride=(2, 2))
        (1): ReLU()
        (2): Conv2d(256, 256, kernel_size=(3, 3), stride=(2, 2))
        (3): ReLU()
    )
    (out): Sequential(
        (0): Linear(in_features=4864, out_features=256, bias=True)
    )
    (pos_enc): RelPositionalEncoding(
    (dropout): Dropout(p=0.1, inplace=False)
    )
)
```

代码实现：

```python
self.embed = subsampling_class(
    input_size,
    output_size,
    dropout_rate,
    pos_enc_class(output_size, positional_dropout_rate),
)
```

其中 `pos_enc_class` 默认为相对位置编码，相对位置编码实现可参考[RelPositionalEncoding](##5.2 位置编码)。

### 3.3 层归一化

模型结构：

```
(after_norm): LayerNorm((256,), eps=1e-05, elementwise_affine=True)
```

代码实现：

```python
# normalize_before: True 表示在一层的每个子块前进行layerNorm，False 表示在一层的每个子块后进行LayerNorm，默认为True
self.normalize_before = normalize_before
self.after_norm = torch.nn.LayerNorm(output_size, eps=1e-5)
```

### 3.4 Conformer 编码器层

模型结构：

```
(encoders): ModuleList(
    (0): ConformerEncoderLayer(
        (self_attn): RelPositionMultiHeadedAttention(
            (linear_q): Linear(in_features=256, out_features=256, bias=True)
            (linear_k): Linear(in_features=256, out_features=256, bias=True)
            (linear_v): Linear(in_features=256, out_features=256, bias=True)
            (linear_out): Linear(in_features=256, out_features=256, bias=True)
            (dropout): Dropout(p=0.0, inplace=False)
            (linear_pos): Linear(in_features=256, out_features=256, bias=False)
		)
        (feed_forward): PositionwiseFeedForward(
            (w_1): Linear(in_features=256, out_features=2048, bias=True)
            (activation): SiLU()
            (dropout): Dropout(p=0.1, inplace=False)
            (w_2): Linear(in_features=2048, out_features=256, bias=True)
		)
        (feed_forward_macaron): PositionwiseFeedForward(
            (w_1): Linear(in_features=256, out_features=2048, bias=True)
            (activation): SiLU()
            (dropout): Dropout(p=0.1, inplace=False)
            (w_2): Linear(in_features=2048, out_features=256, bias=True)
		)
        (conv_module): ConvolutionModule(
            (pointwise_conv1): Conv1d(256, 512, kernel_size=(1,), stride=(1,))
            (depthwise_conv): Conv1d(256, 256, kernel_size=(15,), stride=(1,), groups=256)
            (norm): LayerNorm((256,), eps=1e-05, elementwise_affine=True)
            (pointwise_conv2): Conv1d(256, 256, kernel_size=(1,), stride=(1,))
            (activation): SiLU()
		)
        (norm_ff): LayerNorm((256,), eps=1e-05, elementwise_affine=True)
        (norm_mha): LayerNorm((256,), eps=1e-05, elementwise_affine=True)
        (norm_ff_macaron): LayerNorm((256,), eps=1e-05, elementwise_affine=True)
        (norm_conv): LayerNorm((256,), eps=1e-05, elementwise_affine=True)
        (norm_final): LayerNorm((256,), eps=1e-05, elementwise_affine=True)
        (dropout): Dropout(p=0.1, inplace=False)
)
```

代码实现：

```python
# num_blocks：编码器块的数目，默认为6层编码器
self.encoders = torch.nn.ModuleList([
    ConformerEncoderLayer(
    output_size,
    encoder_selfattn_layer(*encoder_selfattn_layer_args),
    positionwise_layer(*positionwise_layer_args),
    positionwise_layer(*positionwise_layer_args) if macaron_style else None,
    convolution_layer(*convolution_layer_args) if use_cnn_module else None,
    dropout_rate,
    normalize_before,
    ) for _ in range(num_blocks)
])
```

其中 

`encoder_selfattn_layer` 使用相对多头自注意力层 [RelPositionMultiHeadedAttention](##5.3 多头自注意力) 

`positionwise_layer` 使用逐位前馈网络 [PositionwiseFeedForward](##5.4 前馈网络)

`convolution_layer` 使用 `macaron style` 的卷积网络 [ConvolutionModule](##5.5 卷积模块)

## 4、解码器模块实现

模型目录位于 `wenet/transformer/decoder.py-->TransformerDecoder`

### 4.1 解码器嵌入编码

模型结构：

```
(embed): Sequential(
	(0): Embedding(7029, 256)
	(1): PositionalEncoding(
	(dropout): Dropout(p=0.1, inplace=False)
	)
)
```

代码实现：

```python
self.embed = torch.nn.Sequential(
    torch.nn.Embedding(vocab_size, attention_dim),
    PositionalEncoding(attention_dim, positional_dropout_rate),
)
```

其中由 Embedding 模块和 PositionEncoding 两个模块组成，位置编码参考编码器中[位置编码](##5.2 位置编码)实现。

### 4.2 层归一化

模型结构：

```
(after_norm): LayerNorm((256,), eps=1e-05, elementwise_affine=True)
```

代码实现：

```python
# normalize_before: 
#	True 表示在一层的每个子块前进行layerNorm，False 表示在一层的每个子块后进行LayerNorm，默认为True
self.normalize_before = normalize_before
self.after_norm = torch.nn.LayerNorm(attention_dim, eps=1e-5)
```

### 4.3 层输出

模型结构：

```
(output_layer): Linear(in_features=256, out_features=7029, bias=True)
```

代码实现：

```python
# use_output_layer: 是否使用输出层
self.use_output_layer = use_output_layer
self.output_layer = torch.nn.Linear(attention_dim, vocab_size)
```

### 4.4 注意力解码器

模型结构：

```
 (decoders): ModuleList(
     (0): DecoderLayer(
     (self_attn): MultiHeadedAttention(
         (linear_q): Linear(in_features=256, out_features=256, bias=True)
         (linear_k): Linear(in_features=256, out_features=256, bias=True)
         (linear_v): Linear(in_features=256, out_features=256, bias=True)
         (linear_out): Linear(in_features=256, out_features=256, bias=True)
         (dropout): Dropout(p=0.0, inplace=False)
     )
     (src_attn): MultiHeadedAttention(
         (linear_q): Linear(in_features=256, out_features=256, bias=True)
         (linear_k): Linear(in_features=256, out_features=256, bias=True)
         (linear_v): Linear(in_features=256, out_features=256, bias=True)
         (linear_out): Linear(in_features=256, out_features=256, bias=True)
         (dropout): Dropout(p=0.0, inplace=False)
     )
     (feed_forward): PositionwiseFeedForward(
         (w_1): Linear(in_features=256, out_features=2048, bias=True)
         (activation): ReLU()
         (dropout): Dropout(p=0.1, inplace=False)
         (w_2): Linear(in_features=2048, out_features=256, bias=True)
     )
     (norm1): LayerNorm((256,), eps=1e-05, elementwise_affine=True)
     (norm2): LayerNorm((256,), eps=1e-05, elementwise_affine=True)
     (norm3): LayerNorm((256,), eps=1e-05, elementwise_affine=True)
     (dropout): Dropout(p=0.1, inplace=False)
)
```

代码实现：

```python
# num_blocks：解码器块的数目，默认为6层解码器
self.num_blocks = num_blocks
self.decoders = torch.nn.ModuleList([
    DecoderLayer(
        attention_dim,
        MultiHeadedAttention(attention_heads, attention_dim,self_attention_dropout_rate),
        MultiHeadedAttention(attention_heads, attention_dim, src_attention_dropout_rate) if src_attention else None,
        PositionwiseFeedForward(attention_dim, linear_units,dropout_rate),
        dropout_rate,
        normalize_before,
    ) for _ in range(self.num_blocks)
])
```

## 5、子模块实现

### 5.1 卷积子采样

模型目录位于 `wenet/transformer/subsampling-->Conv2dSubsampling4(BaseSubsampling)`

模型结构：

```
 (embed): Conv2dSubsampling4(
      (conv): Sequential(
        (0): Conv2d(1, 256, kernel_size=(3, 3), stride=(2, 2))
        (1): ReLU()
        (2): Conv2d(256, 256, kernel_size=(3, 3), stride=(2, 2))
        (3): ReLU()
      )
      (out): Sequential(
        (0): Linear(in_features=4864, out_features=256, bias=True)
      )
      (pos_enc): RelPositionalEncoding(
        (dropout): Dropout(p=0.1, inplace=False)
      )
    )
```

代码实现：

```python
def __init__(self, idim, odim, dropout_rate,pos_enc_class):
    self.conv = torch.nn.Sequential(
        torch.nn.Conv2d(1, odim, 3, 2),
        torch.nn.ReLU(),
        torch.nn.Conv2d(odim, odim, 3, 2),
        torch.nn.ReLU(),
    )
    self.out = torch.nn.Sequential(
        torch.nn.Linear(odim * (((idim - 1) // 2 - 1) // 2), odim))
    self.pos_enc = pos_enc_class

    
def forward(self, x, x_mask, offset):
    x = x.unsqueeze(1)  # 升维
    x = self.conv(x)
    b, c, t, f = x.size()
    x = self.out(x.transpose(1, 2).contiguous().view(b, t, c * f))
    x, pos_emb = self.pos_enc(x, offset)	# pos_enc_class = RelPositionalEncoding
    return x, pos_emb, x_mask[:, :, 2::2][:, :, 2::2]
```

### 5.2 位置编码

模型目录位于 `wenet/transformer/embedding-->RelPositionalEncoding(PositionalEncoding)`,用于实现（相对）位置编码：

代码实现：

```python
# position_encoding 方法，对绝对位置引入偏置进行编码
def position_encoding(self, offset, size, apply_dropout):
    if isinstance(offset, int):
        assert offset + size < self.max_len
        pos_emb = self.pe[:, offset:offset + size]
	elif isinstance(offset, torch.Tensor) and offset.dim() == 0:  # scalar
        assert offset + size < self.max_len
        pos_emb = self.pe[:, offset:offset + size]
    else:  # GPU上的流式解码
        assert torch.max(offset) + size < self.max_len
        index = offset.unsqueeze(1) + torch.arange(0, size).to(offset.device)
        flag = index > 0
        index = index * flag
        pos_emb = F.embedding(index, self.pe[0])  # B X T X d_model
    if apply_dropout:
        pos_emb = self.dropout(pos_emb)
    return pos_emb


# 位置编码模块
# Class: PositonalEncoding(torch.nn.Moudule)
def __init__(self, d_model, dropout_rate, max_len, reverse):
    super().__init__()
    self.d_model = d_model
    self.xscale = math.sqrt(self.d_model)
    self.dropout = torch.nn.Dropout(p=dropout_rate)
    self.max_len = max_len
    self.pe = torch.zeros(self.max_len, self.d_model)
    position = torch.arange(0, self.max_len, dtype=torch.float32).unsqueeze(1)
    div_term = torch.exp(torch.arange(0, self.d_model, 2, dtype=torch.float32) * 
            -(math.log(10000.0) / self.d_model))
    # 正弦位置核心
    self.pe[:, 0::2] = torch.sin(position * div_term)
    self.pe[:, 1::2] = torch.cos(position * div_term)
    self.pe = self.pe.unsqueeze(0)
    
    
def forward(self, x, offset):
    self.pe = self.pe.to(x.device)
    # 调用 position_encoding 方法
    pos_emb = self.position_encoding(offset, x.size(1), False)
    x = x * self.xscale + pos_emb
    return self.dropout(x), self.dropout(pos_emb)


# 相对位置编码模块，继承了位置编码模块
# Class: RelPositionalEncoding(PositionalEncoding)
def __init__(self, d_model, dropout_rate, max_len):
    super().__init__(d_model, dropout_rate, max_len, reverse=True)

    
def forward(self, x, offset):
    self.pe = self.pe.to(x.device)
    x = x * self.xscale
    pos_emb = self.position_encoding(offset, x.size(1), False)
    return self.dropout(x), self.dropout(pos_emb)
```

### 5.3 多头自注意力

模型目录位于 `wenet/transformer/attention.py-->RelPositionMultiHeadedAttention(MultiHeadedAttention)`

模型结构：

```
(self_attn): RelPositionMultiHeadedAttention(
    (linear_q): Linear(in_features=256, out_features=256, bias=True)
    (linear_k): Linear(in_features=256, out_features=256, bias=True)
    (linear_v): Linear(in_features=256, out_features=256, bias=True)
    (linear_out): Linear(in_features=256, out_features=256, bias=True)
    (dropout): Dropout(p=0.0, inplace=False)
    (linear_pos): Linear(in_features=256, out_features=256, bias=False)
)
```

代码实现：

```python
# 多头注意力模块
# Class: MultiHeadedAttention(nn.Module)
def __init__(self, n_head: int, n_feat: int, dropout_rate: float):
    # 构建多头注意力对象
    super().__init__()
    assert n_feat % n_head == 0
    # We assume d_v always equals d_k
    self.d_k = n_feat // n_head
    self.h = n_head
    self.linear_q = nn.Linear(n_feat, n_feat)
    self.linear_k = nn.Linear(n_feat, n_feat)
    self.linear_v = nn.Linear(n_feat, n_feat)
    self.linear_out = nn.Linear(n_feat, n_feat)
    self.dropout = nn.Dropout(p=dropout_rate)


def forward_qkv(self, queryr, key, value):
    n_batch = query.size(0)
    q = self.linear_q(query).view(n_batch, -1, self.h, self.d_k)
    k = self.linear_k(key).view(n_batch, -1, self.h, self.d_k)  
    v = self.linear_v(value).view(n_batch, -1, self.h, self.d_k)
    q = q.transpose(1, 2)  # (batch, head, time1, d_k)
    k = k.transpose(1, 2)  # (batch, head, time2, d_k)
    v = v.transpose(1, 2)  # (batch, head, time2, d_k)

    return q, k, v


# 相对位置多头自注意力模块，继承了基础的多头注意力模块
# Class: RelPositonMultiHeadedAtten(MultiHeadedAttention)
def __init__(self, n_head, n_feat, dropout_rate):
   	# 相对位置嵌入的多头自注意力
    super().__init__(n_head, n_feat, dropout_rate)
    # 用于位置编码的线性 Transformer
    self.linear_pos = nn.Linear(n_feat, n_feat, bias=False)
    # these two learnable bias are used in matrix c and matrix d
    # as described in https://arxiv.org/abs/1901.02860 Section 3.3
    self.pos_bias_u = nn.Parameter(torch.Tensor(self.h, self.d_k))
    self.pos_bias_v = nn.Parameter(torch.Tensor(self.h, self.d_k))
    torch.nn.init.xavier_uniform_(self.pos_bias_u)
    torch.nn.init.xavier_uniform_(self.pos_bias_v)

    
def forward(self, query, key, value, mask, pos_emb, cache):
    q, k, v = self.forward_qkv(query, key, value)
    q = q.transpose(1, 2)
    new_cache = torch.cat((k, v), dim=-1)
    n_batch_pos = pos_emb.size(0)
    p = self.linear_pos(pos_emb).view(n_batch_pos, -1, self.h, self.d_k)
    p = p.transpose(1, 2)
    q_with_bias_u = (q + self.pos_bias_u).transpose(1, 2)
    q_with_bias_v = (q + self.pos_bias_v).transpose(1, 2)
    # 首先计算矩阵 a 和 矩阵 c 的注意力分数
    matrix_ac = torch.matmul(q_with_bias_u, k.transpose(-2, -1))
    # 然后计算矩阵 b 和 矩阵 d 的注意力分数
    matrix_bd = torch.matmul(q_with_bias_v, p.transpose(-2, -1))
    scores = (matrix_ac + matrix_bd) / math.sqrt(self.d_k)
    
    return self.forward_attention(v, scores, mask), new_cache
```

### 5.4 前馈网络

模型目录位于 `wenet/transformer/positionwise_feed_forward.py-->PositionwiseFeedForward()`

模型结构：

```
(feed_forward): PositionwiseFeedForward(
    (w_1): Linear(in_features=256, out_features=2048, bias=True)
    (activation): SiLU()
    (dropout): Dropout(p=0.1, inplace=False)
    (w_2): Linear(in_features=2048, out_features=256, bias=True)
)
(feed_forward_macaron): PositionwiseFeedForward(
    (w_1): Linear(in_features=256, out_features=2048, bias=True)
    (activation): SiLU()
    (dropout): Dropout(p=0.1, inplace=False)
    (w_2): Linear(in_features=2048, out_features=256, bias=True)
)
```

代码实现：

```python
# Class PositionwiseFeedForward(nn.module)
def __init__(self, idim, hidden_units, dropout_rate, activation):
    # 构建逐位前馈网路对象，默认采用 ReLU 激活
    super(PositionwiseFeedForward, self).__init__()
    self.w_1 = torch.nn.Linear(idim, hidden_units)
    self.activation = activation
    self.dropout = torch.nn.Dropout(dropout_rate)
    self.w_2 = torch.nn.Linear(hidden_units, idim)

    
def forward(self, xs):
    return self.w_2(self.dropout(self.activation(self.w_1(xs))))
```

### 5.5 卷积模块

模型目录位于 `wenet/transformer/convolution.py-->ConvolutionModule`

模型结构：

```
(conv_module): ConvolutionModule(
    (pointwise_conv1): Conv1d(256, 512, kernel_size=(1,), stride=(1,))
    (depthwise_conv): Conv1d(256, 256, kernel_size=(15,), stride=(1,), groups=256)
    (norm): LayerNorm((256,), eps=1e-05, elementwise_affine=True)
    (pointwise_conv2): Conv1d(256, 256, kernel_size=(1,), stride=(1,))
    (activation): SiLU()
)
```

代码实现：

```python
# Class PositionwiseFeedForward(nn.module)
def __init__(self, channels, kernel_size, activation, norm, causal, bias):
    # 卷积核大小设置为 15，norm 默认采用 batch norm，默认采用 ReLU 激活
    super().__init__()
    self.pointwise_conv1 = nn.Conv1d(channels, 2 * channels, kernel_size=1, stride=1, padding=0, bias=bias)
    padding = (kernel_size - 1) // 2
    self.lorder = 0
    self.depthwise_conv = nn.Conv1d(channels, channels, kernel_size, stride=1, padding=padding, groups=channels, bias=bias)
    self.use_layer_norm = True
    self.norm = nn.LayerNorm(channels)
    self.pointwise_conv2 = nn.Conv1d(channels, channels, kernel_size=1, stride=1, padding=0, bias=bias)
    self.activation = activation


def forward(self, x, mask_pad, cache)：
	x = x.transpose(1, 2)
    if mask_pad.size(2) > 0:  # time > 0
        x.masked_fill_(~mask_pad, 0.0)
    new_cache = torch.zeros((0, 0, 0), dtype=x.dtype, device=x.device)
    # GLU 机制（逐点卷积）
    x = self.pointwise_conv1(x)
    x = nn.functional.glu(x, dim=1)
    # 1D 深度卷积
    x = self.depthwise_conv(x)
    # LayerNorm
    x = x.transpose(1, 2)
    x = self.activation(self.norm(x))
    x = x.transpose(1, 2)
    # 第二次逐点卷积
    x = self.pointwise_conv2(x)
    
    if mask_pad.size(2) > 0:  # time > 0
        x.masked_fill_(~mask_pad, 0.0)
    return x.transpose(1, 2), new_cache
```

### 5.6 CMVN

代码实现：

```python
# class GlobalCMVN(nn.module)
def __init__(self, mean, istd, norm_var):
    super().__init__()
    assert mean.shape == istd.shape
    self.norm_var = norm_var
    # The buffer can be accessed from this module using self.mean
    self.register_buffer("mean", mean)
    self.register_buffer("istd", istd)


def forward(self, x: torch.Tensor):
    # 返回归一化的特征
    x = x - self.mean
    if self.norm_var:
        x = x * self.istd
        return x
```

### 5.7 LabelSmoothingLoss

在标准的 CE loss 中，标签的数据分布为：


$$
[0,1,2] -> \begin{aligned} {
				[1.0,0.0,0.0], \\
				[0.0,1.0,0.0], \\
				[0.0,0.0,1.0],		
			}\end{aligned}
$$
在 Smoothing 版本的 CE loss 中，采用真实标签概率，在不同标签进行分布：


$$
smoothing=0.1 \\
[0,1,2] -> \begin{aligned} {
				[0.9,0.05,0.05], \\
				[0.05,0.9,0.05], \\
				[0.05,0.05,0.9],		
			}\end{aligned}
$$
