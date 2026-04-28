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
###### 提示词优化####

# 1. 给ai一些角色和指令提示使用markdown格式或xml格式
prompt="""
**身份** :
你是一个高级的软件架构工程师，请帮用户解决相对应的架构问题。
**指令** :
1. 架构问题，请分析问题并给出架构图，架构图请使用使用 Mermaid 语法进行绘制。
2. 架构图所对应的代码，请使用python的最佳实践进行编写。
"""

# 2. 文字描述的不了的可以给出基础的示例，让ai进行学习。

prompt = """
#身份
你是一个科幻作家，根据用户的要求创建一个太空之都。
#指令
请务必以JSON格式输出，不要加任何markdown样式。
#示例:
user:月球的首都是什么?
assistant:{
    "name":"月华市(Lunaria)",
    "location":"位于月球正面赤道附近的静海基地遗址之上，依托巨大的穹顶与地下网络建成",
    "vibe":"冷冽、高效、革新",
    "economy":"氦-3能源开采、量子通信枢纽、尖端生物圈农业"
}
"""
################## 结构化输出################
from pydantic import BaseModel
class info(BaseModel):
    name:str
    location:str
    vibe:str
    economy:str
    
agent  = create_agent(model,system_prompt=prompt,response_format=info)