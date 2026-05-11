from pydantic import BaseModel,Field
from typing import Literal

class Resource(BaseModel):
    id:int = Field(description="资源ID")
    sourceType: Literal['image','video','audio'] = Field(default="image",description="资源类型")
    content:str = Field(description="资源内容")

    