# Linux 面试题

![img](../../../figs.assets/4982f69711dac4c20aa2ad8c5d79af24.gif)

参考链接：[Linux面试题](https://blog.csdn.net/a303549861/article/details/93754526?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-2.channel_param&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-2.channel_param)

## 常用命令

### 目录相关

#### find 命令

查找指定文件名的文件（不区分大小写）：`find -iname "MyProgram.c"`

对找到的文件执行某个命令：`find -iname "MyProgram.c" -exec md5sum {} \;`

查找 home 目录下的所有空文件：`find ~ -empty`

> 问：如何在 /usr 目录下找出大小超过 10MB 的文件：
>
> 答：`find /usr -type f -size +10240k`
>
> 
>
> 问：如何在 /var 目录下找出 90 天之内未被访问过的文件
>
> 答：`find /var \! -atime -90`
>
> 
>
> 问：如何在整个目录树查找文件 "core"，如发现则无需提示直接删除它们
>
> 答：`find / -name core -exec rm {} \`



#### ls 命令

以易读的方式显示文件大小（显示为 MB, GB...）：`ls -lh`

以最后修改时间升序列出文件：`ls -ltr`

在文件名后面显示文件类型：`ls -F`

#### pwd 命令

输出当前工作目录：`pwd`

#### cd 命令

可以在最近工作的两个目录间切换

#### mkdir 命令

在 home 目录下创建一个名为 temp 的目录：`mkdir ~/temp`

创建一个路径上所有不存在的目录：`mkdir -p dir1/dir2/dir3/dir4`

#### df 命令

以字节为单位输出磁盘使用量：`df -k`

以更符合阅读习惯的方式显示磁盘使用量：`df -h`

显示文件系统类型：`df -T`

#### rm 命令

删除文件前先确认：`rm -i filename.txt`

删除文件前先打印文件名并进行确认：`rm -i file*`

递归删除文件夹下的所有文件，并删除该文件夹：`rm -r example`

#### mv 命令

将 file1 重命名为 file2，如果 file2 存在则提示是否覆盖：`mv -i file1 file2`

`-v` 会输出重命名的过程，当文件名中包含通配符时，这个选项十分方便：`mv -v file1 file2`

#### cp 命令

拷贝 file1 到 file2，并保持文件的权限、属主和时间戳：`cp -p file1 file2`

拷贝 file1 到 file2，如果 file2 存在会提示是否覆盖：`cp -i file1 file2`

>问：有一普通用户每周日凌晨零点零分定期备份 /usr/backup 到 /tmp 目录下，该用户该怎么做
>
>答：`crontab -e; 0 0 * * 7 /bin/cp /usr/backup /tmp`
>
>
>
>问：每周一下午三点将 /tmp/logs 目录下面后缀名为 .log 的所有文件 rsync 同步到备份服务器 192.168.1.100 中同样的目录下面
>
>答：`crontab -e; 0 15 * * 1 rsync -avzP /tmp/logs/*.log root@192.168.1.100:/tmp/logs`

#### mount 命令

如果要挂载一个文件系统，需要先创建一个目录，然后将这个文件系统挂载到这个目录上：`mkdir /u01; mount /dev/sdb1 /u01`

也可以把它添加到 fstab 中进行自动挂载，这样任何时候重启系统，文件系统都会被加载：`/dev/sdb1 /u01 ext2 defaults 0 2`

#### cat 命令

一次查看多个文件的内容：`cat file1 file2`

在每行前面加上行号：`cat -n /etc/logrorate.conf`

> 问：如何查看当前 Linux 系统有几颗物理CPU和每颗CPU的核数
>
> 答：`cat /proc/cpuinfo | grep -c 'physical id'`；`cat /proc/cpuinfo | grep -c 'processor'`

#### tail 命令

显示最后 10 行的文本：`tail filename.txt`

显示指定行数：`tail -n N filename.txt`

实时查看，如果有新行添加到文件尾部，它会继续输出新的行，查看日志非常有用：`tail -f log-file`

#### less 命令

可以在不加载整个文件下显示文件内容，查看大型日志非常有用：`less hug-log-file.log`，向前滚屏 `Ctrl + F`，向后滚屏 `Ctrl + B`

### 通用命令

#### grep 命令

在文件中查找字符串（不区分大小写）：`grep -i "the" demo_file`

输出成功匹配的行，以及该行之后的三行：`grep -A 3 -i "example" demo_file`

在一个文件夹中递归查询包含指定字符串的文件：`grep -r "ramesh" *`

#### sed 命令

将 Docs 系统中的文件复制到 Unix/Linux 后，每个文件都会以 `\r\n` 结尾，sed 可以轻易将其转换为 Unix 格式文件，使用 `\n` 结尾的文件：`sed 's/.$//' filename`

反转文件内容并输出：`sed -n '1!G; h; p' filename`

为非空行添加行号：`sed '/./=' test.txt | sed 'N; s/\n/ /'`

> 问：用 sed 命令将指定的路径 /usr/loacl/http 替换为 /usr/src/local/http
>
> 答：`echo "usr/local/http" | sed 's#/usr/local/#/usr/src/local/#'`
>
> 
>
> 问： 打印 /etc/ssh/sshd_config 的第一百行
>
> 答：`sed -n '100p' /etc/ssh/sshd_config`

#### awk 命令

删除重复行：`$awk '!($0 in array) {array[$0]; print}' temp`

打印 `/etc/passwd` 中包含同样的 uid 和 gid 的行：`awk -F ':' '$3=$4' /etc/passwd`

打印文件中的指定部分的字段：`awk '{print $2,$5}' employee.txt`

> 问：打印 /etc/pawwd 的 1 到 3 行
>
> 答：`sed -n '1,3p' /etc/passwd`；`awk 'NR>=1&&NR<=3{print $0}' /etc/passwd`

#### vim 命令

打开文件并跳到第 10 行：`vim +10 filename.txt`

打开文件跳到第一个匹配的行：`vim +/search-term filename.txt`

以只读方式打开：`vim -R /etc/passwd`

#### diff 命令

比较的时候忽略空白符：`diff -w name_list.txt name_list_new.txt`

#### sort 命令

以升序对文件进行排序：`sort names.txt`

以降序对文件进行排序：`sort -r names.txt`

#### xargs 命令

将所有图片文件拷贝到外部驱动器：`ls *.jpg | xargs -n1 -i cp {} /external-hard-drive/directory `

将系统所有 jpg 文件压缩打包：`find / -name *.jpg -type f -print | xargs tar -cvzf images.tar.gz`

下载文件中列出的所有 url 的页面：`cat url-list.txt | xargs wget -c`

### 压缩相关

#### tar 命令

创建一个新的 tar 文件：`tar cvf archive_name.tar dirname/`

解压 tar 文件：`tar xvf archive_name.tar`

查看 tar 文件：`tar tvf archive_name.tar`

#### gzip 命令

创建一个 `*.gz` 的压缩文件：`gzip test.txt`

解压 `*.gz` 文件：`gzip -d test.txt.gz`

显示压缩的比率：`gzip -l *.gz`

#### bzip2 命令

创建 `*.bz2` 压缩文件：`bzip2 test.txt`

解压 `*.bz2` 文件：`bzip2 -d test.txt.bz2`

#### unzip 命令

解压 `*.zip` 文件：`unzip test.zip`

查看 `*.zip` 文件的内容：`unzip -l jasper.zip`

### 系统命令

#### export 命令

输出跟字符串 oracle 匹配的环境变量：`export | grep ORACLE`

设置全局环境变量：`export ORACLE_HOME=/u01/app/oracle/product/10.2.0`

#### kill 命令

kill 用于终止一个进程，一般先用 `ps -ef` 查看某个进程得到进程号，然后使用 `kill -9 进程号` 终止该进程 （-9 表示强制停止指定进程，一般情况下只需要 `kill 进程号` 就可以结束）

#### passwd 命令

用于在命令行修改密码，使用这个命令要求您首先输入旧密码，然后输入新密码：`passwd`

修改其它用户的密码：`passwd USERNAME`

删除某个用户的密码：`passwd -d USERNAME`

#### su 命令

用于切换用户账号：`su - USERNAME`

用户 john 使用 raj 用户名执行 ls 命令，执行完后返回 john 账号：`su - raj -c ls`

用指定用户登录，并且使用指定的 Shell 程序：`su -s 'SHELLNAME' USERNAME`

#### yum 命令

安装 apache：`yum install httpd`

更新 apache：`yum update httpd`

卸载/删除 apache：`yum remove apache`

#### rpm 命令

使用 rpm 安装 apache：`rpm -ivh httpd-2.2.3-22.0.1.el5.i386.rpm`

更新 apache：`rpm -uvh httpd-2.2.3-22.0.1.el5.i386.rpm`

卸载/删除 apache：`rpm -ev httpd`

#### shutdown 命令

关闭系统并立即关机：`shutdown -h now`

10 分钟后关机：`shutdown -h +10`

重启：`shutdown -r now`

重启期间强制执行系统检查：`shutdown -Fr now`

#### crontab 命令

查看某个用户的 crontab 设置：`crontab -u user -l`

设置一个每十分钟执行一次的计划任务：`*/10 * * * * /home/ramesh/check-disk-space`

#### service 命令

查看服务状态：`service ssh status`

查看所有服务状态：`service --status-all`

重启服务：`service ssh restart`

#### chmod 命令

chmod 用于改变文件和目录的权限

给指定文件的属主和属组所有权限（包括读、写、执行）：`chmod ug+rwx file.txt`

删除指定文件的属组的所有权限：`chmod g-rwx file.txt`

修改目录的权限，以及递归修改目录下面所有文件和子目录的权限：`chmod -R ug+rwx file.txt`

#### chown 命令

chown 用于改变文件属主和属组

同时将某个文件的属主改为 oracle，属组改为 db：`chown oracle:dba dbora.sh`

使用 `-R` 对目录和目录下的文件进行递归修改：`chown -R oracla:dba /home/oracle`

#### uname 命令

显示系统内核名称、主机名、内核版本号、处理器类型之类信息：`uname -a`

#### whereis 命令

当不知道某个命令的位置时可以使用 whereis 命令：`whereis ls`

当想查找某个可执行程序的位置，但这个程序又不在 whereis 的默认目录下，可以使用 `-B` 选项，并指定目录作为这个选项的参数。

在 `/tmp` 目录下查找 lsmk 命令：`whereis -u -B /tmp -f lsmk`

#### locate 命令

显示系统中所有包含 crontab 字符串的文件：`locate crontab`

#### man 命令

显示某个命令的 man 页面：`man crontab`

### 网络相关

#### ifconfig 命令

查看所有网络接口及其状态：`ifconfig -a`

使用 up 和 down 命令启动或停止某个接口：`ifconfig eth0 up` 和 `ifconfig eth0 down`

> 问：用一条命令显示本机 eth0 网卡的 IP 地址，不显示其它字符？
>
> 答：方法1：`ifconfig eth0 | grep inet | awk -F ':' '{print $2}' | awk '{print $1}'`
>
> ​		方法2：`ifconfig eth0 | grep "inet addr" | awk -F '[ :]+' '{print $4}'`

#### ping 命令

ping 一个远程主机，只发 5 个数据包：`ping -c 5 gmail.com`

> 问：如何禁止服务器被 ping？
>
> 答：`echo 1 > /proc/sys/net/ipv4/icmp_echo_ignore_all`不能 ping 通，
>
> ​       `echo 0 > /proc/sys/net/ipv4/icmp_echo_ignore_all`这个时候能 ping 通

#### curl 命令

如果使用 ping 测试某个地址是否能连接，那么 curl 测试 URL 是否可以访问。

> 问：写出一个 curl 命令，访问指定服务器 61.135.167.121 上的如下 URL，**http://www.baidu.com/s?wd=test** ，访问超时是 20秒
>
> 答：`curl --connect-timeout 20 https://61.135.169.121/s?wd=test`

#### wget 命令

使用 wget 从网上下载软件、音乐、视频：`wget http://prdownloads.sourceforge.net/sourceforge/nagios/nagios-3.2.1.tar.gz`

下载文件并以指定的文件名保存文件：`wget -O taglist.zip http://www.vim.org/scripts/download_script.php?src_id=7701`

#### ftp 命令

连接 ftp 服务器并下载文件：`ftp IP/hostname; ftp > mget *.html`

#### ssh 命令

连接远程主机：`ssh username@remotehost.example.com`

#### ps 命令

ps 命令用于显示正在运行的进程的信息

查看当前运行的所有进程：`ps -ef | more`

以树状结构显示当前正在运行的进程，H 表示显示线程的层次结构：`ps -efH | more`

> 问：查看后台所有 java 进程？
>
> 答：ps -ef | grep java

#### uptime 命令

可以快速查看及其负载情况，命令显示 1 分钟、5 分钟、15 分钟平均负载情况，了解服务器负载是趋于紧张还是趋于缓解

#### dmesg 命令

输出系统日志最后 10 行，这些日志可以帮助排查性能问题

#### vmstat 命令

输出系统核心指标，包括 CPU 资源的进程数（CPU 负载情况）、系统可用内存数、交换区写入和读取数量、CPU 时间消耗，可以用来判断 CPU 是否处于繁忙状态。

#### mpstat 命令

显示每个 CPU 占用情况，如果有一个 CPU 占用率特别高，那么有可能是一个单线程应用程序引起的

#### pidstat 命令

显示输出进程的 CPU 占用情况，该命令会持续输出，并且不会覆盖之前的数据，可以方便查看系统动态

#### iostat 命令

读写状态，如果显示的是逻辑设备的数据，那么设备利用率不代表后端实际硬件设备已经饱和。值得注意的是，即使 IO 性能不理想，也不一定意味着这个应用程序会不好，可以利用诸如预读取、写缓存等策略提升应用性能。

#### free 命令

可以查看内存使用情况，`-m` 表示按照兆字节显示。如果可用内存非常少，系统可能会动用交换区（如果配置了的话），这样会增加 IO 开销，降低系统性能。

> 问：Linux 系统里，buffer 和 cache 该如何区分？
>
> 答：Buffer 和 Cache 都是内存中的一块区域。当 CPU 需要写数据到磁盘时，由于磁盘速度比较慢，所以 CPU 先把数据存进 Buffer，然后 CPU 去执行其它任务，Buffer 中的数据定期写入磁盘；当 CPU 需要从磁盘读取数据时，由于磁盘速度比较慢，可以把即将用到的数据提前存入 cache，CPU 直接从 cache 拿数据要快得多。

#### sar 命令

sar 命令可以查看网络设备吞吐率。在排查性能问题时，可以通过网络设备的吞吐量，判断网络设备是否已经饱和。

> 问：我们可以使用哪个命令查看系统的历史负载（比如说两天前的）
>
> 答：查看 22 号的系统负载：`sar -q -f /var/log/sa/sa22`   

#### top 命令

top 命令包含前面好几个命令的检查内容。比如负载情况（uptime）、系统内存使用情况（free）、系统 CPU 使用情况（vmstat）等。因此，通过这个命令，可以全面查看负载的来源。同时，top 命令支持排序，可以按照不同的列排序，方便查找诸如内存占用最多的进程、CPU 占用率最高的进程等。

#### netstat 命令

> 问：如何查看系统都开启了哪些端口
>
> 答：`netstat -lnp`
>
> 
>
> 问：如何查看网络连接状况
>
> 答：`netstat -an`
>
> 问：如何统计当前进程连接数
>
> 答：`netstat -an | grep ESTABLISHED | wc -l`
>
> 
>
> 问：用 netstat 命令配合其它命令，按照源 IP 统计所有到 80 端口的 ESTABLISHED 状态链接的个数？
>
> 答：首先使用命令：`netstat -an | grep ESTABLISHED`，查找并显示当前系统中所有处于 “ESTABLISHED" 状态的网络连接
>
> ​       进一步修改命令：`netstat -an|grep ESTABLISHED|grep ":80"|awk 'BEGIN{FS="[[:space:]:]+"}{print $4}'`，用于查找并提取在端口 80 上处于 "Established" 状态的网络连接的远程 IP 地址
>
> ​       进一步修改命令：`netstat -an|grep ESTABLISHED|grep ":80"|awk 'BEGIN{FS="[[:space:]:]+"}{print $4}'|sort|uniq -c|sort -nr`，在上一条命令基础上，按连接数量从高到低进行排序，以便识别出连接数量最多的 IP 地址

## Linux 概述

### Linux 体系结构

Linux 体系结构可以分为两块：

- 用户空间（User Space）：包括用户应用程序（User Applications）、C 库（C Library）
- 内核空间（Kernel Space）：包括系统调用接口（System Call Interface）、内核（Kernel）、平台架构相关代码（Architecture-Dependent Kener Code）

> 问：为什么 Linux 体系结构要分为用户空间和内核空间？
>
> 答：现代 CPU 实现了不同的工作模式，不同模式下 CPU 可以执行的指令和访问的寄存器不同；Linux 从 CPU 的角度出发，为了保护内核安全，把系统分为两个部分

### Linux 进程间通信方式

1. 管道 pipe、流管道 s_pipe、有名管道 FIFO
2. 信号 signal
3. 消息队列
4. 共享内存
5. 信号量
6. 套接字 socket

### 磁盘、目录和文件

在 Linux 操作系统中，所有被操作系统管理的资源，例如网络接口、磁盘驱动器、打印机、输入输出设备、普通文件或目录都被看做是一个文件。

Linux 系统的重要概念：**一切都是文件**。Linux 是重写 Unix 而来，这个概念被传承了下来，用户可以用读写文件的方式实现对硬件的访问。

Linux 常见目录说明：

- **/bin**：存放二进制可执行文件，常用命令一般都在这里
- **/etc**：存放系统管理和配置文件
- **/home**：用户文件根目录
- **/usr**：存放系统应用程序
- **/opt**：额外安装的可选应用程序包所放置的位置
- **/proc**：虚拟文件系统目录，是系统内存的映射，可以直接访问这个目录获取系统信息
- **/root**：超级用户的主目录（系统管理员）
- **/dev**：用于存放设备文件
- **/lib**：存放系统运行相关库文件
- **/var**：存放运行时需要改变数据的文件，某些大文件溢出区

### 硬链接和软链接

**硬链接**

由于 Linux 下的文件是通过节点（inode）来识别文件。硬链接可以认为是一个指针，指向文件索引节点的指针，每添加一个硬链接，文件的链接数就加 1。

硬链接主要的不足包括：（1）不可以在不同文件系统的文件建立链接（2）只有超级用户才能为目录创建硬链接

**软链接**

软链接克服了硬链接的不足，没有文件系统的限制，任何用户可以创建指向目录的符号链接，它具有更大的灵活性，甚至可以跨越不同机器、不同网络对文件进行链接。

软链接的不足包括：（1）因为链接文件包含源文件的路径信息，当源文件从一个目录移动到其它目录时，再访问链接文件，系统就找不到了，而硬链接则没有这个缺陷；（2）它要系统分配额外的空间用于建立新的索引节点和保存源文件的路径

两者的主要区别如下：

- 硬链接不可以跨分区，软链接可以跨分区
- 硬链接指向一个 inode 节点，而软链接则是创建一个 inode 节点
- 删除硬链接文件不会删除原文件，而删除软链接文件不会删除原文件内容，但会导致软链接失效。

### RAID

RAID 全称为**独立磁盘冗余阵列**(Redundant Array of Independent Disks)，基本思想就是把多个相对便宜的硬盘组合起来，成为一个硬盘阵列组，使性能达到甚至超过一个价格昂贵、 容量巨大的硬盘。RAID 通常被用在服务器电脑上，使用完全相同的硬盘组成一个逻辑扇区，因此操作系统只会把它当做一个硬盘。

RAID 分为不同的等级，各个不同的等级均在数据可靠性及读写性能上做了不同的权衡。在实际应用中，可以依据自己的实际需求选择不同的 RAID 方案。

### 网络

#### iptables 命令

iptables 是一个配置 Linux 内核防火墙命令工具。对于开发来说，主要掌握如何开放端口即可。

把来源 IP 为 192.168.1.101 访问本机 80 端口的包直接拒绝：`iptables -I INPUT -s 192.168.1.101 -p tcp --dport 80 -j REJECT`

开启 80 端口：`iptables -A INPUT -p tcp --dport 80 -j ACCEP`

另外，注意使用 `iptables save` 命令进行保存，否则服务器重启后配置规则将丢失。

#### route 命令

添加一条到 192.168.3.0/24 的路由，网关为：192.168.1.254：`route add -net 192.168.3.0/24 netmask 255.255.255.0 gw 192.168.1.254`

#### tcpdump 命令

在 Linux 系统下按照下面要求抓包：只过滤出 HTTP 服务，目标 IP 为 192.168.0.111，一共抓 1000 个包，并且保存到 1.cap 文件中：`tcpdump -nn -s0 host 192.168.0.111 and port 80 -c 1000 -w 1.cap`

#### 如何设置静态 IP

参见文章 [《Linux 设置静态IP》](https://www.jianshu.com/p/33784a06c1a9) 。这是一个必备技能。

> 问：是否可以给一个网卡配置多个 IP？
>
> 答：可以，但一般比较少这么做；更多的是一台服务器有两个网卡，配置了两个不同的 IP

#### 设置 DNS

全局配置，可以在 `/etc/resolv.conf` 文件中配置

> 问：/etc/hosts 文件做什么用
>
> 答：可以配置指定域名和 IP 的映射关系
>
> 
>
> 问：Linux 下如何指定 dns 服务器，来解析某个域名
>
> 答：使用 dig 命令：`dig @8.8.8.8 www.baidu.com` 使用谷歌 DNS 解析百度

### SHELL

#### Shell 是什么

一个 SHELL 脚本是一个文本文件，包含一个或多个命令。作为系统管理员，我们经常需要使用多个命令来完成一项任务，我们可以添加这些所有命令在一个文本文件（SHELL 脚本）来完成这些日常工作任务。

在 Linux 操作系统，`"/bin/bash"` 是默认登录 shell，是在创建用户时分配的。

> 问：在 SHELL 脚本中，如何写入注释？
>
> 答：注释可以用来描述一个脚本可以做什么和它是如何工作的。每一行注释以 `#` 开头

#### 语法级

在 SHELL 脚本中，可以使用两种类型的变量：

- 系统定义变量：由系统自己创建，可以通过 `set` 命令查看
- 用户定义变量：由用户生成和定义，变量值可以通过 `"echo $<变量名>"` 来查看

在写一个 Shell 脚本时，如果想要检查前一命令是否执行成功，在 `if` 条件中使用 `$?` 可以检查前一个命令的结束状态

如果结束状态是 **0**，说明前一个命令执行成功；如果结束状态不是 **0**，说明命令执行失败。

> 问：Bourne Shell(Bash) 中有哪些特殊的环境变量？
>
> 答：$0：命令行中的脚本名字
>
> $1：第一个命令行参数
>
> $2：第二个命令行参数
>
> $#：命令行参数的数量
>
> $*：所有命令行参数，以空格隔开
>
> 
>
> 问：如何取消变量或取消变量赋值？
>
> 答：`unset` 命令用于取消变量或取消变量赋值，语法：`unset <变量名>`
>
> 
>
> 问：`#!/bin/bash` 的作用
>
> 答：`#!/bin/bash` 是 Shell 脚本的第一行，它的意思是命令通过 `/bin/bash` 来执行

### 实战

#### Linux 操作系统版本

一般来讲，桌面用户首选 Ubuntu；服务器用户首选 RHEL 或 CentOS，两者中首先 Centos。

根据具体需要：

- 安全性要求较高，选择 Debain 或者 FreeBSD
- 需要使用数据库高级服务和电子邮件网络应用可以选择 SUSE
- 想要技术新功能选 Feddora，Feddora 是 RHEL 和 CentOS 的一个测试版和预发布版本

根据**现有状况**，绝大多数互联网公司选择 CentOS，现在比较常用的是 6 系列，市场占用大概一半左右，另外的原因是 CentOS 更侧重于服务器领域，并且无版权约束。

### 网站访问

当用户反馈网站访问慢，主要有以下几个因素：

- 服务器出口带宽不够用
  - 本身服务器购买的出口带宽较小，一旦并发量大，就会造成分给每个用户的出口带宽小，访问速度慢
  - 跨运营商网络导致带宽缩减
- 服务器负载过大，导致响应不过来
  - 分析系统负载，可以使用 uptime 命令查看系统负载。如果负载很高，则使用 top 命令查看 CPU、MEM 等占用情况，要么是 CPU 繁忙，要么是内存不够
  - 如果两者都正常，使用 sar 命令分析网卡流量，分析是否遭到攻击
- 数据库瓶颈
  - 如果慢查询比较多，那么需要开发人员或 DBA 协助进行 SQL 语句优化
  - 如果数据库响应慢，考虑加一个数据库缓存，如 Redis 等。然后，也可以搭建 MySQL 主从，一台 MySQL 服务器负责写，其他几台从数据库负责读
- 网站开发代码没有优化好
  - 例如 SQL 语句没有优化，导致数据库读写耗时



