import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict

# load env variables
load_dotenv("/Users/qilongzhong/Documents/helloagent/hello-agents/learning/.venv")

class HelloAgentsLLM:
    """
    用于调用任何兼容OpenAI接口的服务，并默认使用流式响应
    """
    def __init__(self, model: str = None, apiKey: str = None, baseUrl: str = None, timeout: int = None) -> None:
        """
        初始化客户端
        """
        self.model = model or os.getenv("LLM_MODEL_ID")
        self.apiKey = apiKey or os.getenv("LLM_API_KEY")
        self.baseUrl = baseUrl or os.getenv("LLM_BASE_URL")
        self.timeout = timeout or int(os.getenv("OPENAI_TIMEOUT", 60))
        if not all([self.model, self.apiKey, self.baseUrl]):
            raise ValueError("模型ID、API密钥和服务地址必须被提供或在.env文件中定义。")

        self.client = OpenAI(api_key=self.apiKey, base_url=self.baseUrl, timeout=self.timeout)

    def think(self, messages: List[Dict[str, str]], temperature: float = 0) -> str:
        """
        调用LLM进行思考，并返回响应
        """
        print(f"🧠 正在调用 {self.model} 模型...")
        try:
            response = self.client.chat.completions.create(
                model = self.model,
                messages = messages,
                temperature = temperature,
                stream = True
            )
            # 处理流式响应
            print("✅ 大语言模型响应成功:")
            collected_content = []
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                print(content, end="", flush=True)
                collected_content.append(content)
            # 打印空行
            print()
            return "".join(collected_content)
        except Exception as e:
            print(f"❌ 调用LLM API失败: {e}")
            return None
        
# 使用示例
if __name__ == "__main__":
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant that writes Python code."},
            {"role": "user", "content": "写一个快速排序算法"},
        ]
        print("---调用LLM---")
        llmClient = HelloAgentsLLM()
        responseText = llmClient.think(messages=messages)
        if responseText:
            print("\n\n---完整模型响应---")
            print(responseText)
    except ValueError as e:
        print(e)


