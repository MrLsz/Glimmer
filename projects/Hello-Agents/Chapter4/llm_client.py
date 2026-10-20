import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict

# 加载 .env 文件中的环境变量
load_dotenv()

class HelloAgentsLLM:
    def __init__(self, model: str = None, apiKey: str = None, baseUrl: str = None, timeout: int = None):
        """
        初始化客户端。优先使用传入参数，如果未提供，则从环境变量加载。
        """
        # 同时兼容两套命名：本书的 LLM_* 与常见的 OPENAI_*
        self.model = model or os.getenv("LLM_MODEL_ID") or os.getenv("OPENAI_MODEL")
        self.apiKey = apiKey or os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.baseUrl = baseUrl or os.getenv("LLM_BASE_URL") or os.getenv("OPENAI_BASE_URL")
        self.timeout = timeout or int(os.getenv("LLM_TIMEOUT") or os.getenv("OPENAI_TIMEOUT") or 60)

        if not all([self.model, self.apiKey, self.baseUrl]):
            raise ValueError(
                "请确保提供了模型名称、API Key 和 Base URL。\n"
                "在 Chapter4 目录下创建 .env，内容形如：\n"
                '  LLM_MODEL_ID="Qwen/Qwen3.5-35B-A3B"\n'
                '  LLM_API_KEY="ms-xxxx"\n'
                '  LLM_BASE_URL="https://api-inference.modelscope.cn/v1/"'
            )
        
        self.client = OpenAI(api_key=self.apiKey, base_url=self.baseUrl, timeout=self.timeout)

    def think(self, messages: List[Dict[str, str]], temperature: float = 0) -> str:
        """
        调用大语言模型进行思考，并返回其响应
        """

        print(f"正在调用 {self.model} 模型进行思考...")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True,
            )

            # 处理流式响应
            print("大语言模型响应成功")
            collected_content = []
            for chunk in response:
                if not chunk.choices:
                    continue
                # openai>=1.0 的 delta 是对象而非字典，不能用 .get()
                delta = chunk.choices[0].delta
                content = getattr(delta, "content", None) or ""
                print(content, end="", flush=True)
                collected_content.append(content)

            print() #在流式输出结束后换行
            return "".join(collected_content)
        except Exception as e:
            print(f"调用大语言模型时发生错误: {e}")
            return ""

# --- 客户端使用示例 ---
if __name__ == '__main__':
    try:
        llmClient = HelloAgentsLLM()
        
        exampleMessages = [
            {"role": "system", "content": "You are a helpful assistant that writes Python code."},
            {"role": "user", "content": "写一个快速排序算法"}
        ]
        
        print("--- 调用LLM ---")
        responseText = llmClient.think(exampleMessages)
        if responseText:
            print("\n\n--- 完整模型响应 ---")
            print(responseText)

    except ValueError as e:
        print(e)      
        