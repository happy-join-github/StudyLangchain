from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage,ToolMessage
from langchain.tools import tool
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from config.config import codeConfig
####################参数初始化######################
multimodalModelName = codeConfig.multimodalModel["model"]
multimodalModelApiKey = codeConfig.multimodalModel['api_key']
multimodalModelUrl = codeConfig.multimodalModel['baseurl']

baseName = codeConfig.defaultModel['model']
baseApiKey = codeConfig.defaultModel['api_key']
baseUrl = codeConfig.defaultModel['baseurl']
# 模型初始化
multimodalModel = init_chat_model(model=multimodalModelName,model_provider='openai',api_key=multimodalModelApiKey,base_url = multimodalModelUrl)
baseModel = init_chat_model(model=baseName,model_provider='openai',api_key=baseApiKey,base_url=baseUrl)

# 记忆初始化
dbFilePath = "code/data/22.db"
config = {"configurable":{"thread_id":"abc123"}}
connection = sqlite3.connect(dbFilePath,check_same_thread=False)
checkpointer = SqliteSaver(connection)
checkpointer.setup()
# 记忆管理 信息摘要
# tigger "message"按照信息条数   "fraction"按照百分比  "tokens"按照token
# 当上下文达到85%对上下文进行信息摘要，保留30%的信息。
# summary = SummarizationMiddleware(model=baseModel,trigger=("fraction",0.85),keep=("fanction",0.3))
summary = SummarizationMiddleware(baseModel,trigger=("messages",3),keep=("messages", 1))

# ###########################创建agent智能体##########################
agent = create_agent(multimodalModel,tools=[],middleware=[summary],checkpointer=checkpointer)


message = [HumanMessage("你好，我是小王")]
message2 = [HumanMessage("我最喜欢的食物是米饭")]
message3 = [HumanMessage("我最喜欢的水果是苹果")]

result = agent.invoke({"messages":message},config=config)
# print(result)

result2 = agent.invoke({"messages":message2},config=config)
# print(result2)

result3 = agent.invoke({"messages":message3},config=config)
# print(result3)

result4 = agent.invoke({'messages':[HumanMessage("你好记得我是谁吗")]},config=config)
print(result4)