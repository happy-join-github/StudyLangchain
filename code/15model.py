# 初始化模型
# 自定义模型供应商
from langchain.chat_models import init_chat_model

from config.config import codeConfig

import os
import json

###################数据配置#####################################
filebase = codeConfig.dataPath
api_key = codeConfig.api_key[0]
base_url = codeConfig.modelBaseUrl[0]
modelname = codeConfig.model[0]


###################模型初始化#####################################
model = init_chat_model(model=modelname,model_provider="openai",base_url=base_url,api_key=api_key)

###############################阻塞响应###############################
def invoke_explain(model,filebase):
    invoke_response = model.invoke("你好，你是谁？")
    # print(invoke_response)
    # 将 AIMessage 转为字典（可序列化）
    message_dict = invoke_response.dict()

    # 保存数据
    json.dump(message_dict, open(os.path.join(filebase, "invoke_response.json"), 'w', encoding='utf-8'), indent=4, ensure_ascii=False)

###############################流式传输###############################
stream_response = model.stream("你是谁？")
chunks_data = []
for chunk in stream_response:
    print(chunk)
    chunks_data.append(chunk.dict())

json.dump(chunks_data, open(os.path.join(filebase, "stream_chunks.json"), "w", encoding="utf-8"), indent=4, ensure_ascii=False)

###############################abc###############################