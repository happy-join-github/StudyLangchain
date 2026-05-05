from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage,AIMessage,ToolMessage,SystemMessage
from langgraph.checkpoint.memory import InMemorySaver

from app.core.config import OPENAI_API_KEY,OPENAI_BASE_URL


def init_model():
    # 初始化两个模型一个聊天模型用于搜索，一个多模态大模型用于识别。
    chatModel = init_chat_model(model="",model_provider="openai",baseurl=OPENAI_BASE_URL,apikey=OPENAI_API_KEY)

    pass