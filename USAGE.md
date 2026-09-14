# 使用指南 (Usage Guide)

## 目录

1. [基本用法](#基本用法)
2. [命令行使用](#命令行使用)
3. [Python API 使用](#python-api-使用)
4. [配置说明](#配置说明)
5. [常见场景](#常见场景)

---

## 基本用法

### 方式 1: 命令行使用 (最简单)

```bash
python src/main.py your_book.pdf
```

输出会保存到 `./output` 目录

### 方式 2: 指定输出目录

```bash
python src/main.py your_book.pdf -o ./my_cards
```

### 方式 3: 使用自定义配置

```bash
python src/main.py your_book.pdf -c my_config.json -o ./my_cards
```

---

## 命令行使用

### 帮助信息

```bash
python src/main.py --help
```

### 参数说明

| 参数 | 简写 | 说明 | 示例 |
|------|------|------|------|
| `pdf_path` | - | PDF 文件路径 (必需) | `book.pdf` |
| `--output` | `-o` | 输出目录 | `-o ./cards` |
| `--config` | `-c` | 配置文件路径 | `-c config.json` |

---

## Python API 使用

### 基础示例

```python
from src.pdf_processor import PDFProcessor
from src.card_generator import CardManager
from src.summarizer import TextSummarizer

# 1. 提取 PDF
with PDFProcessor('book.pdf') as processor:
    text = processor.extract_text()
    metadata = processor.extract_metadata()
    print(f"书籍: {metadata['title']}")

# 2. 生成摘要
summarizer = TextSummarizer()
summary = summarizer.summarize(text)
keywords = summarizer.extract_keywords(text, top_k=5)
print(f"摘要: {summary}")
print(f"关键词: {keywords}")

# 3. 创建卡片
from src.card_generator import KnowledgeCard

card = KnowledgeCard(
    id="card_001",
    title="核心概念",
    content=summary,
    keywords=keywords,
    source_page=1,
    source_book=metadata['title']
)

# 4. 保存卡片
manager = CardManager(metadata['title'])
manager.add_card(card)
manager.save_all_cards(
    'output',
    formats=['markdown', 'instagram', 'xiaohongshu']
)
```

### 高级用法

#### 处理多个 PDF

```python
from pathlib import Path

pdf_dir = './books'
for pdf_file in Path(pdf_dir).glob('*.pdf'):
    processor = PDFProcessor(str(pdf_file))
    text = processor.extract_text()
    # 处理文本...
```

#### 自定义卡片样式

```python
from src.card_generator import VisualCardGenerator

# 创建自定义生成器
visual_gen = VisualCardGenerator(template="social")

# 生成特定平台的卡片
instagram_img = visual_gen.generate_instagram_card(card)
xiaohongshu_img = visual_gen.generate_xiaohongshu_card(card)
twitter_img = visual_gen.generate_twitter_card(card)

# 保存
instagram_img.save('card_instagram.png')
xiaohongshu_img.save('card_xiaohongshu.png')
twitter_img.save('card_twitter.png')
```

#### 提取特定页码范围

```python
with PDFProcessor('book.pdf') as processor:
    # 只提取第 10-50 页
    text = processor.extract_text(page_range=(10, 50))
```

---

## 配置说明

### config.json 详解

```json
{
  "pdf_processing": {
    "extract_text": true,        // 是否提取文本
    "extract_tables": true,      // 是否提取表格
    "extract_images": false,     // 是否提取图片
    "language": "zh"             // 语言: "zh" 中文, "en" 英文
  },
  "text_summarization": {
    "model": "facebook/bart-large-cnn",  // 摘要模型
    "max_length": 100,           // 摘要最大长度
    "min_length": 30,            // 摘要最小长度
    "enable_keywords": true,     // 是否提取关键词
    "num_keywords": 5            // 关键词数量
  },
  "card_generation": {
    "templates": ["minimal", "social", "mindmap"],
    "default_template": "minimal"
  },
  "image_export": {
    "platforms": {
      "instagram": {"width": 1080, "height": 1350},
      "xiaohongshu": {"width": 1080, "height": 1440},
      "twitter": {"width": 1200, "height": 675}
    },
    "quality": 95,               // 图片质量 (1-100)
    "format": "PNG"              // 格式: PNG, JPG
  },
  "output": {
    "base_dir": "./output",      // 输出基础目录
    "create_subdirs": true,      // 是否创建子目录
    "formats": ["markdown", "instagram", "xiaohongshu"]
  }
}
```

### 自定义配置示例

```json
{
  "text_summarization": {
    "max_length": 150,
    "min_length": 50,
    "num_keywords": 8
  },
  "output": {
    "formats": ["markdown", "twitter"]  // 只输出这两种格式
  }
}
```

---

## 常见场景

### 场景 1: 快速生成学习卡片

```bash
# 最简单的方式
python src/main.py textbook.pdf
```

输出会包含:
- `output/markdown/` - Markdown 格式的卡片
- `output/instagram/` - Instagram 格式的图片
- `output/xiaohongshu/` - 小红书格式的图片

### 场景 2: 为内容创作优化

编辑 `config.json`:
```json
{
  "output": {
    "formats": ["instagram", "xiaohongshu", "twitter"]
  },
  "text_summarization": {
    "num_keywords": 8
  }
}
```

然后运行:
```bash
python src/main.py book.pdf
```

### 场景 3: 批量处理多个 PDF

创建脚本 `batch_process.py`:
```python
from pathlib import Path
from src.main import Pipeline

pipeline = Pipeline()

for pdf_file in Path('./books').glob('*.pdf'):
    print(f"处理: {pdf_file.name}")
    pipeline.process_pdf(str(pdf_file), f"./output/{pdf_file.stem}")
```

运行:
```bash
python batch_process.py
```

### 场景 4: 只生成 Markdown 卡片

编辑 `config.json`:
```json
{
  "output": {
    "formats": ["markdown"]
  }
}
```

### 场景 5: 自定义输出目录结构

```python
from src.card_generator import CardManager

manager = CardManager('My Book')
# ... 添加卡片 ...

# 为每个平台创建单独的输出目录
manager.save_all_cards(
    './output/my_book/cards',
    formats=['markdown', 'instagram', 'xiaohongshu', 'twitter']
)
```

---

## 输出说明

### 目录结构

```
output/
├── markdown/
│   ├── 001_知识点1.md
│   ├── 002_知识点2.md
│   └── ...
├── instagram/
│   ├── 001_知识点1.png
│   ├── 002_知识点2.png
│   └── ...
├── xiaohongshu/
│   └── ...
└── summary.json
```

### 文件格式

**Markdown 文件示例**:
```markdown
# 知识点标题

## 核心内容
具体的知识点内容描述...

## 关键词
`关键词1` | `关键词2` | `关键词3`

## 来源信息
- **书籍**: 书名
- **页码**: 第 X 页
- **创建时间**: 日期
```

**JSON 总结文件示例**:
```json
{
  "book_title": "书籍名称",
  "total_cards": 20,
  "formats": ["markdown", "instagram"],
  "output_dir": "./output"
}
```

---

## 性能优化

### 处理大型 PDF

对于超过 500 页的 PDF:

1. **分割处理**:
   ```python
   with PDFProcessor('large_book.pdf') as processor:
       # 分章节处理
       text_1 = processor.extract_text(page_range=(0, 100))
       text_2 = processor.extract_text(page_range=(100, 200))
   ```

2. **降低摘要质量以提高速度**:
   ```json
   {
     "text_summarization": {
       "max_length": 50,
       "min_length": 20
     }
   }
   ```

### 节省内存

```python
# 处理完后立即关闭
processor = PDFProcessor('book.pdf')
text = processor.extract_text()
processor.close()  # 释放内存
```

---

## 更多帮助

- 📖 查看 [README.md](README.md) 了解项目概览
- 🐛 遇到问题? [提交 Issue](https://github.com/Rubyecust/pdf-to-knowledge-cards/issues)
- 💡 有建议? [开启讨论](https://github.com/Rubyecust/pdf-to-knowledge-cards/discussions)

---

**祝你使用愉快！** 🚀
