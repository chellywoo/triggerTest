import re
import dmPython

def SQLExtractor(sql_code):
    # 定义一个包含常见SQL操作的正则表达式
    # regex = r"(GRANT|CONNECT|CREATE|INSERT|UPDATE|DROP|SELECT|DELETE|END|BEGIN)[^;]*;"
    regex = r"^\s*(GRANT|CONNECT|CREATE|INSERT|UPDATE|DROP|SELECT|DELETE|BEGIN|END)\b.*[^;]*;"
    pattern = re.compile(regex, re.IGNORECASE | re.MULTILINE)
    # 编译正则表达式模式
    # pattern = re.compile(regex, re.IGNORECASE)
    matcher = pattern.finditer(sql_code)

    sql_buffer = []
    drop_buffer = []

    # trigger_buffer = []
    # for match in matcher:
    #     sql_code = match.group()
    #     if sql_code.upper().startswith("CREATE OR REPLACE TRIGGER"):
    #         trigger_buffer.append(sql_code)
    #         continue
    #     elif trigger_buffer and "END;" in sql_code.upper():
    #         trigger_buffer.append(sql_code)
    #         sql_buffer.append(' '.join(trigger_buffer))
    #         trigger_buffer = []
    #     else:
    #         sql_buffer.append(sql_code)

    for match in matcher:
        sql_code = match.group()
        # 提取CREATE语句
        if sql_code.upper().startswith("CREATE"):
            # create_pattern = re.compile(r"\bCREATE\s", re.IGNORECASE | re.MULTILINE)
            # create_matcher = create_pattern.finditer(sql_code)
            # for create_match in create_matcher:
                # create_statement = create_match.group()
                # if "OR" in create_statement:
                #     drop_statement = f"DROP {create_match.group(3)} {create_match.group(4)}"
                # else:
                #     drop_statement = f"DROP {create_match.group(2)} {create_match.group(3)}"
                # drop_buffer.append(drop_statement + ";")
            words = sql_code.split()
            if 'USER' == words[1].upper():
                sql_buffer.append(f"DROP {words[1]} IF EXISTS {words[2]};")
            if "OR" == words[1].upper():
                drop_statement = f"DROP {words[3]} IF EXISTS {words[4]}"
            else:
                drop_statement = f"DROP {words[1]} IF EXISTS {words[2]}"
            drop_buffer.insert(0, drop_statement + ";")  
        if "END" in sql_code.upper():
            sql_text = sql_buffer.pop()
            sql_code = sql_text + sql_code
            
        # 将原始SQL代码添加到缓冲区
        sql_buffer.append(sql_code)
    # 将DROP语句添加到SQL代码的末尾
    sql_buffer.extend(drop_buffer)

    # 输出转换后的SQL文本
    print("\n".join(sql_buffer))
    return sql_buffer, drop_buffer
# 定义一个函数来执行SQL语句
def execute_sql(sql, user, password, server='127.0.0.1', port=5236):
    # msgs = ''
    try:
        conn = dmPython.connect(user=user, password=password, server=server, port=port)
        cursor = conn.cursor()
        # for sql_exec in sql:
        #     cursor.execute(sql_exec)
        #     if cursor.description:  # 如果是查询语句
        #         msgs += sql_exec
        #         results = cursor.fetchall()
        #         for row in results:
        #             print(row)
        #             msgs += row
        #     else:
        #         conn.commit()  # 提交非查询语句的事务
        # sql = "begin \n" + sql + "\nend"
        cursor.execute(sql)
        # if cursor.description:  # 如果是查询语句
            # msgs += sql_code
        results = cursor.fetchall()
        for row in results:
            print(row)
            # msgs += row
        # else:
            conn.commit()  # 提交非查询语句的事务
        return True, "Success"
    except dmPython.Error as e:
        print(f"数据库操作出错: {e}")
        return False, f"数据库操作出错: {e}"
    finally:
        try:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        except Exception as close_e:
            print(f"关闭游标或连接时出错: {close_e}")
            return f"关闭游标或连接时出错: {close_e}"

# def execute(sql_code, user, password):
#     # 执行查询
#     # sql_statements = []
#     # current_stmt = ""
#     # quote_char = None
#     # for i in range(len(sql_code)):
#     #     char = sql_code[i]
#     #     current_stmt += char
#     #     if char in ('"', "'"):
#     #         if quote_char is None:
#     #             quote_char = char
#     #         elif char == quote_char:
#     #             quote_char = None
#     #     # elif char == 'E'
#     #     elif char == ';' and quote_char is None:
#     #         sql_statements.append(current_stmt.strip())
#     #         current_stmt = ""
#     # if current_stmt:
#     #     sql_statements.append(current_stmt.strip())
#     sql_statements = sql_code
#     success = True
#     error_messages = []
#     for stmt in sql_statements:
#         words = stmt.split()
#         word = words[1].split('/')
#         if words[0].upper() == 'CONNECT':
#             try:
#                 parts = words[1].split('/')
#                 user = parts[0]
#                 password = parts[1].split(';')[0]
#                 continue
#             except Exception as e:
#                 success = False
#                 error_messages.append(f"用户连接出错: {e}")
#                 break
#         elif words[0].upper() == 'DROP' and words[1].upper() == 'USER':
#             user = 'SYSDBA'
#             password = 'SYSDBA'
#         try:
#             execute_sql(stmt, user, password, '127.0.0.1', 5236)
#         except Exception as e:
#             success = False
#             error_messages.append(f"执行SQL语句 {stmt} 出错: {e}")
#     if success:
#         return "所有SQL语句执行成功"
#     return "\n".join(error_messages)

def execute(sql_code, user="SYSDBA", password="SYSDBA") -> (str, str):
        sql_statements = sql_code
        success = True
        msgs = []
        # sql_stmt = []
        sql_stmt = ''
        for stmt in sql_statements:
            words = stmt.split()
            if words[0].upper() == 'CONNECT':
                try:
                    try:
                        success, msg = execute_sql(sql_stmt, user, password)
                        if success:
                            if msg != "Success":
                                msgs.append(msg)
                        else:
                            print (f"执行SQL语句 {sql_stmt} 出错: {msg}")
                            return False, f"执行SQL语句 {sql_stmt} 出错: {msg}"
                        if len(msgs) > 1:
                            first_msg = msgs[0]
                            is_equal = all(msg == first_msg for msg in msgs)
                            if is_equal == False:
                                print("前后对比错误")
                                return False, "前后对比错误"
                    except Exception as e:
                        print (f"执行SQL语句 {sql_stmt} 出错: {e}")
                        return False, f"执行SQL语句 {sql_stmt} 出错: {e}"
                    parts = words[1].split('/')
                    user = parts[0]
                    password = parts[1].split(';')[0]
                    # sql_stmt = []
                    sql_stmt = ''
                    continue
                except Exception as e:
                    success = False
                    print("用户连接出错: {e}")
                    return False, "用户连接出错: {e}"
                    break
            else:
                # sql_stmt.append(stmt)
                sql_stmt += '\n' + stmt
        if sql_stmt != '':
            try:
                        success, msg = execute_sql(sql_stmt, user, password)
                        if success:
                            if msg != "Success":
                                msgs.append(msg)
                        else:
                            print (f"执行SQL语句 {sql_stmt} 出错: {msg}")
                            return False, f"执行SQL语句 {sql_stmt} 出错: {msg}"
                        if len(msgs) > 1:
                            first_msg = msgs[0]
                            is_equal = all(msg == first_msg for msg in msgs)
                            if is_equal == False:
                                print("前后对比错误")
                                return False, "前后对比错误"
            except Exception as e:
                print (f"执行SQL语句 {sql_stmt} 出错: {e}")
                return False, f"执行SQL语句 {sql_stmt} 出错: {e}"

sql_code = """例如，我们假设存在一种情况，其中一个用户 `USER1` 
创建了一个触发器，该触发器在对表进行某些操作时会执行某些高权限的动作。然而，这个触发器的设计存在一个
漏洞，即它允许另一个用户 `USER2` 通过触发这个触发器来执行一些超出它们原本权限的操作。
1. cehsi 
<sex_>
<><><><>
```sql
sql> create user user1 identified by 123456789;
sql> grant create table, create trigger to user1;

sql> CONNECT USER1/123456789;
 
CREATE TABLE USER1.TEMP_TABLE
(
    ID NUMBER(10),
    NAME VARCHAR2(50)
);

 
CREATE OR REPLACE TRIGGER USER1.TRIGGER_CHECK_MAX_SIZE
    BEFORE INSERT OR UPDATE ON USER1.TEMP_TABLE FOR EACH ROW
BEGIN
     
    IF :NEW.NAME IS NOT NULL THEN
        UPDATE USER1.TEMP_TABLE SET ID = ID * 2 + 1 WHERE NAME = :NEW.NAME;
    END IF;
END;
/

INSERT INTO USER1.TEMP_TABLE (ID, NAME) VALUES (1, 'SampleName');
2.ceshi 
CONNECT USER1/123456789;  

DROP TRIGGER USER1.TRIGGER_CHECK_MAX_SIZE;
DROP TABLE USER1.TEMP_TABLE;
```

这个测试用例展示了在一个表上的触发器如何可能因为权限设置不当而导致违反安全模型。在这个例子中，`USER1
` 创建了一个触发器，它在一些条件下允许对表格进行更新操作，这个操作可能会导致权限超越 `USER1` 
的原有权限。

实际中，为了防止类似这种情况的发生，通常需要仔细设计和审查触发器，并且在数据库中实施适当的强制访问控
制策略。只有经过全面测试和风险评估后，才能确保触发器和用户权限的正确配置。"""

sql_text= """安全模型验证：
当触发器在用户user1的授权范围内进行操作时，user2无法通过这些操作来获得对table2的权限，确保了权限的隔离。

恢复过程：

1. 清理数据和对象（如果有的话）：
   - DELETE FROM table1;
     DROP TRIGGER trigger1;
     DROP TABLE table1;
     CONNECT SYS AS SYSDBA;
     REVOKE ANY TRIGGER FROM SYS;
     REVOKE CREATE ANY TABLE FROM SYS;
     DROP USER user1 CASCADE;
     DROP USER user2 CASCADE;
     DROP USER IF EXISTS user1
     CREATE USER user1 IDENTIFIED BY user1_password;
     GRANT CREATE TABLE TO user1;
     GRANT CREATE ANY TRIGGER TO user1;
     DROP USER IF EXISTS user2
     CREATE USER user2 IDENTIFIED BY user2_password;
     GRANT CONNECT TO user2;
     CONNECT user1/user1_password;
     CREATE TABLE table1 ( col1 INT );
     CREATE OR REPLACE TRIGGER trigger1
     BEFORE INSERT ON table1
     FOR EACH ROW
     DECLARE
     CURSOR c_table2 IS
      SELECT col2
      FROM table2;
     DELETE FROM table2;
     CONNECT user2/user2_password;
     INSERT INTO table1 VALUES (1);
     SELECT * FROM table2;
     DROP TRIGGER trigger1;
     DROP TABLE table1;
     REVOKE CREATE ANY TRIGGER, CREATE TABLE FROM user1;
     CREATE ANY TRIGGER`权限。
2. user1创建表table1并定义触发器。
3. user2尝试通过触发table1来获得对table2的操作权限。
4. 确定user2的操作是安全的（符合权限要求），或者不是（违反权限要求）。"""


sql_text1 = """Oracle数据库中触发器违反安全模型的情况
实验一：滥用权限

<SQL>
    -- 连接数据库并创建新的用户
    GRANT CONNECT TO user1 IDENTIFIED BY pwd123456789;
    GRANT CONNECT TO user2 IDENTIFIED BY pwd123456789;
    
    -- 用户1连接数据库并创建表和触发器
    ALTER SESSION SET CURRENT_SCHEMA=user1;
    CREATE TABLE table1 (id INTEGER NOT NULL, name VARCHAR2(10));
    INSERT INTO table1 VALUES (1, 'John');
    COMMIT;
    CREATE OR REPLACE TRIGGER trigger1 
    AFTER DELETE ON table1 
    FOR EACH ROW
    BEGIN
        -- 在触发器中执行删除操作，这会导致用户2无权删除table1
        DELETE FROM table1 WHERE id = :old.id;
    END;
    /
    
    -- 用户2连接数据库并尝试删除一行记录
    ALTER SESSION SET CURRENT_SCHEMA=user2;
    DELETE FROM table1 WHERE id = 1;
</SQL>

<SQL>
在上述实验中，用户2虽然没有删除table1的权限，但由于触发器trigger1的定义，其操作将被触发器处理，最终导致了删除权限的滥用。
评判标准：如果用户2在未获得删除table1权限的情况下可以对其进行删除操作，则可判定触发器违反安全模型。
环境恢复：删除触发器和表，断开连接。
</SQL>

<SQL>



实验二：跨对象权限传递

<SQL>
    -- 创建新的用户
    GRANT CONNECT TO user1 IDENTIFIED BY pwd123456789;
    GRANT CONNECT TO user2 IDENTIFIED BY pwd123456789;
    
    -- 用户1连接数据库并创建表和触发器
    ALTER SESSION SET CURRENT_SCHEMA=user1;
    CREATE TABLE table1 (id INTEGER NOT NULL, name VARCHAR2(10));
    CREATE TABLE table2 (id INTEGER NOT NULL, name VARCHAR2(10));
    GRANT INSERT ON table1 TO user2;
    COMMIT;
    CREATE OR REPLACE TRIGGER trigger2 
    AFTER INSERT ON table1 
    FOR EACH ROW
    BEGIN
        INSERT INTO table2 VALUES (:new.id, :new.name);
    END;
    /
    
    -- 用户2连接数据库并尝试插入一条记录
    ALTER SESSION SET CURRENT_SCHEMA=user2;
    INSERT INTO table1 VALUES (1, 'Jane');
</SQL>

<SQL>
当用户2在table1中插入记录时，触发器trigger2被执行，它将导致对table2的插入操作。尽管用户2对table2没有直接插入的权限，但由于触发器的影响，他能够间接地对table2进行写入操作。
评判标准：如果用户2在其权限下尝试插入table1的同时能够同时插入table2，则可判定触发器违反安全模型。
环境恢复：删除触发器和表，断开连接。
</SQL>

<SQL>



实验三：提权漏洞

<SQL>
    -- 创建新的用户
    GRANT CONNECT TO user1 IDENTIFIED BY pwd123456789;
    GRANT CONNECT TO admin IDENTIFIED BY pwd123456789;
    
    -- admin用户连接数据库并创建触发器
    ALTER SESSION SET CURRENT_SCHEMA=admin;
    CREATE OR REPLACE TRIGGER trigger3 
    AFTER INSERT ON all_objects 
    FOR EACH ROW
    WHEN (new.owner = 'SYS')
    BEGIN
        -- 创建任意触发器的权限下，admin用户可创建表来存储系统信息
        EXECUTE IMMEDIATE 'CREATE TABLE my_sys_info (id INTEGER NOT NULL, name VARCHAR2(10))';
    END;
    /
    
    -- 登录到系统管理员账户admin
    ALTER SESSION SET CURRENT_SCHEMA=ADMIN;
    
    INSERT INTO table1 (id, name) VALUES (1, 'TEST');
</SQL>

<SQL>
在触发器中，我们使用EXECUTE IMMEDIATE 动态SQL执行了表创建语句，这允许admin用户在不拥有任何对象的创建权限的情况下创建表。当触发器触发时，admin用户就可以在数据库中创建任意表了。
评判标准：如果在没有表创建权限的情况下，admin用户能够创建表，则可判定触发器违反安全模型。
环境恢复：删除触发器和表，断开连接。
</SQL>

<SQL>



实验四：提权漏洞

<SQL>
    -- 创建新的用户
    GRANT CONNECT TO user1 IDENTIFIED BY pwd123456789;
    
    -- 用户1连接数据库并创建触发器
    ALTER SESSION SET CURRENT_SCHEMA=user1;
    CREATE OR REPLACE TRIGGER trigger4 
    AFTER INSERT ON user1.table1 
    FOR EACH ROW
    BEGIN
        -- 毫无疑问，用户可以在其他用户表上创建触发器
        EXECUTE IMMEDIATE 'CREATE TABLE other_user_table (id INTEGER NOT NULL)';
    END;
    /
    
    -- 用户1插入数据时触发触发器
    INSERT INTO table1 VALUES (1, 'TEST');
</SQL>

<SQL>
在上述实验中，用户1创建了一个针对自己表的触发器。然后在该触发器内部，再次创建了一个新的表。这看起来像是安全的。但是，当触发器被触发时，用户1实际上是在其他用户表上创建了一个新表。
评判标准：如果在其他用户的表中创建了新表，则可判定触发器违反安全模型。
环境恢复：删除触发器和表，断开连接。
</SQL>"""
sql_code, drop_buffer = SQLExtractor(sql_code)
print(sql_code)

execute(sql_code, 'SYSDBA', 'SYSDBA')
execute(drop_buffer, 'SYSDBA', 'SYSDBA')