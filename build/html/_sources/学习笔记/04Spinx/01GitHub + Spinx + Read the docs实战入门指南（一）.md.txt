### GitHub + Spinx + Read the docs实战入门指南（一）

参考链接：[知乎博客](https://zhuanlan.zhihu.com/p/618869114)

**<u>Spinx</u>**

- **Sphinx是什么?** Sphinx是一个自动生成文档的工具，可以用简洁的语法快速生成优雅的文档。

- **哪些场景要用Sphinx?** 如果想要写书，不想陷入复杂的排版中，可以考虑使用这个。如果有代码项目之类的，可以用它快速生成使用文档，支持markdown语法。

**<u>Read the docs</u>**

- RTD(Read the docs) 是一个文档托管网站，这一点从网站名字上就能看出来。
- 在与Github连接上配置无误的情况下，当Github上有文件改动时，会自动触发RTD自动更新对应的文档。RTD提供了丰富的文档主题，有着灵活的配置，可以满足大部分的需求。
- Github Pages是Github下自带的静态网站托管服务，选择合适主题后，也可根据Github的内容，自动排版和更新对应内容到网站中。

![](01.assets/image-20230508121129552.png)

1. 安装spinx：

   ```
   pip install spinx
   ```

2. 执行sphinx-quickstart：

   ```
   (venv) D:\ProgramFile\TestProject>sphinx-quickstart
   ```

3. 生成最原始的文档文件：

   ```
   make html
   ```

4. 查看效果。在`build/html/index.html`下可以查看最基本的Sphinx文档系统搭建

#### 二、定制化

定制化配置在`source/conf.py`中设置

1. 