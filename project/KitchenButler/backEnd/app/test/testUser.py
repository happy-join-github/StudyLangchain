import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import unittest
from app.schemas.user import UserModel
from app.databases.user import User
from app.databases import DataBases
import hashlib

# 确保数据库已初始化
db = DataBases()
user = User()
class TestUserRoutes(unittest.TestCase):
    def test_login(self):
        user_data = UserModel(username="admin", password="admin123", nickname="admin", phone="18853335444", email="5468512463@qq.com")
        result = user.getUserByUsername(user_data.username, user_data.password)
        print(f"test_login result: {result}")
        self.assertEqual(result['message'], "查询成功")

    def test_register(self):
        
        user_data = UserModel(username="testuser", password="test123456", nickname="测试用户", phone="13800138000", email="test@example.com")
        user.insertUser(user=user_data)
        print(f"test_register: 用户已插入")
        
        # 验证注册是否成功
        result = user.getUserByUsername(user_data.username, user_data.password)
        if result['data']:
            self.assertEqual(result['message'], "查询成功")
        else:
            self.assertEqual(result['message'], "查询失败")
        
        print(f"test_register 查询结果: {result}")

if __name__ == '__main__':
    unittest.main(verbosity=2)