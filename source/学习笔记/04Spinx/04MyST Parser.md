### MyST Parser

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

#### 1、排印

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

#### 2、删除线

​	使用 "strikethrough" 扩展允许使用 `"~~"` 给文本添加一个删除线。

​	例子 `~~strikethrough with *emphasis*~~` 可以转换为 ~~strikethrough with *emphasis*~~。

注意：此扩展目前仅支持HTML输出。

#### 3、数学快捷方式

通过在 `conf.py` 添加以下其中一项或两项支持解析数学公式：

- "dollarmath"：用于解析 `$` 和 `$$` 封装的数学公式
- "amsmath"：用于 `amsmath LaTex` 环境直接解析

启用 "dollarmath" 将支持解析以下语法：

- 行内公式： `$...$`  

- 行间公式 ：`$$...$$`
- 带公式编号的公式： `$$...$$(1)`

如果嵌套其它块元素（列表或引用），数学公式也会起作用。

如果添加 "amsmath" 可以直接使用 LaTex 等式，同样在其它块元素环境中也适用。

#### 4、超链接

​	添加 "linkify" 到 "myst_enable_extensions" 将自动识别 web URL 并添加超链接：

`www.example.com` -> www.example.com

这个扩展需要安装 "linkify-it-py"，使用 `pip install linkify-it-py`进行安装。

#### 5、替换

​	添加 "substitution" 到 "myst_enable_extensions"  将需要添加替换

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
---
```

可以使用内联或块使用 “{{}}” 这些替换

#### 6、使用冒号对围栏进行编码

​	添加 "colon_fence" 到 "myst_enable_extensions" 可以使用 ":::" 分隔符表示指令，而不是使用 "```"。

