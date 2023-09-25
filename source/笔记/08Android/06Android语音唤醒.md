# Android 语音唤醒

部署项目：https://github.com/ZhongliangLi-github/SpeechApplication

参考项目：https://github.com/wolfpaulus/hotword

CMU Sphinx File 语音识别工具包下载地址：[CMU Sphinx - Browse /Acoustic and Language Models at SourceForge.net](https://sourceforge.net/projects/cmusphinx/files/Acoustic and Language Models/)

CMU Sphinx 语音识别入门教程：[CMU Sphinx 语音识别入门：利用Sphinx-4搭建应用 - 简书 (jianshu.com)](https://www.jianshu.com/p/0ddd1dff815d)；[利用sphinx4实现中文命令词识别 - 简书 (jianshu.com)](https://www.jianshu.com/p/40ee296e2f0e)；[使用PocketSphinx设置中文唤醒词 ](https://github.com/wzpan/dingdang-robot/issues/45)

LM工具箱：[Sphinx Knowledge Base Tool VERSION 3 (cmu.edu)](http://www.speech.cs.cmu.edu/tools/lmtool-new.html)

## CMU Sphinx 语音识别入门

Sphinx 4 是一个纯 Java 语音识别库，它提供了一个快速而简单的 API 接口，在 CMUSphinx 声学模型的帮助下将语音记录转换为文本。它可以在服务器端和桌面应用程序中使用，除了语音识别，Sphinx 还有助于说话人识别、调整模型将现有转录与音频时间对齐等。

CMU Sphinx 是一个领先的语音识别工具包，具有用于构建语音应用程序的各种工具，CMU Sphinx 包含许多用于不同任务和应用程序的开发包，以下介绍每个开发包的用途：

- Pocketsphinx：C 语言开发的轻量级语音识别引擎
- Sphinxtrain：声学模型训练工具
- Sphixbase：Pocketsphinx 和 Sphinxtrain 的基础类库
- Sphinx4：Java 语言开发的可调节、可修改的语音识别引擎

我们的语音唤醒采用Pocketsphinx模块

## 语音唤醒

语音唤醒是语音应用的一部分，在[部署项目](https://github.com/ZhongliangLi-github/SpeechApplication)中实现，主要使用了 `ListeningActivity.java` 类和 `WakeWordRecognizer` 类实现，以下详细介绍语音唤醒在安卓设备的实现过程：

首先下载 [CMU Sphinx ](https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/Mandarin/cmusphinx-zh-cn-5.2.tar.gz/download)中文语音识别模型。

然后在开源项目[hotword](https://github.com/wolfpaulus/hotword)中获取aar文件 `pocketsphinx-android-5prealpha-release.aar`，里面存放了语音唤醒的具体实现方法。

接下来需要设置唤醒词，新建 `words.dic` 文件，设置“小趣小趣”作为唤醒词，文件内容如下：

```
小趣小趣 x iao3 q v4 x iao3 q v4
```

使用类似方法可以生成其它唤醒词，也可以生成多个唤醒词。同时为 `words.dic` 生成 `.md5` 文件。

编写 `WakeWordRecognizer.java` 类用于实现语音唤醒，首先实例化一个语音识别对象，定义初始灵敏度为 80，该灵敏度可通过滑动条进行自主控制，并在 `setup()`进行初始化设置：

```kotlin
private SpeechRecognizer recognizer;
private int sensibility = 80;

/**
 * 初始化并启动语音唤醒器
 * 通过添加监听器处理语音输入事件
 * 灵敏度决定了唤醒词被激活的难易程度
 * addKeyphraseSearch() 方法添加了一个关键词搜索，用于检测用户是否说出了唤醒词
 */
private void setup() {
    try {
        final Assets assets = new Assets(context);
        final File assetDir = assets.syncAssets();

        Log.i(LOG_TAG, "Changing Recognition Threshold to " + sensibility);

        recognizer = SpeechRecognizerSetup.defaultSetup()
        .setAcousticModel(new File(assetDir, "models/zh-cn-ptm"))   // 设置音频模型文件
        .setDictionary(new File(assetDir, "models/lm/words.dic"))   // 设置字典文件
        .setKeywordThreshold(Float.parseFloat("1.e-" + 4 * sensibility))    // 设置唤醒词灵敏度值
        .getRecognizer();   // 获取 SpeechRecognizer 对象的引用
        recognizer.addKeyphraseSearch(WAKEWORD_SEARCH, context.getString(R.string.wake_word)); // 添加关键词搜索
        recognizer.addListener(this);
        recognizer.startListening(WAKEWORD_SEARCH);

        Log.d(LOG_TAG, "... listening");

    } catch (IOException e) {
        Log.e(LOG_TAG, e.toString());
    }
}
```

实现 `RecognitionListener` 的接口方法，其中 `onPartialResult()` 为主要需要实现的方法，监听器一直监听录音状态，如果检测到唤醒词则触发设备震动，并且根据当前所处的 Activity 状态执行不同的动作。

```kotlin
@Override
public void onPartialResult(Hypothesis hypothesis) {
    if (hypothesis != null) {
        final String text = hypothesis.getHypstr();
        Log.d(LOG_TAG, "on partial: " + text);
        // 如果检测到唤醒词
        if (text.equals(context.getString(R.string.wake_word))) {
            vibrator.vibrate(100);   // 使用 Vibrator API 给设备震动 100ms
            if (activity.getSupportActionBar() != null) {
                // 如果当前 Activity 存在 ActionBar，将副标题设置为空字符串
                activity.getSupportActionBar().setSubtitle("");
            }
            if (activity.getClass() == ListeningActivity.class) {
                // 使用 Activity 上下文启动 MainActivity
                Intent intent = new Intent(activity, MainActivity.class);
                activity.startActivity(intent);
            } else if (activity.getClass() == MainActivity.class) {
                onPause();
                SpeechRecognition recognition = new SpeechRecognition(activity, this);
                recognition.startRecord();
                recognition.stopRecord();
                onResume();
            }
        }
    }
}	
```

`ListeningActivity.java` 类定义了一个 APP 界面，该代码首先实例化 `WakeWordRecognizer` 对象：

```kotlin
wakeWordRecognizer = new WakeWordRecognizer(this);
```

监听唤醒状态并通过滑动条设置唤醒灵敏度，首先为 SeekBar 添加一个进度改变监听器，当拖动 seekBar 时，该监听器可以根据 SeekBar 的进度更新灵敏度的值，同时为 SeekBar 设置了两个触摸事件监听器，但未具体实现，当停止滑动 SeekBar 时，执行 onStopTrackingTouch() 方法，获得 seekBar 最终进度，重新启动语音唤醒监听器，这段代码用于设置语音识别的灵敏度，并允许用户通过 SeekBar 调整，实现了 SeekBar 相关监听器，可以更新语音唤醒相应设置

```kotlin
seekbar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
    public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
        threshold.setText(String.valueOf(progress));
    }

    public void onStartTrackingTouch(SeekBar seekBar) {
        // intentionally empty
    }

    public void onStopTrackingTouch(final SeekBar seekBar) {
        sensibility = seekBar.getProgress();
        Log.i(LOG_TAG, "Changing Recognition Threshold to " + sensibility);
        threshold.setText(String.valueOf(sensibility));
        wakeWordRecognizer.setSensibility(sensibility);
        onPause();
        onResume();
    }
});
```

定义了两个 Override 方法用于重新启动唤醒识别器实现对唤醒生命周期的控制：

```kotlin
@Override
protected void onResume() {
    super.onResume();
    if (wakeWordRecognizer != null){
        wakeWordRecognizer.onResume(); // 重新启动识别器
    }
}

@Override
protected void onPause() {
    super.onPause();
    if (wakeWordRecognizer != null){
        wakeWordRecognizer.onPause(); // 停止识别器
    }
}
```

重启和停止的具体实现方法在 `WakeWordRecognizer` 类中定义：

```kotlin
public void onResume() {
    setup(); // 重新启动监听
    Log.d(LOG_TAG, "... listening");
}

public void onPause() {
    if (recognizer != null) {
        recognizer.removeListener(this);
        recognizer.stop();
        recognizer.shutdown();
    }
}
```



## 出现问题及解决方法

- **Using flatDirs should be avoided because it doesn't support any meta-data formats**

  在 `build.gradle (Module: app)` 中添加安卓代码块：

  ```groovy
  android { ..
    sourceSets {
          main {
              jniLibs.srcDirs = ['libs']
          }
      }
  }
  ```

  然后在下面添加依赖：

  ```groovy
  implementation fileTree(dir: 'libs', include: ['*.?ar'])
  implementation (files("libs/pocketsphinx-android-5prealpha-release.aar"))
  ```

  删除掉原文件的内容：

  ```groovy
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

   ```groovy
   repositories {
   	google()
   }
   ```

2. 在 `build.gradle (Module: app)` 中添加共享库文件：

   ```groovy
   dependencies {
       implementation "androidx.constraintlayout:constraintlayout:2.1.0"
   }
   ```

3. 需要在 `activity_listening.xml` 和 `activity_main.xml` 文件中，将 `android.support.constraint.ConstraintLayout` 替换为 `androidx.constraintlayout.widget.ConstraintLayout`，然后将 `android.support.constraint.Guideline` 替换为 `androidx.constraintlayout.widget.Guideline`，可以解决程序中断的问题。

   ```groovy
   <androidx.constraintlayout.widget.ConstraintLayout
   	...
   </androidx.constraintlayout.widget.ConstraintLayout>
   ```

> Guideline 是一种特殊的控件，它在界面上是看不见的（被标记为 View.Gone），只是用来做参考线，它一般有水平和垂直两种



- 'compileDebugJavaWithJavac' task (current target is 1.8) and 'compileDebugKotlin' task (current target is 17) jvm target compatibility should be set to the same Java version.

这是从 Java 代码转换为 Kotlin 代码时的报错信息，需要在 `build.gradle (Module: app)` 中添加以下代码，操作会将 Java 和 Kotlin 目标版本都设置为 1.8，保证了它们之间的兼容性

```groovy
compileOptions {
    sourceCompatibility JavaVersion.VERSION_1_8
    targetCompatibility JavaVersion.VERSION_1_8
}
kotlinOptions {
    jvmTarget = '1.8'
}
```

- MD5 文件生成

  为单个文件生成其对应 MD5 文件，以下示例为 `words.dic` 文件生成其 MD5 文件

  ```shell
  (Get-FileHash words.dic -Algorithm MD5).Hash | Out-File -Encoding ASCII words.dic.md5
  ```

  文件夹内所有文件生成 MD5 文件，文件名为原始文件名 + '.md5'，Windows 实现代码：

  ```shell
  cd 文件夹路径
  Get-ChildItem -Path .\* -File | ForEach-Object {
      $filename = $_.Name
      $hashvalue = (Get-FileHash -Path $_.FullName -Algorithm MD5).Hash
      $newname = $filename + '.md5'
      $hashvalue | Out-File -Encoding ASCII $newname
  }
  ```

  
