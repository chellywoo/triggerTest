import dmPython
import re

def SQLExtractor(sql_code):
    # regex = r"(GRANT|CONNECT|CREATE|INSERT|UPDATE|DROP|SELECT|DELETE|END|BEGIN)[^;]*;"
    regex = r"(((GRANT|REVOKE|CONNECT|CREATE|INSERT|UPDATE|DROP|SELECT|DELETE|BEGIN|END)(\s+[^\s;]+)+;))|((?m)^--.*$)"

    pattern = re.compile(regex, re.IGNORECASE)
    matcher = pattern.finditer(sql_code)

    sql_buffer = []
    drop_buffer = []
    cover_list = [0,0,0,0,0]
    for match in matcher:
        sql_code = match.group()
        if sql_code.upper().startswith("CREATE"):
            words = sql_code.split()
            if words[1].upper() == "TRIGGER" or (len(words) > 3 and words[3].upper() == "TRIGGER"):
                cover_list = count(sql_code, cover_list)
            if words[1].upper() == "PROCEDURE" or (len(words) > 3 and words[3].upper() == "PROCEDURE"):
                cover_list[2] = 1
            if 'ROLE' == words[1].upper():
                cover_list[4] = 1
            if 'USER' == words[1].upper():
                sql_buffer.append(f"DROP {words[1]} IF EXISTS {words[2]};")
            if "OR" == words[1].upper():
                drop_statement = f"DROP {words[3]} IF EXISTS {words[4]}"
            else:
                drop_statement = f"DROP {words[1]} IF EXISTS {words[2]}"
            drop_buffer.insert(0, drop_statement + ";")  
        if sql_code.upper().startswith("GRANT"):
            if 'CREATE ANY TRIGGER' in sql_code.upper():
                cover_list[4] = 1
            if 'CONNECT' in sql_code.upper():
                sql_code = sql_code.replace('CONNECT','CREATE SESSION')
        if "END" in sql_code.upper():
            sql_text = sql_buffer.pop()
            sql_code = sql_text + sql_code
        sql_buffer.append(sql_code)
    sql_buffer.extend(drop_buffer)
    print("\n".join(sql_buffer))
    print("触发器结果为：{}".format(cover_list))
    return sql_buffer, drop_buffer 

def count(sql_code, list):
    # 按行分割语句
    lines = sql_code.split('\n')

    for line in lines:
        line = line.strip()
        if line.upper().startswith('BEFORE') or line.upper().startswith('AFTER'):
            parts = line.split()
            if len(parts) > 2:
                if parts[2].upper() == "OR":
                    list[1] = 1
                else:
                    list[0] = 1

    if 'EXECUTE IMMEDIATE' in sql_code.upper():
        list[3] = 1
    return list

sql_code = """例如，我们假设存在一种情况，其中一个用户 `USER1` 
创建了一个触发器，该触发器在对表进行某些操作时会执行某些高权限的动作。然而，这个触发器的设计存在一个
漏洞，即它允许另一个用户 `USER2` 通过触发这个触发器来执行一些超出它们原本权限的操作。
1. cehsi 
<sex_>
<><><><>
```sql
CREATE OR REPLACE PROCEDURE log_access AS
    v_currentdate DATE := SYSDATE;
BEGIN
    -- 仅允许在工作日的9:00至17:00间提交插入操作
    IF TO_CHAR(v_currentdate, 'D') NOT IN (1, 7) AND TO_CHAR(v_currentdate, 
'hh24:mi') BETWEEN '09:00' AND '17:00' THEN
        INSERT INTO personal_data (id, name, social_security_number) VALUES (1, 
'John Doe', '123-45-6789');
INSERT INTO personal_data (id, name, social_security_number) VALUES (NULL, 
'Unauthorized Access', TO_CHAR(v_currentdate,'dd-mm-yyyy hh:mi:ss am'));END 
IF;END log_access;
insert_trigger`，当在表`personal_data`上发生插入操作时自动调用存储过程`log_access
`。
```sql
sql> create user user1 identified by 1234;
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

insert_trigger`，当在表`personal_data`上发生插入操作时自动调用存储过程`log_access
`。
```sql

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

SQLExtractor(sql_code)

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


# SQLExtractor(sql_text1)
import os
def logNum(self, list):
    # 如果文件不存在，则创建并初始化内容为0
    if not os.path.exists(self.folder + "/count/triggerType.txt"):
        with open(self.folder + "/count/triggerType.txt", 'w') as file:
            for _ in range(5):
                file.write('0\n')

    # 从文件中读取数据并转换为数组
    file_data_array = []
    with open(self.folder + "/count/triggerType.txt", 'r') as file:
        for line in file.readlines():
            try:
                file_data_array.append(int(line.strip()))
            except ValueError:
                print(f"无法将行 {line} 转换为整数，跳过。")

        # 确保文件中的数据长度与给定数组长度相同
    if len(file_data_array)!= len(list):
        raise ValueError("文件中的数据长度与给定数组长度不匹配。")

    # 对应位置相加
    result_array = [list[i] + file_data_array[i] for i in range(len(list))]
    print(result_array)

def update_file1(data_array):
    file_path = "promptEngineer/count/triggerType.txt"
    if not os.path.exists(file_path):
        initialize_file1()
    with open(file_path, 'r+', encoding='utf-8') as file:
        lines = file.readlines()
        new_lines = []
        pointer = 0
        for i in range(len(data_array)):
            new_value = int(lines[pointer].strip().split(': ')[1]) + data_array[i]
            new_lines.append(lines[pointer].replace(lines[pointer].strip().split(': ')[1], str(new_value)))
            pointer += 1

        # 计算数组中1的个数并更新组合出现次数
        combination_count = sum(data_array)
        if combination_count > 1:
            new_combination_value = int(lines[pointer].strip().split(': ')[1]) + 1
            new_lines.append(lines[pointer].replace(lines[pointer].strip().split(': ')[1], str(new_combination_value)))
        pointer += 1

        # 更新测例总数
        new_total_value = int(lines[pointer].strip().split(': ')[1]) + 1
        new_lines.append(lines[pointer].replace(lines[pointer].strip().split(': ')[1], str(new_total_value)))

        file.seek(0)
        file.writelines(new_lines)

def initialize_file1():
    os.makedirs("promptEngineer/count", exist_ok=True)
    if not os.path.exists("promptEngineer/count/triggerType.txt"):
        with open('promptEngineer/count/triggerType.txt', 'w') as file:
            file.write("单条件触发器出现次数: 0\n")
            file.write("多条件触发触发器出现次数: 0\n")
            file.write("使用触发器调用存储过程/函数出现次数: 0\n")
            file.write("动态sql执行出现次数: 0\n")
            file.write("角色与权限授予出现次数: 0\n")
            file.write("组合出现次数: 0\n")
            file.write("测例的总数: 0\n")
# folder = "promptEngineer"
# data_array = [1, 0, 0, 1, 0]
# update_file1( data_array)
# data_array = [1, 1, 0, 1, 0]
# update_file1( data_array)


    def execute(self, sql_code, user="SYSDBA", password="SYSDBA") -> (str, str):
        sql_statements = sql_code
        success = True
        msgs = []

        for stmt in sql_statements:
            words = stmt.split()
            if words[0].upper() == 'CONNECT':
                try:
                    parts = words[1].split('/')
                    user = parts[0]
                    password = parts[1].split(';')[0]
                    
                    continue
                except Exception as e:
                    success = False
                    print("用户连接出错: {e}")
                    return False, "用户连接出错: {e}"
                    break
            elif words[0].upper() == 'DROP' and words[1].upper() == 'USER':
                user = "SYSDBA"
                password = "SYSDBA"
            try:
                success, msg = self.execute_sql(stmt, user, password)
                if success:
                    if msg != "Success":
                        msgs.append(msg)
                else:
                    print (f"执行SQL语句 {stmt} 出错: {msg}")
                    return False, f"执行SQL语句 {stmt} 出错: {msg}"
            except Exception as e:
                print (f"执行SQL语句 {stmt} 出错: {e}")
                return False, f"执行SQL语句 {stmt} 出错: {e}"
            if len(msgs) > 1:
                first_msg = msgs[0]
                is_equal = all(msg == first_msg for msg in msgs)
                if is_equal == False:
                    print("前后对比错误")
                    return False, "前后对比错误"
        return success, msgs