from openai import OpenAI
import re
import numpy as np

def generate_deaf(sql_code) -> str:
    # sql = "\n".join(sql_code)
    prompt = "根据上下文，请在我要求的地方插入复杂SQL语句，结合原始文本输出，不允许增加无效SQL语句，不允许修改其他地方的SQL，不用分析原因直接告诉我结果:"
    sql = prompt + "\n" + sql_code
    client = OpenAI(
        api_key="sk-67d0f834d27e46eeb819368970a64075", # 如果您没有配置环境变量，请在此处用您的API Key进行替换
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope服务的base_url
    )
    # completion = client.chat.completions.create(
    #     model="qwen2.5-coder-32b-instruct", # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    #     messages=[
    #         {'role': 'system', 'content': '你是Oracle数据库的安全保卫者，你要不断的发现数据库在触发器的使用过程中可能存在的安全漏洞，并给出对应的测试用例。'},
    #         {'role': 'user', 'content': sql}
    #     ],
    # )
    
    # parameters = {
    #         "batch_size": 1,
    #         "temperature": 1.0,
    #         "max_length": 300
    #     }
    completion = client.chat.completions.create(model="qwen2.5-coder-32b-instruct", 
            messages=[
                {'role': 'system', 'content': '你是Oracle数据库的安全保卫者，你要不断的发现数据库在触发器的使用过程中可能存在的安全漏洞，并给出对应的测试用例。'},
                {'role': 'user', 'content': sql}
            ], temperature=1.2)
    sx = completion.choices[0].message.content

    return sx

def extract_sql(sql) -> []:
    regex = r"(GRANT|REVOKE|CONNECT|CREATE|INSERT|UPDATE|DROP|SELECT|DELETE|DECLARE|BEGIN|IF|EXECUTE|ELSE|DBMS)\s[^;]*;|(END)[^;]*;"
    pattern = re.compile(regex, re.IGNORECASE | re.MULTILINE)
    matcher = pattern.finditer(sql)
    sql_buffer = [] ## 原始sql
    for match in matcher:
        sql_code = match.group()
        sql_buffer.append(sql_code)
    # print("sql测例提取结果为：","\n".join(sql_buffer))
    return sql_buffer

sql_code = """DROP USER IF EXISTS user1 CASCADE;
CREATE USER user1 IDENTIFIED BY "123456789";
GRANT CREATE SESSION, CREATE TABLE, CREATE TRIGGER TO user1;
DROP USER IF EXISTS user2 CASCADE;
CREATE USER user2 IDENTIFIED BY "123456789";
GRANT CREATE SESSION TO user2;
CONNECT user1/"123456789";
DROP TABLE IF EXISTS table1 CASCADE;
CREATE TABLE table1 (id NUMBER PRIMARY KEY);
DROP TABLE IF EXISTS table2 CASCADE;
CREATE TABLE table2 (id NUMBER PRIMARY KEY);
INSERT INTO table1 (id) VALUES (1);
GRANT INSERT ON table1 TO user2;
CONNECT user2/"123456789";
DROP TRIGGER IF EXISTS trg_after_insert CASCADE;
CREATE OR REPLACE TRIGGER trg_after_insert
AFTER INSERT ON table1
FOR EACH ROW
DECLARE
BEGIN
    IF 2 > 1 THEN
        INSERT INTO table2 (id) VALUES (1);
    ELSE
        --请在此处插入可以正常执行的代码
    END IF;
END;
CONNECT user1/"123456789";
INSERT INTO table1 (id) VALUES (2);
SELECT * FROM table2;
CONNECT user2/"123456789";
INSERT INTO table1 (id) VALUES (3);
SELECT * FROM table2;
CONNECT user1/"123456789";
DROP USER user2 CASCADE;
DROP USER user1 CASCADE;"""

resp = generate_deaf(sql_code)
sql = extract_sql(resp)
print("\n".join(sql))
