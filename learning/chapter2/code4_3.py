# ReAct 提示词模板
REACT_PROMPT_TEMPLATE = """
请注意，你是一个有能力调用外部工具的智能助手。

可用工具如下:
{tools}

请严格按照以下格式进行回应:

Thought: 你的思考过程，用于分析问题、拆解任务和规划下一步行动。
Action: 你决定采取的行动，必须是以下格式之一:
- `{{tool_name}}[{{tool_input}}]`:调用一个可用工具。
- `Finish[最终答案]`:当你认为已经获得最终答案时。
- 当你收集到足够的信息，能够回答用户的最终问题时，你必须在Action:字段后使用 Finish[最终答案] 来输出最终答案。

现在，请开始解决以下问题:
Question: {question}
History: {history}
"""

from code4_2 import ToolExecutor
from code4_1 import HelloAgentsLLM
from code4_2 import search, calculator
import re

class ReActAgent:
    """
    接收用户输入的问题，格式化prompt消息，调用工具执行器，整合历史记录，输出最终答案。
    """
    def __init__(self, llm_client: HelloAgentsLLM, tool_executor: ToolExecutor, max_steps: int = 5):
        self.llm_client = llm_client
        self.tool_executor = tool_executor
        self.max_steps = max_steps
        self.history = []

    def run(self, question: str):
        """
        运行ReAct Agent
        """
        self.history = []   # 清空历史消息
        current_step = 0

        while current_step < self.max_steps:
            current_step += 1
            print(f"---当前步骤: {current_step}---")

            # 1. 格式化提示词
            tools = self.tool_executor.getAvailableTools()
            history = '\n'.join(self.history)
            prompt = REACT_PROMPT_TEMPLATE.format(question=question, tools=tools, history=history)

            # 2. 调用大模型
            message = [{'role': 'user', 'content': prompt}]
            result = self.llm_client.think(messages=message)
            self.history.append(result)

            if not result:
                print('错误：LLM未能返回有效响应')
                break

            # 3. 解析LLM输出
            thought, action = self._parse_output(result)
            if thought:
                print(f"思考: {thought}")
            if not action:
                print(f"警告：未能解析出有效的Action，流程终止")
                break

            # 4. 执行工具
            # 4.1 finish
            if action.startswith("Finish") or action.startswith("`Finish"):
                # 提取答案并结束
                final_answer = re.match(r"Finish\[(.*)\]", action).group(1)
                print(f"最终答案: {final_answer}")
                break

            tool_name, tool_input = self._parse_action(action)
            if not tool_name or not tool_input:
                # 处理无效的Action格式
                continue

            print(f"Action:\n工具: {tool_name}, 输入: {tool_input}")

            # 4.2 调用工具
            tool = self.tool_executor.getTool(tool_name)
            if not tool:
                observation = f"工具 {tool_name} 不存在"
            else:
                observation = tool(tool_input)

            # 5. 工具调用后的观察
            print(f"Observation: {observation}")
            self.history.append(f"Action: {action}")
            self.history.append(f"Observation: {observation}")

        # 本次问题结束
        print("\n---当前步骤: 结束---")
        return None

    def _parse_output(self, text: str):
        """
        解析LLM输出
        """
        # Thought: 匹配到 Action: 或文本末尾
        thought_match = re.search(r"Thought:\s*(.*?)(?=\nAction:|$)", text, re.DOTALL)
        # Action: 匹配到文本末尾
        action_match = re.search(r"Action:\s*(.*?)$", text, re.DOTALL)

        thought = thought_match.group(1).strip() if thought_match else None
        action = action_match.group(1).strip() if action_match else None

        return thought, action
    
    def _parse_action(self, action_text: str):
        """解析Action字符串，提取工具名和输入
        """
        match = re.match(r"(\w+)\[(.*)\]", action_text, re.DOTALL)
        if match:
            return match.group(1), match.group(2)
        return None, None

if __name__ == '__main__':
    llm_client = HelloAgentsLLM()
    tool_executor = ToolExecutor()
    tool_executor.registerTool("search", "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。", search)
    tool_executor.registerTool("calculator", "一个简单的计算器工具。当你需要计算数学表达式或算式时，应使用此工具。", calculator)
    agent = ReActAgent(llm_client=llm_client, tool_executor=tool_executor)
    agent.run("华为最新手机型号及主要卖点？")
    agent.run("(100+12)×10÷3=?")