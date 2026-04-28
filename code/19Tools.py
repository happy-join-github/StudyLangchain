#####初始化操作###########
# 模型key baseurl,初始化
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage,ToolMessage,AIMessage,SystemMessage
from config.config import codeConfig

###########模型初始化#############
# 多模态大模型
MultimodalModel = codeConfig.MultimodalModel
model_name = MultimodalModel['model']
model_baseurl = MultimodalModel['baseurl']
model_key = MultimodalModel['api_key']

model = init_chat_model(model_name,model_provider='openai',base_url=model_baseurl,api_key=model_key)


################工具####################
from langchain_core.tools import tool
from pydantic import BaseModel,Field
from typing import Literal,Tuple
import math
# 工具名称
# 工具作用
# 工具参数

# 添加装饰器(name,descript)
@tool
def squareRoot(x:float):
    """Calculate the square root of a number
    Args:
    x: a num
    """
    return math.sqrt(x)

class weatherInput(BaseModel):
    position:str|Tuple[float,float] = Field(default="beijing",description="位置")
    units:Literal['fahrenheit',"celsius"] = Field(default="celsius",description="温度单位")
    inclue_forecast:bool = Field(False,description="Include 5-day forecast")

@tool
def weather(position:str|Tuple[float,float],units:Literal['fahrenheit',"celsius"]="celsius",inclue_forecast:bool=False):
    """get weather of position"""
    pass
    
@tool(args_schema=weatherInput)
def weather1(position,units,inclue_forecast):
    """get weather of position"""
    pass




##################创建agent#############
# 'weather1','weather',
agent = create_agent(model,tools=[squareRoot])


###############调用agent###############
response = agent.invoke({"messages":[HumanMessage("25的平方根是多少")]})
final_answer = response["messages"][-1].content
print(final_answer)
# for message in response.messages:
#     print(message.prety_print())