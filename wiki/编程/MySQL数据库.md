# MySQL数据库

MySQL数据库的核心知识和操作指南，内容来源于《MySQL必知必会》。

## 一、SQL基础

### 1.1 什么是SQL

**SQL（Structured Query Language）**：结构化查询语言，是用于访问和处理数据库的标准计算机语言。

### 1.2 SQL特点

- SQL不区分大小写
- SQL语句必须以分号结尾
- SQL使用关键字进行操作

### 1.3 检索数据

#### SELECT语句

```sql
-- 检索单个列
SELECT column_name FROM table_name;

-- 检索多个列
SELECT column1, column2 FROM table_name;

-- 检索所有列
SELECT * FROM table_name;

-- 检索不同的值
SELECT DISTINCT column_name FROM table_name;

-- 限制结果
SELECT column_name FROM table_name LIMIT 5;        -- 返回前5行
SELECT column_name FROM table_name LIMIT 5,5;      -- 返回第6-10行
```

### 1.4 排序数据

#### ORDER BY子句

```sql
-- 单列排序
SELECT column_name FROM table_name ORDER BY column_name;

-- 多列排序
SELECT column1, column2 FROM table_name ORDER BY column1, column2;

-- 指定排序方向
SELECT column_name FROM table_name ORDER BY column_name DESC;  -- 降序
SELECT column_name FROM table_name ORDER BY column_name ASC;   -- 升序
```

### 1.5 过滤数据

#### WHERE子句

```sql
-- 相等检查
SELECT * FROM table_name WHERE column_name = 'value';

-- 不相等检查
SELECT * FROM table_name WHERE column_name <> 'value';

-- 范围检查
SELECT * FROM table_name WHERE column_name BETWEEN 1 AND 10;

-- 空值检查
SELECT * FROM table_name WHERE column_name IS NULL;
```

### 1.6 数据过滤

#### 组合WHERE子句

```sql
-- AND操作符
SELECT * FROM table_name WHERE column1 = 'value1' AND column2 = 'value2';

-- OR操作符
SELECT * FROM table_name WHERE column1 = 'value1' OR column2 = 'value2';

-- IN操作符
SELECT * FROM table_name WHERE column_name IN ('value1', 'value2');

-- NOT操作符
SELECT * FROM table_name WHERE NOT column_name = 'value';
```

### 1.7 用通配符进行过滤

#### LIKE操作符

```sql
-- %通配符（匹配任意字符出现任意次数）
SELECT * FROM table_name WHERE column_name LIKE 'jet%';    -- 以jet开头
SELECT * FROM table_name WHERE column_name LIKE '%anvil%'; -- 包含anvil
SELECT * FROM table_name WHERE column_name LIKE '%s';      -- 以s结尾

-- _通配符（只匹配单个字符）
SELECT * FROM table_name WHERE column_name LIKE '_ton anvil';
```

### 1.8 用正则表达式进行搜索

#### REGEXP操作符

```sql
-- 基本字符串匹配
SELECT * FROM table_name WHERE column_name REGEXP '1000';

-- OR匹配
SELECT * FROM table_name WHERE column_name REGEXP '1000|2000';

-- 匹配几个字符之一
SELECT * FROM table_name WHERE column_name REGEXP '[123] Ton';

-- 字符范围
SELECT * FROM table_name WHERE column_name REGEXP '[1-5] Ton';

-- 特殊字符匹配
SELECT * FROM table_name WHERE column_name REGEXP '\\.';  -- 匹配.
```

## 二、计算字段

### 2.1 拼接字段

```sql
-- CONCAT函数（MySQL）
SELECT CONCAT(column1, ' ', column2) FROM table_name;

-- 去除空格
SELECT CONCAT(RTRIM(column1), ' ', RTRIM(column2)) FROM table_name;

-- 使用别名
SELECT CONCAT(column1, ' ', column2) AS new_name FROM table_name;
```

### 2.2 执行算术计算

```sql
-- 算术运算符
SELECT column1, column2, column1 + column2 AS total FROM table_name;

-- 支持的操作符：+ - * /
```

## 三、数据处理函数

### 3.1 文本处理函数

```sql
-- 大小写转换
SELECT UPPER(column_name) FROM table_name;    -- 转大写
SELECT LOWER(column_name) FROM table_name;    -- 转小写

-- 字符串长度
SELECT LENGTH(column_name) FROM table_name;

-- 去除空格
SELECT LTRIM(column_name) FROM table_name;    -- 去左空格
SELECT RTRIM(column_name) FROM table_name;    -- 去右空格
SELECT TRIM(column_name) FROM table_name;     -- 去两端空格

-- 子串操作
SELECT LEFT(column_name, 3) FROM table_name;       -- 取左3个字符
SELECT RIGHT(column_name, 3) FROM table_name;      -- 取右3个字符
SELECT SUBSTRING(column_name, 1, 3) FROM table_name; -- 取第1-3个字符

-- 字符串拼接
SELECT CONCAT(column1, column2) FROM table_name;

-- 查找子串位置
SELECT LOCATE('abc', column_name) FROM table_name;

-- 替换字符串
SELECT REPLACE(column_name, 'old', 'new') FROM table_name;
```

### 3.2 日期和时间处理函数

```sql
-- 获取当前日期时间
SELECT NOW();

-- 获取当前日期
SELECT CURDATE();

-- 获取当前时间
SELECT CURTIME();

-- 提取日期部分
SELECT DATE(datetime_column) FROM table_name;

-- 提取年、月、日
SELECT YEAR(datetime_column) FROM table_name;
SELECT MONTH(datetime_column) FROM table_name;
SELECT DAY(datetime_column) FROM table_name;

-- 日期格式化
SELECT DATE_FORMAT(datetime_column, '%Y-%m-%d') FROM table_name;
SELECT TIME_FORMAT(datetime_column, '%H:%i:%s') FROM table_name;

-- 日期加减
SELECT DATE_ADD(datetime_column, INTERVAL 1 DAY) FROM table_name;
SELECT DATE_SUB(datetime_column, INTERVAL 1 DAY) FROM table_name;

-- 日期差
SELECT DATEDIFF(date1, date2) FROM table_name;
```

### 3.3 数值处理函数

```sql
-- 绝对值
SELECT ABS(column_name) FROM table_name;

-- 圆整
SELECT CEIL(column_name) FROM table_name;     -- 向上取整
SELECT FLOOR(column_name) FROM table_name;    -- 向下取整
SELECT ROUND(column_name, 2) FROM table_name; -- 四舍五入保留2位小数

-- 取模
SELECT MOD(column1, column2) FROM table_name;

-- 幂运算
SELECT POW(column_name, 2) FROM table_name;   -- 平方
SELECT SQRT(column_name) FROM table_name;     -- 开方

-- 随机数
SELECT RAND();
```

### 3.4 聚集函数

```sql
-- 计数
SELECT COUNT(*) FROM table_name;              -- 统计行数
SELECT COUNT(column_name) FROM table_name;    -- 统计非NULL行数

-- 求和
SELECT SUM(column_name) FROM table_name;

-- 平均值
SELECT AVG(column_name) FROM table_name;

-- 最大值
SELECT MAX(column_name) FROM table_name;

-- 最小值
SELECT MIN(column_name) FROM table_name;

-- 组合使用
SELECT COUNT(*) AS num_items,
       AVG(column_name) AS avg_value,
       MAX(column_name) AS max_value,
       MIN(column_name) AS min_value,
       SUM(column_name) AS total_value
FROM table_name;
```

## 四、分组数据

### 4.1 GROUP BY子句

```sql
-- 简单分组
SELECT column_name, COUNT(*) AS count
FROM table_name
GROUP BY column_name;

-- 多列分组
SELECT column1, column2, COUNT(*) AS count
FROM table_name
GROUP BY column1, column2;

-- 过滤分组（HAVING）
SELECT column_name, COUNT(*) AS count
FROM table_name
GROUP BY column_name
HAVING COUNT(*) >= 5;
```

### 4.2 SELECT子句顺序

```sql
SELECT   -- 要返回的列或表达式
FROM     -- 从中检索数据的表
WHERE    -- 行级过滤
GROUP BY -- 分组
HAVING   -- 组级过滤
ORDER BY -- 输出排序顺序
LIMIT    -- 要检索的行数
```

## 五、子查询

### 5.1 子查询基础

```sql
-- WHERE中的子查询
SELECT * FROM table_name
WHERE column_name IN (SELECT column_name FROM another_table);

-- 列子查询
SELECT * FROM table_name
WHERE column_name = (SELECT column_name FROM another_table WHERE condition);

-- 行子查询
SELECT * FROM table_name
WHERE (column1, column2) = (SELECT column1, column2 FROM another_table WHERE condition);
```

### 5.2 相关子查询

```sql
-- 关联外部查询
SELECT * FROM table_name t1
WHERE column_name = (SELECT column_name FROM table_name t2 WHERE t2.id = t1.id);
```

## 六、联结表

### 6.1 联结基础

```sql
-- 内联结
SELECT t1.column1, t2.column2
FROM table1 t1
INNER JOIN table2 t2 ON t1.id = t2.table1_id;

-- 多表联结
SELECT t1.column1, t2.column2, t3.column3
FROM table1 t1
INNER JOIN table2 t2 ON t1.id = t2.table1_id
INNER JOIN table3 t3 ON t2.id = t3.table2_id;

-- 使用WHERE语法（旧式）
SELECT t1.column1, t2.column2
FROM table1 t1, table2 t2
WHERE t1.id = t2.table1_id;
```

### 6.2 联结类型

```sql
-- 左联结
SELECT t1.column1, t2.column2
FROM table1 t1
LEFT JOIN table2 t2 ON t1.id = t2.table1_id;

-- 右联结
SELECT t1.column1, t2.column2
FROM table1 t1
RIGHT JOIN table2 t2 ON t1.id = t2.table1_id;

-- 全联结
SELECT t1.column1, t2.column2
FROM table1 t1
FULL JOIN table2 t2 ON t1.id = t2.table1_id;
```

## 七、组合查询

### 7.1 UNION操作符

```sql
-- 简单组合
SELECT column1, column2 FROM table1
UNION
SELECT column1, column2 FROM table2;

-- 包含重复
SELECT column1, column2 FROM table1
UNION ALL
SELECT column1, column2 FROM table2;
```

## 八、全文本搜索

### 8.1 MATCH和AGAINST

```sql
-- 全文本搜索
SELECT * FROM table_name
WHERE MATCH(column_name) AGAINST('search term');

-- 布尔模式
SELECT * FROM table_name
WHERE MATCH(column_name) AGAINST('search term' IN BOOLEAN MODE);

-- 扩展搜索
SELECT * FROM table_name
WHERE MATCH(column_name) AGAINST('search term' WITH QUERY EXPANSION);
```

## 九、插入、更新和删除

### 9.1 插入数据

```sql
-- 插入单行
INSERT INTO table_name (column1, column2, column3)
VALUES ('value1', 'value2', 'value3');

-- 插入多行
INSERT INTO table_name (column1, column2, column3)
VALUES ('value1', 'value2', 'value3'),
       ('value4', 'value5', 'value6');

-- 插入查询结果
INSERT INTO table_name (column1, column2)
SELECT column1, column2 FROM another_table;
```

### 9.2 更新数据

```sql
-- 更新单列
UPDATE table_name
SET column_name = 'new_value'
WHERE condition;

-- 更新多列
UPDATE table_name
SET column1 = 'value1', column2 = 'value2'
WHERE condition;
```

### 9.3 删除数据

```sql
-- 删除行
DELETE FROM table_name WHERE condition;

-- 删除所有行
DELETE FROM table_name;

-- 使用TRUNCATE（更快）
TRUNCATE TABLE table_name;
```

## 十、创建和操纵表

### 10.1 创建表

```sql
CREATE TABLE table_name (
    column1 datatype NOT NULL,
    column2 datatype DEFAULT 'value',
    column3 datatype,
    PRIMARY KEY (column1)
);

-- 常用数据类型
-- INT          整数
-- DECIMAL(m,n) 小数
-- VARCHAR(n)   变长字符串
-- CHAR(n)      定长字符串
-- TEXT         文本
-- DATE         日期
-- DATETIME     日期时间
-- TIMESTAMP    时间戳
-- BLOB         二进制数据
-- ENUM         枚举
```

### 10.2 修改表

```sql
-- 添加列
ALTER TABLE table_name ADD column_name datatype;

-- 删除列
ALTER TABLE table_name DROP COLUMN column_name;

-- 修改列类型
ALTER TABLE table_name MODIFY column_name new_datatype;

-- 重命名表
RENAME TABLE table_name TO new_name;

-- 删除表
DROP TABLE table_name;
```

## 十一、视图

### 11.1 创建视图

```sql
-- 创建视图
CREATE VIEW view_name AS
SELECT column1, column2
FROM table_name
WHERE condition;

-- 使用视图
SELECT * FROM view_name;

-- 删除视图
DROP VIEW view_name;
```

## 十二、存储过程

### 12.1 创建存储过程

```sql
-- 创建存储过程
DELIMITER //
CREATE PROCEDURE procedure_name()
BEGIN
    SELECT * FROM table_name;
END //
DELIMITER ;

-- 调用存储过程
CALL procedure_name();
```

### 12.2 带参数的存储过程

```sql
-- IN参数
DELIMITER //
CREATE PROCEDURE procedure_name(IN param_name datatype)
BEGIN
    SELECT * FROM table_name WHERE column_name = param_name;
END //
DELIMITER ;

-- OUT参数
DELIMITER //
CREATE PROCEDURE procedure_name(OUT param_name datatype)
BEGIN
    SELECT COUNT(*) INTO param_name FROM table_name;
END //
DELIMITER ;
```

## 十三、游标

### 13.1 使用游标

```sql
-- 声明游标
DECLARE cursor_name CURSOR FOR
SELECT column1, column2 FROM table_name;

-- 打开游标
OPEN cursor_name;

-- 使用游标
FETCH cursor_name INTO variable1, variable2;

-- 关闭游标
CLOSE cursor_name;
```

## 十四、触发器

### 14.1 创建触发器

```sql
-- INSERT触发器
CREATE TRIGGER trigger_name
AFTER INSERT ON table_name
FOR EACH ROW
BEGIN
    -- 触发器逻辑
END;

-- UPDATE触发器
CREATE TRIGGER trigger_name
AFTER UPDATE ON table_name
FOR EACH ROW
BEGIN
    -- 触发器逻辑
END;

-- DELETE触发器
CREATE TRIGGER trigger_name
AFTER DELETE ON table_name
FOR EACH ROW
BEGIN
    -- 触发器逻辑
END;
```

## 十五、事务处理

### 15.1 事务基础

```sql
-- 开始事务
START TRANSACTION;

-- 执行SQL语句
INSERT INTO table_name ...;
UPDATE table_name ...;
DELETE FROM table_name ...;

-- 提交事务
COMMIT;

-- 回滚事务
ROLLBACK;
```

### 15.2 事务隔离级别

```sql
-- 设置隔离级别
SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE;
```

## 十六、安全管理

### 16.1 用户管理

```sql
-- 创建用户
CREATE USER 'username'@'hostname' IDENTIFIED BY 'password';

-- 授予权限
GRANT SELECT, INSERT, UPDATE ON database_name.* TO 'username'@'hostname';

-- 撤销权限
REVOKE SELECT, INSERT, UPDATE ON database_name.* FROM 'username'@'hostname';

-- 删除用户
DROP USER 'username'@'hostname';
```

### 16.2 权限类型

```sql
-- 全局权限
GRANT ALL PRIVILEGES ON *.* TO 'username'@'hostname';

-- 数据库权限
GRANT ALL PRIVILEGES ON database_name.* TO 'username'@'hostname';

-- 表权限
GRANT SELECT, INSERT, UPDATE ON database_name.table_name TO 'username'@'hostname';

-- 列权限
GRANT SELECT (column1, column2) ON database_name.table_name TO 'username'@'hostname';
```

## 十七、数据库维护

### 17.1 备份数据

```sql
-- 使用mysqldump
mysqldump -u username -p database_name > backup.sql

-- 恢复数据
mysql -u username -p database_name < backup.sql
```

### 17.2 日志管理

```sql
-- 查看日志
SHOW VARIABLES LIKE 'log_%';

-- 错误日志
-- 查询日志
-- 慢查询日志
-- 二进制日志
```

## 十八、性能优化

### 18.1 索引

```sql
-- 创建索引
CREATE INDEX index_name ON table_name (column1, column2);

-- 创建唯一索引
CREATE UNIQUE INDEX index_name ON table_name (column1);

-- 删除索引
DROP INDEX index_name ON table_name;
```

### 18.2 查询优化

```sql
-- 使用EXPLAIN分析查询
EXPLAIN SELECT * FROM table_name WHERE condition;

-- 使用LIMIT限制结果
SELECT * FROM table_name LIMIT 100;

-- 避免使用SELECT *
SELECT column1, column2 FROM table_name;

-- 使用合适的JOIN
SELECT * FROM table1 t1
INNER JOIN table2 t2 ON t1.id = t2.table1_id;
```

## 十九、相关链接

- [Metabase BI工具](Metabase%20BI工具.md)