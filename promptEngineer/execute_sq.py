import re
sql_code = """
CREATE USER test_user IDENTIFIED BY TEST_PASSWORD123;
CONNECT test_user/TEST_PASSWORD123;
SELECT CURRENT_USER FROM DUAL;
CREATE TABLE sensitive_info (id NUMBER PRIMARY KEY, info VARCHAR2(100));
CREATE TABLE secure_table (
    id NUMBER PRIMARY KEY,
    data VARCHAR2(200)
);
尝试更新敏感信息表INSERT时尝试更新敏感信息表，尽管用户通常没有直接访问此表的权限。

CREATE OR REPLACE TRIGGER trg_secure_table
AFTER INSERT ON secure_table
FOR EACH ROW
AS
BEGIN
    IF NAME = 1 then
        UPDATE sensitive_info
        SET info = 'Sensitive data accessed via trigger'
        WHERE ID = :inserting.new.id;
    end if;
END;

INSERT INTO secure_table VALUES (1, 'Initial data');
SELECT * FROM secure_table;
INSERT以执行触发器
INSERT INTO secure_table VALUES (2, 'Another data');
SELECT * FROM sensitive_info;
SELECT应该是用来验证触发器是否正确设置了信息，但实际可能因触发错误而无法查看。

-- 删除创建的表和触发器，清理环境
DROP TRIGGER trg_secure_table;
DROP TABLE secure_table CASCADE CONSTRAINTS;
DROP TABLE sensitive_info CASCADE CONSTRAINTS;"""
def extract_sql(sql) -> ([], [], []):
    # regex = r"(GRANT|REVOKE|CONNECT|CREATE|INSERT|UPDATE|DROP|SELECT|DELETE|DECLARE|BEGIN|END|IF|EXECUTE|ELSE|DBMS)[^;]*;"
    regex = r"(GRANT|REVOKE|CONNECT|CREATE|INSERT|UPDATE|DROP|SELECT|DELETE|DECLARE|BEGIN|END|IF|EXECUTE|ELSE|DBMS)\s[^;]*;|(END)[^;]*;"
    # pattern = re.compile(regex, re.IGNORECASE)
    # regex = r"^\s*(GRANT|CONNECT|CREATE|INSERT|UPDATE|DROP|SELECT|DELETE|BEGIN|END)[^;]*;"
    pattern = re.compile(regex, re.IGNORECASE | re.MULTILINE)
    matcher = pattern.finditer(sql)
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
            #     sql_buffer.append(f"DROP {words[1]} IF EXISTS {words[2]} CASCADE;")
            # if 'USER' == words[1].upper():
            #     sql_buffer.append(f"DROP {words[1]} IF EXISTS {words[2]} CASCADE;")
            
            drop_statement = ""
            if "OR" == words[1].upper():
                drop_statement = ''
                split1 = words[4].split("(")
                drop_statement = f"DROP {words[3]} IF EXISTS {split1[0]} CASCADE;"
                sql_buffer.append(drop_statement)
            else:
                split1 = words[2].split("(")
                drop_statement = f"DROP {words[1]} IF EXISTS {split1[0]} CASCADE;"
                sql_buffer.append(drop_statement)
                
            drop_buffer.insert(0, drop_statement)  
        if sql_code.upper().startswith("GRANT"):
            if 'ANY' in sql_code.upper():
                cover_list[4] = 1
            if 'CONNECT' in sql_code.upper():
                sql_code = sql_code.replace('CONNECT','CREATE SESSION')
        # if sql_code.upper().startswith("BEGIN") and sql_buffer:
        #     sql_text = sql_buffer.pop()
        #     sql_code = sql_text + sql_code
        if sql_code.upper().startswith("END"):
            if sql_buffer == []:
                continue
            sql_text = sql_buffer.pop()
            sql_code = sql_text + "\n" + sql_code
        if len(sql_code.upper().split()) == 1:
                continue
        sql_buffer.append(sql_code)
    # sql_buffer.extend(drop_buffer)
    print("sql测例提取结果为：" + "\n".join(sql_buffer))
    print("触发器结果为：{}".format(cover_list))
    return sql_buffer, drop_buffer, cover_list 
def count(sql_code, list):
    # 按行分割语句
    lines = sql_code.split('\n')
    for line in lines:
        line = line.strip()
        if line.upper().startswith('BEFORE') or line.upper().startswith('AFTER'):
            if "OR" in line.upper():
                list[1] += 1
            else : list[0] += 1
    if 'EXECUTE IMMEDIATE' in sql_code.upper():
        list[3] = 1
    return list


extract_sql(sql_code)