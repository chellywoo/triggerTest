import re
import dmPython
def extract_sql( sql_code) -> ([], []):
        regex = r"(GRANT|REVOKE|CONNECT|CREATE|INSERT|UPDATE|DROP|SELECT|DELETE|BEGIN|END)[^;]*;"
        # pattern = re.compile(regex, re.IGNORECASE)
        # regex = r"^\s*(GRANT|CONNECT|CREATE|INSERT|UPDATE|DROP|SELECT|DELETE|BEGIN|END)[^;]*;"
        pattern = re.compile(regex, re.IGNORECASE | re.MULTILINE)
        matcher = pattern.finditer(sql_code)

        sql_buffer = []
        drop_buffer = []
        # cover_list = [0,0,0,0,0]
        for match in matcher:
            sql_code = match.group()
            if sql_code.upper().startswith("CREATE"):
                words = sql_code.split()
                # if words[1].upper() == "TRIGGER" or (len(words) > 3 and words[3].upper() == "TRIGGER"):
                #     cover_list = self.count(sql_code, cover_list)
                # if words[1].upper() == "PROCEDURE" or (len(words) > 3 and words[3].upper() == "PROCEDURE"):
                #     cover_list[2] = 1
                # if 'ROLE' == words[1].upper():
                #     # cover_list[4] = 1
                #     sql_buffer.append(f"DROP {words[1]} IF EXISTS {words[2]} CASCADE;")
                # if 'USER' == words[1].upper():
                #     sql_buffer.append(f"DROP {words[1]} IF EXISTS {words[2]} CASCADE;")
                
                drop_statement = ""
                if "OR" == words[1].upper():
                    drop_statement = ''
                    if words[3].upper() == "PROCEDURE":
                        split1 = words[4].split("(")
                        drop_statement = f"DROP {words[3]} IF EXISTS {split1[0]} CASCADE;"
                    else:
                        drop_statement = f"DROP {words[3]} IF EXISTS {words[4]} CASCADE;"
                    sql_buffer.append(drop_statement)
                else:
                    if words[1].upper() == "PROCEDURE":
                        split1 = words[2].split("(")
                        drop_statement = f"DROP {words[1]} IF EXISTS {split1[0]} CASCADE;"
                    else:
                        drop_statement = f"DROP {words[1]} IF EXISTS {words[2]} CASCADE;"
                    sql_buffer.append(drop_statement)
                    
                drop_buffer.insert(0, drop_statement)  
            if sql_code.upper().startswith("GRANT"):
                # if 'CREATE ANY TRIGGER' in sql_code.upper():
                #     cover_list[4] = 1
                if 'CONNECT' in sql_code.upper():
                    sql_code = sql_code.replace('CONNECT','CREATE SESSION')
            if sql_code.upper().startswith("BEGIN") and sql_buffer:
                sql_text = sql_buffer.pop()
                sql_code = sql_text + sql_code
            if sql_code.upper().startswith("END"):
                if sql_buffer == []:
                    continue
                sql_text = sql_buffer.pop()
                sql_code = sql_text + sql_code
            sql_buffer.append(sql_code)
        # sql_buffer.extend(drop_buffer)
        print("\n".join(sql_buffer))
        # print("触发器结果为：{}".format(cover_list))
        return sql_buffer, drop_buffer 


def execute( sql_code, user="SYSDBA", password="SYSDBA") -> (str, str):
        sql_statements = sql_code
        success = True
        msgs = []
        sql_stmt = []
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
                    sql_stmt = []
                    continue
                except Exception as e:
                    success = False
                    print("用户连接出错: {e}")
                    return False, "用户连接出错: {e}"
                    break
            else:
                # sql_stmt += stmt
                sql_stmt.append(stmt)
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

    #     for stmt in sql_statements:
    #         words = stmt.split()
    #         if words[0].upper() == 'CONNECT':
    #             try:
    #                 self.execute_sql(sql_stmt, user, password)
    #                 parts = words[1].split('/')
    #                 user = parts[0]
    #                 password = parts[1].split(';')[0]
    #                 continue
    #             except Exception as e:
    #                 success = False
    #                 print("用户连接出错: {e}")
    #                 return False, "用户连接出错: {e}"
    #                 break
    #         elif words[0].upper() == 'DROP' and words[1].upper() == 'USER':
    #             user = "SYSDBA"
    #             password = "SYSDBA"
    #             sql_stmt += stmt
    #         try:
    #             success, msg = self.execute_sql(stmt, user, password)
    #             if success:
    #                 if msg != "Success":
    #                     msgs.append(msg)
    #             else:
    #                 print (f"执行SQL语句 {stmt} 出错: {msg}")
    #                 return False, f"执行SQL语句 {stmt} 出错: {msg}"
    #         except Exception as e:
    #             print (f"执行SQL语句 {stmt} 出错: {e}")
    #             return False, f"执行SQL语句 {stmt} 出错: {e}"
    #         if len(msgs) > 1:
    #             first_msg = msgs[0]
    #             is_equal = all(msg == first_msg for msg in msgs)
    #             if is_equal == False:
    #                 print("前后对比错误")
    #                 return False, "前后对比错误"
        return success, msgs
    
def execute_sql( sql, user, password) -> (str, str):
        msgs = ""
        try:
            conn = dmPython.connect(user=user, password=password, server='127.0.0.1', port=int(5236))
            cursor = conn.cursor()
            for stmt in sql:
                cursor.execute(stmt)
                if cursor.description:  # 如果是查询语句
                    results = cursor.fetchall()
                    for row in results:
                        print(row)
                        msgs += str(row) + "\n"
                else:
                    conn.commit()  # 提交非查询语句的事务
            if msgs == "":
                return True, "Success"
            else:
                return True, msgs
        except dmPython.Error as e:
            return False, f"数据库操作出错: {e}"
        finally:
            try:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
            except Exception as close_e:
                return f"关闭游标或连接时出错: {close_e}"

sql_code1 = """
CREATE USER trigger_test_user IDENTIFIED BY StrongPassword123;
GRANT CREATE SESSION, CREATE TRIGGER, CREATE TABLE TO trigger_test_user;

CONNECT SYSDBA/SYSDBA;

CREATE TABLE sensitive_data (
    id NUMBER,
    description VARCHAR2(100)
);


CREATE TABLE sensitive_log (
    id NUMBER,
    action VARCHAR2(100)
);

GRANT INSERT ON sensitive_data TO trigger_test_user;

CREATE OR REPLACE TRIGGER trg_sensitive_data_insert
AFTER INSERT ON sensitive_data
FOR EACH ROW
BEGIN
    -- 尝试插入日志记录，即使触发器所有者admin用户没有权限插入敏感_log表
    INSERT INTO sensitive_log (id, action) VALUES (:NEW.id, 'Insert by user: ' || USER);
END;

SELECT * FROM sensitive_data;


CONNECT trigger_test_user/StrongPassword123;

INSERT INTO SYSDBA.sensitive_data (id, description) VALUES (1, 'Test Description');


CONNECT SYSDBA/SYSDBA;

SELECT * FROM SYSDBA.sensitive_data;

SELECT * FROM SYSDBA.sensitive_log;
""" 

# sql_code, drop_buffer = extract_sql(sql_code1)
# print(sql_code)
# execute(sql_code, 'SYSDBA', 'SYSDBA')
# execute(drop_buffer, 'SYSDBA', 'SYSDBA')

import dmPython

class DatabaseExecutor:
    def __init__(self, server='127.0.0.1', port=5236):
        self.server = server
        self.port = port

    def execute(self, sql_code, user="SYSDBA", password="SYSDBA"):
        connection_string = f"{user}/{password}@{self.server}:{self.port}"
        sql_statements = self._parse_sql(sql_code)
        results = []

        for stmt in sql_statements:
            if "CONNECT" in stmt.upper():
                user, password = self._extract_credentials(stmt)
                connection_string = f"{user}/{password}@{self.server}:{self.port}"
                continue
            
            success, msg = self.execute_sql(stmt, connection_string)
            if not success:
                return False, msg
            if msg != 'Success':
                results.append(msg)

        if len(results) > 1:
            first_msg = results[0]
            is_equal = all(msg == first_msg for msg in results)
            if is_equal == False:
                print("前后对比错误")
                return False, "前后对比错误"
        return True, results

    def execute_sql(self, sql, connection_string):
        try:
            with dmPython.connect(connection_string) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    if cursor.description:  # 查询语句
                        return True, [str(row) for row in cursor.fetchall()]
                    else:  # 非查询语句
                        conn.commit()
                        return True, "Success"
        except dmPython.Error as e:
            return False, f"数据库操作出错: {e}"

    def _parse_sql(self, sql_code):
        return [stmt.strip() for stmt in sql_code.split(';') if stmt.strip()]

    def _extract_credentials(self, connect_stmt):
        _, credentials = connect_stmt.split()
        user, password = credentials.split('/')
        return user, password.split(';')[0]

# 示例用法
executor = DatabaseExecutor()
sql_code = "CONNECT SYSDBA/SYSDBA; SELECT * FROM MY_TABLE; UPDATE MY_TABLE SET name='John' WHERE id=1;"
success, messages = executor.execute(sql_code)
print("成功:", success, "消息:", messages)
