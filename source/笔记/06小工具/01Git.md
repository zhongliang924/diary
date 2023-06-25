# Git

## 1、删除仓库里面的某个文件

在github上只能删除仓库,却无法删除文件夹或文件, 所以只能通过命令来解决

```
git pull origin main	# 将远程仓库里面的项目拉下来
git rm hello.py			# 删除hello.py文件
git commit -m "删除了hello.py"		# 提交操作说明
git push -u origin main	# 将项目更新提交到github项目上去
```

