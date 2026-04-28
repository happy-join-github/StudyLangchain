import sys
import os

# 👇 必须放在最前面！确保 app 能被导入
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from app import init_db

# 初始化数据库
init_db()

from app.api.routes import router
import uvicorn
from app.core.config import host, port


app = FastAPI(title="LangChain + FastAPI Demo")
app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port)