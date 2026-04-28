import sqlite3
from pathlib import Path
import os
def init_db():
    from app.core.config import db_path
    """初始化 SQLite 数据库，创建 data/user.db 和 users 表"""
    # 确保 data 目录存在
    Path(db_path).mkdir(exist_ok=True)
    
    dbFullpath = os.path.join(db_path,'user.db')
    if Path(dbFullpath):
        return 
    conn = sqlite3.connect(dbFullpath)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            nickname TEXT NOT NULL,
            phone TEXT  NOT NULL UNIQUE,
            email TEXT  NOT NULL UNIQUE,
            createdTime DATETIME DEFAULT CURRENT_TIMESTAMP,
            updateTime DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
    print(f"✅ 数据库已初始化: {dbFullpath}")