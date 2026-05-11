import hashlib
from pathlib import Path
import base64

from fastapi import APIRouter, Query, UploadFile, File

from app.model.LoginRequest import UserModel
from app.model.PredictRequest import PredictRequest
from app.schemas.response import Response
from app.databases.user import User
from app.utils.response import CommonResponse
from app.core.config import imgspath
from app.databases.resource import Resource
from app.agent.manage import ModelInIt

############## 初始化区域################

router = APIRouter()
user = User()
resource = Resource()
model = ModelInIt()
######################################


@router.get("/login")
async def login(
    username: str = Query(..., alias="username", description="用户名"),
    password: str = Query(..., alias="password", description="密码")
):
    # 手动创建UserModel实例，触发验证
    # user_data = UserModel(username=username, password=password)

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

    return CommonResponse.success(message="登录成功", data=userResponse)


@router.post("/register")
async def register(request: UserModel):
    user = User(UserModel.username, UserModel.password)
    result: Response = user.getUserByUsername(request.username)
    if not result['data']:
        return result

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
    user_data['token'] = hashlib.md5(
        request.username.encode("utf-8")).hexdigest()
    return CommonResponse.success(message="注册成功", data=user_data)


@router.post('/upload')
async def upload(file: UploadFile = File(...)):
    # 定义上传目录
    upload_dir = imgspath
    Path(upload_dir).mkdir(exist_ok=True)

    # 保存文件
    file_path = upload_dir / file.filename
    try:
        file_content = await file.read()
        with open(file_path, 'wb') as f:
            f.write(file_content)

        # 将图片转换为base64编码并写入数据库
        base64_content = base64.b64encode(file_content).decode('utf-8')
        from app.schemas.resource import Resource as ResourceSchema
        resource_data = ResourceSchema(
            sourceType="image", content=base64_content)
        resource.insertFile(resource_data)

        file_info = {
            'filename': file.filename,
            'content_type': file.content_type,
            'file_path': str(file_path)
        }
        return CommonResponse.success(message="文件上传成功", data=file_info)
    except Exception as e:
        return CommonResponse.error(message=f"文件上传失败: {str(e)}")


def getFile(filename):
    with open(filename, 'rb') as f:
        content = f.read()
    bsContent = base64.b64encode(content).decode("utf-8")
    return bsContent

@router.post("/ask")
async def predictImg(request: PredictRequest):
    try:
        image_base64 = getFile(request.image_path)
        
        chatmodel = model.multimodalModel
        message = [{"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}},
            {"type": "text", "text": f"{request.prompt}"},
        ]}]
        
        response = chatmodel.invoke(input=message)
        result_text = response.content
        
        query = {"query": f"请根据{result_text}这些食材给我5个菜谱,按照营养价值和制作的难易程度给我排序。"}
        search_model = model.searchModel
        
        recipes = []
        for result in search_model.stream(query):
            if isinstance(result, dict):
                search_results = result.get('results', [])
            else:
                search_results = getattr(result, 'results', [])

            for item in search_results:
                recipes.append({
                    "title": item.get("title", ""),
                    "content": item.get("content", ""),
                    "url": item.get("url", ""),
                    "score": item.get("score", 0)
                })
        
        return CommonResponse.success(
            message="识别成功",
            data={
                "ingredients": result_text,
                "recipes": recipes
            }
        )
    except FileNotFoundError:
        return CommonResponse.error(message="图片文件不存在")
    except Exception as e:
        return CommonResponse.error(message=f"识别失败: {str(e)}")
    
