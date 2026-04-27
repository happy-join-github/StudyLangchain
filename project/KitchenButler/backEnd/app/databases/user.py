from app.core import config
from app.schemas.response import Response
from app.schemas.user import UserModel
import sqlite3

path = config.db_path

connection = sqlite3.connect(path,check_same_thread=False)
class User:
    def __init__(self):
        self.cursor = connection.cursor()

    def getUserByUsername(self,username:str)->Response:
        sql = f"select * from user where username={username}"
        user = self.cursor.fetchone(sql)
        if not user:
            return {'status':200,"message":"没查询到，请检查用户名","data":user}

        return {'status':200,"message":"成功","data":user}

    def insertUser(self,user:UserModel):
        # TODO 请更新
        sql = "insert into "
        pass



user = User()
