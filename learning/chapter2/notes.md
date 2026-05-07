# Environment And basic tool
```python
pip install openai python-dotenv
```
1. Config apikey: `APIKEY, MODEL_ID, BASEURL`
2. Core codes: 
    - `self.client = OpenAI(api_key=APIKEY, base_url=BASEURL, timeout=timeout)`
    - Stream Type: `response = self.client.chat.completions.create(model=self.model, messages=messages, temperature=temperature, stream=True)`
    - Collect chunks: `for chunk in response: print(chunk.choices[0].delta.content or "")`

# ReAct
Means Reasoning and Acting. The ReAct framework recognizes that thinking and acting are Complementary.
- Thought: Reasoning. The thought is the process of reasoning, planning, and decision-making.
- Action: Acting. Generally, the action is a call of an external tool, such as search for something.
- Observation: Observation is the process of gathering information from the environment and tools.
## Tool
A good tool should contain below core elements:
1. Name: a unique identifier.
2. Description: a clear NL description of the tool.
3. Execution Logic: the logic of the tool, including the input and output.
## Tool Executor
Unified manager registers and schedules tools.
## ReAct Prompt Example
- Character Definition
- tools
- Thought / Action
- {question} / {history}
```
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
```

# Features, limitations and debug tricks of ReAct
1. Main features:
    - High Explainability
    - DP and Self-Correction
    - Tool Collaboration Capabilities

2. Limitations:
    - Strong Dependency on LLM
    - Efficiency of Execution
    - Vulnerability of Prompt
    - Might Fall into Local Optimum

# Plan-and-Solve
1. Planning Phase
    - prompt: Character definition; Task Description; Format Constraintion
2. Solving Phase
3. Executor And Status Management
    - Executor not only executes every step in plan, but also manages the status of the plan. It records the results of every step, and provides them to the following step.
    - prompt: Original question; Entire plan; History steps and results; Current step.

# Reflection
Reflection introduces a post-hoc self-correction mechanism for agents. Core workflow can be summarized by three concise loop: execute, reflect, and optimize.
## Cases Configuration and Memory Design
