from langchain_core.messages import HumanMessage,SystemMessage,AIMessage,ToolMessage
from langchain.agents import create_agent
from config.config import Config
from langchain.chat_models import init_chat_model
from utils.utils import Utils

utils = Utils()
########### 文本模型############
chatConfig = Config().defaultModel
chatModel = init_chat_model(model=chatConfig['model'],model_provider="openai",base_url=chatConfig['baseurl'],api_key=chatConfig['api_key'])

######### 多模态模型##########
MultimodalConfig = Config().MultimodalModel
multimodalModel = init_chat_model(model=MultimodalConfig['model'],model_provider="openai",base_url=MultimodalConfig['baseurl'],api_key=MultimodalConfig['api_key'])

########## 智能体初始化#############
chatAgent = create_agent(model=chatModel)
multimodalAgent = create_agent(model=multimodalModel)

########## 智能体交互#############
# image_path = r"code\data\6.jpg"
# # 读取并编码图片
# with open(image_path, 'rb') as f:
#     image_base64 = base64.b64encode(f.read()).decode('utf-8')
image_base64 = utils.image2base64(r"code\data\8.jpg")
# 多模态消息格式 - 使用列表包含图片和文本
message = HumanMessage(content=[
    {"type": "text", "text": "请描述一下图片内容"},
    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
])

response = multimodalModel.stream(input=[message])
for chunk in response:
    if hasattr(chunk, 'content') and chunk.content:
        print(chunk.content, end="", flush=True)

# multimodalAgent.invoke(messages=[HumanMessage(content="你好，你是谁？")])

