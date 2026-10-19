from urllib import response

from dotenv import load_dotenv
from hello_agents import HelloAgentsLLM, ToolRegistry
from hello_agents.tools import CalculatorTool
from my_simple_agent import MySimpleAgent

# 加载环境变量
load_dotenv()

# 创建LLM实例
llm = HelloAgentsLLM()

# 测试1： 基础对话Agent(无工具)
print("=== 测试1: 基础对话")
basic_agent = MySimpleAgent(
    name="基础助手",
    llm=llm,
    system_prompt="你是一个友好的AI助手，请用简洁明了的方式回答问题"
)
response1 = basic_agent.run("你好，请介绍下自己")
print(f"基础对话响应：{response1}\n")

#测试2： 带工具的Agent
