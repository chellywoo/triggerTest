import jieba
from collections import Counter

# 你的文本
import re

def extract_keywords(file_path, top_n=6):
    with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

    sql_code_block_pattern = r'```sql(.*?)```'
    text = re.sub(sql_code_block_pattern, '', text, flags=re.DOTALL)
        # 移除单行SQL代码
    single_line_sql_pattern = r'`.*?`'
    text = re.sub(single_line_sql_pattern, '', text)
    # print(text)

    # 定义中文停用词列表
    stopwords = set([' ', '的', '\n', '，', '：', '在', '了', '是', '我', '有', '和', '就', '不','-','`','*','中','。'])


    words = jieba.cut(text)
    # 去除空字符串# 去除停用词和空字符串
    # 去除停用词、空字符串、英文单词和数字
    words = [word for word in words if word not in stopwords and not word.isdigit() and word.isalpha()]

    # 计数
    word_counts = Counter(words)

    # print(word_counts)

    # 获取最常见的词
    most_common_words = word_counts.most_common(top_n)

    # 打印最常见的词
    # print(most_common_words)

    # 提取词汇
    extracted_keywords = [word for word, count in most_common_words]

    # 打印提取的关键词
    # print(extracted_keywords)
    return extracted_keywords

file_path = "config/documentation/sql/dm8_6.md"
words = extract_keywords(file_path)
print(words)