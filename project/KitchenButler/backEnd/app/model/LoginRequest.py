from pydantic import BaseModel, Field,field_validator
class UserModel(BaseModel):
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码（至少6位）")

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError('密码长度至少为6位')
        # 可选：增加更多规则，如必须包含数字/字母等
        return v