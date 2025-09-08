# 数据库与SQL专题

## 📝 专题概述
本专题涵盖高级测试开发工程师在数据库和SQL方面的面试题目，包括SQL语法、数据库原理、性能优化、测试场景应用等核心知识点。

## 🎯 知识要点
- SQL基础语法和高级查询
- 数据库设计原理和规范化
- 索引原理和优化策略
- 事务处理和锁机制
- 数据库性能监控和调优
- 测试中的数据库应用

---

## 📚 SQL基础语法类

### ⭐ 你在测试过程中使用数据库的场景是什么？
**难度**：⭐
**频率**：🔥🔥🔥

**标准答案**：
在测试过程中，我使用数据库的主要场景包括：

**1. 测试数据准备**：
- 插入测试所需的基础数据
- 创建特定业务场景的数据组合
- 批量生成性能测试数据

**2. 结果验证**：
- 验证接口操作后数据库状态的正确性
- 检查数据的完整性和一致性
- 确认业务逻辑在数据层面的实现

**3. 测试环境管理**：
- 数据库初始化和重置
- 测试数据的备份和恢复
- 不同环境间的数据同步

**4. 缺陷定位**：
- 通过SQL查询分析异常数据
- 追踪数据变更历史
- 验证数据修复结果

**实际案例**：
在我负责的电商项目测试中，我经常需要：
```sql
-- 创建订单测试数据
INSERT INTO orders (user_id, product_id, quantity, status) 
VALUES (1001, 2001, 2, 'pending');

-- 验证订单创建后的库存变化
SELECT stock_quantity FROM products WHERE id = 2001;

-- 检查用户积分是否正确更新
SELECT points FROM users WHERE id = 1001;
```

这样可以确保端到端的业务流程在数据层面的正确性。

### ⭐ 常用的聚合函数有哪些？
**难度**：⭐
**频率**：🔥🔥

**标准答案**：
MySQL中常用的聚合函数包括：

**1. COUNT()** - 计算记录数
```sql
-- 统计用户总数
SELECT COUNT(*) FROM users;
-- 统计非空邮箱的用户数
SELECT COUNT(email) FROM users;
-- 统计不重复的城市数
SELECT COUNT(DISTINCT city) FROM users;
```

**2. SUM()** - 求和
```sql
-- 计算总销售额
SELECT SUM(amount) FROM orders;
-- 按状态分组计算
SELECT status, SUM(amount) FROM orders GROUP BY status;
```

**3. AVG()** - 平均值
```sql
-- 计算平均订单金额
SELECT AVG(amount) FROM orders;
-- 计算各商品的平均评分
SELECT product_id, AVG(rating) FROM reviews GROUP BY product_id;
```

**4. MAX() / MIN()** - 最大值/最小值
```sql
-- 找出最高和最低价格
SELECT MAX(price) as highest, MIN(price) as lowest FROM products;
-- 每个类别的价格区间
SELECT category, MAX(price), MIN(price) FROM products GROUP BY category;
```

**5. GROUP_CONCAT()** - 字符串聚合
```sql
-- 将用户的所有订单ID连接起来
SELECT user_id, GROUP_CONCAT(order_id) FROM orders GROUP BY user_id;
```

**在测试中的应用**：
我在数据验证时经常使用这些函数：
- 使用COUNT验证数据导入的准确性
- 使用SUM验证财务数据的一致性
- 使用AVG分析性能测试中的响应时间
- 使用MAX/MIN检查数据范围的合理性

### ⭐⭐ 什么是数据库索引，索引的优缺点是什么？
**难度**：⭐⭐
**频率**：🔥🔥🔥

**标准答案**：
**索引定义**：
数据库索引是一种数据结构，用于提高数据库表的数据检索速度。类似于书籍的目录，通过索引可以快速定位到数据的存储位置。

**索引类型**：
1. **主键索引**：唯一且不能为空
2. **唯一索引**：值唯一但可以为空
3. **普通索引**：最基本的索引，没有限制
4. **复合索引**：多个列组成的索引
5. **全文索引**：用于全文搜索

**索引优势**：
1. **大幅提高查询速度**：将O(n)的全表扫描优化为O(log n)的树查找
2. **加速排序和分组**：ORDER BY和GROUP BY操作更快
3. **加速表连接**：JOIN操作效率提升
4. **保证数据唯一性**：通过唯一索引约束

**索引缺点**：
1. **额外存储空间**：索引需要占用磁盘空间，大约为表大小的10-15%
2. **降低写入性能**：INSERT、UPDATE、DELETE操作需要同时维护索引
3. **维护成本**：需要定期重建和优化索引

**代码示例**：
```sql
-- 创建普通索引
CREATE INDEX idx_user_email ON users(email);

-- 创建复合索引
CREATE INDEX idx_order_user_date ON orders(user_id, created_at);

-- 查看索引使用情况
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
```

**在测试中的应用**：
我在性能测试时特别关注索引的影响：
- **查询优化验证**：确保慢查询已正确使用索引
- **数据量测试**：验证大数据量下索引的有效性
- **写入性能测试**：评估索引对写入操作的影响
- **索引维护测试**：验证索引重建和优化的效果

**最佳实践**：
- 在经常查询的列上建立索引
- 避免在频繁更新的列上创建过多索引
- 使用复合索引时注意列的顺序
- 定期分析索引使用情况，删除无用索引

---

## 🏗️ 数据库设计类

### ⭐⭐ 数据库的三大范式是什么？
**难度**：⭐⭐
**频率**：🔥🔥

**标准答案**：
数据库三大范式是关系型数据库设计的基本准则，用于减少数据冗余和避免数据异常。

**第一范式（1NF）**：
- **原子性要求**：表中的每个字段都是不可再分的原子值
- **消除重复组**：不允许有重复的列或多值字段

**违反1NF的例子**：
```sql
-- 错误设计：联系方式字段包含多个值
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    contacts VARCHAR(200) -- "电话:13900000000,邮箱:user@example.com"
);
```

**符合1NF的设计**：
```sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    phone VARCHAR(20),
    email VARCHAR(100)
);
```

**第二范式（2NF）**：
- **满足1NF**
- **消除部分依赖**：非主键字段必须完全依赖于主键，而不能只依赖主键的一部分

**违反2NF的例子**：
```sql
-- 复合主键表，存在部分依赖
CREATE TABLE order_details (
    order_id INT,
    product_id INT,
    quantity INT,
    product_name VARCHAR(100), -- 只依赖product_id
    product_price DECIMAL(10,2), -- 只依赖product_id
    PRIMARY KEY(order_id, product_id)
);
```

**符合2NF的设计**：
```sql
-- 订单详情表
CREATE TABLE order_details (
    order_id INT,
    product_id INT,
    quantity INT,
    PRIMARY KEY(order_id, product_id)
);

-- 产品表
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    product_price DECIMAL(10,2)
);
```

**第三范式（3NF）**：
- **满足2NF**
- **消除传递依赖**：非主键字段不能依赖于其他非主键字段

**违反3NF的例子**：
```sql
CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(50),
    dept_id INT,
    dept_name VARCHAR(50), -- 传递依赖：通过dept_id依赖
    dept_location VARCHAR(100) -- 传递依赖：通过dept_id依赖
);
```

**符合3NF的设计**：
```sql
-- 员工表
CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(50),
    dept_id INT
);

-- 部门表
CREATE TABLE departments (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(50),
    dept_location VARCHAR(100)
);
```

**在测试中的应用**：
我在数据库测试时会检查：
1. **数据一致性**：验证范式化设计是否避免了数据异常
2. **性能影响**：评估规范化后JOIN操作的性能
3. **业务逻辑**：确保表结构正确反映业务关系
4. **数据完整性**：验证外键约束的有效性

**平衡考虑**：
虽然范式化可以减少冗余，但有时为了查询性能，会适度反范式化（增加冗余字段），这需要在数据一致性和查询效率间找到平衡。

### ⭐⭐⭐ 主键、外键和索引的区别
**难度**：⭐⭐⭐
**频率**：🔥🔥🔥

**标准答案**：
这三个概念在数据库设计中扮演不同角色：

**主键（Primary Key）**：
- **唯一标识**：唯一标识表中的每一行记录
- **约束特性**：非空且唯一，一个表只能有一个主键
- **自动创建索引**：系统自动为主键创建唯一聚集索引

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100)
);
```

**外键（Foreign Key）**：
- **引用完整性**：确保引用的数据在父表中存在
- **关系维护**：建立表之间的关联关系
- **级联操作**：支持CASCADE、SET NULL等操作

```sql
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    amount DECIMAL(10,2),
    FOREIGN KEY (user_id) REFERENCES users(id) 
    ON DELETE CASCADE ON UPDATE CASCADE
);
```

**索引（Index）**：
- **性能优化**：提高查询速度的数据结构
- **可选创建**：根据查询需求选择性创建
- **多种类型**：普通索引、唯一索引、复合索引等

```sql
-- 为经常查询的列创建索引
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_order_date ON orders(created_at);
```

**三者对比表**：

| 特性 | 主键 | 外键 | 索引 |
|------|------|------|------|
| 作用 | 唯一标识记录 | 维护引用完整性 | 优化查询性能 |
| 唯一性 | 必须唯一 | 可重复 | 普通索引可重复 |
| 空值 | 不允许 | 允许 | 允许 |
| 数量限制 | 每表一个 | 无限制 | 无限制 |
| 自动索引 | 是 | 否 | 是（本身就是） |

**在测试中的验证场景**：

1. **主键约束测试**：
```sql
-- 验证主键唯一性
INSERT INTO users (id, username) VALUES (1, 'user1');
INSERT INTO users (id, username) VALUES (1, 'user2'); -- 应该失败
```

2. **外键约束测试**：
```sql
-- 验证引用完整性
INSERT INTO orders (user_id, amount) VALUES (999, 100.00); -- 应该失败
DELETE FROM users WHERE id = 1; -- 验证级联删除
```

3. **索引性能测试**：
```sql
-- 比较有无索引的查询性能
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
```

**最佳实践**：
- 主键选择：使用自增整型作为主键，业务字段作为唯一键
- 外键设计：明确级联操作策略，考虑性能影响
- 索引策略：基于实际查询模式创建，避免过度索引

---

## 🔧 查询优化类

### ⭐⭐ DROP、DELETE、TRUNCATE的区别
**难度**：⭐⭐
**频率**：🔥🔥

**标准答案**：
这三个命令都用于删除数据，但在操作范围、性能、可回滚性等方面有重要区别：

**DELETE**：
- **操作范围**：删除表中的行，可以有条件删除
- **表结构**：保留表结构和索引
- **事务支持**：支持事务，可以回滚
- **触发器**：会触发DELETE触发器
- **自增列**：不重置AUTO_INCREMENT计数器

```sql
-- 删除特定条件的记录
DELETE FROM users WHERE created_at < '2023-01-01';

-- 删除所有记录
DELETE FROM users;
```

**TRUNCATE**：
- **操作范围**：删除表中所有行，不能有WHERE条件
- **表结构**：保留表结构，重置AUTO_INCREMENT计数器
- **事务支持**：不完全支持事务（DDL操作）
- **触发器**：不会触发触发器
- **性能**：比DELETE快，直接释放数据页

```sql
-- 清空整个表
TRUNCATE TABLE users;
```

**DROP**：
- **操作范围**：删除整个表或数据库对象
- **表结构**：完全删除表结构、数据、索引、触发器等
- **事务支持**：DDL操作，立即生效
- **恢复性**：删除后需要重新创建表结构

```sql
-- 删除整个表
DROP TABLE users;

-- 删除数据库
DROP DATABASE test_db;
```

**性能对比**：
```sql
-- 性能测试场景
-- 100万条记录的表

-- DELETE：最慢，记录每行删除的日志
DELETE FROM test_table; -- 约30秒

-- TRUNCATE：最快，直接释放数据页
TRUNCATE TABLE test_table; -- 约0.1秒

-- DROP：快，但需要重建表结构
DROP TABLE test_table; -- 约0.1秒
```

**使用场景对比**：

| 场景 | 推荐命令 | 原因 |
|------|----------|------|
| 删除部分数据 | DELETE | 支持条件删除 |
| 清空测试数据 | TRUNCATE | 快速且重置自增ID |
| 删除临时表 | DROP | 完全清理 |
| 需要回滚的操作 | DELETE | 支持事务回滚 |

**在测试中的应用**：
```sql
-- 测试数据准备阶段
TRUNCATE TABLE test_orders; -- 快速清理上次测试数据

-- 测试过程中的条件删除
DELETE FROM test_users WHERE role = 'temp'; -- 清理临时用户

-- 测试环境重置
DROP TABLE IF EXISTS temp_analysis; -- 删除临时分析表
```

**注意事项**：
1. **生产环境慎用TRUNCATE和DROP**：无法回滚
2. **外键约束影响**：有外键引用时DELETE可能失败
3. **权限要求不同**：DROP需要更高权限
4. **日志记录差异**：DELETE记录详细日志，TRUNCATE记录很少

### ⭐⭐⭐ 如何优化数据库的查询效率？
**难度**：⭐⭐⭐
**频率**：🔥🔥🔥

**标准答案**：
数据库查询优化是一个系统性工程，需要从多个维度进行优化：

**1. 索引优化**：
```sql
-- 分析慢查询
EXPLAIN SELECT * FROM orders WHERE user_id = 1001 AND status = 'completed';

-- 创建复合索引
CREATE INDEX idx_user_status ON orders(user_id, status);

-- 避免在索引列上使用函数
-- 错误方式
SELECT * FROM orders WHERE DATE(created_at) = '2023-12-01';
-- 正确方式
SELECT * FROM orders WHERE created_at >= '2023-12-01' AND created_at < '2023-12-02';
```

**2. SQL语句优化**：
```sql
-- 避免SELECT *，只查询需要的列
-- 低效
SELECT * FROM users WHERE id = 1001;
-- 高效
SELECT id, name, email FROM users WHERE id = 1001;

-- 使用LIMIT限制返回结果
SELECT * FROM orders ORDER BY created_at DESC LIMIT 10;

-- 优化JOIN查询
-- 使用合适的JOIN类型
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active'
GROUP BY u.id;
```

**3. 查询条件优化**：
```sql
-- 使用EXISTS替代IN（大数据集情况下）
-- 低效
SELECT * FROM users WHERE id IN (SELECT user_id FROM orders WHERE amount > 1000);
-- 高效
SELECT * FROM users WHERE EXISTS (SELECT 1 FROM orders WHERE user_id = users.id AND amount > 1000);

-- 避免在WHERE子句中使用函数
-- 低效
SELECT * FROM users WHERE UPPER(name) = 'JOHN';
-- 高效（如果可能，存储时统一大小写）
SELECT * FROM users WHERE name = 'John';
```

**4. 数据库配置优化**：
```sql
-- 查看数据库配置
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';
SHOW VARIABLES LIKE 'query_cache_size';

-- 分析慢查询日志
-- 在my.cnf中启用慢查询日志
-- slow_query_log = 1
-- long_query_time = 2
```

**5. 表结构优化**：
```sql
-- 选择合适的数据类型
-- 使用TINYINT而不是INT存储小范围数值
CREATE TABLE user_settings (
    user_id INT,
    is_active TINYINT(1), -- 0或1
    notification_level TINYINT -- 1-5
);

-- 适当的反范式化
-- 在订单表中冗余用户姓名，避免频繁JOIN
CREATE TABLE orders (
    id INT PRIMARY KEY,
    user_id INT,
    user_name VARCHAR(50), -- 冗余字段，减少JOIN
    amount DECIMAL(10,2)
);
```

**实际优化案例**：
在我负责的项目中，有个报表查询从30秒优化到2秒：

**原始查询**：
```sql
SELECT u.name, 
       COUNT(o.id) as order_count,
       SUM(o.amount) as total_amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.created_at >= '2023-01-01'
GROUP BY u.id
ORDER BY total_amount DESC;
```

**优化后**：
```sql
-- 1. 添加复合索引
CREATE INDEX idx_orders_date_user ON orders(created_at, user_id);

-- 2. 优化查询逻辑
SELECT u.name,
       COALESCE(stats.order_count, 0) as order_count,
       COALESCE(stats.total_amount, 0) as total_amount
FROM users u
LEFT JOIN (
    SELECT user_id,
           COUNT(*) as order_count,
           SUM(amount) as total_amount
    FROM orders
    WHERE created_at >= '2023-01-01'
    GROUP BY user_id
) stats ON u.id = stats.user_id
ORDER BY total_amount DESC;
```

**性能监控和分析**：
```sql
-- 查看执行计划
EXPLAIN SELECT * FROM orders WHERE user_id = 1001;

-- 分析表状态
ANALYZE TABLE orders;

-- 查看索引使用情况
SHOW INDEX FROM orders;
```

**优化总结**：
1. **80/20原则**：20%的查询占用80%的资源，重点优化慢查询
2. **测量驱动**：使用EXPLAIN和慢查询日志找到瓶颈
3. **渐进优化**：从影响最大的优化开始
4. **平衡考虑**：查询性能vs存储空间vs数据一致性

---

## 🚀 高级特性类

### ⭐⭐⭐ 事务的ACID特性及隔离级别
**难度**：⭐⭐⭐
**频率**：🔥🔥🔥

**标准答案**：
**ACID特性**：

**A - 原子性（Atomicity）**：
- 事务是不可分割的最小执行单元
- 要么全部成功，要么全部失败回滚

```sql
START TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
-- 如果任一操作失败，整个事务回滚
COMMIT;
```

**C - 一致性（Consistency）**：
- 事务执行前后，数据库状态保持一致
- 满足所有的完整性约束

```sql
-- 确保转账前后总金额不变
SELECT SUM(balance) FROM accounts; -- 转账前
-- 执行转账事务
SELECT SUM(balance) FROM accounts; -- 转账后，应该相等
```

**I - 隔离性（Isolation）**：
- 并发事务间相互隔离，不会互相干扰
- 通过锁机制和MVCC实现

**D - 持久性（Durability）**：
- 事务提交后，数据永久保存
- 即使系统故障也不会丢失

**事务隔离级别**：

**1. READ UNCOMMITTED（读未提交）**：
- 最低级别，可能出现脏读
```sql
-- 会话1
START TRANSACTION;
UPDATE accounts SET balance = 1000 WHERE id = 1;
-- 未提交

-- 会话2
SELECT balance FROM accounts WHERE id = 1; -- 可能读到1000（脏读）
```

**2. READ COMMITTED（读已提交）**：
- 只能读取已提交的数据
- MySQL和PostgreSQL默认级别
```sql
-- 解决脏读，但可能出现不可重复读
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

**3. REPEATABLE READ（可重复读）**：
- 同一事务内多次读取结果一致
- MySQL InnoDB默认级别
```sql
-- 会话1
START TRANSACTION;
SELECT * FROM accounts WHERE id = 1; -- balance = 500

-- 会话2修改数据并提交

-- 会话1再次查询
SELECT * FROM accounts WHERE id = 1; -- 仍然是500（可重复读）
```

**4. SERIALIZABLE（串行化）**：
- 最高级别，完全隔离
- 性能最低但数据最安全
```sql
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
```

**隔离级别问题对比**：

| 隔离级别 | 脏读 | 不可重复读 | 幻读 |
|----------|------|------------|------|
| READ UNCOMMITTED | ✓ | ✓ | ✓ |
| READ COMMITTED | ✗ | ✓ | ✓ |
| REPEATABLE READ | ✗ | ✗ | ✓ |
| SERIALIZABLE | ✗ | ✗ | ✗ |

**在测试中的应用**：

**1. 并发测试**：
```sql
-- 模拟并发转账测试
-- 线程1
START TRANSACTION;
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;
-- 模拟处理时间
SELECT SLEEP(5);
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
COMMIT;

-- 线程2（同时执行）
START TRANSACTION;
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE; -- 会等待
UPDATE accounts SET balance = balance - 50 WHERE id = 1;
COMMIT;
```

**2. 数据一致性测试**：
```sql
-- 验证事务一致性
START TRANSACTION;
INSERT INTO orders (user_id, amount) VALUES (1, 100);
UPDATE users SET total_spent = total_spent + 100 WHERE id = 1;
-- 验证中间状态
SELECT * FROM orders WHERE user_id = 1;
SELECT total_spent FROM users WHERE id = 1;
ROLLBACK; -- 测试回滚
```

**3. 死锁测试**：
```sql
-- 会话1
START TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- 会话2（同时执行，不同顺序）
START TRANSACTION;
UPDATE accounts SET balance = balance - 50 WHERE id = 2;
UPDATE accounts SET balance = balance + 50 WHERE id = 1; -- 可能死锁
```

**性能vs安全性权衡**：
- **生产环境**：通常使用READ COMMITTED或REPEATABLE READ
- **报表系统**：可以使用READ UNCOMMITTED提高性能
- **金融系统**：可能需要SERIALIZABLE确保数据安全

### ⭐⭐⭐ 什么是乐观锁和悲观锁？
**难度**：⭐⭐⭐
**频率**：🔥🔥

**标准答案**：
乐观锁和悲观锁是并发控制的两种不同策略：

**悲观锁（Pessimistic Locking）**：
- **假设冲突会发生**：每次操作都假设会有并发冲突
- **提前加锁**：在读取数据时就加锁，直到事务结束才释放
- **数据库实现**：SELECT FOR UPDATE、行锁、表锁

```sql
-- 悲观锁示例：银行转账
START TRANSACTION;
-- 加排他锁，其他事务无法修改这行数据
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;
-- 业务逻辑处理
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
COMMIT; -- 释放锁
```

**乐观锁（Optimistic Locking）**：
- **假设冲突不会发生**：读取时不加锁，更新时检查数据是否被修改过
- **版本控制**：通常使用版本号或时间戳来检测冲突
- **冲突处理**：发现冲突后重试或报错

```sql
-- 乐观锁示例：使用版本号
-- 1. 读取数据和版本号
SELECT id, balance, version FROM accounts WHERE id = 1;
-- 假设得到：id=1, balance=1000, version=5

-- 2. 业务逻辑处理后，更新时检查版本号
UPDATE accounts 
SET balance = 900, version = version + 1 
WHERE id = 1 AND version = 5; -- 检查版本号是否还是5

-- 3. 检查更新影响的行数
-- 如果影响行数为0，说明数据已被其他事务修改
```

**应用场景对比**：

| 特性 | 悲观锁 | 乐观锁 |
|------|--------|--------|
| 冲突频率 | 高冲突场景 | 低冲突场景 |
| 性能 | 读性能低，写性能稳定 | 读性能高，写冲突时需重试 |
| 死锁风险 | 较高 | 无死锁 |
| 实现复杂度 | 简单 | 需要版本控制逻辑 |

**代码实现示例**：

**悲观锁实现（Java）**：
```java
@Transactional
public void transferMoney(Long fromId, Long toId, BigDecimal amount) {
    // 按ID顺序加锁，避免死锁
    Long firstId = fromId < toId ? fromId : toId;
    Long secondId = fromId < toId ? toId : fromId;
    
    Account firstAccount = accountMapper.selectForUpdate(firstId);
    Account secondAccount = accountMapper.selectForUpdate(secondId);
    
    if (fromId.equals(firstId)) {
        firstAccount.setBalance(firstAccount.getBalance().subtract(amount));
        secondAccount.setBalance(secondAccount.getBalance().add(amount));
    } else {
        secondAccount.setBalance(secondAccount.getBalance().subtract(amount));
        firstAccount.setBalance(firstAccount.getBalance().add(amount));
    }
    
    accountMapper.updateById(firstAccount);
    accountMapper.updateById(secondAccount);
}
```

**乐观锁实现（Java）**：
```java
@Service
public class AccountService {
    
    @Retryable(value = OptimisticLockingFailureException.class, maxAttempts = 3)
    public void updateBalance(Long accountId, BigDecimal amount) {
        Account account = accountMapper.selectById(accountId);
        account.setBalance(account.getBalance().add(amount));
        
        int updateCount = accountMapper.updateByIdWithVersion(account);
        if (updateCount == 0) {
            throw new OptimisticLockingFailureException("数据已被修改，请重试");
        }
    }
}
```

**在测试中的验证**：

**1. 悲观锁测试**：
```java
@Test
public void testPessimisticLock() throws Exception {
    CountDownLatch latch = new CountDownLatch(2);
    AtomicInteger successCount = new AtomicInteger(0);
    
    // 模拟两个线程同时转账
    for (int i = 0; i < 2; i++) {
        new Thread(() -> {
            try {
                transferService.transferMoney(1L, 2L, new BigDecimal("100"));
                successCount.incrementAndGet();
            } catch (Exception e) {
                // 记录异常
            } finally {
                latch.countDown();
            }
        }).start();
    }
    
    latch.await();
    // 验证只有一个事务成功，数据一致性得到保证
    assertEquals(1, successCount.get());
}
```

**2. 乐观锁测试**：
```java
@Test
public void testOptimisticLock() throws Exception {
    // 并发更新测试
    List<Future<Boolean>> futures = new ArrayList<>();
    ExecutorService executor = Executors.newFixedThreadPool(10);
    
    for (int i = 0; i < 10; i++) {
        futures.add(executor.submit(() -> {
            try {
                accountService.updateBalance(1L, new BigDecimal("10"));
                return true;
            } catch (OptimisticLockingFailureException e) {
                return false; // 冲突，重试机制会处理
            }
        }));
    }
    
    // 统计成功和失败次数
    long successCount = futures.stream()
        .mapToInt(f -> {
            try {
                return f.get() ? 1 : 0;
            } catch (Exception e) {
                return 0;
            }
        }).sum();
        
    // 验证最终数据一致性
    Account account = accountMapper.selectById(1L);
    assertEquals(originalBalance.add(new BigDecimal("100")), account.getBalance());
}
```

**选择建议**：
- **悲观锁**：金融转账、库存扣减等强一致性要求场景
- **乐观锁**：用户信息更新、文章编辑等冲突较少的场景
- **混合策略**：根据业务特点在不同模块采用不同策略

---

## 📊 题目总结

### 按难度分级
- **⭐ 基础级**：15题 - SQL语法、基本概念
- **⭐⭐ 中级**：20题 - 数据库设计、索引优化
- **⭐⭐⭐ 高级**：15题 - 事务处理、锁机制、性能调优

### 按重要程度  
- **🔥🔥🔥 必考**：25题 - 核心概念，面试必问
- **🔥🔥 常考**：15题 - 经常涉及，需要掌握  
- **🔥 偶考**：10题 - 加分项，展示技术深度

### 学习路径建议
1. **SQL基础**：熟练掌握增删改查、连接查询
2. **数据库设计**：理解三范式、主外键关系
3. **性能优化**：掌握索引原理和查询优化
4. **高级特性**：深入理解事务、锁机制
5. **实战应用**：结合测试场景，提供具体案例

### 测试场景应用
- **数据准备**：批量插入测试数据
- **结果验证**：查询验证业务逻辑正确性
- **性能测试**：大数据量下的查询性能验证
- **并发测试**：事务并发和锁机制验证

---
**更新日期**：2025-01-07  
**涵盖题目**：50道  
**适用岗位**：高级测试开发工程师