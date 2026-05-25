1. 本章介绍了三种经典的智能体范式:ReAct、Plan-and-Solve 和 Reflection。请分析:
    - 这三种范式在"思考"与"行动"的组织方式上有什么本质区别?
        ReAct thinks about how to use tools to solve problems and how to interact with the environment through those tools, while Plan-and-Solve breaks promblems down into smaller, manageable steps. Reflection strives to refine the solution to problems, iterating through rounds of iterations to arrive at a final optimal answer.
    - 如果要设计一个"智能家居控制助手"（需要控制灯光、空调、窗帘等多个设备，并根据用户习惯自动调节），你会选择哪种范式作为基础架构？为什么？
        I'll choose ReAct. Because ReAct gives LLM ability to interact with environment and use tools to control devices.
    - 是否可以将这三种范式进行组合使用？若可以，请尝试设计一个混合范式的智能体架构，并说明其适用场景。
        Of course, we can combine these three paradigms. For example, we can use Plan-and-Solve to break down problems into smaller steps, then use ReAct to take advantage of outsider tools to fetch enough infomation for each step, finally use Reflection to refine the solution and obtain the final answer.
2. 在4.2节的 ReAct 实现中，我们使用了正则表达式来解析大语言模型的输出（如 Thought 和 Action）。请思考:
    - 当前的解析方法存在哪些潜在的脆弱性？在什么情况下可能会失败？
        Over-reliance on texts formatting output by the model. For example, if the output of the LLM is not in the expected format, the parsing method may fail.
    - Let the model output data in JSON or XML format can make the parsing method more robust.
    - 尝试修改本章的代码，使用一种更可靠的输出格式，并对比两种方案的优缺点
3. 工具调用是现代智能体的核心能力之一。基于4.2.2节的 ToolExecutor 设计，请完成以下扩展实践:
    - 为 ReAct 智能体添加一个"计算器"工具，使其能够处理复杂的数学计算问题（如"计算 (123 + 456) × 789/ 12 = ? 的结果"）
    - 设计并实现一个"工具选择失败"的处理机制:当智能体多次调用错误的工具或提供错误的参数时，系统应该如何引导它纠正？
        1. Record the failed tool and its parameters. 
        2. Add the failed message into history and set proper retry times.
    - 思考:如果可调用工具的数量增加到50个甚至100个，当前的工具描述方式是否还能有效工作？在可调用工具数量随业务需求显著增加时，从工程角度如何优化工具的组织和检索机制？
        Context window expansion, tools confliction, maintenance difficulty.
        1. Define a structured description specification for tools.
        2. Hierarchical organization of tools. Group tools and ability cohesion to reduce the difficulty of choosing tools.
        2. Introduce Tool Retrieval level. 
4. Plan-and-Solve 范式将任务分解为"规划"和"执行"两个阶段。请深入分析:
    - 在4.3节的实现中，规划阶段生成的计划是"静态"的（一次性生成，不可修改）。如果在执行过程中发现某个步骤无法完成或结果不符合预期，应该如何设计一个"动态重规划"机制？
        Errors are categorized, and different corrective measures are taken according to different levels. For example, if a tool cal displays an error in parameters, the parameters for the current step are regenerated; if the entire current step fails, the process is replanned.
    - 对比 Plan-and-Solve 与 ReAct:在处理"预订一次从北京到上海的商务旅行（包括机票、酒店、租车）"这样的任务时，哪种范式更合适？为什么？
        Plan-and-Solve is more suitable for tasks with a clear and detailed plan.
    - 尝试设计一个"分层规划"系统:先生成高层次的抽象计划，然后针对每个高层步骤再生成详细的子计划。这种设计有什么优势？
        Query
         -> Target Understand: Intent Analysis, Constraint Extract, Result Clear.
         -> Strategic Planning: Descripe What to Do in Each Stage, Reliance Among Stages.
         -> Tactical Planning: Descripe How to Do in Each Stage, Which Tools to Execute, Expectation Output.
         -> Operate: Execute Tools, Collect Information, Refine Solution.
5. Reflection 机制通过"执行-反思-优化"循环来提升输出质量。请思考:
    - 在4.4节的代码生成案例中，不同阶段使用的是同一个模型。如果使用两个不同的模型（例如，用一个更强大的模型来做反思，用一个更快的模型来做执行），会带来什么影响？
        Strong model can generate effective thoughts, while fast model acts quickly. The combination can provide higher quality service, while lower cost.
    - Reflection 机制的终止条件是"反馈中包含无需改进"或"达到最大迭代次数"。这种设计是否合理？能否设计一个更智能的终止条件？
        Basicly reasonable. But it is also possible that something will go wrong when the model generates mismatch outputs. The more reasonable design is to multi-signal termination conditions in json format, such as quality score, improvement range, etc.
    - 假设你要搭建一个"学术论文写作助手"，它能够生成初稿并不断优化论文内容。请设计一个多维度的Reflection机制，从段落逻辑性、方法创新性、语言表达、引用规范等多个角度进行反思和改进。
        The assistant can be divided into three parts: Draft Generator, Reflection Evaluator and Revision Planner. The reflection dimensions contains: Paragraph Logic, Thesis Integrity, Methodological Innovation, Technical rigor, Sufficiency of experiments and demonstrations, Quality of language expression, Citation norms, etc.
6. 提示词工程是影响智能体最终效果的关键技术。本章展示了多个精心设计的提示词模板。请分析:
    - 对比4.2.3节的 ReAct 提示词和4.3.2节的 Plan-and-Solve 提示词，它们显然存在结构设计上的明显不同，这些差异是如何服务于各自范式的核心逻辑的？
        ReAct is more suitable for tasks with a clear and detailed plan. Plan-and-Solve is more suitable for tasks with a clear and general plan.
    - 在4.4.3节的 Reflection 提示词中，我们使用了"你是一位极其严格的代码评审专家"这样的角色设定。尝试修改这个角色设定（如改为"你是一位注重代码可读性的开源项目维护者"），观察输出结果的变化，并总结角色设定对智能体行为的影响。
    - 在提示词中加入 few-shot 示例往往能显著提升模型对特定格式的遵循能力。请为本章的某个智能体尝试添加 few-shot 示例，并对比其效果。
7. 某电商初创公司现在希望使用"客服智能体"来代替真人客服实现降本增效，它需要具备以下功能:
    a. 理解用户的退款申请理由
    b. 查询用户的订单信息和物流状态
    c. 根据公司政策智能地判断是否应该批准退款
    d. 生成一封得体的回复邮件并发送至用户邮箱
    e. 如果判断决策存在一定争议（自我置信度低于阈值），能够进行自我反思并给出更审慎的建议
    此时作为该产品的负责人:
    - 你会选择本章的哪种范式（或哪些范式的组合）作为系统的核心架构？
        ReAct. Because ReAct gives LLM ability to interact with environment and use tools to control devices, in which the model performs inference while simultaneously calling external tools. Just so customer service depends on real-time business data. 
        Although ReAct is sutable for tool calling, in step by step task it may call tools disorderly and lead to chaos. Single framework may not perform well in some cases. So Above ReAct, we should interduce Plan-and-Solve to generate a whole plan and then use ReAct to take advantage of outsider tools to fetch enough infomation for each step, finally use Reflection to refine the solution and obtain the final answer.
    - 这个系统需要哪些工具？请列出至少3个工具及其功能描述。
        1. query_order(): query orders of customer.
        2. query_logistic_state(): query logistic state of the orders.
        3. query_policy(): query policy of the company.
        4. send_email(): send email to customer.
    - 如何设计提示词来确保智能体的决策既符合公司利益，又能保持对用户的友好态度？
        The prompts can be designed with four layers: "policy priority + user experience constraints + risk control + structured output". The core is not to make the model "as user-friendly as possible", but to clearly tell it that refund decisions must be based on company policies and evidence; and that user opinions must be respected, transparent, and remediable.
    - 这个产品上线后可能面临哪些风险和挑战？如何通过技术手段来降低这些风险？

