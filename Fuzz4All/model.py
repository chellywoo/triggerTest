from typing import List
# import torch
# from transformers import AutoTokenizer, AutoModelForCausalLM
# from diffusers import StoppingCriteriaList, EndOfFunctionCriteria
from openai import OpenAI

# 假设的OpenAI API客户端类
class OpenAI:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def generate(self, prompt: str, parameters: dict) -> List[str]:
        # 这里应该是API调用的代码，我们使用print来模拟
        print(f"Sending request to {self.base_url} with prompt: {prompt} and parameters: {parameters}")
        # 模拟API响应
        return ["API response for prompt: " + prompt]

# 修改后的StarCoder类，使用API客户端
class StarCoder:
    def __init__(self, model_name: str, device: str, eos: List, max_length: int):
        self.device = device
        self.max_length = max_length
        self.eos = eos
        self.api_client = client = OpenAI(
            api_key="sk-67d0f834d27e46eeb819368970a64075", # 如果您没有配置环境变量，请在此处用您的API Key进行替换
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope服务的base_url
        )

    def generate(self, prompt: str, batch_size=1, temperature=1.2) -> List[str]:
        completion = self.api_client.chat.completions.create(
            model="qwen2.5-coder-32b-instruct", # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            messages=[
                {'role': 'system', 'content': '你是Oracle数据库的安全保卫者，你要不断的发现数据库在触发器的使用过程中可能存在的安全漏洞，并给出对应的测试用例。'},
                {'role': 'user', 'content': prompt}
            ],
            temperature = temperature,
            max_token = self.max_length
        )
        output = completion.choices[0].message.content
        return output


def make_model(eos: List, model_name: str, device: str, max_length: int):
    kwargs_for_model = {
        "model_name": model_name,
        "eos": eos,
        "device": device,
        "max_length": max_length,
    }

    print("=== Model Config ===")
    print(f"model_name: {model_name}")
    for k, v in kwargs_for_model.items():
        print(f"{k}: {v}")

    if "starcoder" in model_name.lower():
        model_obj = StarCoder(**kwargs_for_model)
    else:
        # default
        model_obj = StarCoder(**kwargs_for_model)

    model_obj_class_name = model_obj.__class__.__name__
    print(f"model_obj (class name): {model_obj_class_name}")
    print("====================")

    return model_obj

# 示例使用
eos_tokens = ["EOF"]  # 假设的EOF标记
model = make_model(eos=eos_tokens, model_name="starcoder", device="cpu", max_length=3000)
output = model.generate("Hello, world!")
print(output)