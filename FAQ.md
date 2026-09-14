# 常见问题 (FAQ)

## 安装相关

### Q: 安装过程中出现 "pip: command not found"

**A:** 这通常意味着:
1. Python 没有正确安装
2. Python 没有添加到系统 PATH

解决方案:
- 重新安装 Python，勾选 "Add Python to PATH"
- 使用完整路径: `python -m pip install -r requirements.txt`

### Q: 安装依赖时很慢

**A:** 可以尝试:
1. 使用国内源
   ```bash
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```
2. 升级 pip
   ```bash
   pip install --upgrade pip
   ```

### Q: 某个依赖安装失败

**A:** 尝试:
1. 单独安装该依赖
   ```bash
   pip install pdfplumber --no-cache-dir
   ```
2. 检查是否需要 C++ 编译工具 (对于某些包)
3. 查看该包的 GitHub issue

---

## 使用相关

### Q: 如何处理密码保护的 PDF?

**A:** 目前工具不支持加密 PDF。解决方案:
1. 使用 Adobe Reader 或其他工具解除密码保护
2. 或者在代码中修改 `pdf_processor.py`:
   ```python
   self.pdf = pdfplumber.open(self.pdf_path, password="your_password")
   ```

### Q: 如何提取扫描版 PDF (图片格式)?

**A:** 扫描版 PDF 需要 OCR 处理。解决方案:
1. 使用 Tesseract OCR
   ```bash
   pip install pytesseract pillow
   ```
2. 修改 `pdf_processor.py` 添加 OCR 功能
3. 或使用在线 OCR 服务先转换成文本

### Q: 生成的卡片数量太少

**A:** 可能的原因:
1. PDF 内容不足 - 检查 PDF 质量
2. 知识点提取设置过严格 - 修改 `summarizer.py`
3. 尝试增加 `config.json` 中的关键词数量

### Q: 如何自定义卡片样式?

**A:** 修改 `src/card_generator.py` 中的:
1. `colors` 字典 - 调整颜色
2. `generate_card_image()` - 修改排版
3. 字体大小和位置参数

---

## 性能相关

### Q: 处理大型 PDF 时很慢

**A:** 优化建议:
1. 分章节处理
   ```python
   text = processor.extract_text(page_range=(0, 100))
   ```
2. 减少生成的卡片数量
3. 降低摘要长度
4. 使用更快的 NLP 模型

### Q: 内存使用过多

**A:** 解决方案:
1. 及时释放资源
   ```python
   processor.close()
   ```
2. 处理较小的 PDF 文件
3. 减少同时加载的数据

### Q: GPU 加速不可用

**A:** 这通常不是问题，CPU 处理也足够快。如需 GPU:
1. 确保安装了 `torch` 的 GPU 版本
2. 检查 NVIDIA 驱动程序
3. 修改 `summarizer.py` 使用 GPU

---

## 输出相关

### Q: 生成的图片中文显示乱码

**A:** 这是字体问题。解决方案:

**Windows**:
```python
# 在 card_generator.py 中修改
title_font = ImageFont.truetype("C:\\Windows\\Fonts\\msyh.ttc", 36)
```

**macOS**:
```python
title_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 36)
```

**Linux**:
```bash
sudo apt-get install fonts-wqy-microhei
```

### Q: 图片生成失败

**A:** 检查:
1. 输出目录是否存在且有写权限
2. 磁盘空间是否充足
3. 图片尺寸设置是否合理
4. Pillow 是否正确安装

### Q: 如何修改输出图片尺寸?

**A:** 修改 `config.json`:
```json
{
  "image_export": {
    "platforms": {
      "custom": {"width": 1000, "height": 1500}
    }
  }
}
```

### Q: 如何生成 JPG 而不是 PNG?

**A:** 修改 `config.json`:
```json
{
  "image_export": {
    "format": "JPG",
    "quality": 85
  }
}
```

---

## 功能相关

### Q: 支持哪些语言?

**A:** 目前支持:
- 中文 (需要安装 `zh_core_web_sm`)
- 英文 (需要安装 `en_core_web_sm`)
- 其他语言需要下载相应的 spaCy 模型

### Q: 支持哪些 PDF 格式?

**A:** 支持:
- 标准文本 PDF ✓
- 扫描版 PDF ✗ (需要 OCR)
- 加密 PDF ✗ (需要密码)
- 特殊格式 PDF (可能不完全支持)

### Q: 如何添加自定义知识点提取规则?

**A:** 修改 `src/summarizer.py` 中的 `extract_knowledge_points()` 方法

### Q: 支持思维导图导出吗?

**A:** 目前支持 JSON 格式的思维导图数据。要导出为其他格式:
1. 使用在线工具转换 JSON
2. 或集成第三方库如 `mindmaps`

---

## 数据隐私相关

### Q: 数据是否安全?

**A:** 是的:
- 所有处理在本地进行
- 不上传任何数据到服务器
- 除非你手动使用在线模型

### Q: 如何处理敏感文件?

**A:** 建议:
1. 使用本地模型 (避免云 API)
2. 在隔离环境运行
3. 处理完成后删除中间文件

---

## 贡献相关

### Q: 如何报告 Bug?

**A:** 提交 Issue 包含:
1. Python 版本
2. 操作系统
3. 错误信息
4. 复现步骤

### Q: 如何提交代码改进?

**A:** 
1. Fork 项目
2. 创建功能分支
3. 提交 Pull Request

### Q: 如何翻译文档?

**A:** 
1. Fork 项目
2. 在 `docs/i18n/` 中添加翻译
3. 提交 Pull Request

---

## 其他

### Q: 可以用于商业用途吗?

**A:** 可以。项目使用 MIT License，允许商业使用。

### Q: 有更新吗?

**A:** 
- ⭐ Star 项目以获取更新通知
- 👁️ Watch 项目以接收新版本提醒

### Q: 我想要某个新功能

**A:** 
1. 在 GitHub 创建 Feature Request
2. 或自己实现并提交 Pull Request
3. 或开启讨论获取社区反馈

---

## 获得进一步帮助

- 📖 查看项目文档
- 💬 开启 GitHub Discussions
- 📧 联系项目维护者
- 🐛 提交 Bug Report

---

**有其他问题？欢迎在 GitHub 提问！** 😊
