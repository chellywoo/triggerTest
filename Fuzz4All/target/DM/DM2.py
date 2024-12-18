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
    dm_database = 'SYSDBA'
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
            write_back_name = "/tmp/temp{}.fuzz".format(self.CURRENT_TIME)
            try:
                with open(write_back_name, "w", encoding="utf-8") as f:
                    f.write(code)
            except:
                pass
        return write_back_name

    def wrap_prompt(self, prompt: str) -> str:
        """Wraps the prompt in a comment and appends the necessary SQL structure."""
        return f"/* {prompt} */\n{self.prompt_used['separator']}\n{self.prompt_used['begin']}"

    def wrap_in_comment(self, prompt: str) -> str:
        """Wraps the given prompt in a SQL comment."""
        return f"-- {prompt}"

    def filter(self, code: str) -> bool:
        """Checks if the generated code contains necessary SQL structures."""
        clean_code = code.replace(self.prompt_used["begin"], "").strip()
        return self.prompt_used["target_api"] in clean_code

    def clean(self, code: str) -> str:
        """Removes comments from the code."""
        return comment_remover(code, lang="dm")

    def clean_code(self, code: str) -> str:
        """Further cleans the code, removing empty lines and unnecessary structures."""
        code = comment_remover(code, lang="dm")
        return "\n".join(
            line for line in code.split("\n") if line.strip() and line.strip() != self.prompt_used["begin"]
        )

    def validate_individual(self, filename) -> (FResult, str):
        try:
            # 读取 SQL 文件内容
            with open(filename, "r", encoding="utf-8") as f:
                sql_code = f.read()

            # 去除 SQL 代码中的注释
            sql_code = self.clean(sql_code)
            print(sql_code)

            # 执行 SQL 语句
            # 假设我们有一个 execute_sql 方法来执行 SQL 脚本
            success, output = self.execute_sql(sql_code)

            if success:
                return FResult.SAFE, output
            else:
                return FResult.FAILURE, output

        except Exception as e:
            return FResult.ERROR, str(e)

    def execute_sql(self, sql_code) -> (bool, str):
        try:
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
        
            stdout, stderr = process.communicate(input=sql_code, timeout=120)
            # print("stdout:", stdout)
            # print("stderr:", stderr)

            if process.returncode == 0:
                # SQL 执行成功
                return True, stdout
            else:
                # SQL 执行失败
                return False, stderr
        except subprocess.TimeoutExpired:
            # 超时处理
            return False, "SQL execution timed out"