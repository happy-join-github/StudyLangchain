from app.core.config import db_path
from app.schemas.response import Response
from app.utils.response import CommonResponse
from app.schemas.resource import Resource
import sqlite3

class Resource:
    def __init__(self):
        self.connc = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.connc.cursor()
        

    def insertFile(self,resource:Resource)->Response:
        sql = "insert into resources (sourceType,content,preContent) value(?,?,?)"

        try:
            self.cursor.execute(sql,(resource.sourceType,resource.content,resource.preContent))

            self.connc.commit()
        except Exception as e:
            return CommonResponse.error(status=500,message="数据上传失败")