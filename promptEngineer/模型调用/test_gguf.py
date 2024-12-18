
# from ctransformers import AutoModelForCausalLM
# from transformers import AutoTokenizer, pipeline
from transformers import AutoModelForCausalLM, AutoTokenizer
device = "cuda" # the device to load the model onto

model_id = "/home/useradmin/LXQ/Qwen2.5-Coder-14B-GGUF"  # 模型标识符
gguf_file = "Qwen2.5-Coder-14B-Instruct-Q5_K_M-LOT.gguf"  # GGUF文件名

# 加载分词器和模型
tokenizer = AutoTokenizer.from_pretrained(model_id, gguf_file=gguf_file, clean_up_tokenization_spaces=True)
model = AutoModelForCausalLM.from_pretrained(model_id, gguf_file=gguf_file).to(device)

prompt = "Give me a short introduction to large language model."
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt},
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
)
model_inputs = tokenizer([text], return_tensors="pt").to(device)

generated_ids = model.generate(
    model_inputs.input_ids,
    max_new_tokens=512,
)
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
print(response)