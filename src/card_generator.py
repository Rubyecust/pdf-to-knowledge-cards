"""
Knowledge Card Generator
生成纯文本和视觉卡片
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from datetime import datetime
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap


@dataclass
class KnowledgeCard:
    """知识卡片数据结构"""
    id: str
    title: str
    content: str
    keywords: List[str]
    source_page: int
    source_book: str
    mindmap_structure: Optional[Dict] = None
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()


class MarkdownCardGenerator:
    """生成 Markdown 格式的卡片"""
    
    def __init__(self, book_title: str = ""):
        self.book_title = book_title
    
    def generate_markdown(self, card: KnowledgeCard) -> str:
        """
        生成 Markdown 卡片
        
        Args:
            card: 知识卡片
            
        Returns:
            Markdown 文本
        """
        template = f"""# {card.title}

## 核心内容
{card.content}

## 关键词
{' | '.join([f'`{kw}`' for kw in card.keywords])}

## 来源信息
- **书籍**: {card.source_book or self.book_title}
- **页码**: 第 {card.source_page} 页
- **创建时间**: {card.created_at}

---
"""
        
        # 如果有思维导图结构
        if card.mindmap_structure:
            template += "\n## 思维导图\n"
            template += self._mindmap_to_markdown(card.mindmap_structure)
        
        return template
    
    @staticmethod
    def _mindmap_to_markdown(node: Dict, level: int = 0) -> str:
        """递归生成思维导图 Markdown"""
        indent = "  " * level
        text = f"{indent}- {node.get('name', '')}\n"
        
        for child in node.get('children', []):
            text += MarkdownCardGenerator._mindmap_to_markdown(child, level + 1)
        
        return text
    
    def save_markdown_cards(self, cards: List[KnowledgeCard], 
                           output_dir: str) -> List[str]:
        """
        保存多个 Markdown 卡片
        
        Args:
            cards: 卡片列表
            output_dir: 输出目录
            
        Returns:
            保存的文件路径列表
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        file_paths = []
        for i, card in enumerate(cards):
            filename = f"{i+1:03d}_{card.title.replace(' ', '_')}.md"
            filepath = output_path / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.generate_markdown(card))
            
            file_paths.append(str(filepath))
            print(f"✓ 保存卡片: {filename}")
        
        return file_paths


class VisualCardGenerator:
    """生成视觉卡片（图片）"""
    
    def __init__(self, template: str = "minimal"):
        """
        初始化视觉卡片生成器
        
        Args:
            template: 卡片模板 ('minimal', 'social', 'mindmap')
        """
        self.template = template
        self.colors = {
            'minimal': {
                'bg': (255, 255, 255),
                'title': (33, 33, 33),
                'text': (80, 80, 80),
                'accent': (52, 152, 219),
                'keywords': (149, 165, 166)
            },
            'social': {
                'bg': (240, 248, 255),
                'title': (25, 25, 112),
                'text': (70, 70, 70),
                'accent': (255, 140, 0),
                'keywords': (220, 20, 60)
            },
            'mindmap': {
                'bg': (245, 245, 245),
                'title': (44, 62, 80),
                'text': (52, 73, 94),
                'accent': (46, 204, 113),
                'keywords': (241, 196, 15)
            }
        }
    
    def generate_card_image(self, card: KnowledgeCard, 
                           width: int = 1080, height: int = 1350) -> Image.Image:
        """
        生成卡片图片
        
        Args:
            card: 知识卡片
            width: 图片宽度
            height: 图片高度
            
        Returns:
            PIL Image 对象
        """
        # 创建图片
        img = Image.new('RGB', (width, height), 
                       self.colors[self.template]['bg'])
        draw = ImageDraw.Draw(img)
        
        # 加载字体（使用系统字体）
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 36)
            text_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 22)
            small_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 16)
        except:
            # 如果系统字体不可用，使用默认字体
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        y_position = 40
        colors = self.colors[self.template]
        margin = 40
        max_width = width - 2 * margin
        
        # 1. 标题
        draw.text((margin, y_position), card.title, 
                 fill=colors['title'], font=title_font)
        y_position += 80
        
        # 2. 内容
        wrapped_text = textwrap.wrap(card.content, width=60)
        for line in wrapped_text[:8]:  # 限制行数
            draw.text((margin, y_position), line,
                     fill=colors['text'], font=text_font)
            y_position += 40
        
        y_position += 20
        
        # 3. 关键词
        draw.text((margin, y_position), "关键词:", 
                 fill=colors['accent'], font=text_font)
        y_position += 35
        
        keywords_text = " | ".join(card.keywords)
        wrapped_keywords = textwrap.wrap(keywords_text, width=70)
        for line in wrapped_keywords:
            draw.text((margin + 20, y_position), line,
                     fill=colors['keywords'], font=small_font)
            y_position += 30
        
        y_position += 30
        
        # 4. 来源信息
        draw.line([(margin, y_position), (width - margin, y_position)],
                 fill=colors['accent'], width=2)
        y_position += 20
        
        source_text = f"📖 {card.source_book} • 第 {card.source_page} 页"
        draw.text((margin, y_position), source_text,
                 fill=colors['text'], font=small_font)
        y_position += 35
        
        created_text = f"🕐 {card.created_at[:10]}"
        draw.text((margin, y_position), created_text,
                 fill=colors['text'], font=small_font)
        
        return img
    
    def generate_instagram_card(self, card: KnowledgeCard) -> Image.Image:
        """
        生成 Instagram 专用卡片 (1080x1350)
        """
        return self.generate_card_image(card, width=1080, height=1350)
    
    def generate_xiaohongshu_card(self, card: KnowledgeCard) -> Image.Image:
        """
        生成小红书专用卡片 (1080x1440)
        """
        return self.generate_card_image(card, width=1080, height=1440)
    
    def generate_twitter_card(self, card: KnowledgeCard) -> Image.Image:
        """
        生成 Twitter 专用卡片 (1200x675)
        """
        return self.generate_card_image(card, width=1200, height=675)
    
    def save_card_image(self, card: KnowledgeCard, 
                       output_path: str, 
                       platform: str = "instagram") -> str:
        """
        保存卡片图片
        
        Args:
            card: 知识卡片
            output_path: 输出路径
            platform: 平台 ('instagram', 'xiaohongshu', 'twitter')
            
        Returns:
            保存的文件路径
        """
        if platform == "instagram":
            img = self.generate_instagram_card(card)
        elif platform == "xiaohongshu":
            img = self.generate_xiaohongshu_card(card)
        elif platform == "twitter":
            img = self.generate_twitter_card(card)
        else:
            img = self.generate_card_image(card)
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        img.save(output_path, quality=95)
        print(f"✓ 保存图片卡片: {output_path}")
        
        return output_path
    
    def save_multiple_cards(self, cards: List[KnowledgeCard],
                           output_dir: str,
                           platform: str = "instagram") -> List[str]:
        """
        保存多个卡片图片
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        file_paths = []
        for i, card in enumerate(cards):
            filename = f"{i+1:03d}_{card.title.replace(' ', '_')}.png"
            filepath = output_path / filename
            
            self.save_card_image(card, str(filepath), platform)
            file_paths.append(str(filepath))
        
        return file_paths


class CardManager:
    """卡片管理器 - 统一接口"""
    
    def __init__(self, book_title: str = ""):
        self.book_title = book_title
        self.cards = []
        self.markdown_gen = MarkdownCardGenerator(book_title)
    
    def add_card(self, card: KnowledgeCard):
        """添加卡片"""
        self.cards.append(card)
    
    def save_all_cards(self, output_dir: str, 
                      formats: List[str] = ["markdown", "instagram"]):
        """
        保存所有卡片为多种格式
        
        Args:
            output_dir: 输出目录
            formats: 格式列表 ['markdown', 'instagram', 'xiaohongshu', 'twitter']
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 保存 Markdown
        if "markdown" in formats:
            markdown_dir = output_path / "markdown"
            self.markdown_gen.save_markdown_cards(self.cards, str(markdown_dir))
        
        # 保存图片
        for platform in ["instagram", "xiaohongshu", "twitter"]:
            if platform in formats:
                image_dir = output_path / platform
                visual_gen = VisualCardGenerator()
                visual_gen.save_multiple_cards(
                    self.cards, str(image_dir), platform
                )
    
    def export_json(self, output_path: str):
        """导出为 JSON"""
        cards_data = [asdict(card) for card in self.cards]
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(cards_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 导出 JSON: {output_path}")


# 使用示例
if __name__ == "__main__":
    # 创建示例卡片
    card = KnowledgeCard(
        id="card_001",
        title="人工智能基础",
        content="人工智能是计算机科学的一个分支，旨在研究和应用使计算机能够执行通常需要人类智能的任务的理论和方法。",
        keywords=["AI", "机器学习", "深度学习"],
        source_page=45,
        source_book="深度学习入门"
    )
    
    # 生成 Markdown
    md_gen = MarkdownCardGenerator("深度学习入门")
    markdown = md_gen.generate_markdown(card)
    print("=== Markdown 卡片 ===")
    print(markdown)
    
    # 生成图片
    visual_gen = VisualCardGenerator(template="minimal")
    img = visual_gen.generate_instagram_card(card)
    img.save("test_card.png")
    print("\n✓ 图片卡片已保存到: test_card.png")
