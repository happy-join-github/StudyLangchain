
class CommonResponse:
    def __init__(self):
        self.status: int = 200
        self.message: str = "成功"
        self.data: object = {}

    def success(self, status, message, data={}):
        status = status if status else self.status
        message = message if message else self.message
        data = data if data else self.data
        return {"status": status, "message": message, "data": data}

    def error(self, status, message):
        status = status if status else self.status
        message = message if message else "失败"
        data = data if data else self.data
        return {"status": status, "message": message, "data": data}


common_response = CommonResponse()
