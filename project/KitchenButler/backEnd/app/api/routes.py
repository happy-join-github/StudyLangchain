from fastapi import APIRouter
from schemas.user import UserModel
from app.schemas.response import Response
from app.databases.user import user
from app.utils.response import common_response
router = APIRouter()


@router.get("/login")
async def login(request:UserModel):
    if request.username=="admin" and request.password=="admin123":
        return common_response.success(message="登录成功")
    else:
        return common_response.error(message="用户名或密码错误")
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
async def register(request:UserModel):
    result:Response = user.getUserByUsername(request.username)
    if result:
        return common_response.error(message="用户名已存在")
    user_data = {
        "username": request.username,
        "password": request.password,
        "nickname": request.nickname,
        "phone": request.phone,
        "email": request.email
    }
    user.insertUser(user=user_data)
    
