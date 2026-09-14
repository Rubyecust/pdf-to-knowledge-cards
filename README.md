# 📚 PDF to Knowledge Cards

将书籍或读书笔记转换成思维导图式的知识卡片，然后在社交平台分享。

## ✨ 核心功能

- 📄 **PDF 解析**: 智能提取 PDF 中的文本和结构
- 🧠 **AI 总结**: 基于 NLP 自动生成核心知识点
- 🎨 **视觉卡片**: 生成美观的图片卡片（支持多种模板）
- 📍 **来源引用**: 保留原文引用和页码
- 🌳 **思维导图**: 构建知识点间的关系
- 📤 **社交分享**: 优化各平台尺寸（Instagram、小红书等）

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 基础使用

```python
from pdf_processor import PDFProcessor
from card_generator import CardGenerator

# 1. 提取 PDF
processor = PDFProcessor("your_book.pdf")
chapters = processor.extract_chapters()

# 2. 生成知识卡片
generator = CardGenerator()
cards = generator.generate_cards(chapters)

# 3. 导出为图片
generator.export_images(cards, output_dir="./cards/")
```

## 📁 项目结构

```
pdf-to-knowledge-cards/
├── src/
│   ├── pdf_processor.py       # PDF 解析模块
│   ├── summarizer.py          # NLP 摘要模块
│   ├── card_generator.py      # 卡片生成模块
│   ├── templates/             # 卡片模板
│   │   ├── minimal.json
│   │   ├── mindmap.json
│   │   └── social_media.json
│   └── utils.py               # 工具函数
├── examples/
│   ├── example.py             # 使用示例
│   └── sample.pdf             # 示例 PDF
├── output/                    # 输出目录
│   └── cards/
├── tests/                     # 单元测试
├── requirements.txt
├── .gitignore
└── README.md
```

## 🔧 技术栈

| 功能 | 工具库 |
|------|--------|
| PDF 解析 | `pdfplumber` / `PyMuPDF` |
| 文本摘要 | `transformers` (Hugging Face) |
| NLP 处理 | `spaCy` |
| 图片生成 | `Pillow` / `reportlab` |
| 数据处理 | `pandas` |

## 📝 工作流程

```
PDF 文件
   ↓
[1] 文本提取 (pdf_processor.py)
   ↓
[2] 分章节/分段落
   ↓
[3] AI 摘要 & 关键词提取 (summarizer.py)
   ↓
[4] 构建知识图谱 (knowledge_graph.py)
   ↓
[5] 生成卡片 (card_generator.py)
   ↓
[6] 渲染为图片 (image_renderer.py)
   ↓
输出卡片 (PNG/JPG)
```

## 🎯 使用场景

- 📚 **学生**: 快速生成学习卡片
- 📖 **书评博主**: 生成可分享的读书笔记
- 🎓 **讲师**: 创建课程知识卡片
- 📱 **内容创作者**: 优化社交媒体分享

## ⚙️ 配置

编辑 `config.json` 自定义:
- 卡片模板样式
- AI 摘要长度
- 社交平台优化尺寸
- 输出格式

## 📊 输出格式

### 纯文本卡片 (Markdown)
```markdown
# 知识点：人工智能基础

**核心概念**: 机器学习是AI的重要分支

**来源**: 《深度学习入门》第5章，第45页

**关键词**: 机器学习、神经网络、算法

**思维导图**:
- AI
  ├── 机器学习
  │   ├── 监督学习
  │   └── 无监督学习
  └── 深度学习
```

### 视觉卡片 (PNG/JPG)
- 支持多种主题
- 自动排版
- 高清导出

## 📦 依赖版本

- Python >= 3.8
- pdfplumber >= 0.9.0
- transformers >= 4.30.0
- spacy >= 3.5.0
- pillow >= 9.0.0
- pandas >= 1.5.0

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 📞 联系方式

有任何问题？[提交 Issue](https://github.com/Rubyecust/pdf-to-knowledge-cards/issues)
