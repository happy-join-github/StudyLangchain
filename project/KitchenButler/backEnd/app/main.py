import sys
import os

# 👇 必须放在最前面！确保 app 能被导入
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import init_db

# 初始化数据库
init_db()

from app.api.routes import router
import uvicorn
from app.core.config import host, port


app = FastAPI(title="LangChain + FastAPI Demo")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源（开发环境可以用 *，生产环境建议指定具体的前端地址）
    allow_credentials=True, # 允许携带 Cookie 等凭证
    allow_methods=["*"],    # 允许所有的请求方法（GET, POST, PUT, DELETE 等）
    allow_headers=["*"],    # 允许所有的请求头
)

app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port)