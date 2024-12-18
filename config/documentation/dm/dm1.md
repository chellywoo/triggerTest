### 触发器在自主访问控制中问题
- 自主访问控制在安全模型中的规定如下：
  - 主体必须拥有对客体的访问权限才能访问客体
  - 权限的授予和传播情况需要记录在系统中
  - 权限的传播范围：只限于该对象本身，不会影响其他对象的访问权限
​	针对触发器进行关于自主访问控制的测试的目的是：用户在触发器的使用过程中是否会直接或间接的获取到某些信息，或者使用其他用户的权限，从而间接的获取到自己未曾拥有的权限，乃至获取到DBA权限。
##### 触发器传播权限
  测试目的：测试触发器是否能够使得调用者获取到自己没有的权限
  测试过程：
（1）  实验一
- 前提条件：用户user1拥有创建表、触发器的权限；用户user1创建表table1，并在表上创建触发器，授予用户user2插入该表的权限
- 测试步骤：
  1. user1创建以下类型的触发器：
     ```sql
     connect sysdba/SYSDBA;
     create user user1 identified by 123456789;
     grant create table, create trigger to user1;
     connect user1/123456789;
     create table table1(id int, name varchar(20));
     create or replace trigger insert_table1
     after insert on table1
     for each row
     begin
     		delete from table1 where id = 1;
     end;
     grant insert on table1 to user2;
     ```
​	2. user2插入数据到table1触发触发器
- 测试结果：查看user1用户下table1表的数据，id = 1的那一行数据已经被删除。
**总结**：在这个实验中，user2用户虽然没有table1表的删除权限，但是因为在插入数据时，触发了触发器insert_table1，而触发器在执行的时候采用的是所有者的权限，也就是user1用户的权限，user2用户通过触发器间接的使用了user1用户的权限，从而能删除表table1中的数据。
（2）实验二
- 前提条件：用户user1拥有创建表、触发器的权限；用户user1创建表table1、tabel2，并在表table1上创建触发器，授予用户user2插入表table1的权限。
- 测试步骤：
  1. user1创建以下类型的触发器：
     ```sql
     connect sysdba/SYSDBA;
     create user user1 identified by 123456789;
     grant create table, create trigger to user1;
     connect user1/123456789;
     create table table1(id int, name varchar(20), age int);
     create table table2(id int, name varchar(20), age int);
     create or replace trigger insert_table2
     after insert on table1
     for each row
     begin
     		insert into table2 values(new.id, new.name, new.age);
     end;
     grant insert on table1 to user2;
     ```
  2. user2插入数据(2, 'user2',12)到表table1，触发触发器insert_table2
- 测试结果：查看user1用户下table2表的数据，user2插入到table1的这行数据成功插入到table2中。
**总结**：在这个实验中，user2用户虽然没有table2表的插入权限，但是因为在插入数据时，触发了触发器insert_table2，而触发器在执行的时候采用的是所有者的权限，也就是user1用户的权限，user2用户通过触发器间接的使用了user1用户的权限，从而能插入数据到表table2中。
关键词：用户, 触发器, 权限, 创建