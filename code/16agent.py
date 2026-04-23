from langchain.agents import create_agent
from config.config import Config
from langchain.chat_models import init_chat_model

modelConfig = Config().defaultModel
model = init_chat_model(model=modelConfig['model'],model_provider="openai",base_url=modelConfig['baseurl'],api_key=modelConfig['api_key'])
agent = create_agent(model=model)

# 调用智能体
invoke_data = {"messages":[{"role":"user","content":"你好"}]}
invoke_response = agent.invoke(invoke_data)
print(invoke_response.content)
stream_data = {"message":[{"role":'user',"content":"你是谁"}]}
stream_resopnse = agent.stream(stream_data,stream_mode="messages")

for token,meta_data in stream_resopnse:
    print(token.content,end="",flush=True)
