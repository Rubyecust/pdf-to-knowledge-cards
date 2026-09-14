# 安装指南 (Installation Guide)

## 系统要求

- **操作系统**: Windows / macOS / Linux
- **Python 版本**: >= 3.8
- **内存**: 建议 4GB 以上

## 快速安装

### 1. 克隆仓库

```bash
git clone https://github.com/Rubyecust/pdf-to-knowledge-cards.git
cd pdf-to-knowledge-cards
```

### 2. 创建虚拟环境 (推荐)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 安装 spaCy 语言模型 (可选)

对于中文处理:
```bash
python -m spacy download zh_core_web_sm
```

对于英文处理:
```bash
python -m spacy download en_core_web_sm
```

### 5. 安装 NLTK 数据 (可选)

```bash
python -m nltk.downloader punkt
```

## 验证安装

运行示例脚本验证安装:

```bash
cd examples
python quick_start.py
```

如果看到以下输出，说明安装成功:
```
✓ 示例1: 创建基础卡片
✓ 示例2: 生成视觉卡片
✓ 示例3: 文本摘要
✓ 示例4: 批量卡片
✓ 所有示例运行完成！
```

## 故障排除

### 问题 1: 找不到模块

**错误信息**: `ModuleNotFoundError: No module named 'pdfplumber'`

**解决方案**:
```bash
# 确保激活了虚拟环境
pip install pdfplumber
```

### 问题 2: PDF 处理错误

**错误信息**: `FileNotFoundError: [Errno 2] No such file or directory`

**解决方案**:
- 检查 PDF 文件路径是否正确
- 确保 PDF 文件存在且可读

### 问题 3: 内存不足

**错误信息**: `MemoryError`

**解决方案**:
- 处理较小的 PDF 文件
- 增加系统内存
- 调整配置文件中的处理参数

### 问题 4: 生成图片出现中文乱码

**原因**: 系统缺少合适的中文字体

**解决方案**:

#### macOS
```bash
# 已安装 PingFang 字体
# 无需额外操作
```

#### Windows
```bash
# 使用系统字体 (通常已安装)
# 编辑 card_generator.py 中的字体路径:
# Windows 字体通常位于: C:\\Windows\\Fonts
```

#### Linux
```bash
# 安装中文字体
sudo apt-get install fonts-wqy-microhei
```

然后修改 `src/card_generator.py` 中的字体路径:
```python
title_font = ImageFont.truetype("/usr/share/fonts/opentype/wqy/wqy-microhei.ttc", 36)
```

## 使用 Docker (可选)

如果你有 Docker，可以使用容器化运行:

```bash
# 构建 Docker 镜像
docker build -t pdf-to-cards .

# 运行容器
docker run -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output pdf-to-cards python src/main.py input/sample.pdf
```

## 下一步

安装完成后，你可以：

1. **阅读快速开始** - 查看 [README.md](README.md)
2. **运行示例** - 参考 [examples/quick_start.py](examples/quick_start.py)
3. **处理你的 PDF** - 使用主程序处理自己的 PDF 文件

## 获取帮助

如果遇到问题，请：

1. 查看 [FAQ.md](FAQ.md)
2. 提交 [Issue](https://github.com/Rubyecust/pdf-to-knowledge-cards/issues)
3. 查看项目文档

---

**祝你使用愉快！** 🎉
