import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.databases.user import User
user = User()
import unittest
from app.api.routes import UserModel
from app.databases.user import UserModel as UserModelDB
from app.databases.response import Response
from app.api.routes import CommonResponse
import hashlib
class TestUserRoutes(unittest.TestCase):
    def test_login(self):
        user_data = UserModel(username="admin", password="admin123")
        result: Response = user.getUserByUsername(user_data.username, user_data.password)
        self.assertEqual(result['message'],"登录成功")
        self.assertEqual(result['data'],user_data)
        token = hashlib.md5(user_data.username.encode("utf-8")).hexdigest()
        self.assertEqual(result['data']['token'],token)

    def test_register(self):
        user_data = UserModel(username="admin", password="admin123",nickname="admin",phone="12345678901",email="admin@example.com")
        result: Response = user.insertUser(user=user_data)
        self.assertEqual(result['message'],"注册成功")
        self.assertEqual(result['data'],user_data)
        try:
            result = user.getUserByUsername(user_data.username, user_data.password)
            self.assertEqual(result['message'],"查询成功")
            self.assertEqual(result['data'],user_data)
        except:
            self.fail("查询用户失败")


