import os
class Config:
    def __init__(self):
        # 模型配置
        self.modelBaseUrl = ['https://dashscope.aliyuncs.com/compatible-mode/v1']
        self.model = ['qwen-plus-2025-07-28',"qwen3.5-omni-plus"]
        self.api_key = ['']
        self.defaultModel = {"baseurl":self.modelBaseUrl[0],"model":self.model[0],"api_key":self.api_key[0]} 
        self.MultimodalModel = {"baseurl":self.modelBaseUrl[0],"model":self.model[1],"api_key":self.api_key[1]}
        # dataPath
        self.dataPath = os.path.join(os.getcwd(),"code","data")


codeConfig = Config()
