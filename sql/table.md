# 表结构

> sqlite版本
> 
> 在 SQLite 中，使用 INTEGER 代替 INT，使用 TEXT 代替 VARCHAR。
> 

1. 创建学生表并插入数据
```sql
CREATE TABLE students (
    studentNo INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    sex TEXT,
    hometown TEXT,
    age INTEGER,
    class TEXT,
    card TEXT
);

INSERT INTO students (name, sex, hometown, age, class, card) VALUES
('张三', '男', '北京', 18, '1班', '340322199200224253'),
('李四', '男', '上海', 19, '1班', '340322199200246754'),
('王五', '男', '广州', 20, '2班', '340322199200247654'),
('小明', '男', '深圳', 21, '2班', NULL),
('小红', '女', '杭州', 21, '3班', '340322199200276543'),
('小李', '女', '成都', 26, '2班', '340322199200297655');
```
2. 创建课程表并插入数据
```sql
CREATE TABLE courses (
    courseNo INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);

INSERT INTO courses (name) VALUES
('数学'),
('英语'),
('计算机'),
('系统设计'),
('数据库'),
('导论与实践');
```
3. 创建成绩表并插入数据
```sql
CREATE TABLE scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    courseNo INTEGER,
    studentNo INTEGER
);

INSERT INTO scores (courseNo, studentNo) VALUES
(1, 1),
(1, 2),
(4, 2),
(4, 3);
```

1. 创建部门表并插入数据
```sql
CREATE TABLE departments (
    deptid INTEGER PRIMARY KEY,
    deptname TEXT NOT NULL -- 部门名称
);

INSERT INTO departments (deptid, deptname) VALUES
('1001', '市场部'),
('1002', '测试部'),
('1003', '开发部');
```
2. 创建员工表并插入数据
```sql
CREATE TABLE employees (
    empid INTEGER PRIMARY KEY,
    empname TEXT NOT NULL, -- 姓名
    sex TEXT DEFAULT NULL, -- 性别
    deptid INTEGER, -- 部门编号
    jobs TEXT DEFAULT NULL, -- 职位
    politicalstatus TEXT DEFAULT NULL, -- 政治面貌
    leader INTEGER DEFAULT NULL -- 领导
);

INSERT INTO employees (empid, empname, sex, deptid, jobs, politicalstatus, leader) VALUES
(1, '王小明', '男', 1001, '开发部', '团员', 9),
(2, '张三', '女', 1002, '测试部', '团员', 4),
(3, '李四', '男', 1003, '开发部', '职员', 1),
(4, '赵五', '女', 1001, '市场部', '经理', 3),
(5, '孙六', '男', 1002, '测试部', '职员', 2),
(6, '周七', '女', 1003, '开发部', '职员', 4),
(7, '吴八', '男', 1001, '市场部', '职员', null);
```
3. 创建工资表并插入数据
```sqlite
CREATE TABLE salary (
    sid INTEGER PRIMARY KEY,
    empid INTEGER NOT NULL,
    salary INTEGER NOT NULL -- 工资
);

INSERT INTO salary (sid, empid, salary) VALUES
(1, 7, 2100),
(2, 6, 5000),
(3, 5, 2000),
(4, 9, 1900),
(5, 1, 5000),
(6, 12, 2600),
(7, 4, 1900);
```



学生表 课程表 教师表

部门表 员工表 工资表



sqllite工具

```
https://sqlitestudio.pl/
```





## 题目



1、查询学生"百里守约"的基本信息

```
```

