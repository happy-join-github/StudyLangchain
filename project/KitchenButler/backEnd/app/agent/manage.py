from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage,AIMessage,ToolMessage,SystemMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_tavily import TavilySearch
from app.core.config import OPENAI_API_KEY,OPENAI_BASE_URL,tavily_API_KEY,memory_db_path,predictImgModel
import os
import sqlite3

class ModelInIt:
    def __init__(self):
        # 初始化两个模型一个聊天模型一个模型
        self.multimodalModel = init_chat_model(
            model=predictImgModel,
            model_provider="openai",
            # model_kwargs={"base_url": OPENAI_BASE_URL, "api_key": OPENAI_API_KEY}
            base_url = OPENAI_BASE_URL,
            api_key = OPENAI_API_KEY
        )
        # 初始化上下文数据库
        con = sqlite3.connect(memory_db_path,check_same_thread=False)
        checkpoint = SqliteSaver(con)
        # 初始化上下文
        checkpoint.setup()


        sys_prompt = """你是一个识别食材的机器人。根据用户上传的图片，识别出图片中的食材。

**严格遵守以下输出规则：**
1. 只输出食材名称，不要任何其他文字
2. 每行只写一个食材
3. 不要使用任何标记符号（如 -、*、1.、# 等）
4. 不要添加任何分类标题（如"肉类："、"蔬菜类："）
5. 不要添加英文注释（如土豆(Potatoes)）
6. 不要使用 Markdown 格式

**正确的输出示例：**
土豆
茄子
胡萝卜
番茄
五花肉
大蒜
月桂叶

**错误的输出示例（不要这样写）：**
- 土豆
* 茄子
1. 胡萝卜
- **肉类**: 五花肉
土豆 (Potatoes)

请识别图片中的食材，只输出食材名称："""
        multimodalAgent = create_agent(self.multimodalModel, system_prompt=sys_prompt, checkpointer=checkpoint)
    
    
        # 搜索模型tavily
        os.environ["TAVILY_API_KEY"] = tavily_API_KEY
        self.searchModel = TavilySearch(max_result=10,time_range='week')

