import re

def extract_sql_statements(sql_text):
    # 正则表达式，用于匹配SQL关键字开头的语句
    keyword_pattern = re.compile(
        r"(CREATE|INSERT|UPDATE|DELETE|ALTER|DROP|GRANT|REVOKE|TRIGGER|SELECT|BEGIN)\s+",
        re.IGNORECASE
    )
    
    # 正则表达式，用于匹配BEGIN...END块
    begin_end_pattern = re.compile(
        r"BEGIN\s+([\s\S]*?)\s+END\s*;",
        re.IGNORECASE | re.DOTALL
    )

    def process_begin_end(text):
        """递归处理BEGIN...END块，确保完整的语句被捕获。"""
        while True:
            match = begin_end_pattern.search(text)
            if not match:
                break
            # 替换BEGIN...END块为单个占位符
            placeholder = f"BEGIN...END_PLACEHOLDER_{id(match)}"
            text = text[:match.start()] + placeholder + text[match.end():]
        return text

    # 初始化变量
    sql_text = process_begin_end(sql_text)
    statements = []
    current_statement = ""

    # 按行处理SQL文本
    for line in sql_text.splitlines():
        # 如果行开始是一个新的SQL语句关键字
        if keyword_pattern.match(line.lstrip()):
            # 如果当前语句不为空，则添加到statements列表
            if current_statement.strip():
                statements.append(current_statement.strip())
            # 开始一个新的语句
            current_statement = line
        else:
            # 否则，继续添加到当前语句
            current_statement += "\n" + line
    
    # 添加最后一个语句
    if current_statement.strip():
        statements.append(current_statement.strip())

    # 将占位符替换回BEGIN...END块
    for i, statement in enumerate(statements):
        while "BEGIN...END_PLACEHOLDER_" in statement:
            start_index = statement.index("BEGIN...END_PLACEHOLDER_")
            end_index = start_index + len("BEGIN...END_PLACEHOLDER_")
            placeholder_id = statement[start_index:end_index]
            original_block = begin_end_pattern.search(sql_text).group(0)
            statement = statement.replace(placeholder_id, original_block, 1)
        statements[i] = statement

    return [stmt + ";" for stmt in statements]

# 示例文本
sql_text = """
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
    UPDATE sensitive_info
    SET info = 'Sensitive data accessed via trigger'
    WHERE ID = :new.id;
END;
"""

# 提取SQL语句
extracted_statements = extract_sql_statements(sql_text)

# 打印提取的SQL语句
for statement in extracted_statements:
    print(statement)
    print('-' * 3/4)