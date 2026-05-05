from app.core.config import db_path
from pathlib import Path
import sqlite3
import logging
class DataBases:
    def __init__(self):
        # 确保 data 目录存在
        self.existDir()
        # 创建数据库链接
        self.connect = sqlite3.connect(db_path,check_same_thread=False)
        self.cursor = self.connect.cursor()
        # 初始化视乎句酷
        self.createUser()
        self.createResource()
        
    
    def existDir(self):
        Path(db_path).parent.mkdir(exist_ok=True)

    def createUser(self):
        self.cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            nickname TEXT NOT NULL,
            phone TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            created_time TEXT DEFAULT (datetime('now', 'localtime')),
            update_time TEXT DEFAULT (datetime('now', 'localtime'))
        );
        
        CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
        CREATE INDEX IF NOT EXISTS idx_users_phone ON users(phone);
        
        INSERT OR IGNORE INTO users (username, password, nickname, phone, email)
        VALUES ('admin', 'admin123', '超级管理员', '18853335444', '5468512463@qq.com');
        """)
        self.connect.commit()
        logging.info("✅ 用户数据库已初始化")
        
    
    def createResource(self):
        self.cursor.executescript("""
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sourceType TEXT NOT NULL,
            content TEXT NOT NULL,
            createTime TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
            preContent TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_resources_source_type ON resources(sourceType);
        """)
        self.connect.commit()
        # 关闭数据库链接
        self.connect.close()
        logging.info("✅ 资源数据库已初始化")
        