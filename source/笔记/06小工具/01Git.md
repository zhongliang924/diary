# Git

## 常见 git 命令

新增文件命令：`git add`

提交文件命令：`git commit -m`

查看工作区状况：`git status -s`

拉取合并远程分支操作：`git fetch/merge` 或者 `git pull`

查看提交记录命令：`git reflog`

## git pull 和 git fetch

Git fetch branch 是把名为 branch 的远程分支拉取到本地。Git pull 是在 fetch 的基础上，把 branch 分支与当前分支进行合并；因此

pull = fetch + merge

## 撤销提交

如果需要撤销提交到索引区的文件，可以通过 `git reset HEAD file`

如果需要撤销提交到本地厂库的文件，可以通过 `git reset --soft HEAD^n` 恢复至上一次提交的状态

## 如何把本地仓库内容推向一个空的远程仓库

首先确保本地仓库和远程之间是连通的，如果提交失败，则需要以下命令进行连通：

```
git remote add origin XXXX
```

XXXX 是远程仓库地址。

如果是第一次推送，执行命令：

```
git push -u origin master
```

其中 -u 是指定 origin 为默认主支

之后的提交，只需要下面的命令：

```
git push origin master
```

