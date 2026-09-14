#!/usr/bin/env python3
"""
快速开始示例
展示如何使用 PDF to Knowledge Cards
"""

import sys
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from card_generator import KnowledgeCard, MarkdownCardGenerator, VisualCardGenerator
from summarizer import TextSummarizer


def example_1_basic_card():
    """示例 1: 创建基础卡片"""
    print("\n" + "="*60)
    print("示例 1: 创建基础卡片")
    print("="*60 + "\n")
    
    # 创建一张卡片
    card = KnowledgeCard(
        id="example_001",
        title="机器学习基础",
        content="监督学习是指在有标签数据的指导下进行训练，模型学习输入和输出之间的映射关系。",
        keywords=["机器学习", "监督学习", "训练"],
        source_page=45,
        source_book="深度学习入门"
    )
    
    # 生成 Markdown
    md_gen = MarkdownCardGenerator("深度学习入门")
    markdown = md_gen.generate_markdown(card)
    
    print("生成的 Markdown 卡片:")
    print(markdown)
    
    return card


def example_2_visual_card(card):
    """示例 2: 生成视觉卡片"""
    print("\n" + "="*60)
    print("示例 2: 生成视觉卡片")
    print("="*60 + "\n")
    
    # 生成图片卡片
    visual_gen = VisualCardGenerator(template="minimal")
    
    # Instagram 格式
    print("生成 Instagram 格式卡片 (1080x1350)...")
    visual_gen.save_card_image(
        card,
        "output/example_instagram.png",
        platform="instagram"
    )
    
    # 小红书格式
    print("生成小红书格式卡片 (1080x1440)...")
    visual_gen.save_card_image(
        card,
        "output/example_xiaohongshu.png",
        platform="xiaohongshu"
    )
    
    # Twitter 格式
    print("生成 Twitter 格式卡片 (1200x675)...")
    visual_gen.save_card_image(
        card,
        "output/example_twitter.png",
        platform="twitter"
    )
    
    print("\n✓ 卡片已保存到 output/ 目录")


def example_3_summarization():
    """示例 3: 文本摘要和关键词提取"""
    print("\n" + "="*60)
    print("示例 3: 文本摘要和关键词提取")
    print("="*60 + "\n")
    
    sample_text = """
    深度学习是机器学习的一个分支，它使用人工神经网络来模仿人脑的学习过程。
    深度学习在计算机视觉、自然语言处理和语音识别等领域取得了巨大的成功。
    神经网络由多个层次组成，每个层次包含多个神经元，这些神经元通过权重和偏置进行连接。
    通过反向传播算法，我们可以更新权重和偏置，使得模型的预测更加准确。
    """
    
    summarizer = TextSummarizer()
    
    # 摘要
    print("原始文本:")
    print(sample_text)
    
    print("\n摘要结果:")
    summary = summarizer.summarize(sample_text, max_length=50, min_length=20)
    print(summary)
    
    # 关键词
    print("\n关键词提取:")
    keywords = summarizer.extract_keywords(sample_text, top_k=5)
    print(f"关键词: {', '.join(keywords)}")
    
    # 文本结构
    print("\n文本结构分析:")
    structure = summarizer.analyze_structure(sample_text)
    for key, value in structure.items():
        print(f"  {key}: {value}")


def example_4_batch_cards():
    """示例 4: 批量生成卡片"""
    print("\n" + "="*60)
    print("示例 4: 批量生成卡片")
    print("="*60 + "\n")
    
    from card_generator import CardManager
    
    # 创建多张卡片
    cards_data = [
        {
            "title": "神经网络基础",
            "content": "神经网络是由大量的人工神经元相互连接而成的网络",
            "keywords": ["神经元", "连接", "网络"]
        },
        {
            "title": "卷积神经网络",
            "content": "CNN 在图像识别任务中表现优异，通过卷积操作提取特征",
            "keywords": ["CNN", "卷积", "图像识别"]
        },
        {
            "title": "循环神经网络",
            "content": "RNN 适合处理序列数据，具有记忆功能",
            "keywords": ["RNN", "序列", "记忆"]
        }
    ]
    
    manager = CardManager("深度学习教程")
    
    for i, data in enumerate(cards_data):
        card = KnowledgeCard(
            id=f"batch_{i+1:03d}",
            title=data["title"],
            content=data["content"],
            keywords=data["keywords"],
            source_page=10 + i,
            source_book="深度学习教程"
        )
        manager.add_card(card)
    
    # 保存所有格式
    print(f"生成 {len(cards_data)} 张卡片...")
    manager.save_all_cards(
        "output/batch_example",
        formats=["markdown", "instagram", "xiaohongshu"]
    )
    
    print("✓ 批量卡片已保存")


def main():
    """主函数"""
    print("\n" + "="*60)
    print("PDF to Knowledge Cards - 快速开始示例")
    print("="*60)
    
    # 创建输出目录
    Path("output").mkdir(exist_ok=True)
    
    try:
        # 运行示例
        card = example_1_basic_card()
        example_2_visual_card(card)
        example_3_summarization()
        example_4_batch_cards()
        
        print("\n" + "="*60)
        print("✓ 所有示例运行完成！")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ 示例运行过程中出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
