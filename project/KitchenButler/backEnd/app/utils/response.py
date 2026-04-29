class CommonResponse:
    @staticmethod
    def success( status=200, message="成功",data=None):
        return {"status": status, "message": message, "data": data if data is not None else {}}

    @staticmethod
    def error( status=200, message="失败", data=None):
        return {"status": status, "message": message, "data": data if data is not None else {}}