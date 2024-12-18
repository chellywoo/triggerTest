import subprocess
import re

import yaml

def validate_individual(sql_code):
        try:
            # 执行 SQL 语句
            # 假设我们有一个 execute_sql 方法来执行 SQL 脚本
            success, output = execute_sql(sql_code)

            if success:
                print ("SQL executed successfully")
            else:
                print( output)

        except Exception as e:
            return print(str(e))
def execute_sql(sql_code):
        # 这里需要实现具体的 SQL 执行逻辑
        # 例如，使用 Oracle 数据库的 SQL*Plus 或其他工具来执行 SQL 脚本
        # 以下是一个使用 subprocess 调用 SQL*Plus 的示例
        try:
            # 使用 subprocess 调用 SQL*Plus 执行 SQL 脚本
            process = subprocess.Popen(
                ["./disql", "SYSDBA/SYSDBA"],
                # input=sql_code,  # 输入 SQL 代码
                # capture_output=True,
                encoding="utf-8",
                # timeout=60,  # 设置超时时间
                # text=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd = "/home/useradmin/dmdbms/bin"
            )
        
            stdout, stderr = process.communicate(input=sql_code)
            # 打印输出以供调试
            print("stdout:", stdout)
            print("stderr:", stderr)

            # 检查 process 的返回码
            if process.returncode == 0:
                # SQL 执行成功
                return True, stdout
            else:
                # SQL 执行失败
                return False, stderr
        except subprocess.TimeoutExpired:
            # 超时处理
            return False, "SQL execution timed out"
def comment_remover(text, lang="cpp"):
    if lang == "cpp" or lang == "go" or lang == "java":

        def replacer(match):
            s = match.group(0)
            if s.startswith("/"):
                return " "  # note: a space and not an empty string
            else:
                return s

        pattern = re.compile(
            r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
            re.DOTALL | re.MULTILINE,
        )
        return re.sub(pattern, replacer, text)
    elif lang == "dm":
        # pattern = re.compile(r'^[\u4e00-\u9fff].*?$\n', re.MULTILINE)
        # pattern = re.compile(
        #     r'--.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        #     re.DOTALL | re.MULTILINE,
        # )
        pattern = re.compile(
            r'--.*?$|/\*.*?\*/|"(?:\\.|[^\\"])*"|^\*.*?$\n|^[\u4e00-\u9fff].*?$\n|^【.*?$\n|^\..*?$\n|^<.*?$\n',
            re.DOTALL | re.MULTILINE,
        )
    
         # 将匹配到的行替换为空字符串，即删除这些行
        text = re.sub(pattern, '', text)
        # # 移除包含中文字符的行
        text = re.sub(r'[\u4e00-\u9fff]', '', text)
        text = re.sub(r'(?:^\d+(\.).*?$|^[\u4e00-\u9fff].*?$|<[^>]+>|^`.*?$)\n', '', text, flags=re.MULTILINE)

        
        # 移除多余的空行
        text = re.sub(r'\n+', '\n', text)
        
        # 移除行首和行尾的空白字符
        text = re.sub(r'^\s+|\s+$', '', text, flags=re.MULTILINE)
        
        # 移除所有 < > 包含的内容
        # text = re.sub(r'<[^>]+>', '', text)
        
        # 移除以数字加点开头的整行
        # text = re.sub(r'^\d+\..*?$\n', '', text, flags=re.MULTILINE)
        
        # 移除所有中文标点符号
        text = re.sub(r'[，。！？、；：“”（）《》【】…—`]', '', text)
        
        # 移除任何非 SQL 代码块的内容
        # 假设 SQL 代码块由 SQL 语句组成，我们保留这些语句
        # 此正则表达式匹配 SQL 语句的开始和结束
        text = re.sub(r'(?s)```.*?```', '', text)
        
        # 移除任何非 SQL 语句的文本
        # 保留 SQL 语句和 SQL 相关的命令
        # text = re.sub(r'(?s)(CONNECT .*?;|CREATE USER.*?;|GRANT.*?;|CREATE TABLE.*?;|INSERT INTO.*?;)', r'\1', text, flags=re.MULTILINE)
        
        # 移除 SQL 注释
        text = re.sub(r'-.*?$', '', text, flags=re.MULTILINE)
        
        # 移除多行注释
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL | re.MULTILINE)
        return text.strip()
        # 移除文件的第一行
        # 通过分割和重新组合行来实现，从而保留原始的行结构
        # lines = text.split('\n')
        # if len(lines) > 1:
        #     text = '\n'.join(lines[1:])

        # # 移除以数字加点开头的整行、以中文字符开头的整行、包含中文字符的整行
        # # 移除所有 < > 包含的内容、以三个反引号```开头的整行
        # text = re.sub(r'(?:^\d+\..*?$|^[\u4e00-\u9fff].*?$|<[^>]+>|^`.*?$)\n', '', text, flags=re.MULTILINE)

        # # 移除多余的空行
        # text = re.sub(r'\n+', '\n', text)

        # # # 移除所有中文字符和中文标点符号
        # text = re.sub(r'[\u4e00-\u9fff，。！？、；：“”（）《》【】…—`]', '', text)

        # # 移除以数字1.开头的整行
        # text = re.sub(r'^\d+\..*?$\n', '', text, flags=re.MULTILINE)
        # # 移除以中文字符开头的整行
        # # 使用 \u4e00-\u9fff 匹配常用的中文字符范围
        # text = re.sub(r'^[\u4e00-\u9fff].*?$\n', '', text, flags=re.MULTILINE)
        # # 移除所有 < > 包含的内容
        # text = re.sub(r'<[^>]+>', '', text)
        # # 移除以三个反引号```开头的整行
        # text = re.sub(r'^```.*?$\n', '', text, flags=re.MULTILINE)
        # # 移除包含中文字符的整行
        # text = re.sub(r'[\u4e00-\u9fff].*?$\n', '', text, flags=re.MULTILINE)

        # text = re.sub(r'[\u4e00-\u9fff]', '', text)
        # text = re.sub(r'^\s*$\n', '', text, flags=re.MULTILINE)

        # # 移除多余的空行
        # text = re.sub(r'\n+', '\n', text)


        # # 移除所有中文标点符号
        # text = re.sub(r'[，。！？、；：“”（）《》【】…—`]', '', text)

        # return text
        # return re.sub(pattern, replacer, text)
    elif lang == "smt2":
        return re.sub(r";.*", "", text)
    else:
        # TODO (Add other lang support): temp, only facilitate basic c/cpp syntax
        # raise NotImplementedError("Only cpp supported for now")
        return text
def count(stdout):
        server_pattern = r'服务器\[LOCALHOST:5236\]'
        execute_number_pattern = r'执行号:(\d+)'

        # 统计服务器信息出现的次数
        server_count = len(re.findall(server_pattern, stdout))

        # 统计执行号出现的次数
        execute_number_count = len(re.findall(execute_number_pattern, stdout))

        print(f"服务器信息出现的次数: {server_count}")
        print(f"执行号出现的次数: {execute_number_count}")
# stdout = """服务器[LOCALHOST:5236]:处于普通打开状态
# 登录使用时间 : 1.744(ms)
# disql V8
# SQL> 操作已执行
# 已用时间: 12.045(毫秒). 执行号:43601.
# SQL> 
# 服务器[LOCALHOST:5236]:处于普通打开状态
# 登录使用时间 : 1.536(ms)
# SQL> 2   3   4   5   操作已执行
# 已用时间: 4.119(毫秒). 执行号:43801.
# SQL> 2   3   4   5   6   7   8   操作已执行
# 已用时间: 6.023(毫秒). 执行号:43802.
# SQL> 影响行数 1

# 已用时间: 0.365(毫秒). 执行号:43803.
# SQL> 
# 服务器[LOCALHOST:5236]:处于普通打开状态
# 登录使用时间 : 1.588(ms)
# SQL> 操作已执行
# 已用时间: 3.728(毫秒). 执行号:44001.
# SQL> 操作已执行
# 已用时间: 6.051(毫秒). 执行号:44002.
# SQL>"""

# count(stdout)
# sql_code = """例如，我们假设存在一种情况，其中一个用户 `USER1` 
# 创建了一个触发器，该触发器在对表进行某些操作时会执行某些高权限的动作。然而，这个触发器的设计存在一个
# 漏洞，即它允许另一个用户 `USER2` 通过触发这个触发器来执行一些超出它们原本权限的操作。
# 1. cehsi 
# <sex_>
# <><><><>
# ```sql
# grant create table, create trigger to user1;


# CONNECT USER1/123456789;
 
# CREATE TABLE USER1.TEMP_TABLE
# (
#     ID NUMBER(10),
#     NAME VARCHAR2(50)
# );

 
# CREATE OR REPLACE TRIGGER USER1.TRIGGER_CHECK_MAX_SIZE
#     BEFORE INSERT OR UPDATE ON USER1.TEMP_TABLE FOR EACH ROW
# BEGIN
     
#     IF :NEW.NAME IS NOT NULL THEN
#         UPDATE USER1.TEMP_TABLE SET ID = ID * 2 + 1 WHERE NAME = :NEW.NAME;
#     END IF;
# END;
# /

# INSERT INTO USER1.TEMP_TABLE (ID, NAME) VALUES (1, 'SampleName');
# 2.ceshi 
# CONNECT USER1/123456789;  

# DROP TRIGGER USER1.TRIGGER_CHECK_MAX_SIZE;
# DROP TABLE USER1.TEMP_TABLE;
# ```

# 这个测试用例展示了在一个表上的触发器如何可能因为权限设置不当而导致违反安全模型。在这个例子中，`USER1
# ` 创建了一个触发器，它在一些条件下允许对表格进行更新操作，这个操作可能会导致权限超越 `USER1` 
# 的原有权限。

# 实际中，为了防止类似这种情况的发生，通常需要仔细设计和审查触发器，并且在数据库中实施适当的强制访问控
# 制策略。只有经过全面测试和风险评估后，才能确保触发器和用户权限的正确配置。"""
# text = comment_remover(sql_code, "dm")
# print(text)

# validate_individual(text)
# sql_text = """
# 【测试用例1】

# **测试目标：** 演示如何通过触发器绕过自主访问控制，导致用户能够访问超越其授权范围的记录。

# **测试过程：**

# 1. **环境准备：**
#     - 创建管理员用户和用户A、用户B。
#     - 用户A具有INSERT权限，用户B具有SELECT权限。
#     - 创建表`EMPLOYEE`并赋予用户A、用户B不同权限。

# ```sql
# -- 管理员登录
# CREATE USER user_a IDENTIFIED BY password;
# CREATE USER user_b IDENTIFIED BY password;
# GRANT CONNECT, RESOURCE TO user_a;
# GRANT CONNECT TO user_b;

# -- 用户A登录
# CREATE TABLE employee (id NUMBER PRIMARY KEY, name VARCHAR2(30));
# GRANT INSERT ON employee TO user_a;
# ...

# """
# text = comment_remover(sql_text, "dm")
# print(text)
# # print(fres)
# # print(res)


from snownlp import SnowNLP
class KeywordExtractor:
    def __init__(self, docs):
        self.docs = docs
        self.D = len(docs)
        if self.D == 0:
            raise ValueError("文档列表不能为空")
        self.avgdl = sum([len(doc) + 0.0 for doc in docs]) / self.D

    def extract_keywords(self, num_keywords=3):
        keywords_list = []
        for doc in self.docs:
            s = SnowNLP(doc.strip())
            keywords = s.keywords(num_keywords)
            keywords_list.append(keywords)
        return keywords_list

# 读取文件内容
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()
    return content

# 保存关键词到文件
def save_keywords_to_file(keywords_list, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for keywords in keywords_list:
            file.write(', '.join(keywords) + '\n')

# 主函数
def main():
    input_file_path = '/home/useradmin/LXQ/fuzz4all/config/documentation/sql/dm8.md'  # 输入文件路径
    output_file_path = '/home/useradmin/LXQ/fuzz4all/output.txt'  # 输出文件路径
    num_keywords = 3  # 提取的关键词数量

    # 读取文件内容
    text_list = read_file(input_file_path)

    # 初始化关键词提取器
    try:
        extractor = KeywordExtractor(text_list)
    except ValueError as e:
        print(e)
        return
    
    # 提取关键词
    keywords_list = extractor.extract_keywords( num_keywords)

    # 保存关键词到文件
    save_keywords_to_file(keywords_list, output_file_path)

    print("关键词提取完成，结果已保存到", output_file_path)

main()