### Markdown

​	为支持基于 Markdown 的文档，Sphinx 可以使用 MyST Parser 。MyST-Parser 是一个用于解析 CommonMark Markdown 风格的 Python 包。

#### 快速配置

​	要配置 Sphinx 以获取 Markdown 支持，请按以下步骤进行：

1. 安装 Markdown parser：

   ```
   pip install --upgrade myst-parser
   ```

2. 添加 myst_parser 进入 configured 扩展清单：

   ```
   extionsions = ['myst_parser']
   ```

3. 如果要使用扩展名不是 .md 的 Markdown 文件，需要调整 <u>source_suffix</u> 变量：

   ```
   source_suffix = {
       '.rst': 'restructuredtext',
       '.txt': 'markdown',
       '.md': 'markdown',
   }
   ```

4. 可以进一步配置 MyST Parser 以允许标准 CommonMark 不支持的自定义语法，需要阅读 MyST Parser 文档中的更多信息。

