from langchain_core.messages import HumanMessage,SystemMessage,AIMessage,ToolMessage
from langchain.agents import create_agent
from config.config import Config
from langchain.chat_models import init_chat_model


########### 模型初始化############
modelConfig = Config().defaultModel
model = init_chat_model(model=modelConfig['model'],model_provider="openai",base_url=modelConfig['baseurl'],api_key=modelConfig['api_key'])


########## 智能体初始化#############
agent = create_agent(model=model)


########### 文本模型############

######### 多模态模型##########
