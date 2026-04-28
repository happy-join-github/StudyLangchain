import base64
import os

class Utils:
        

    def image2base64(self,image_path):
        with open(image_path, "rb") as f:
            image_data = f.read()
            image_base64 = base64.b64encode(image_data).decode("utf-8")
        return image_base64




utils = Utils()