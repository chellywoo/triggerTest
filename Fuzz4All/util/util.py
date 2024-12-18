import re

import yaml


def comment_remover(text, lang="dm"):
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
        # 定义一个包含常见SQL操作的正则表达式
        regex = r"(GRANT|REVOKE|CONNECT|CREATE|INSERT|UPDATE|DROP|SELECT|DELETE)[^;]*;"
        # 编译正则表达式模式
        pattern = re.compile(regex, re.IGNORECASE)
        # 匹配所有SQL语句
        matcher = pattern.finditer(text)

        sql_buffer = []
        drop_buffer = []
        for match in matcher:
            sql_code = match.group()
            # 提取CREATE语句
            if sql_code.upper().startswith("CREATE"):
                words = sql_code.split()
                try:
                    if 'USER' == words[1]:
                        sql_buffer.append(f"DROP {words[1]} IF EXISTS {words[2]}")
                    if "OR" == words[1]:
                        drop_statement = f"DROP {words[3]} IF EXISTS {words[4]}"
                    else:
                        drop_statement = f"DROP {words[1]} IF EXISTS {words[2]}"
                    drop_buffer.insert(0, drop_statement + ";")  
                except:
                    return []
            if "END" in sql_code.upper():
                sql_text = sql_buffer.pop()
                sql_code = sql_text + sql_code
                
            # 将原始SQL代码添加到缓冲区
            sql_buffer.append(sql_code)
        # 将DROP语句添加到SQL代码的末尾
        sql_buffer.extend(drop_buffer)
        print("\n".join(sql_buffer))
        return sql_buffer, drop_buffer
    elif lang == "smt2":
        return re.sub(r";.*", "", text)
    else:
        # TODO (Add other lang support): temp, only facilitate basic c/cpp syntax
        # raise NotImplementedError("Only cpp supported for now")
        return text


# most fuzzing targets should be some variation of source code
# so this function is likely fine, but we can experiment with
# other more clever variations
def simple_parse(gen_body: str):
    # first check if its a code block
    if "```" in gen_body:
        func = gen_body.split("```")[1]
        func = "\n".join(func.split("\n")[1:])
    else:
        func = ""
    return func


def create_chatgpt_docstring_template(
    system_message: str, user_message: str, docstring: str, example: str, first: str
):
    messages = [{"role": "system", "content": system_message}]
    messages.append({"role": "user", "content": docstring})
    messages.append({"role": "user", "content": example})
    if first != "":
        messages.append({"role": "user", "content": user_message})
        messages.append({"role": "assistant", "content": "```\n{}\n```".format(first)})
    messages.append({"role": "user", "content": user_message})
    return messages


def natural_sort_key(s):
    _nsre = re.compile("([0-9]+)")
    return [
        int(text) if text.isdigit() else text.lower() for text in re.split(_nsre, s)
    ]


def load_config_file(filepath: str):
    """Load the config file."""
    with open(filepath, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config
