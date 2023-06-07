# 3-LFEformer-Local Feature Enhancement Using Sliding Window With Deformability for Automatic Speech Recognition

论文链接：https://ieeexplore.ieee.org/document/10035529

​	本文提出了一个可变形滑动窗口(Sliding Windows with Deformability)的局部特征增强模块，简称 SWD，采用基于嵌入层深度的可变窗口大小。SWD 模块可以插入到 Transformer 网络中，称为 LFEformer，可用于 ASR。这种网络善于捕捉全局和局部特征，有利于模型改进。局部特征和全局特征分别由 SWD 模块和 Transformer 网络中的注意力机制提取。性能在Aishell-1、HKUST 和 WSJ 上进行测试。可以获得 0.5%、0.8% 和 0.3% WER 改进。

## 一、引言

​	在 ASR 领域已经开发大量基于 Transformer 模型提高性能，例如局部特征增强与特征融合。Transformer 网络中的注意力机制用于建立长期依赖关系，这些依赖关系视为全局特征而不是局部特征。可以利用卷积核注意力提取局部和全局上下文信息；在固定大小滑动窗口下提取局部注意力，然后将其添加到全局特征中。但一方面自注意力机制不适用于局部特征提取，另一方面固定窗口限制 tokens 间交互是局部特征提取的次优方案。

​	本文提出了一个可变滑动窗口(SWD)模块捕获鲁棒局部特征，这些特征集成到 Transformer 提取的全局特征中用于最终预测。

​	来自更高层的特征更关注语义信息，但细节信息较弱，来自浅层的特征主要关注细节信息，很大程度上，细节信息在 ASR 领域最终结果的预测起着重要作用，因此特征融合称为解决这一问题的主要解决方案。使用 SWD 模块从嵌入层中提取局部信息，提取的特征传送到 Transformer 网络每一层的编码器和解码器中。本文将 SWD 与传统的 Transformer 网络相结合，提出了一种新的网络架构，名为 LFEformer。本文的主要工作如下：

- 所提出的 LFEformer 网络可以充分利用注意力机制提取的全局特征和 SWD 模块提取的局部特征进行预测，有助于 ASR 领域的模型改进
- SWD 作为一个局部特征提取器，可以有效从嵌入层中提取特征，提取的特征是通过基于层的深度的可变窗口大小的滑动窗口输入到每一层中。此外，来自嵌入层令牌之间的交互只计算一次，因此 SWD 模块中的参数与 Transformer 相比可以忽略不记
- 大量实验验证提出的 LFEformer 网络的有效性。与原始 Transformer 相比，在 Aishell-1 数据集上仅增加 0.32M 的模型参数，可以减少 0.5% 的 CER，在 HKUST 数据集上可实现 0.8% CER 改进，在 WSJ 上可实现 0.7%/0.3% 的性能改进。

## 二、方法



​	

