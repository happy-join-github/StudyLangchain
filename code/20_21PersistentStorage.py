#####初始化操作###########
# 模型key baseurl,初始化
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage,ToolMessage,AIMessage,SystemMessage
from config.config import codeConfig

###################数据配置#####################################
api_key = codeConfig.api_key[0]
base_url = codeConfig.modelBaseUrl[0]
modelname = codeConfig.model[0]

###################模型初始化#####################################
model = init_chat_model(model=modelname,model_provider="openai",base_url=base_url,api_key=api_key)


#############################智能体初始化#########################
from langgraph.checkpoint.memory import InMemorySaver

# 内存保存记忆
# agent = create_agent(model,tools=[],system_prompt="",checkpointer=InMemorySaver())
# config = {'configurable':{"thread_id":"1"}}
# agent.stream({"messages":[HumanMessage("你好今天潍坊的天气怎么样？")]},config=config)



##########使用数据库保存############
################# 使用postgresql##############
# langgraph-checkpoint-postgre



############## 使用sql############
# langgraph-checkpoint-sqlite

import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
# 链接数据库
connection = sqlite3.connect("data/checkpoints.db",check_same_thread=False)
# 初始化
checkpointer = SqliteSaver(connection)
# 自动建表
checkpointer.setup()
# 指定
agent = create_agent(model,tools=[],checkpointer=checkpointer)
config = {'configurable':{"thread_id":"1"}}
agent.stream({"messages":[HumanMessage("你好今天潍坊的天气怎么样？")]},config=config)
