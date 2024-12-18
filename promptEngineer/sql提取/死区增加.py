def modify_text(text):
    # 找到begin的位置
    text = text.upper()
    begin_index = text.find('BEGIN')
    if begin_index != -1:
        # 在begin之后插入if 2 > 1 THEN
        text = text[:begin_index + 5] + ' \n IF 2 > 1 THEN' + text[begin_index + 5:]
    
    # 找到end的位置
    end_index = text.rfind('END')
    if end_index != -1:
        # 在最末位的end之前插入else ---死区代码 END if;
        text = text[:end_index] + ' ELSE \n--请在此处插入可以正常执行的代码 \n END IF;\n' + text[end_index:]
    return text

# 原始文本
original_text = """
CREATE OR REPLACE TRIGGER trg_after_insert ON public_table 
AFTER INSERT 
FOR EACH ROW 
BEGIN 
INSERT INTO protected_table(id,sensitive_data) VALUES(:NEW.id,'sensitive info');
END trg_after_insert;
"""

# 修改后的文本
modified_text = modify_text(original_text)
print(modified_text)
