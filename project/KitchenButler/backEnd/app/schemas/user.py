from typing import Optional
from pydantic import BaseModel, Field, EmailStr, field_validator
import re

class UserModel(BaseModel):
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码（至少6位）")
    nickname: Optional[str] = Field(None, description="昵称")
    phone: Optional[str] = Field(None, description="手机号")
    email: Optional[EmailStr] = Field(None, description="邮箱")

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError('密码长度至少为6位')
        # 可选：增加更多规则，如必须包含数字/字母等
        return v

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not re.match(r'^1[3-9]\d{9}$', v):
                raise ValueError('手机号格式不正确，应为11位中国大陆手机号')
        return v