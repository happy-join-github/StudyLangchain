from fastapi import APIRouter,Query
from app.model.LoginRequest import UserModel
from app.schemas.response import Response
from app.databases.user import user
from app.utils.response import CommonResponse
import hashlib
router = APIRouter()


@router.get("/login")
async def login(
    username: str = Query(..., alias="username", description="用户名"),
    password: str = Query(..., alias="password", description="密码")
):
    # 手动创建UserModel实例，触发验证
    user_data = UserModel(username=username, password=password)
    token = hashlib.md5(user_data.username.encode("utf-8")).hexdigest()
    if user_data.username == "admin" and user_data.password == "admin123":
        return CommonResponse.success(message="登录成功",data={"token":token})
    else:
        return CommonResponse.error(message="用户名或密码错误",data={"token":""})
    
    # result:Response = user.getUserByUsername(request.username)
    # if not result['data']:
    #     return common_response.error(message="请检查用户名")
    # username = request.username
    # password = request.password
    # un = result['data']['username']
    # pwd = result['data']['password']
    # if pwd!=password and username!=un:
    #     return common_response.error(message="用户名或密码错误")
    # return common_response.success(message="登录成功")


@router.post("/register")
async def register(request: UserModel):
    result: Response = user.getUserByUsername(request.username)
    if result:
        return CommonResponse.error(message="用户名已存在")
    user_data = {
        "username": request.username,
        "password": request.password,
        "nickname": request.nickname,
        "phone": request.phone,
        "email": request.email
    }
    user.insertUser(user=user_data)
