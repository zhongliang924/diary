# 树莓派Triton环境安装

在树莓派终端使用 pip 进行 python 环境安装：

```
pip3 install tritonclient[all]
pip3 install soundfile
pip3 install typing_extensions==4.3.0
```

在服务端（NX）拉起语音识别服务：

```
cd lzl/wenet-triton/
bash run.sh
```

服务拉起成功：

![](../../../figs.assets/image-20230711090901760.png)

在树莓派客户端执行识别程序：

```
python3 client.py --audio_file=mid.wav --url=10.0.0.253:8001
```

树莓派获得识别结果：

![](../../../figs.assets/image-20230711091715500.png)

多条音频文件识别：

```
python3 client.py --wavscp=wav.scp --trans=refer.txt --url=10.0.0.253:8001
```

![](../../../figs.assets/image-20230711092759942.png)