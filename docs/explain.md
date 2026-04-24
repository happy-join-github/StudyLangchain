用户问为什么推荐使用方式三（BaseTool 继承）。让我简洁地解释一下推荐的原因。

## 推荐 BaseTool 的原因

| 特性 | `@tool` | `Tool` 类 | `BaseTool` |
|------|:-------:|:---------:|:----------:|
| 输入验证 | ❌ | ❌ | ✅ Pydantic 自动校验 |
| 类型提示 | ❌ | ❌ | ✅ 完整类型定义 |
| 异步支持 | ❌ | ❌ | ✅ `_arun` 方法 |
| 配置属性 | ❌ | 部分 | ✅ 完整 |
| 复杂逻辑 | ⚠️ 勉强 | ⚠️ 勉强 | ✅ 原生支持 |
| 错误处理 | 内嵌 | 内嵌 | ✅ 结构化 |

### 具体原因

**1. 输入验证 - 防止 LLM 传错参数**

```python
# BaseTool 可以限制参数范围
class ImagePromptInput(BaseModel):
    image_path: str = Field(description="图片路径")
    max_results: int = Field(default=5, ge=1, le=20)  # 自动校验范围
```

**2. 描述更规范 - examples 示例**

```python
image_path: str = Field(
    description="本地图片路径",
    examples=["D:/photo.png", "C:/images/test.jpg"]  # LLM 更懂怎么调用
)
```

**3. 异步支持**

```python
class MyTool(BaseTool):
    def _run(self, query): ...
    async def _arun(self, query): ...  # 支持 async/await
```

**4. 你的场景适合用 BaseTool**

你的工具涉及：
- 浏览器自动化（可能失败，需要重试）
- 文件上传（需要路径校验）
- 长时间等待（异步更高效）
- 多步骤流程（需要清晰的状态管理）

**简单工具用 `@tool`，复杂工具用 `BaseTool`**