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
    result: Response = user.getUserByUsername(username, password)
if not result['data']:
        return result
    data = result['data']
    userResponse = {
        "username": data[0],
        "nickname": data[3],
        "phone": data[4],
        "email": data[5],
    }
    
    token = hashlib.md5(userResponse['username'].encode("utf-8")).hexdigest()
    userResponse['token'] = token
   
    return CommonResponse.success(message="登录成功",data=userResponse)


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
    result: Response = user.insertUser(user=user_data)
    if not result['data']:
        return CommonResponse.error(message="注册失败")
    user_data['token'] = hashlib.md5(request.username.encode("utf-8")).hexdigest()
    return CommonResponse.success(message="注册成功",data=user_data)


@router.post('/upload')
async def upload():
    pass

@router.post("/ask")
async def predictImg(request):
    filename = request.filename
    
