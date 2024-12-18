import os
import time
from pathlib import Path
from typing import List

import subprocess
from Fuzz4All.target.target import FResult, Target
from Fuzz4All.util.util import comment_remover
import re
import dmPython

# 获取达梦数据库连接
def get_dm_connection():
    # 假设连接配置
    dm_user = 'SYSDBA'
    dm_password = 'SYSDBA'
    dm_host = '127.0.0.1'
    dm_port = '5236'
    return dmPython.connect(user=dm_user, password=dm_password, server=dm_host, port=int(dm_port))

# 获取达梦数据库版本信息
def get_dm_version_info():
    connection = get_dm_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM v$version;")
    version = [row[0] for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return version

# 获取达梦数据库主要版本号（模拟获取最新 C++版本）
def get_most_recent_dm_version():
    all_versions = get_dm_version_info()
    version_numbers = [re.search(r'(\d+\.\d+\.\d+)', ver).group(1) if re.search(r'(\d+\.\d+\.\d+)', ver) else None for ver in all_versions]
    sorted_versions = sorted([version for version in version_numbers if version is not None], key=lambda x: [int(y) for y in x.split('.')])
    if len(sorted_versions) > 0:
        return sorted_versions[-1]
    else:
        return "no Oracle version found"
MOST_RECENT_DM_VERSION = get_most_recent_dm_version()

class DMTarget(Target):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.folder = "Results/test"
            
        # self.sql_buffer = []
        # self.drop_buffer = []
        self.SYSTEM_MESSAGE = "你是Oracle数据库的安全保卫者，你要不断的发现数据库在触发器的使用过程中可能存在的安全漏洞，并给出对应的测试用例。"
        if kwargs["template"] == "fuzzing_with_config_file":
            config_dict = kwargs["config_dict"]
            self.prompt_used = self._create_prompt_from_config(config_dict)
            self.config_dict = config_dict
        else:
            raise NotImplementedError

    def write_back_file(self, code: str, write_back_name: str = "") -> str:
        # 这里可以将查询写入文件或其他存储位置，为了简化示例，只打印
        """Writes the generated SQL code to a file and returns the file path."""
        if write_back_name != "":
            try:
                with open(write_back_name, "w", encoding="utf-8") as f:
                    f.write(code)
            except:
                pass
        else:
            write_back_name = "tmp/temp{}.fuzz".format(self.CURRENT_TIME)
            try:
                with open(write_back_name, "w", encoding="utf-8") as f:
                    f.write(code)
            except:
                pass
        return write_back_name

    def wrap_prompt(self, prompt: str) -> str:
        """Wraps the prompt in a comment and appends the necessary SQL structure."""
        return f"-- {prompt} \n{self.prompt_used['separator']}\n{self.prompt_used['begin']}"

    def wrap_in_comment(self, prompt: str) -> str:
        """Wraps the given prompt in a SQL comment."""
        return f"-- {prompt}"

    def filter(self, code: str) -> bool:
        """Checks if the generated code contains necessary SQL structures."""
        clean_code = code.replace(self.prompt_used["begin"], "").strip()
        return self.prompt_used["target_api"] in clean_code

    def clean(self, code: str) -> str:
        """Removes comments from the code."""
        # sql, drop_msg = comment_remover(code, lang="dm")
        # return sql
        code, drop, trigger = self.extract_sql(code)
        return "\n".join(code)
        # return "\n".join(self.sql_buffer)
    
    def clean_code(self, code: str) -> str:
        """Further cleans the code, removing empty lines and unnecessary structures."""
        code, drop, trigger = self.extract_sql(code)
        return "\n".join(code)
        # return "\n".join(self.sql_buffer)

    # def extract_sql(self, code: str) -> ([], []):
    #      # 定义一个包含常见SQL操作的正则表达式
    #     regex = r"(GRANT|CONNECT|CREATE|INSERT|UPDATE|DROP|SELECT|DELETE|END|BEGIN)[^;]*;"
    #     # 编译正则表达式模式
    #     pattern = re.compile(regex, re.IGNORECASE)
    #     # 匹配所有SQL语句
    #     matcher = pattern.finditer(code)

    #     sql_buffer = []
    #     drop_buffer = []
    #     for match in matcher:
    #         sql_code = match.group()
    #         # 提取CREATE语句
    #         if sql_code.upper().startswith("CREATE"):
    #             words = sql_code.split()
    #             try:
    #                 if 'USER' == words[1]:
    #                     sql_buffer.append(f"DROP {words[1]} IF EXISTS {words[2]}")
    #                 if "OR" == words[1]:
    #                     drop_statement = f"DROP {words[3]} IF EXISTS {words[4]}"
    #                 else:
    #                     drop_statement = f"DROP {words[1]} IF EXISTS {words[2]}"
    #                 drop_buffer.insert(0, drop_statement + ";")  
    #             except:
    #                 return []
    #         if "END" in sql_code.upper():
    #             sql_text = sql_buffer.pop()
    #             sql_code = sql_text + sql_code
                
    #         sql_buffer.append(sql_code)
    #     sql_buffer.extend(drop_buffer)
    #     print("\n".join(sql_buffer))
    #     return sql_buffer, drop_buffer
    def extract_sql(self, sql_code) -> ([], [], []):
        regex = r"(GRANT|REVOKE|CONNECT|CREATE|INSERT|UPDATE|DROP|SELECT|DELETE|BEGIN|END)[^;]*;"
        # pattern = re.compile(regex, re.IGNORECASE)
        # regex = r"^\s*(GRANT|CONNECT|CREATE|INSERT|UPDATE|DROP|SELECT|DELETE|BEGIN|END)[^;]*;"
        pattern = re.compile(regex, re.IGNORECASE | re.MULTILINE)
        matcher = pattern.finditer(sql_code)

        sql_buffer = []
        drop_buffer = []
        cover_list = [0,0,0,0,0]
        for match in matcher:
            sql_code = match.group()
            if sql_code.upper().startswith("CREATE"):
                words = sql_code.split()
                if words[1].upper() == "TRIGGER" or (len(words) > 3 and words[3].upper() == "TRIGGER"):
                    cover_list = self.count(sql_code, cover_list)
                if words[1].upper() == "PROCEDURE" or (len(words) > 3 and words[3].upper() == "PROCEDURE"):
                    cover_list[2] = 1
                if 'ROLE' == words[1].upper():
                    cover_list[4] = 1
                    sql_buffer.append(f"DROP {words[1]} IF EXISTS {words[2]} CASCADE;")
                if 'USER' == words[1].upper():
                    sql_buffer.append(f"DROP {words[1]} IF EXISTS {words[2]} CASCADE;")
                
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
                if 'CREATE ANY TRIGGER' in sql_code.upper():
                    cover_list[4] = 1
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
        print("触发器结果为：{}".format(cover_list))
        return sql_buffer, drop_buffer, cover_list 

    def count(self, sql_code, list):
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
    
    
    def validate_individual(self, filename) -> (FResult, str):
        try:
            # 读取 SQL 文件内容
            with open(filename, "r", encoding="utf-8") as f:
                sql_code = f.read()
            print(sql_code)

            sql_buffer, drop_buffer, trigger = self.extract_sql(sql_code)
            # print(sql_code)
            if sql_buffer == [] or sum(trigger) == 0:
                return FResult.SAFE, ""
            else:
                self.update_file(trigger)
            
            # 执行 SQL 语句
            # success, output = self.execute(self.sql_buffer)
            success, output = self.execute(sql_buffer)
            # if self.drop_buffer != []:
                # self.execute(self.drop_buffer)
            if drop_buffer != []:
                self.execute(drop_buffer)

            if success:
                return FResult.SAFE, output
            else:
                if output == "前后对比错误":
                    return FResult.FAILURE, output
                else :
                    print(output)
                    return FResult.ERROR, output

        except Exception as e:
            print(e)
            return FResult.ERROR, str(e)

    def execute(self, sql_code, user="SYSDBA", password="SYSDBA") -> (str, str):
        sql_statements = sql_code
        success = True
        msgs = []
        sql_stmt = []
        for stmt in sql_statements:
            words = stmt.split()
            if words[0].upper() == 'CONNECT':
                try:
                    try:
                        success, msg = self.execute_sql(sql_stmt, user, password)
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
    
    def execute_sql(self, sql, user, password) -> (str, str):
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

    def update_file(self, data_array):
        file_path = self.folder + "/count/triggerType.txt"
        if not os.path.exists(file_path):
            self.initialize_file(file_path)
        with open(file_path, 'r+') as file:
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
            else:
                new_lines.append(lines[pointer])
            
            pointer += 1

            # 更新测例总数
            new_total_value = int(lines[pointer].strip().split(': ')[1]) + 1
            new_lines.append(lines[pointer].replace(lines[pointer].strip().split(': ')[1], str(new_total_value)))

            file.seek(0)
            file.writelines(new_lines)

    def initialize_file(self, file_path):
        os.makedirs(self.folder + "/count", exist_ok=True)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.write("单条件触发器出现次数: 0\n")
                file.write("多条件触发触发器出现次数: 0\n")
                file.write("使用触发器调用存储过程/函数出现次数: 0\n")
                file.write("动态sql执行出现次数: 0\n")
                file.write("角色与权限授予出现次数: 0\n")
                file.write("组合出现次数: 0\n")
                file.write("测例的总数: 0\n")