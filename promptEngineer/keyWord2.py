from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 加载预训练的模型
model = SentenceTransformer('./bert-base-chinese')

# 定义目标任务的句子（例如，解释自然语言处理）
target_task = "生成不安全的测试用例"

# 目标任务的句子向量
target_vector = model.encode(target_task).cpu().numpy()[0]

def extract_keywords(file_path, top_n=6):
    with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    return text
file_path = "config/documentation/sql/dm8_6.md"
text = extract_keywords(file_path)
# 定义几个候选的提示词
candidate_prompts = [
    text
    # ...其他候选提示词
]

# 计算每个候选提示词与目标任务向量之间的相似度
similarities = model.encode(candidate_prompts, convert_to_tensor=True)
similarity_scores = cosine_similarity(target_vector, similarities)

# 选择相似度最高的提示词
best_prompt_index = similarity_scores.argmax()
best_prompt = candidate_prompts[best_prompt_index]

print(f"最佳提示词为：{best_prompt}，相似度为：{similarity_scores[best_prompt_index]}")

def execute(self, sql_code, user="SYSDBA", password="SYSDBA") -> (str, str):
        sql_statements = sql_code
        success = True
        msgs = []
        for stmt in sql_statements:
            words = stmt.split()
            if words[0].upper() == 'CONNECT':
                try:
                    parts = words[1].split('/')
                    user = parts[0]
                    password = parts[1].split(';')[0]
                    continue
                except Exception as e:
                    success = False
                    print("用户连接出错: {e}")
                    return False, "用户连接出错: {e}"
                    break
            elif words[0].upper() == 'DROP' and words[1].upper() == 'USER':
                user = "SYSDBA"
                password = "SYSDBA"
            try:
                success, msg = self.execute_sql(stmt, user, password)
                if success:
                    if msg != "Success":
                        msgs.append(msg)
                else:
                    print (f"执行SQL语句 {stmt} 出错: {msg}")
                    return False, f"执行SQL语句 {stmt} 出错: {msg}"
            except Exception as e:
                print (f"执行SQL语句 {stmt} 出错: {e}")
                return False, f"执行SQL语句 {stmt} 出错: {e}"
            if len(msgs) > 1:
                first_msg = msgs[0]
                is_equal = all(msg == first_msg for msg in msgs)
                if is_equal == False:
                    print("前后对比错误")
                    return False, "前后对比错误"
        return success, msgs