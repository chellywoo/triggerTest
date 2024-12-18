import jieba
import numpy as np
from snownlp import SnowNLP
from gensim.models import KeyedVectors,Word2Vec

def extract_keywords(file_path, top_n=6):
    with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    return text
file_path = "config/documentation/sql/dm8_6.md"
text = extract_keywords(file_path)
# 假设我们有一个预训练的中文词向量模型

model = Word2Vec.load("distilbert-word2vec_256k-MLM_best/pytorch_model.bin")

# model = KeyedVectors.load_word2vec_format("nlpl_43/model.bin", binary=True, unicode_errors="ignore")
# from gensim.models import KeyedVectors
# from huggingface_hub import hf_hub_download
# model = KeyedVectors.load_word2vec_format(hf_hub_download(repo_id="Word2vec/nlpl_43", filename="model.bin"), binary=True, unicode_errors="ignore")


# 示例中文文本
# text = "自然语言处理是人工智能领域的一个重要方向。"

# 步骤1: 分词
words = jieba.cut(text)
words = list(set(words))
print("分词结果：", "/ ".join(words))

# 步骤2: 词向量获取
vectors = [model[word] for word in words if word in model]
if vectors:
    sentence_vector = np.mean(vectors, axis=0)
else:
    sentence_vector = np.zeros(model.vector_size)

# 步骤3: 语义相似度计算（示例：寻找最相似的词）
target_word = "访问控制"  # 目标词
similar_words = []
for word in model.index_to_key:
    if word in words:
        similarity = model.similarity(word, target_word)
        similar_words.append((word, similarity))
similar_words.sort(key=lambda x: x[1], reverse=True)
# 输出最相似的词
if similar_words:
    print("最相似的词：", similar_words[:5])
else:
    print(f"没有找到与'{target_word}'相似的词。")

# 步骤4: 句法分析（使用SnowNLP进行简单的句子成分分析）
s = SnowNLP(text)
print("句子成分：", s.tags)

# 步骤5: 信息融合（这里仅展示如何将句法分析结果与词向量结合）
# 这里我们简单地将词性标注结果与词向量结合，实际应用中可能需要更复杂的融合策略
for word, flag in s.tags:
    if flag in ['n', 'vn', 'v']:  # 名词、名动词、动词
        word_vector = model[word] if word in model else np.zeros(model.vector_size)
        # 这里可以添加将词向量和词性信息融合的逻辑
        print(f"{word}({flag}): {word_vector}")

# 注意：实际应用中，步骤5的信息融合策略会根据具体任务需求进行设计。