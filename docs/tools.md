# 豆包图片分析工具

本文档介绍如何将 **图片分析工作流程** 注册为 LangChain 工具。

---

## 功能概述

**工作流程**：

```
输入图片 → 上传Gitee → 获取URL → 访问豆包 → 输入提示词 → 获取响应 → 保存本地
```

**完整流程说明**：

| 步骤 | 操作 | 说明 |
|------|------|------|
| 1 | 输入图片 | 用户提供本地图片路径 |
| 2 | 上传 Gitee | 调用 `push_image_to_gitee` 上传到预设仓库 |
| 3 | 获取 URL | 返回 Gitee 原始文件访问链接 |
| 4 | 访问豆包 | 打开 `https://www.doubao.com/chat` |
| 5 | 输入提示词 | 将图片 URL 注入输入框，让豆包分析图片 |
| 6 | 获取响应 | 等待豆包返回分析结果 |
| 7 | 保存本地 | 将响应内容保存为 JSON 文件 |

---

## 核心代码实现

### 1. 基础工具类 `DoubaoImageAnalyzer`

```python
"""
豆包图片分析工具
功能：上传图片到 Gitee，让豆包分析并返回提示词
"""

import os
import json
from DrissionPage import ChromiumPage
from typing import Optional

from utils import push_image_to_gitee


class DoubaoImageAnalyzer:
    """豆包图片分析器"""
    
    DOUBao_URL = "https://www.doubao.com/chat"
    
    def __init__(self, data_dir: str = r'D:\langchain\code\data'):
        """
        初始化分析器
        
        Args:
            data_dir: 响应结果保存目录
        """
        self.data_dir = data_dir
        self.page: Optional[ChromiumPage] = None
    
    def analyze_image(self, image_path: str) -> dict:
        """
        分析图片并获取提示词
        
        Args:
            image_path: 本地图片路径
            
        Returns:
            dict: 包含 status, url, response, save_path
        """
        result = {
            "status": "error",
            "image_path": image_path,
            "gitee_url": None,
            "response": None,
            "save_path": None,
            "error": None
        }
        
        try:
            # ========== 步骤 1-3: 上传图片到 Gitee ==========
            print(f"📤 正在上传图片: {image_path}")
            gitee_url = push_image_to_gitee(image_path)
            result["gitee_url"] = gitee_url
            print(f"✅ 图片已上传: {gitee_url}")
            
            # ========== 步骤 4-6: 访问豆包并分析 ==========
            print("🌐 正在打开豆包...")
            response_text = self._get_doubao_response(gitee_url)
            result["response"] = response_text
            print(f"📝 豆包响应长度: {len(response_text)} 字符")
            
            # ========== 步骤 7: 保存结果 ==========
            save_path = self._save_response(response_text)
            result["save_path"] = save_path
            result["status"] = "success"
            
        except Exception as e:
            result["error"] = str(e)
            print(f"❌ 分析失败: {e}")
        
        return result
    
    def _get_doubao_response(self, image_url: str) -> str:
        """访问豆包并获取响应"""
        
        # 构建提示词
        prompt = f"{image_url} 请阅读这个图片，请给我分析这个图片的提示词"
        
        # 初始化浏览器
        self.page = ChromiumPage()
        
        try:
            # 打开豆包网页
            self.page.get(self.DOUBao_URL)
            
            # 等待输入框加载
            self.page.wait.ele_loaded('tag:textarea', timeout=30)
            
            # 注入提示词到输入框
            self.page.run_js(f"""
            function updateTextArea(value) {{
                const element = document.querySelector("textarea");
                if (element) {{
                    element.value = value;
                    const event = new Event('input', {{ bubbles: true }});
                    element.dispatchEvent(event);
                }}
            }}
            updateTextArea(`{prompt}`);
            """)
            
            # 聚焦并发送
            textarea = self.page.ele('tag:textarea')
            if textarea:
                textarea.focus()
                textarea.press('Enter')
            
            # 等待响应生成
            self.page.wait.ele_loaded('css:div[data-message-id]', timeout=300)
            
            # 获取响应内容
            response = self.page.run_js("""
            function getContent(title_index) {
                const messages = document.querySelectorAll("div[data-message-id]");
                if (messages.length >= 2 && title_index < messages.length) {
                    return {
                        'content': messages[title_index].textContent,
                        'problem': messages[title_index - 1].textContent
                    };
                } else {
                    return {"content": "error", "problem": "no response"};
                }
            }
            return getContent(1);
            """)
            
            return response.get('content', response.get('content', 'error'))
            
        finally:
            if self.page:
                self.page.quit()
    
    def _save_response(self, content: str) -> str:
        """保存响应到本地"""
        os.makedirs(self.data_dir, exist_ok=True)
        
        output_file = os.path.join(self.data_dir, 'doubao_response.json')
        data = {
            "content": content,
            "save_time": str(os.popen('date').read().strip())
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 结果已保存: {output_file}")
        return output_file
```

---

### 2. 独立函数版本（简单直接）

如果你不需要类封装，可以使用函数版本：

```python
"""
豆包图片分析 - 函数版本
"""

import os
import json
from DrissionPage import ChromiumPage
from utils import push_image_to_gitee


def analyze_image_to_prompt(image_path: str, save_dir: str = r'D:\langchain\code\data') -> dict:
    """
    分析图片，获取豆包生成的提示词
    
    Args:
        image_path: 本地图片路径
        save_dir: 结果保存目录
        
    Returns:
        dict: 包含 gitee_url, response, save_path
    """
    result = {}
    
    # 1. 上传图片到 Gitee
    print(f"📤 上传图片: {image_path}")
    gitee_url = push_image_to_gitee(image_path)
    result['gitee_url'] = gitee_url
    
    # 2. 构建提示词
    prompt = f"{gitee_url} 请阅读这个图片，请给我分析这个图片的提示词"
    
    # 3. 打开豆包
    print("🌐 打开豆包...")
    page = ChromiumPage()
    
    try:
        page.get('https://www.doubao.com/chat')
        page.wait.ele_loaded('tag:textarea', timeout=30)
        
        # 4. 注入提示词
        page.run_js(f"""
        const textarea = document.querySelector("textarea");
        if (textarea) {{
            textarea.value = `{prompt}`;
            textarea.dispatchEvent(new Event('input', {{ bubbles: true }}));
        }}
        """)
        
        # 5. 发送
        textarea = page.ele('tag:textarea')
        textarea.focus()
        textarea.press('Enter')
        
        # 6. 等待响应
        page.wait.ele_loaded('css:div[data-message-id]', timeout=300)
        
        # 7. 获取响应
        response = page.run_js("""
        const msgs = document.querySelectorAll("div[data-message-id]");
        return msgs.length >= 2 ? msgs[1].textContent : "error";
        """)
        result['response'] = response
        
        # 8. 保存结果
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, 'doubao_response.json')
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        result['save_path'] = save_path
        
    finally:
        page.quit()
    
    return result
```

---

## LangChain 工具注册

### 方法一：使用 @tool 装饰器

```python
from langchain_core.tools import tool


@tool
def analyze_image_get_prompt(image_path: str) -> str:
    """分析图片，获取图片提示词。
    
    工作流程：
    1. 将图片上传到 Gitee 获取 URL
    2. 打开豆包网站
    3. 让豆包分析图片并返回提示词
    4. 将响应保存到本地
    
    Args:
        image_path: 本地图片的绝对路径，例如 "D:/images/photo.png"
        
    Returns:
        JSON 格式的分析结果，包含 gitee_url、response 和 save_path
    """
    from doubao_image_analyzer import analyze_image_to_prompt
    
    result = analyze_image_to_prompt(image_path)
    
    return json.dumps(result, ensure_ascii=False, indent=2)


@tool  
def upload_image_to_gitee(image_path: str) -> str:
    """上传图片到 Gitee 图床。
    
    将本地图片上传到预设的 Gitee 仓库，返回可访问的 URL。
    用于需要分享图片或获取图片网络链接的场景。
    
    Args:
        image_path: 图片的本地路径
        
    Returns:
        Gitee 原始文件访问链接
    """
    from utils import push_image_to_gitee
    return push_image_to_gitee(image_path)
```

### 方法二：使用 Tool 类

```python
from langchain_core.tools import Tool
from pydantic import BaseModel, Field


class ImagePromptInput(BaseModel):
    image_path: str = Field(
        description="本地图片的绝对路径，例如 'D:/images/photo.png' 或 'C:/Users/photo.jpg'"
    )


def analyze_image(image_path: str) -> str:
    """分析图片"""
    from doubao_image_analyzer import analyze_image_to_prompt
    result = analyze_image_to_prompt(image_path)
    return json.dumps(result, ensure_ascii=False)


image_prompt_tool = Tool(
    name="analyze_image_prompt",
    description=(
        "分析图片并获取提示词。当你需要分析图片内容、"
        "提取图片特征、获取图片生成提示词时使用。"
        "输入是本地图片的绝对路径。"
    ),
    func=analyze_image,
    args_schema=ImagePromptInput,
)
```

### 方法三：使用 BaseTool（推荐）

```python
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Optional


class ImagePromptInput(BaseModel):
    """图片分析输入参数"""
    image_path: str = Field(
        description="本地图片的绝对路径",
        examples=["D:/images/photo.png", "C:/Users/test.jpg"]
    )


class AnalyzeImagePromptTool(BaseTool):
    """豆包图片分析工具
    
    功能：
    - 上传图片到 Gitee
    - 访问豆包网站
    - 获取图片提示词分析
    - 保存结果到本地
    """
    
    name: str = "analyze_image_prompt"
    description: str = (
        "分析图片并获取提示词。这个工具会："
        "1. 将图片上传到 Gitee 图床"
        "2. 打开豆包网站"
        "3. 让 AI 分析图片并返回详细的提示词"
        "4. 将响应结果保存到本地 JSON 文件"
        "适用于需要提取图片特征、分析图片内容、或获取图片生成提示词的场景。"
    )
    args_schema: Type[BaseModel] = ImagePromptInput
    
    data_dir: str = r'D:\langchain\code\data'
    
    def _run(self, image_path: str) -> str:
        """执行图片分析"""
        from doubao_image_analyzer import DoubaoImageAnalyzer
        
        analyzer = DoubaoImageAnalyzer(data_dir=self.data_dir)
        result = analyzer.analyze_image(image_path)
        
        if result['status'] == 'success':
            return (
                f"✅ 分析完成！\n\n"
                f"📤 图片链接: {result['gitee_url']}\n\n"
                f"📝 提示词响应:\n{result['response']}\n\n"
                f"💾 已保存至: {result['save_path']}"
            )
        else:
            return f"❌ 分析失败: {result['error']}"
```

---

## 在 Agent 中使用

### 完整示例

```python
from langchain_openai import ChatOpenAI
from langchain.agents import AgentType, initialize_agent
from langchain.tools.doubao.langchain_tools import (
    AnalyzeImagePromptTool,
    upload_image_to_gitee,
)


def create_image_agent():
    """创建图片分析 Agent"""
    
    # 1. 初始化 LLM
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.7,
    )
    
    # 2. 准备工具
    tools = [
        AnalyzeImagePromptTool(),
        upload_image_to_gitee,  # 单独的图片上传工具
    ]
    
    # 3. 创建 Agent
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
    )
    
    return agent


def main():
    """使用示例"""
    agent = create_image_agent()
    
    # 直接分析图片
    result = agent.run("帮我分析这张图片的提示词：D:/temp/my_photo.png")
    print(result)
    
    # 或者更自然的对话
    result = agent.run(
        "我有一张图片在 D:/temp/landscape.jpg，"
        "请帮我上传到 Gitee，然后让豆包分析这张图片，"
        "获取它的提示词并保存结果"
    )
    print(result)


if __name__ == "__main__":
    main()
```

---

## 工具配置说明

### 修改 Gitee 仓库配置

编辑 `utils.py` 中的配置：

```python
# 源目录（Git 仓库本地路径）
SOURCE_PATH = os.path.abspath(r"D:/source")

# Gitee 仓库的 raw 文件访问前缀
GITEE_RAW_BASE = "https://gitee.com/a2431242530qqcom/material-warehouse/raw/main/"
```

### 修改保存目录

```python
# 方法 1: 代码中指定
analyzer = DoubaoImageAnalyzer(data_dir='D:/my_data')

# 方法 2: 修改默认值
class AnalyzeImagePromptTool(BaseTool):
    data_dir: str = r'D:\your\custom\path'
```

---

## 常见问题

### Q: 上传失败怎么办？
检查：
1. Gitee 仓库是否已克隆到本地 `SOURCE_PATH`
2. Git 是否已配置认证信息
3. 网络连接是否正常

### Q: 豆包响应超时？
当前超时设置 `timeout=300`（5分钟）。可以在 `app.py` 中调整：

```python
page.wait.ele_loaded('css:div[data-message-id]', timeout=600)  # 10分钟
```

### Q: 如何只上传图片不分析？
使用单独的 `upload_image_to_gitee` 工具：

```python
@tool
def upload_image(image_path: str) -> str:
    """上传图片到 Gitee"""
    return push_image_to_gitee(image_path)
```

---

## 文件结构

```
code/tools/doubao/
├── app.py                    # 原始脚本
├── utils.py                  # Gitee 上传工具
├── doubao_image_analyzer.py  # 新增：图片分析器类
└── langchain_tools.py        # 新增：LangChain 工具封装

code/data/                    # 保存目录
└── doubao_response.json       # 分析结果
```

---

## 快速开始

### 1. 创建分析器文件 `code/tools/doubao/doubao_image_analyzer.py`

将上面的 `DoubaoImageAnalyzer` 类保存到该文件。

### 2. 创建 LangChain 工具文件 `code/tools/doubao/langchain_tools.py`

将工具注册代码保存到该文件。

### 3. 在 Agent 中使用

```python
from langchain.agents import initialize_agent
from langchain_openai import ChatOpenAI
from langchain.tools.doubao.langchain_tools import AnalyzeImagePromptTool

llm = ChatOpenAI(model="gpt-4")
agent = initialize_agent(
    tools=[AnalyzeImagePromptTool()],
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
)

# 使用
agent.run("分析 D:/temp/photo.png")
```

---

*文档更新时间：2026-04-24*
