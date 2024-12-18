import re

import yaml


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
        # return re.sub(pattern, replacer, text)
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
