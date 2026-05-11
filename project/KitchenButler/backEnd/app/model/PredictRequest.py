from pydantic import BaseModel, Field

class PredictRequest(BaseModel):
    prompt: str = Field(..., description="用户提问")
    image_path: str = Field(..., description="图片路径")