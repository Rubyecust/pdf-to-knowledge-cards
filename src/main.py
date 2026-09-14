#!/usr/bin/env python3
"""
PDF to Knowledge Cards - Main Program
主程序：完整的工作流程
"""

import os
import json
import argparse
from pathlib import Path
from typing import List

from pdf_processor import PDFProcessor
from summarizer import TextSummarizer, KnowledgeExtractor
from card_generator import KnowledgeCard, MarkdownCardGenerator, VisualCardGenerator, CardManager


class Pipeline:
    """完整的处理流程"""
    
    def __init__(self, config_path: str = "config.json"):
        """
        初始化流程
        
        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.summarizer = TextSummarizer()
        self.extractor = KnowledgeExtractor()
    
    @staticmethod
    def _load_config(config_path: str) -> dict:
        """加载配置文件"""
        if not os.path.exists(config_path):
            print(f"⚠ 配置文件不存在: {config_path}")
            return {}
        
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def process_pdf(self, pdf_path: str, output_dir: str = None) -> bool:
        """
        处理 PDF 文件的完整流程
        
        Args:
            pdf_path: PDF 文件路径
            output_dir: 输出目录
            
        Returns:
            是否成功
        """
        if not os.path.exists(pdf_path):
            print(f"✗ PDF 文件不存在: {pdf_path}")
            return False
        
        # 设置输出目录
        if output_dir is None:
            output_dir = self.config.get('output', {}).get('base_dir', './output')
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        print(f"\n{'='*60}")
        print(f"开始处理 PDF: {pdf_path}")
        print(f"输出目录: {output_dir}")
        print(f"{'='*60}\n")
        
        try:
            # 1. 提取 PDF
            print("[1/5] 提取 PDF 内容...")
            with PDFProcessor(pdf_path) as processor:
                # 获取元数据
                metadata = processor.extract_metadata()
                book_title = metadata.get('title', 'Unknown Book')
                print(f"  📖 书名: {book_title}")
                print(f"  📄 页数: {metadata.get('pages')}")
                
                # 提取文本
                full_text = processor.extract_text()
                print(f"  ✓ 提取文本长度: {len(full_text)} 字")
            
            # 2. 提取知识点
            print("\n[2/5] 提取知识点...")
            knowledge_points = self.extractor.extract_knowledge_points(full_text)
            print(f"  ✓ 提取到 {len(knowledge_points)} 个知识点")
            
            # 3. 生成卡片
            print("\n[3/5] 生成卡片...")
            cards = []
            for i, point in enumerate(knowledge_points[:20]):  # 限制数量
                # 摘要
                summary = self.summarizer.summarize(
                    point['content'],
                    max_length=self.config['text_summarization']['max_length'],
                    min_length=self.config['text_summarization']['min_length']
                )
                
                # 创建卡片
                card = KnowledgeCard(
                    id=f"card_{i+1:03d}",
                    title=point['content'][:50],  # 前50个字作为标题
                    content=summary,
                    keywords=point['keywords'],
                    source_page=point.get('position', 0) + 1,
                    source_book=book_title
                )
                cards.append(card)
            
            print(f"  ✓ 生成 {len(cards)} 张卡片")
            
            # 4. 导出卡片
            print("\n[4/5] 导出卡片...")
            manager = CardManager(book_title)
            for card in cards:
                manager.add_card(card)
            
            formats = self.config.get('output', {}).get('formats', ['markdown', 'instagram'])
            manager.save_all_cards(output_dir, formats)
            print(f"  ✓ 导出格式: {', '.join(formats)}")
            
            # 5. 生成总结
            print("\n[5/5] 生成处理总结...")
            summary_file = Path(output_dir) / "summary.json"
            summary_data = {
                'book_title': book_title,
                'total_cards': len(cards),
                'formats': formats,
                'output_dir': str(output_dir)
            }
            
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary_data, f, ensure_ascii=False, indent=2)
            
            print(f"  ✓ 总结已保存: {summary_file}")
            
            print(f"\n{'='*60}")
            print(f"✓ 处理完成！")
            print(f"{'='*60}\n")
            
            return True
        
        except Exception as e:
            print(f"\n✗ 处理过程中出错: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='PDF to Knowledge Cards - 将 PDF 转换为知识卡片'
    )
    parser.add_argument(
        'pdf_path',
        help='PDF 文件路径'
    )
    parser.add_argument(
        '-o', '--output',
        help='输出目录',
        default=None
    )
    parser.add_argument(
        '-c', '--config',
        help='配置文件路径',
        default='config.json'
    )
    
    args = parser.parse_args()
    
    # 创建流程
    pipeline = Pipeline(args.config)
    
    # 处理 PDF
    success = pipeline.process_pdf(args.pdf_path, args.output)
    
    exit(0 if success else 1)


if __name__ == '__main__':
    main()
