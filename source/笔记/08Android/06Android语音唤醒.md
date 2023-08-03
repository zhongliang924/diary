# Android 语音唤醒

参考项目：https://github.com/wolfpaulus/hotword

CMU Sphinx File 语音识别工具包下载地址：[CMU Sphinx - Browse /Acoustic and Language Models at SourceForge.net](https://sourceforge.net/projects/cmusphinx/files/Acoustic and Language Models/)

CMU Sphinx 语音识别入门教程：[CMU Sphinx 语音识别入门：利用Sphinx-4搭建应用 - 简书 (jianshu.com)](https://www.jianshu.com/p/0ddd1dff815d)；[利用sphinx4实现中文命令词识别 - 简书 (jianshu.com)](https://www.jianshu.com/p/40ee296e2f0e)；[使用PocketSphinx设置中文唤醒词 ](https://github.com/wzpan/dingdang-robot/issues/45)

LM工具箱：[Sphinx Knowledge Base Tool VERSION 3 (cmu.edu)](http://www.speech.cs.cmu.edu/tools/lmtool-new.html)



## 问题解决

- **Using flatDirs should be avoided because it doesn't support any meta-data formats**

  在 `build.gradle (Module: app)` 中添加安卓代码块：

  ```
  android { ..
    sourceSets {
          main {
              jniLibs.srcDirs = ['libs']
          }
      }
  }
  ```

  然后在下面添加依赖：

  ```
  implementation fileTree(dir: 'libs', include: ['*.?ar'])
  implementation (files("libs/pocketsphinx-android-5prealpha-release.aar"))
  ```

  删除掉原文件的内容：

  ```
  repositories {
      flatDir {
          dirs 'libs'
      }
  }
  
  implementation fileTree(dir: 'libs', include: ['*.jar'])
  implementation(name: 'pocketsphinx-android-5prealpha-release', ext: 'aar')
  ```

  

- **Cannot resolve class android.support.constraint.ConstraintLayout**

1. 确保 `build.gradle (Project: Name)` 中定义了 `maven.google.com`：

   ```
   repositories {
   	google()
   }
   ```

2. 在 `build.gradle (Module: app)` 中添加共享库文件：

   ```
   dependencies {
       implementation "androidx.constraintlayout:constraintlayout:2.1.0"
   }
   ```

3. 需要在 `activity_listening.xml` 和 `activity_main.xml` 文件中，将 `android.support.constraint.ConstraintLayout` 替换为 `androidx.constraintlayout.widget.ConstraintLayout`，然后将 `android.support.constraint.Guideline` 替换为 `androidx.constraintlayout.widget.Guideline`，可以解决程序中断的问题。

   ```
   <androidx.constraintlayout.widget.ConstraintLayout
   	...
   </androidx.constraintlayout.widget.ConstraintLayout>
   ```

> Guideline 是一种特殊的控件，它在界面上是看不见的（被标记为 View.Gone），只是用来做参考线，它一般有水平和垂直两种







