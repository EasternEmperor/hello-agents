"""
A good tool should contain below core elements:
1. Name: a unique identifier.
2. Description: a clear NL description of the tool.
3. Execution Logic: the logic of the tool, including the input and output.
"""

from serpapi import Client as SerpApiClient
import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict

# load env variables
load_dotenv("/Users/qilongzhong/Documents/helloagent/hello-agents/learning/.venv")


def search(query: str) -> str:
    """
    一个基于SERPAPI的搜索工具
    它会智能地解析搜索结果，优先返回直接答案或知识图谱信息
    """
    print(f'🔍 正在执行 [SerPapi] 网页搜索: {query}')
    try:
        SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")
        if not SERPAPI_KEY:
            raise ValueError("SERPAPI_KEY is not set")
        
        params = {
            "engine": "google",
            "q": query,
            "gl": "cn",     # 国家代码
            "hl": "zh-cn"   # 语言代码
        }

        client = SerpApiClient(api_key=SERPAPI_KEY)
        results = client.search(params)

        # 智能解析：优先寻找最直接的答案
        if "answer_box_list" in results:
            return "\n".join(results["answer_box_list"])
        if "answer_box" in results and "answer" in results["answer_box"]:
            return results["answer_box"]["answer"]
        if "knowledge_graph" in results and "description" in results["knowledge_graph"]:
            return results["knowledge_graph"]["description"]
        if "organic_results" in results and len(results["organic_results"]) > 0:
            # 没有直接答案，返回前三个有机结果的搜索
            snippets = [
                f'[{i + 1}] {res.get('title', '')}\n{res.get('snippet', '')}'
                for i, res in enumerate(results["organic_results"][:3])
            ]
            return "\n\n".join(snippets)
        
        return "未找到相关结果"
    except Exception as e:
        return f"搜索失败：{e}"
    
import re, ast
def calculator(query: str) -> str:
    """
    一个简单的计算器工具，如(123 + 456) × 789/ 12 = ?
    """
    print(f"🧮 正在计算算式结果: {query}")
    try:
        # 1. 解析算式
        # 查找 = 号
        formula = re.search(r'\s*(.*?)(?==)', query)
        print(f"提取出算式: {formula}")
        if not formula:
            return "未找到算式"
        formula = formula.group(1).strip()
        # 2. 替换算式中运算符：✖️->*, ➗->/
        formula = formula.replace("×", "*").replace("÷", "/")
        # 3. 计算结果
        print(f"计算公式: {formula}")
        result = eval(formula)
        return str(result)
    except Exception as e:
        return f"计算失败：{e}"

from typing import Dict, Any

class ToolExecutor:
    """
    一个工具执行器，负责管理和执行工具
    """
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}

    def registerTool(self, name: str, description: str, func: callable):
        """
        注册一个工具
        """
        if name in self.tools:
            print(f"Warning: 工具 '{name}' 已存在，将被覆盖")

        self.tools[name] = {"description": description, "func": func}
        print(f"工具 '{name}' 注册成功")

    def getTool(self, name: str) -> callable:
        """
        根据名称获取一个工具
        """
        return self.tools.get(name, {}).get("func")
    
    def getAvailableTools(self) -> str:
        """
        获取可用工具列表
        """
        return "\n".join(f"* {name}: {tool['description']}" for name, tool in self.tools.items())
    
if __name__ == "__main__":
    # 1. 初始化工具执行器
    executor = ToolExecutor()

    # 2. 注册工具
    executor.registerTool("search", "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。", search)
    executor.registerTool("calculator", "一个简单的计算器工具，如(123 + 456) × 789/ 12 = ?", calculator)

    # 3. 打印可用工具
    print("\n可用工具列表:")
    print(executor.getAvailableTools())

    # 4. 智能体的Action调用
    # 4.1 search工具调用
    print("\n--- 执行 Action: Search['英伟达最新的GPU型号是什么'] ---")
    tool_name = "search"
    tool_input = "英伟达最新的GPU型号是什么"

    tool_function = executor.getTool(tool_name)
    if tool_function:
        observation = tool_function(tool_input)
        print("--- 观察 ---")
        print(observation)
    else:
        print(f"工具 '{tool_name}' 未注册")

    # 4.2 calculator工具调用
    print("\n--- 执行 Action: Calculator['(123 + 456) × 789/ 12 = ?'] ---")
    tool_name = "calculator"
    tool_input = "(123 + 456) × 789/ 12 = ?"

    tool_function = executor.getTool(tool_name)
    if tool_function:
        observation = tool_function(tool_input)
        print("--- 观察 ---")
        print(observation)
    else:
        print(f"工具 '{tool_name}' 未注册")
