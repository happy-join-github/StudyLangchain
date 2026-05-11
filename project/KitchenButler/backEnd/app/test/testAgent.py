import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import unittest
import logging
import json
from app.agent.manage import ModelInIt
from app.api.routes import getFile
from app.utils.response import CommonResponse
from app.core.config import imgspath
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TestAskEndpoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logger.info("初始化测试：创建 ModelInIt 实例")
        cls.model = ModelInIt()
        cls.getFile = getFile
        cls.imgspath = imgspath
        logger.info("ModelInIt 实例创建成功")

    # def test_getFile(self):
    #     logger.info("开始测试：test_getFile")
    #     test_image = os.path.join(self.imgspath, "test1.jpg")
    #     if os.path.exists(test_image):
    #         logger.info(f"读取测试图片: {test_image}")
    #         result = getFile(test_image)
    #         logger.info(f"Base64 编码长度: {len(result)}")
    #         self.assertIsInstance(result, str)
    #         self.assertTrue(len(result) > 0)
    #         logger.info("test_getFile 测试通过")
    #     else:
    #         logger.warning(f"测试图片不存在: {test_image}")
    #         print(f"测试图片不存在: {test_image}")

    # def test_multimodal_model(self):
    #     logger.info("开始测试：test_multimodal_model")
    #     image_path = os.path.join(self.imgspath, "test1.jpg")

    #     if not os.path.exists(image_path):
    #         logger.warning(f"测试图片不存在，跳过多模态模型测试: {image_path}")
    #         self.skipTest("测试图片不存在，跳过多模态模型测试")

    #     logger.info(f"读取图片并转换为 Base64: {image_path}")
    #     image_base64 = getFile(image_path)
    #     # logger.info(f"Base64 长度: {len(image_base64)}")

    #     chatmodel = self.model.multimodalModel
        
    #     logger.info("调用多模态模型进行食材识别")

    #     message = [{"role": "user", "content": [
    #         {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}},
    #         {"type": "text", "text": "请识别图片中的食材"}
    #     ]}]

    #     response = chatmodel.invoke(input=message)
    #     logger.info(f"模型响应: {response.content}")

    #     self.assertTrue(hasattr(response, 'content'))
    #     logger.info("test_multimodal_model 测试通过")

    # def test_search_model(self):
    #     logger.info("开始测试：test_search_model")
    #     query = {"query": "西红柿炒鸡蛋的做法"}
    #     # query = {"query": f"请根据{result_text}这些食材给我5个菜谱,按照营养价值和制作的难易程度给我排序。"}
    #     logger.info(f"搜索查询: {query['query']}")

    #     search_model = self.model.searchModel
    #     logger.info("调用搜索模型")

    #     results = []
    #     for result in search_model.stream(query):
    #         if isinstance(result, dict):
    #             search_results = result.get('results', [])
    #         else:
    #             search_results = getattr(result, 'results', [])

    #         if search_results:
    #             logger.info(f"获取到 {len(search_results)} 个搜索结果")
    #             for item in search_results:
    #                 results.append({
    #                     "title": item.get("title", ""),
    #                     "content": item.get("content", ""),
    #                     "url": item.get("url", ""),
    #                     "score": item.get("score", 0)
    #                 })
    #                 logger.debug(f"搜索结果项: {item.get('title', '')}")

    #     logger.info(f"总共获取到 {len(results)} 个搜索结果")
    #     self.assertGreater(len(results), 0)
    #     if results:
    #         logger.info(f"第一个结果: {results[0]}")
    #     logger.info("test_search_model 测试通过")

    def test_ask_integration(self):
        logger.info("开始测试：test_ask_integration (集成测试)")
        image_path = os.path.join(self.imgspath, "test1.jpg")

        if not os.path.exists(image_path):
            logger.warning(f"测试图片不存在，跳过集成测试: {image_path}")
            self.skipTest("测试图片不存在，跳过集成测试")

        logger.info(f"步骤1: 读取图片 {image_path}")
        image_base64 = getFile(image_path)
        # logger.info(f"图片 Base64 长度: {len(image_base64)}")

        chatmodel = self.model.multimodalModel
        logger.info("步骤2: 调用多模态模型识别食材")

        message = [{"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}},
            {"type": "text", "text": "请识别图片中的食材"}
        ]}]

        response = chatmodel.invoke(input=message)
        result_text = response.content
        logger.info(f"识别到的食材: {result_text}")

        query = {"query": f"请根据{result_text}这些食材给我5个菜谱,按照营养价值和制作的难易程度给我排序。"}
        logger.info(f"步骤3: 搜索菜谱，查询: {query['query']}")
        search_model = self.model.searchModel

        recipes = []
        for result in search_model.stream(query):
            if isinstance(result, dict):
                search_results = result.get('results', [])
            else:
                search_results = getattr(result, 'results', [])

            if search_results:
                logger.info(f"获取到 {len(search_results)} 个菜谱")
                for item in search_results:
                    recipes.append({
                        "title": item.get("title", ""),
                        "content": item.get("content", ""),
                        "url": item.get("url", ""),
                        "score": item.get("score", 0)
                    })
        

        logger.info(f"步骤4: 构建最终响应，共 {len(recipes)} 个菜谱")
        
        json.dump(recipes,open('data/response.json','w',encoding="utf-8"),ensure_ascii=False,indent=4)
        final_result = CommonResponse.success(
            message="识别成功",
            data={
                "ingredients": result_text,
                "recipes": recipes
            }
        )

        logger.info(f"集成测试结果: {final_result}")
        self.assertEqual(final_result['message'], "识别成功")
        self.assertIn("ingredients", final_result['data'])
        self.assertIn("recipes", final_result['data'])
        logger.info("test_ask_integration 测试通过")

if __name__ == '__main__':
    logger.info("=" * 50)
    logger.info("开始运行 testAgent 测试")
    logger.info("=" * 50)
    unittest.main(verbosity=2)