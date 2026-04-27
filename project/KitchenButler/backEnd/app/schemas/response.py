from pydantic import BaseModel,Field

class Response(BaseModel):
    status:int = Field(200,description="状态码")
    message:str = Field("成功",description="信息")
    data:object = Field(default={},description="数据")