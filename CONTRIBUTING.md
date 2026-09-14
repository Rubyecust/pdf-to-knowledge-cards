# 贡献指南 (Contributing Guide)

我们欢迎各种形式的贡献！无论是代码、文档、报告 Bug 还是提议建议。

## 如何开始

### 1. Fork 项目

在 GitHub 上点击 "Fork" 按钮

### 2. 克隆你的 Fork

```bash
git clone https://github.com/YOUR_USERNAME/pdf-to-knowledge-cards.git
cd pdf-to-knowledge-cards
```

### 3. 创建功能分支

```bash
git checkout -b feature/your-feature-name
```

### 4. 提交改动

```bash
git add .
git commit -m "Add your feature description"
```

### 5. 推送到 Fork

```bash
git push origin feature/your-feature-name
```

### 6. 创建 Pull Request

在 GitHub 上创建 PR，描述你的改动

---

## 代码风格

我们遵循 PEP 8 标准：

```python
# ✓ 好的例子
def extract_knowledge_points(text: str) -> List[Dict]:
    """提取知识点"""
    points = []
    for line in text.split('\n'):
        if line.strip():
            points.append(line.strip())
    return points

# ✗ 不好的例子
def extract_knowledge_points(txt):
    pts=[]
    for l in txt.split('\n'):
        pts.append(l)
    return pts
```

### 命名规范

- 函数名: `snake_case` (lowercase_with_underscores)
- 类名: `PascalCase` (CapitalizedWords)
- 常量: `UPPER_CASE` (UPPERCASE_WITH_UNDERSCORES)
- 私有方法: `_private_method` (以下划线开头)

### 注释和文档

```python
def process_pdf(pdf_path: str, output_dir: str = None) -> bool:
    """
    处理 PDF 文件的完整流程
    
    Args:
        pdf_path: PDF 文件路径
        output_dir: 输出目录 (默认: ./output)
        
    Returns:
        处理是否成功
        
    Raises:
        FileNotFoundError: PDF 文件不存在时
        ValueError: 输出目录无效时
    """
    # 实现...
```

---

## 报告 Bug

### 问题模板

```markdown
## 问题描述
清晰简洁地描述 bug

## 复现步骤
1. ...
2. ...
3. ...

## 期望行为
应该发生什么

## 实际行为
实际发生了什么

## 环境信息
- OS: [e.g. Ubuntu 20.04]
- Python: [e.g. 3.9.0]
- 依赖版本: [运行 pip freeze]

## 错误日志
```
粘贴完整的错误消息
```
```

---

## 请求功能

```markdown
## 功能描述
这个功能应该做什么?

## 用例
在什么情况下会用到这个功能?

## 可能的实现
你有想到的实现方式吗?
```

---

## 开发环境设置

### 安装开发依赖

```bash
pip install -r requirements.txt
pip install pytest pytest-cov black flake8
```

### 运行测试

```bash
pytest tests/ -v
```

### 代码格式化

```bash
black src/
```

### 代码检查

```bash
flake8 src/ --max-line-length=100
```

---

## Pull Request 检查清单

- [ ] 代码遵循项目风格
- [ ] 已添加测试
- [ ] 测试通过
- [ ] 文档已更新
- [ ] 提交消息清晰
- [ ] 没有添加不必要的依赖

---

## 文档贡献

### 修改现有文档

1. 编辑相应的 `.md` 文件
2. 检查格式和拼写
3. 提交 Pull Request

### 添加新文档

1. 在相应目录创建 `.md` 文件
2. 遵循现有文档风格
3. 在 README 中添加链接

---

## 翻译贡献

### 添加新语言翻译

1. 创建 `docs/i18n/{language}/` 目录
2. 翻译文档文件
3. 在 README 中添加语言选项

---

## 许可证

通过提交代码，你同意你的代码将在 MIT License 下发布。

---

## 行为准则

### 我们的承诺

我们致力于为所有人提供一个欢迎和包容的社区。

### 预期行为

- 尊重他人
- 欢迎不同观点
- 接受建设性批评
- 专注于对社区最有益的事情

### 不可接受的行为

- 骚扰、歧视或人身攻击
- 发布他人私人信息
- 其他不专业的行为

### 报告问题

如果你目睹或经历不当行为，请联系项目维护者。

---

## 致谢

感谢所有为这个项目做出贡献的人！🎉

---

**欢迎加入我们！** 🚀
