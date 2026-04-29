from app.core import config
from app.schemas.response import Response
from app.schemas.user import UserModel
import os
import sqlite3

path = config.db_path
db_name = os.path.join(path, "user.db")

connection = sqlite3.connect(db_name, check_same_thread=False)


class User:
    def __init__(self):
        self.connection = connection
        self.cursor = connection.cursor()

    def getUserByUsername(self, username: str) -> Response:
        sql = f"select * from user where username={username}"
        user = self.cursor.fetchone(sql)
        self.connection.close()
        if not user:
            return {'status': 200, "message": "没查询到，请检查用户名", "data": user}

        return {'status': 200, "message": "成功", "data": user}

    def insertUser(self, user: UserModel):
        # TODO 请更新
        self.cursor.execute("""
        INSERT INTO users (username, password, nickname, phone, email, updateTime)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, (user.username, user.password, user.nickname, user.phone, user.email))
        self.connection.commit()
        self.connection.close()


user = User()
