

# Android APK

## Android

项目地址：https://github.com/wenet-e2e/wenet

目录位于 ：`./runtime/android`

版本信息：Gradle 版本为 7.2，Gradle 插件版本为 7.1.3

![](../../figs.assets/image-20230703174718916.png)

Android 端的流式 ASR 模型，目前是模型部署在手机上，模型大小大概有 100MB，后续需要通过抛接数据的方式将模型部署在 NX 上进行推理。

连接 Android 手机，我的安卓手机的 Android 版本为 12.0，安装对应 12.0 版本的 SDK，编译程序，在手机上得到 Wenet APP，打开 APP 可以实现在线语音识别功能

![](../../figs.assets/image-20230703175847942.png)





## 问题

**No variants found for ‘:app‘. Check build files to ensure at least one variant exists.**

更新 gradele 升级到了 7.2 版本

![](../../figs.assets/image-20230703145819149.png)

会遇到`"No variants found for ':app'. Check build files to ensure at least one variant exists."`的提示，需要 Android Gradle 插件版本和 Gradle 版本匹配，参考https://developer.android.google.cn/studio/releases/gradle-plugin?hl=zh-cn#updating-gradle，项目中更改成 7.1.3

![](../../figs.assets/image-20230703150903409.png)

