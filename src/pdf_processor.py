"""
PDF Processing Module
提取 PDF 文本、结构、表格等内容
"""

import pdfplumber
import re
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class TextBlock:
    """文本块数据结构"""
    content: str
    page: int
    position: Tuple[float, float]  # (x, y)
    is_heading: bool = False
    heading_level: int = 0  # 1=H1, 2=H2, etc.


@dataclass
class Chapter:
    """章节数据结构"""
    title: str
    page_start: int
    page_end: int
    sections: List[Dict]  # 包含标题和内容


class PDFProcessor:
    """PDF 处理器 - 解析和提取 PDF 内容"""
    
    def __init__(self, pdf_path: str):
        """
        初始化 PDF 处理器
        
        Args:
            pdf_path: PDF 文件路径
        """
        self.pdf_path = pdf_path
        self.pdf = None
        self.text_blocks = []
        self._load_pdf()
    
    def _load_pdf(self):
        """加载 PDF 文件"""
        try:
            self.pdf = pdfplumber.open(self.pdf_path)
            print(f"✓ PDF 加载成功: {self.pdf_path}")
            print(f"  总页数: {len(self.pdf.pages)}")
        except Exception as e:
            print(f"✗ PDF 加载失败: {e}")
            raise
    
    def extract_text(self, page_range: Tuple[int, int] = None) -> str:
        """
        提取所有文本
        
        Args:
            page_range: (start, end) 页码范围，None 表示全部
            
        Returns:
            提取的文本
        """
        if not self.pdf:
            return ""
        
        start = page_range[0] if page_range else 0
        end = page_range[1] if page_range else len(self.pdf.pages)
        
        text = ""
        for page_num in range(start, min(end, len(self.pdf.pages))):
            page = self.pdf.pages[page_num]
            text += f"\n--- Page {page_num + 1} ---\n"
            text += page.extract_text()
        
        return text
    
    def extract_chapters(self) -> List[Chapter]:
        """
        尝试识别并提取章节
        基于常见的标题模式（如 "第X章", "Chapter X", etc.）
        
        Returns:
            章节列表
        """
        chapters = []
        current_chapter = None
        chapter_pattern = re.compile(
            r'(第\s*[一二三四五六七八九十百千万零\d]+\s*章|Chapter\s*\d+|第\s*\d+\s*部分)',
            re.IGNORECASE
        )
        
        for page_num, page in enumerate(self.pdf.pages):
            text = page.extract_text()
            lines = text.split('\n')
            
            for line in lines:
                # 检测章节标题
                if chapter_pattern.search(line):
                    if current_chapter:
                        chapters.append(current_chapter)
                    current_chapter = Chapter(
                        title=line.strip(),
                        page_start=page_num,
                        page_end=page_num,
                        sections=[]
                    )
                elif current_chapter:
                    current_chapter.page_end = page_num
        
        if current_chapter:
            chapters.append(current_chapter)
        
        return chapters
    
    def extract_tables(self, page_num: int = None) -> List[Dict]:
        """
        提取表格
        
        Args:
            page_num: 页码（None 表示所有页）
            
        Returns:
            表格列表
        """
        tables = []
        
        if page_num is not None:
            pages = [self.pdf.pages[page_num]]
        else:
            pages = self.pdf.pages
        
        for idx, page in enumerate(pages):
            page_tables = page.extract_tables()
            for table in page_tables:
                tables.append({
                    'page': idx,
                    'data': table
                })
        
        return tables
    
    def extract_metadata(self) -> Dict:
        """
        提取 PDF 元数据
        
        Returns:
            元数据字典
        """
        return {
            'title': self.pdf.metadata.get('Title', 'Unknown'),
            'author': self.pdf.metadata.get('Author', 'Unknown'),
            'subject': self.pdf.metadata.get('Subject', ''),
            'pages': len(self.pdf.pages),
        }
    
    def extract_text_blocks(self) -> List[TextBlock]:
        """
        提取文本块并保留位置信息
        
        Returns:
            文本块列表
        """
        blocks = []
        
        for page_num, page in enumerate(self.pdf.pages):
            # 获取页面文本和位置
            text_dict = page.extract_text_dict()
            
            if 'blocks' in text_dict or 'lines' in text_dict:
                for block in text_dict.get('blocks', []):
                    if 'lines' in block:
                        for line in block['lines']:
                            x0 = line.get('x0', 0)
                            top = line.get('top', 0)
                            text = ''.join([span.get('text', '') 
                                          for span in line.get('spans', [])])
                            
                            if text.strip():
                                blocks.append(TextBlock(
                                    content=text.strip(),
                                    page=page_num,
                                    position=(x0, top)
                                ))
        
        return blocks
    
    def close(self):
        """关闭 PDF 文件"""
        if self.pdf:
            self.pdf.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# 使用示例
if __name__ == "__main__":
    # 示例用法
    processor = PDFProcessor("sample.pdf")
    
    # 提取文本
    text = processor.extract_text()
    print(f"提取的文本长度: {len(text)}")
    
    # 提取章节
    chapters = processor.extract_chapters()
    print(f"检测到 {len(chapters)} 个章节")
    
    # 提取表格
    tables = processor.extract_tables()
    print(f"检测到 {len(tables)} 个表格")
    
    # 提取元数据
    metadata = processor.extract_metadata()
    print(f"PDF 信息: {metadata}")
    
    processor.close()
