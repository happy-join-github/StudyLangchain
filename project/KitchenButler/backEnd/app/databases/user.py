from app.schemas.response import Response
from app.schemas.user import UserModel
from app.core.config import db_path
from app.utils.response import CommonResponse
import sqlite3

class User:
    def __init__(self):
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def getUserByUsername(self, username: str, password: str) -> Response:
        sql = "SELECT * FROM users WHERE username = ?"
        self.cursor.execute(sql, (username,))
        user = self.cursor.fetchone()
        if not user:
            return CommonResponse.error(message="没查询到，请检查用户名")
        
        # fetchone 返回的是元组，需要通过索引访问字段（password 在索引 2）
        if password != user[2]:
            return CommonResponse.error(message="用户名或密码错误")
        
        return CommonResponse.success(message="查询成功",data=user)
    def insertUser(self, user: UserModel):
        # TODO 请更新
        try:
            self.cursor.execute("""
            INSERT INTO users (username, password, nickname, phone, email, update_time)
            VALUES (?, ?, ?, ?, ?, datetime('now', 'localtime'))
            """, (user.username, user.password, user.nickname, user.phone, user.email))
            self.connection.commit()
            return CommonResponse.success(message="注册成功",data=user)
        except sqlite3.IntegrityError:
            return CommonResponse.error(message="用户名已存在")
        except sqlite3.Error as e:
            return CommonResponse.error(message="注册失败",data=str(e))



