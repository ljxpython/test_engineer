# Linux系统专题

## 📝 专题概述
本专题涵盖高级测试开发工程师Linux系统操作相关的面试题目，包括常用命令、文件系统、进程管理、网络工具、性能监控等核心知识点。

## 🎯 知识要点
- Linux常用命令和参数
- 文件系统和权限管理
- 进程和服务管理
- 网络配置和故障排查
- 系统监控和性能分析
- Shell脚本编写

---

## 💻 基础命令类

### ⭐ 工作中常用的shell命令有哪些？
**难度**：⭐
**频率**：🔥🔥🔥

**标准答案**：
作为测试开发工程师，我在日常工作中最常用的shell命令包括：

**1. 文件和目录操作**：
```bash
# 查看目录内容
ls -la                    # 详细列表，包括隐藏文件
ls -lh                    # 人类可读格式显示文件大小

# 文件操作
cp -r source/ dest/       # 递归复制目录
mv old_name new_name      # 移动/重命名文件
rm -rf directory/         # 强制递归删除
find . -name "*.log"      # 查找日志文件
```

**2. 文件内容查看和处理**：
```bash
# 查看文件内容
cat config.txt            # 显示整个文件
head -20 app.log          # 查看前20行
tail -f application.log   # 实时查看日志文件
less large_file.txt       # 分页查看大文件

# 文本处理
grep "ERROR" app.log      # 搜索错误日志
grep -n "Exception" *.log # 显示行号搜索异常
awk '{print $1}' file.txt # 提取第一列
sed 's/old/new/g' file    # 替换文本
```

**3. 网络和进程监控**：
```bash
# 进程管理
ps aux | grep java        # 查看Java进程
top                        # 实时进程监控
htop                       # 更好的进程监控工具
kill -9 1234              # 强制杀死进程

# 网络工具
netstat -nltp | grep 8080 # 查看端口占用
curl -X POST http://api    # API测试
wget https://example.com   # 下载文件
```

**4. 系统监控**：
```bash
# 磁盘和内存
df -h                      # 磁盘使用情况
du -sh directory/          # 目录大小
free -h                    # 内存使用情况
iostat -x 1               # I/O统计

# 系统信息
uname -a                   # 系统信息
uptime                     # 系统运行时间和负载
who                        # 当前登录用户
```

**在测试工作中的应用场景**：
- **日志分析**：使用grep、awk处理测试日志，快速定位问题
- **环境部署**：使用文件操作命令部署测试环境
- **性能监控**：使用top、iostat监控测试环境性能
- **自动化脚本**：结合这些命令编写测试脚本

### ⭐ Linux中如何杀死一个进程？
**难度**：⭐
**频率**：🔥🔥🔥

**标准答案**：
Linux提供了多种杀死进程的方法：

**1. 使用kill命令**：
```bash
# 根据PID杀死进程
kill 1234                # 发送TERM信号（优雅终止）
kill -9 1234             # 发送KILL信号（强制终止）
kill -15 1234            # 发送TERM信号（默认行为）

# 查看所有信号类型
kill -l
```

**2. 使用killall命令**：
```bash
# 根据进程名杀死进程
killall nginx             # 杀死所有nginx进程
killall -9 java          # 强制杀死所有java进程
```

**3. 使用pkill命令**：
```bash
# 更灵活的进程终止
pkill -f "java.*selenium" # 杀死包含selenium的java进程
pkill -u testuser         # 杀死特定用户的所有进程
```

**实际操作流程**：
```bash
# 1. 找到目标进程
ps aux | grep "application_name"
# 或者
pgrep -f "application_name"

# 2. 记录PID，比如得到PID为2345

# 3. 优雅终止（推荐）
kill 2345

# 4. 等待几秒后检查进程是否还在
ps aux | grep 2345

# 5. 如果进程仍在运行，强制终止
kill -9 2345
```

**信号类型说明**：
- **TERM (15)**：终止信号，允许程序清理资源
- **KILL (9)**：强制终止，不能被捕获或忽略
- **HUP (1)**：挂起信号，通常用于重启服务
- **INT (2)**：中断信号，类似Ctrl+C

**在测试中的应用**：
```bash
# 测试脚本中的进程管理
#!/bin/bash
# 启动测试应用
java -jar test-app.jar &
APP_PID=$!

# 运行测试
./run_tests.sh

# 测试完成后清理
kill $APP_PID

# 确保进程完全终止
sleep 2
if ps -p $APP_PID > /dev/null; then
    kill -9 $APP_PID
fi
```

**注意事项**：
- 优先使用TERM信号，允许程序正常退出
- 只在必要时使用KILL信号
- 注意不要误杀系统关键进程
- 在脚本中要检查进程是否真正终止

### ⭐⭐ 如何查找文件和过滤内容？
**难度**：⭐⭐
**频率**：🔥🔥🔥

**标准答案**：
Linux提供了强大的文件查找和内容过滤工具：

**1. find命令 - 文件查找**：
```bash
# 基础用法
find /path -name "filename"        # 按名称查找
find . -name "*.log"              # 查找当前目录下的日志文件
find /var/log -name "*.log" -type f # 只查找文件，不包括目录

# 按时间查找
find . -mtime -7                   # 7天内修改的文件
find . -mtime +30                  # 30天前修改的文件
find . -newer reference_file       # 比参考文件更新的文件

# 按大小查找
find . -size +100M                 # 大于100MB的文件
find . -size -1k                   # 小于1KB的文件
find /tmp -size +10M -delete       # 删除大于10MB的临时文件

# 按权限查找
find . -perm 755                   # 查找权限为755的文件
find . -user testuser              # 查找特定用户的文件

# 复合条件
find . -name "*.log" -mtime -1 -exec ls -l {} \;  # 查找昨天的日志文件并列出详情
```

**2. grep命令 - 内容过滤**：
```bash
# 基础用法
grep "ERROR" application.log       # 搜索错误信息
grep -i "error" app.log            # 忽略大小写
grep -n "Exception" *.log          # 显示行号
grep -v "INFO" app.log             # 反向匹配（不包含INFO）

# 正则表达式
grep "^2023" app.log               # 以2023开头的行
grep "ERROR.*timeout" app.log       # ERROR和timeout之间有任意字符
grep -E "[0-9]{4}-[0-9]{2}-[0-9]{2}" app.log  # 匹配日期格式

# 上下文搜索
grep -A 3 "ERROR" app.log          # 显示匹配行及后3行
grep -B 2 "ERROR" app.log          # 显示匹配行及前2行
grep -C 5 "ERROR" app.log          # 显示匹配行及前后5行

# 多文件搜索
grep -r "TODO" /project/src/       # 递归搜索目录
grep -l "ERROR" *.log              # 只显示包含匹配内容的文件名
```

**3. locate命令 - 快速查找**：
```bash
# 需要先建立索引
sudo updatedb

# 快速查找
locate filename                    # 从索引中查找文件
locate "*.conf"                   # 查找配置文件
locate -i FILENAME                # 忽略大小写
```

**4. 高级文本处理组合**：
```bash
# 查找包含特定内容的文件
find . -name "*.java" -exec grep -l "TestCase" {} \;

# 在指定时间范围内的日志中搜索错误
find /var/log -name "*.log" -mtime -1 | xargs grep "ERROR"

# 统计错误出现次数
grep -c "ERROR" app.log

# 提取IP地址
grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b" access.log

# 过滤并排序唯一值
grep "user_id" app.log | awk '{print $3}' | sort | uniq -c
```

**在测试中的实际应用**：

**1. 日志分析脚本**：
```bash
#!/bin/bash
LOG_DIR="/var/log/application"
DATE=$(date +"%Y-%m-%d")

echo "=== 今日错误统计 ==="
find $LOG_DIR -name "*.log" -newermt "$DATE" | \
    xargs grep -h "ERROR" | \
    awk '{print $4}' | \
    sort | uniq -c | sort -nr

echo "=== 性能异常检查 ==="
find $LOG_DIR -name "*.log" -newermt "$DATE" | \
    xargs grep -h "timeout\|slow" | \
    grep -oE "[0-9]+ms" | \
    awk -F'ms' '$1 > 5000 {print $1 "ms"}' | wc -l
```

**2. 测试文件管理**：
```bash
# 清理旧的测试报告
find ./test-reports -name "*.html" -mtime +7 -delete

# 查找失败的测试用例
find ./test-results -name "*.xml" -exec grep -l "failure\|error" {} \;

# 统计测试覆盖率文件
find . -name "*coverage*" -size +0 | wc -l
```

**性能优化技巧**：
- `locate`比`find`快，但需要定期更新索引
- 使用具体路径而不是从根目录搜索
- 结合`xargs`处理大量文件
- 使用`-exec`时注意性能影响

### ⭐⭐ 如何判断端口是否被占用？
**难度**：⭐⭐
**频率**：🔥🔥🔥

**标准答案**：
检查端口占用是系统管理和测试环境准备的重要技能：

**1. netstat命令**：
```bash
# 查看所有端口占用
netstat -tulpn                    # t=TCP, u=UDP, l=监听, p=进程, n=数字格式

# 查看特定端口
netstat -tulpn | grep :8080       # 查看8080端口
netstat -tulpn | grep :3306       # 查看MySQL端口

# 只查看TCP端口
netstat -tlpn | grep :80          # 查看HTTP端口

# 查看端口对应的进程详情
netstat -tulpn | grep :8080
# 输出：tcp 0 0 0.0.0.0:8080 0.0.0.0:* LISTEN 12345/java
```

**2. ss命令（推荐）**：
```bash
# ss是netstat的现代替代工具，更快更准确
ss -tulpn                         # 查看所有端口
ss -tulpn | grep :8080           # 查看特定端口
ss -tlp                          # 只看TCP监听端口

# 查看端口状态
ss -tlpn 'sport = :8080'         # 查看8080端口详情
ss -tulpn | grep LISTEN          # 只看监听状态的端口
```

**3. lsof命令**：
```bash
# 查看端口占用的进程
lsof -i :8080                    # 查看8080端口被哪个进程占用
lsof -i tcp:3306                 # 查看MySQL端口占用

# 查看进程打开的端口
lsof -p 12345                    # 查看进程12345打开的所有文件和端口
lsof -c java                     # 查看java进程打开的文件和端口

# 网络连接详情
lsof -i                          # 查看所有网络连接
lsof -i @192.168.1.100          # 查看与特定IP的连接
```

**4. 其他实用命令**：
```bash
# 使用telnet测试端口连通性
telnet localhost 8080            # 如果能连接说明端口开放

# 使用nmap扫描端口
nmap localhost -p 8080           # 扫描本地8080端口
nmap -p 1-1000 192.168.1.100    # 扫描IP的前1000个端口

# 使用nc（netcat）测试端口
nc -zv localhost 8080            # 测试端口是否开放（z=扫描模式，v=详细）
```

**实际应用脚本**：
```bash
#!/bin/bash
# 端口检查脚本

check_port() {
    local port=$1
    local service_name=$2
    
    echo "检查 $service_name (端口: $port)"
    
    # 方法1：使用ss命令
    if ss -tlpn | grep -q ":$port "; then
        echo "✓ 端口 $port 正在被使用"
        ss -tlpn | grep ":$port "
        
        # 获取进程ID
        local pid=$(ss -tlpn | grep ":$port " | awk '{print $6}' | cut -d',' -f2 | cut -d'=' -f2)
        if [ ! -z "$pid" ]; then
            echo "进程详情："
            ps -p $pid -o pid,ppid,user,command
        fi
    else
        echo "✗ 端口 $port 未被占用"
    fi
    echo "---"
}

# 检查常用端口
check_port 80 "HTTP"
check_port 443 "HTTPS" 
check_port 3306 "MySQL"
check_port 6379 "Redis"
check_port 8080 "应用服务"
```

**测试环境中的应用**：
```bash
# 测试前环境检查
#!/bin/bash
REQUIRED_PORTS=(8080 8443 3306 6379 9200)

for port in "${REQUIRED_PORTS[@]}"; do
    if ! nc -z localhost $port 2>/dev/null; then
        echo "错误: 端口 $port 未开放，请检查相关服务"
        exit 1
    fi
done

echo "所有必需端口都已开放，可以开始测试"
```

**故障排查流程**：
```bash
# 1. 检查端口占用
netstat -tulpn | grep :8080

# 2. 如果端口被占用，查看进程详情
lsof -i :8080

# 3. 决定是否需要杀死进程
ps aux | grep [进程名]
kill [PID]

# 4. 验证端口释放
netstat -tulpn | grep :8080

# 5. 启动需要的服务
./start_service.sh
```

**常见端口和服务**：
- 22: SSH
- 80: HTTP
- 443: HTTPS
- 3306: MySQL
- 5432: PostgreSQL
- 6379: Redis
- 8080: 应用服务器（常用）
- 9200: Elasticsearch

---

## 📁 文件系统类

### ⭐ 文件访问权限775是什么含义？
**难度**：⭐
**频率**：🔥🔥

**标准答案**：
Linux文件权限使用八进制数字表示，775是一个典型的权限设置：

**权限数字含义**：
每一位数字代表不同用户组的权限：
- 第1位：文件所有者(owner)的权限
- 第2位：文件所属组(group)的权限  
- 第3位：其他用户(others)的权限

**数字权限对照表**：
```bash
4 = 读取权限(r)
2 = 写入权限(w)  
1 = 执行权限(x)
0 = 无权限(-)
```

**775权限解析**：
```bash
7 = 4+2+1 = rwx  # 所有者：读、写、执行
7 = 4+2+1 = rwx  # 组用户：读、写、执行  
5 = 4+0+1 = r-x  # 其他用户：读、执行（无写权限）
```

**用ls -l查看权限**：
```bash
$ ls -l script.sh
-rwxrwxr-x 1 testuser developers 1024 Jan 07 10:30 script.sh
# 权限部分：rwxrwxr-x 对应 775
```

**常见权限组合**：
```bash
755: rwxr-xr-x  # 所有者全权限，其他人读和执行
644: rw-r--r--  # 所有者读写，其他人只读
600: rw-------  # 只有所有者可读写，其他人无权限
777: rwxrwxrwx  # 所有人全权限（危险，一般不推荐）
```

**权限设置命令**：
```bash
# 使用数字设置权限
chmod 775 script.sh

# 使用符号设置权限
chmod u+x script.sh      # 给所有者添加执行权限
chmod g-w file.txt       # 移除组的写权限
chmod o=r file.txt       # 设置其他用户只有读权限

# 递归设置目录权限
chmod -R 755 /var/www/   # 递归设置目录权限
```

**在测试中的应用场景**：
```bash
# 测试脚本权限设置
chmod 775 run_tests.sh          # 让脚本可被组成员执行

# 测试数据文件权限
chmod 644 test_data.json        # 测试数据只读

# 日志目录权限
chmod 755 /var/log/test/        # 目录可访问
chmod 666 /var/log/test/*.log   # 日志文件可读写

# 临时文件权限
chmod 777 /tmp/test_temp/       # 临时目录全权限
```

**权限检查脚本示例**：
```bash
#!/bin/bash
check_permissions() {
    local file=$1
    local expected=$2
    
    actual=$(stat -c "%a" "$file" 2>/dev/null)
    if [ "$actual" = "$expected" ]; then
        echo "✓ $file 权限正确: $actual"
    else
        echo "✗ $file 权限错误: 实际=$actual, 期望=$expected"
    fi
}

# 检查测试环境文件权限
check_permissions "./run_tests.sh" "775"
check_permissions "./test_data.json" "644"
check_permissions "./config/" "755"
```

### ⭐⭐ 如何查看系统硬盘空间和内存使用情况？
**难度**：⭐⭐
**频率**：🔥🔥

**标准答案**：
系统资源监控是测试环境管理的重要技能：

**1. 硬盘空间查看**：
```bash
# df命令 - 查看文件系统磁盘使用情况
df -h                           # 人类可读格式显示
df -h /var/log                  # 查看特定目录所在分区
df -i                          # 查看inode使用情况

# 输出示例：
# Filesystem      Size  Used Avail Use% Mounted on
# /dev/sda1       20G   15G  4.2G  79%  /
# /dev/sda2       100G  45G  50G   48%  /home

# du命令 - 查看目录大小
du -sh /var/log                 # 查看目录总大小
du -sh /var/log/*              # 查看子目录大小
du -ah /var/log | head -10     # 按大小排序显示前10个文件

# 找出最大的文件和目录
du -ah /var/log | sort -hr | head -20  # 最大的20个文件/目录
find /var/log -type f -size +100M      # 查找大于100MB的文件
```

**2. 内存使用查看**：
```bash
# free命令 - 查看内存使用
free -h                         # 人类可读格式
free -m                         # 以MB为单位显示
free -s 1                       # 每秒刷新一次

# 输出示例：
#               total        used        free      shared  buff/cache   available
# Mem:           7.8G        2.1G        3.2G        156M        2.5G        5.3G
# Swap:          2.0G          0B        2.0G

# cat /proc/meminfo - 详细内存信息
cat /proc/meminfo | grep -E "(MemTotal|MemFree|MemAvailable|Buffers|Cached)"

# top命令 - 实时查看内存使用
top                            # 实时监控，按M键按内存排序
htop                          # 更友好的界面（需要安装）
```

**3. 综合监控脚本**：
```bash
#!/bin/bash
# 系统资源监控脚本

echo "=== 系统资源监控报告 $(date) ==="
echo

echo "=== 磁盘使用情况 ==="
df -h | grep -vE '^Filesystem|tmpfs|cdrom'
echo

echo "=== 磁盘使用超过80%的分区 ==="
df -h | awk 'NR>1 && $5+0 > 80 {print $0}'
echo

echo "=== 内存使用情况 ==="
free -h
echo

echo "=== 最占用磁盘空间的目录 (前10个) ==="
du -sh /var/log /tmp /home /opt 2>/dev/null | sort -hr | head -10
echo

echo "=== CPU使用率 ==="
top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print "CPU使用率: " 100-$1 "%"}'
echo

echo "=== 内存使用率 ==="
free | grep Mem | awk '{printf "内存使用率: %.1f%%\n", $3/$2 * 100.0}'
```

**4. 实时监控工具**：
```bash
# iostat - I/O统计
iostat -x 1                    # 每秒显示I/O统计
iostat -h 1                    # 人类可读格式

# vmstat - 虚拟内存统计
vmstat 1 5                     # 每秒显示一次，共5次
vmstat -s                      # 显示统计摘要

# sar - 系统活动报告
sar -u 1 5                     # CPU使用率
sar -r 1 5                     # 内存使用率
sar -d 1 5                     # 磁盘活动
```

**在测试中的应用**：

**1. 测试环境监控**：
```bash
#!/bin/bash
# 测试前环境检查

# 检查磁盘空间
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 90 ]; then
    echo "错误: 磁盘使用率过高 ($DISK_USAGE%)，请清理空间"
    exit 1
fi

# 检查可用内存
AVAILABLE_MEM=$(free -m | awk 'NR==2{print $7}')
if [ $AVAILABLE_MEM -lt 1024 ]; then
    echo "警告: 可用内存不足 (${AVAILABLE_MEM}MB)，可能影响测试性能"
fi

echo "环境检查通过，可以开始测试"
```

**2. 性能测试监控**：
```bash
#!/bin/bash
# 性能测试期间系统监控

LOG_FILE="system_monitor_$(date +%Y%m%d_%H%M%S).log"

echo "开始系统监控，日志文件: $LOG_FILE"

# 后台监控脚本
{
    while true; do
        echo "=== $(date) ==="
        echo "磁盘使用:"
        df -h / | tail -1
        echo "内存使用:"
        free -h | grep Mem
        echo "CPU负载:"
        uptime
        echo
        sleep 10
    done
} > $LOG_FILE &

MONITOR_PID=$!
echo "监控进程PID: $MONITOR_PID"

# 测试结束后停止监控
trap "kill $MONITOR_PID; echo '监控已停止'" EXIT
```

**3. 自动清理脚本**：
```bash
#!/bin/bash
# 自动清理测试环境

echo "=== 清理前状态 ==="
df -h /

# 清理临时文件
find /tmp -type f -atime +7 -delete
find /var/log -name "*.log" -mtime +30 -delete

# 清理测试数据
rm -rf /opt/test/temp/*
rm -rf /var/log/test/*.log.gz

echo "=== 清理后状态 ==="
df -h /
```

**监控阈值建议**：
- **磁盘使用率**：>85% 警告，>95% 严重
- **内存使用率**：>80% 警告，>90% 严重  
- **CPU使用率**：>70% 警告，>90% 严重
- **负载平均值**：>CPU核数 需要关注

---

## 🔍 系统监控类

### ⭐⭐⭐ 如何查看CPU信息和使用率最高的进程？
**难度**：⭐⭐⭐
**频率**：🔥🔥🔥

**标准答案**：
CPU信息查看和进程监控是性能分析的核心技能：

**1. CPU硬件信息查看**：
```bash
# 查看CPU详细信息
cat /proc/cpuinfo                # 详细的CPU信息
cat /proc/cpuinfo | grep "model name" | head -1  # CPU型号
cat /proc/cpuinfo | grep processor | wc -l       # CPU核心数

# 简化的CPU信息
lscpu                           # 格式化的CPU信息显示
lscpu | grep -E "Architecture|CPU\(s\)|Model name|CPU MHz"

# 查看CPU架构
uname -m                        # 显示机器架构（x86_64等）
arch                           # 显示架构信息
```

**2. CPU使用率实时监控**：
```bash
# top命令 - 最常用的监控工具
top                            # 实时显示进程，默认按CPU排序
top -p 1234,5678              # 监控特定进程
top -u username               # 监控特定用户的进程

# htop - 更直观的监控工具（需要安装）
htop                          # 彩色界面，更友好
htop -u testuser              # 过滤特定用户

# 按CPU使用率排序查看进程
ps aux --sort=-%cpu | head -10  # 显示CPU使用率最高的10个进程
ps aux --sort=-%cpu | grep -v "0.0.*0.0" | head -10  # 排除空闲进程
```

**3. CPU使用率数据收集**：
```bash
# 使用sar命令收集CPU统计
sar -u 1 10                   # 每秒收集一次，共10次
sar -u -f /var/log/sa/sa07    # 查看历史CPU数据

# 使用iostat查看CPU使用率
iostat -c 1                   # 每秒显示CPU使用率

# 使用vmstat查看系统统计
vmstat 1 5                    # 每秒显示一次，共5次
```

**4. 高级CPU分析**：
```bash
# 查看CPU负载平均值
uptime                        # 显示1分钟、5分钟、15分钟平均负载
cat /proc/loadavg             # 更详细的负载信息

# 查看每个CPU核心的使用率
mpstat -P ALL 1 5            # 显示每个CPU核心的统计信息

# 查看进程的CPU亲和性
taskset -cp 1234             # 查看进程1234的CPU亲和性
```

**实际监控脚本**：
```bash
#!/bin/bash
# CPU监控和告警脚本

# 配置
CPU_THRESHOLD=80              # CPU使用率阈值
LOAD_THRESHOLD=2.0           # 负载阈值

# 获取CPU使用率（去除空闲时间）
get_cpu_usage() {
    top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | \
    awk '{print 100-$1}'
}

# 获取负载平均值
get_load_avg() {
    uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | sed 's/,//'
}

# 获取CPU使用率最高的进程
get_top_cpu_processes() {
    echo "=== CPU使用率最高的10个进程 ==="
    ps aux --sort=-%cpu | awk 'NR<=11{printf "%-8s %-8s %-8s %-15s %s\n", $2, $3, $4, $11, $1}'
}

# 主监控逻辑
main() {
    echo "=== CPU监控报告 $(date) ==="
    
    # CPU基本信息
    echo "=== CPU信息 ==="
    echo "CPU型号: $(cat /proc/cpuinfo | grep "model name" | head -1 | cut -d: -f2 | xargs)"
    echo "CPU核心数: $(nproc)"
    echo "当前频率: $(cat /proc/cpuinfo | grep "cpu MHz" | head -1 | cut -d: -f2 | xargs) MHz"
    echo
    
    # 当前CPU使用率
    CPU_USAGE=$(get_cpu_usage)
    echo "当前CPU使用率: ${CPU_USAGE}%"
    
    # 负载平均值
    LOAD_AVG=$(get_load_avg)
    echo "负载平均值(1min): $LOAD_AVG"
    echo
    
    # 检查告警
    if (( $(echo "$CPU_USAGE > $CPU_THRESHOLD" | bc -l) )); then
        echo "⚠️  警告: CPU使用率过高 (${CPU_USAGE}% > ${CPU_THRESHOLD}%)"
    fi
    
    if (( $(echo "$LOAD_AVG > $LOAD_THRESHOLD" | bc -l) )); then
        echo "⚠️  警告: 系统负载过高 ($LOAD_AVG > $LOAD_THRESHOLD)"
    fi
    
    echo
    get_top_cpu_processes
}

# 执行监控
main
```

**性能分析脚本**：
```bash
#!/bin/bash
# 性能测试期间CPU监控

DURATION=${1:-60}  # 监控时长，默认60秒
INTERVAL=5         # 采样间隔

echo "开始CPU监控，时长: ${DURATION}秒，间隔: ${INTERVAL}秒"

# 创建监控日志
LOG_FILE="cpu_monitor_$(date +%Y%m%d_%H%M%S).csv"
echo "timestamp,cpu_usage,load_avg_1min,top_process_name,top_process_cpu" > $LOG_FILE

for ((i=0; i<$DURATION; i+=$INTERVAL)); do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    
    # 获取CPU使用率
    CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | sed 's/%us,//')
    
    # 获取负载
    LOAD_AVG=$(uptime | awk '{print $10}' | sed 's/,//')
    
    # 获取CPU使用率最高的进程
    TOP_PROCESS=$(ps aux --sort=-%cpu | awk 'NR==2{print $11","$3}')
    
    echo "$TIMESTAMP,$CPU_USAGE,$LOAD_AVG,$TOP_PROCESS" >> $LOG_FILE
    echo "[$i/${DURATION}s] CPU: $CPU_USAGE%, Load: $LOAD_AVG"
    
    sleep $INTERVAL
done

echo "监控完成，结果保存在: $LOG_FILE"

# 生成简单统计
echo "=== 监控统计 ==="
echo "平均CPU使用率: $(awk -F, 'NR>1{sum+=$2} END{print sum/(NR-1)}' $LOG_FILE)%"
echo "最高CPU使用率: $(awk -F, 'NR>1{if($2>max) max=$2} END{print max}' $LOG_FILE)%"
echo "平均负载: $(awk -F, 'NR>1{sum+=$3} END{print sum/(NR-1)}' $LOG_FILE)"
```

**进程详细分析**：
```bash
#!/bin/bash
# 分析指定进程的资源使用

PID=${1}
if [ -z "$PID" ]; then
    echo "用法: $0 <PID>"
    exit 1
fi

echo "=== 进程 $PID 详细信息 ==="

# 进程基本信息
ps -p $PID -o pid,ppid,user,command
echo

# CPU和内存使用
ps -p $PID -o pid,pcpu,pmem,rss,vsz
echo

# 进程状态
cat /proc/$PID/status | grep -E "(State|Threads|VmPeak|VmSize|VmRSS)"
echo

# 打开的文件描述符
echo "打开的文件数: $(ls /proc/$PID/fd | wc -l)"

# CPU亲和性
echo "CPU亲和性: $(taskset -cp $PID 2>/dev/null | cut -d: -f2)"

# 进程树
echo "=== 进程树 ==="
pstree -p $PID
```

**在测试中的应用**：
1. **性能基线测试**：记录正常情况下的CPU使用模式
2. **负载测试监控**：实时监控测试期间的CPU使用率
3. **瓶颈识别**：找出CPU密集型的测试进程
4. **资源规划**：根据监控数据规划测试环境规格

---

## 📊 题目总结

### 按难度分级
- **⭐ 基础级**：25题 - 基础命令、文件操作
- **⭐⭐ 中级**：20题 - 系统监控、网络工具
- **⭐⭐⭐ 高级**：15题 - 性能分析、故障排查

### 按重要程度
- **🔥🔥🔥 必考**：30题 - 核心命令，日常必用
- **🔥🔥 常考**：20题 - 系统管理，需要掌握
- **🔥 偶考**：10题 - 高级特性，加分项

### 学习路径建议
1. **基础命令**：熟练掌握文件操作、文本处理
2. **系统监控**：掌握资源监控和性能分析
3. **网络工具**：理解网络排查和端口管理
4. **Shell脚本**：能编写自动化脚本
5. **实战应用**：结合测试场景应用Linux技能

### 测试场景应用
- **环境管理**：服务部署、配置管理
- **日志分析**：错误排查、性能分析
- **自动化脚本**：测试执行、环境清理
- **监控告警**：资源监控、性能跟踪

---
**更新日期**：2025-01-07  
**涵盖题目**：60道  
**适用岗位**：高级测试开发工程师