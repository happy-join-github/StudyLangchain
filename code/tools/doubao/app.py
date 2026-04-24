import os
import json
from DrissionPage import ChromiumPage
from utils import push_image_to_gitee

# 配置路径
data_dir = r'D:\langchain\code\data'
source_path = r"D:/temp/my_photo.png"

# 上传图片并构建提示词
url = push_image_to_gitee(source_path)
prompt_text = f"{url} 请阅读这个图片，请给我分析这个图片的提示词"

# 初始化浏览器页面
page = ChromiumPage()

try:
    # 打开豆包网页
    page.get('https://www.doubao.com/chat')
    
    # 等待页面加载完成（等待输入框出现）
    page.wait.ele_loaded('tag:textarea', timeout=30)
    
    # 注入提示词到输入框
    page.run_js(f"""
    function updateTextArea(value) {{
        const element = document.querySelector("textarea");
        if (element) {{
            element.value = value;
            // 触发 input 事件使界面更新
            const event = new Event('input', {{ bubbles: true }});
            element.dispatchEvent(event);
        }}
    }}
    updateTextArea(`{prompt_text}`);
    """)

    # 聚焦到 textarea 并按 Enter 发送
    textarea = page.ele('tag:textarea')
    if textarea:
        textarea.focus()          # 聚焦输入框
        textarea.press('Enter')   # 模拟按下回车键
    
    # 等待响应生成（等待至少两个消息块：提问 + 回答）
    page.wait.ele_loaded('css:div[data-message-id]', timeout=300)
    problem_id = 1
    # 获取响应内容（使用提供的 JS 函数逻辑）
    result = page.run_js(f"""
    function getContent(title_index) {{
        const messages = document.querySelectorAll("div[data-message-id]");
        if (messages.length >= 2 && title_index < messages.length) {{
            return {{
                'content': messages[title_index].textContent,
                'problem': messages[title_index - 1].textContent
            }};
        }} else {{
            return {{"content": "error", "problem": messages.length > 0 ? messages[0].textContent : "no question"}};
        }}
    }}
    return getContent({problem_id});  // 获取第一个回答（索引为1）
    """)
    
    # 保存结果到 data 目录
    os.makedirs(data_dir, exist_ok=True)
    output_file = os.path.join(data_dir, 'doubao_response.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        
    print(f"响应已保存至: {output_file}")
    print("问题:", result.get('problem', ''))
    print("回答:", result.get('content', ''))

finally:
    # 关闭浏览器
    page.quit()