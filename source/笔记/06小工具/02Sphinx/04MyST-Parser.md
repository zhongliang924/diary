# MyST-Parser

​	以下语法是可选的（默认情况下禁用），可以通过配置 Sphinx `conf.py` 配置文件启用。目标是添加更多对 Markdown 友好语法。

```
myst_enable_extensions = [
    "amsmath",
    "attrs_inline",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]
```

## 1、排印

​	添加 "smartquotes" 到 "myst_enable_extentions" 自动将标准引用转换为其它变体： `'single quotes'` 表示单个引用， `"double quotes"` 表示双倍引用。

​	添加 "replacement" 到 "myst_enable_extentions" 将自动转换一些常见的排版文本：

| text           | converted |
| -------------- | --------- |
| `(c)`, `(C)`   | ©         |
| `(tm)`, `(TM)` | ™         |
| `(r)`, `(R)`   | ®         |
| `(p)`, `(P)`   | §         |
| `+-`           | ±         |
| `...`          | …         |
| `?....`        | ?..       |
| `!....`        | !..       |
| `????????`     | ???       |
| `!!!!!`        | !!!       |
| `,,,`          | ,         |
| `--`           | –         |
| `---`          | —         |

## 2、删除线

​	使用 "strikethrough" 扩展允许使用 `"~~"` 给文本添加一个删除线。

​	例子 `~~strikethrough with *emphasis*~~` 可以转换为 ~~strikethrough with *emphasis*~~。

注意：此扩展目前仅支持HTML输出。

## 3、数学快捷方式

通过在 `conf.py` 添加以下其中一项或两项支持解析数学公式：

- "dollarmath"：用于解析 `$` 和 `$$` 封装的数学公式
- "amsmath"：用于 `amsmath LaTex` 环境直接解析

启用 "dollarmath" 将支持解析以下语法：

- 行内公式： `$...$`  

- 行间公式 ：`$$...$$`
- 带公式编号的公式： `$$...$$(1)`

如果嵌套其它块元素（列表或引用），数学公式也会起作用。

如果添加 "amsmath" 可以直接使用 LaTex 等式，同样在其它块元素环境中也适用。

## 4、超链接

​	添加 "linkify" 到 "myst_enable_extensions" 将自动识别 web URL 并添加超链接：

`www.example.com` -> www.example.com

这个扩展需要安装 "linkify-it-py"，使用 `pip install linkify-it-py`进行安装。

## 5、替换

​	添加 "substitution" 到 "myst_enable_extensions" 将需要添加替换

```
---
myst:
  substitutions:
    key1: "I'm a **substitution**"
    key2: |
      ```{note}
      {{ key1 }}
```
    key3: |
      ```{image} img/fun-fish.png
      :alt: fishy
      :width: 200px
      ```
    key4: example
可以使用内联或块使用 `“{{}}”` 这些替换

## 6、冒号编码

​	添加 "colon_fence" 到 "myst_enable_extensions" 可以使用 ":::" 分隔符表示指令，而不是使用 "```"。使用冒号也可以使内容正确呈现。与普通指令类似，这种指令可以嵌套

## 7、自生成 header anchors

​	MyST Parser 自动为 header anchors 生成标签 "slugs"，这样可以从 markdown 链接中引用它们。例如，可以本地使用 header bookmark 链接；\[](#header-anchor)；或交叉文件\[](path/to/file.md#header-anchor)。为了实现，请使用 `myst_heading_anchors=DEPTH` 配置选项，其中 Depth 表示要为其生成链接的头级别深度，

​	例如设置 `myst_heading_anchors=3`  可以为 heading anchors 生成 h1,h2和h3 级别的标签，在 markdown 中对应于 #,##和###。可以将 markdown 链接直接插入到文档中的标题生成的 anchors。几个例子：

[跳回顶部](#MyST Parser)

[跳到其它md文件](./03Markdown.md)

## 8、Anchor slug 结构

​	slugs 旨在针对 Github 部署进一步的优化：

- 将所有字母转换为小写字母
- 使用 `-` 替换所有空格
- 删除所有特殊字符 

​	要更改 slug 生成功能，设置 `myst_heading_slug_func` 函数。接受一个字符串并返回一个字符串。

## 9、定义列表

​	添加 "deflist" 到 "my_enable_extions" 能够使用自定义列表，自定义列表使用 `markdown-it-py deflist` 插件，其基于 Pandoc 定义列表规范：

> 每个术语必须放在一行上，可以选择后面跟着一个空行，并且后面必须跟随着一个或多个定义，定义以冒号或波浪号开头，可以缩进一个或两个空格

> 一个术语可以有多个定义，每个定义可以由一个或多个块元素组成（段落、代码块、列表等）。

## 10、任务列表

​	添加 "tasklist" 到 "myst_enable_extensions" 能够使用任务列表，任务列表同样使用 `markdown-it-py deflist` 插件，并应用于 [] 和 [x] 项。

```
- [ ] An item that needs doing
- [x] An item that is complete
```

- [ ] An item that needs doing
- [x] An item that is complete

## 11、字段列表

​	添加 "fieldlist" 到 "myst_enable_extensions" 能够使用字段列表，字段列表基于 reStructureText 语法从字段名称到字段正文的映射。

```
:name only:
:name: body
:*Nested syntax*: Both name and body may contain **nested syntax**.
:Paragraphs: Since the field marker may be quite long, the second
   and subsequent lines of a paragraph do not have to line up
   with the first line.
:Blocks:

  As well as paragraphs, any block syntaxes may be used in a field body:

  - Me
  - Myself
  - I

  ```python
  print("Hello, world!")
```
这一部分暂时在 Typora 里面无法可视化呈现。

## 12、属性

​	属性是通过向元素添加额外的信息来丰富标准 CommonMark 语法的一种方式。属性使用大括号 {} 指定，例如：

```
{#my-id .my_class key="value"}
```

位于块元素之间或内联元素之后，在大括号中可以识别以下语法：

- `.foo` 将 `foo` 指定为一个类，通过这种方式给出多个类，它们将被组合
- `#foo` 将 `foo` 指定为标识符，一个元素只有一个标识符，如果给定多个标识符，则使用最后一个标识符
- `key="value"` 指定键值对属性， 当值完全由 ASCII 字符或 '_' 或 ':' 或 '-' 组成时，可以不需要引号，可以使用 '\\' 转义
- `%` 开始一个注释，该注释以 `}` 或下一个 `%` 结束

属性是累积的，如果多个属性彼此跟随，则内部属性将覆盖外部属性，如果给定了多个类，它们就会组合在一起。

## 13、HTML 图像

​	MyST 提供了一些不同的语法用于在文档中包含图像，第一种是标准的 Markdown 语法：

它在可应用的配置方面受到限制，例如设置宽度。

​	MyST 允许使用指令，如 image 和 figure：

但该语法不会在常见的Markdown查看器中显示图像（例如在 Github 上查看文件）。

​	最后一个选项是直接使用 HTML，这通常不是一个好的选择，因为 HTML 在构建过程中被视为纯文本，因此 Sphinx 不会识别出要复制的图像文件，也不会将 HTML 输出为非 HTML 输出格式。

​	通过将 `"html_image"` 添加到 "myst_enable_extensions" 尝试将任何孤立的 img 标记转换为 Sphinx 中使用的内部表示：

## 14、Markdown 图形

​	通过将 `"colon_fence"` 添加到 "myst_enable_extensions" 可将上述两种扩展语法结合，图形块必须包含两个组件：以 Markdown 或 HTML 语法显示的图像、用于标题的单个段落。第一行参数是可选的，作为 reference target。

## 15、HTML 警告

​	通过将 `"html_admonition"` 添加到 "myst_enable_extensions" 可以解析 `<div class="admonition">` 块，这些块内部转换为 Sphinx 警告指令，适用于所有输出格式。当关心查看源码时，例如在 Jupyter Notebooks 中查看时很有帮助。



