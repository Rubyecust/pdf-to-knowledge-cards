"""
Text Summarization Module
使用 NLP 提取关键信息和摘要
"""

import re
from typing import List, Dict, Tuple
from transformers import pipeline
import spacy
from nltk.tokenize import sent_tokenize
import warnings

warnings.filterwarnings('ignore')


class TextSummarizer:
    """文本摘要和关键词提取"""
    
    def __init__(self, model_name: str = "facebook/bart-large-cnn"):
        """
        初始化摘要模型
        
        Args:
            model_name: Hugging Face 模型名称
        """
        self.summarizer = pipeline("summarization", model=model_name)
        
        # 加载 spaCy 模型用于 NLP
        try:
            self.nlp = spacy.load("zh_core_web_sm")  # 中文模型
        except:
            try:
                self.nlp = spacy.load("en_core_web_sm")  # 英文模型
            except:
                print("⚠ spaCy 模型未安装，部分功能受限")
                self.nlp = None
    
    def summarize(self, text: str, max_length: int = 100, 
                  min_length: int = 30) -> str:
        """
        总结文本
        
        Args:
            text: 输入文本
            max_length: 最大长度（词数）
            min_length: 最小长度（词数）
            
        Returns:
            摘要文本
        """
        # 清理文本
        text = self._clean_text(text)
        
        if len(text.split()) < 50:
            return text  # 文本过短，直接返回
        
        try:
            summary = self.summarizer(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )
            return summary[0]['summary_text']
        except Exception as e:
            print(f"摘要生成失败: {e}")
            return text[:200]
    
    def extract_keywords(self, text: str, top_k: int = 5) -> List[str]:
        """
        提取关键词
        
        Args:
            text: 输入文本
            top_k: 返回的关键词数量
            
        Returns:
            关键词列表
        """
        text = self._clean_text(text)
        
        if not self.nlp:
            # 简单的基于频率的关键词提取
            words = text.lower().split()
            word_freq = {}
            for word in words:
                if len(word) > 2:  # 过滤短词
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            keywords = sorted(
                word_freq.items(),
                key=lambda x: x[1],
                reverse=True
            )[:top_k]
            return [kw[0] for kw in keywords]
        
        doc = self.nlp(text)
        
        # 提取命名实体和高频词
        entities = [ent.text for ent in doc.ents]
        
        # 简单的词频统计
        words = [token.text for token in doc 
                if not token.is_stop and token.is_alpha]
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        top_words = sorted(
            word_freq.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_k - len(entities)]
        
        keywords = entities + [w[0] for w in top_words]
        return keywords[:top_k]
    
    def extract_sentences(self, text: str, num_sentences: int = 3) -> List[str]:
        """
        提取最重要的句子
        
        Args:
            text: 输入文本
            num_sentences: 返回的句子数量
            
        Returns:
            句子列表
        """
        text = self._clean_text(text)
        
        try:
            sentences = sent_tokenize(text)
        except:
            sentences = text.split('。')
        
        if len(sentences) <= num_sentences:
            return sentences
        
        # 简单的句子评分（基于长度和关键词）
        keywords = self.extract_keywords(text, top_k=5)
        
        def score_sentence(sent: str) -> float:
            score = 0
            for keyword in keywords:
                score += sent.lower().count(keyword.lower())
            score += len(sent.split()) * 0.1  # 偏好较长的句子
            return score
        
        scored_sentences = [
            (sent, score_sentence(sent))
            for sent in sentences
        ]
        
        top_sentences = sorted(
            scored_sentences,
            key=lambda x: x[1],
            reverse=True
        )[:num_sentences]
        
        # 按原始顺序返回
        top_sentences = sorted(
            top_sentences,
            key=lambda x: sentences.index(x[0])
        )
        
        return [sent for sent, _ in top_sentences]
    
    def analyze_structure(self, text: str) -> Dict[str, any]:
        """
        分析文本结构
        
        Args:
            text: 输入文本
            
        Returns:
            结构分析字典
        """
        lines = text.split('\n')
        
        structure = {
            'total_lines': len(lines),
            'total_words': len(text.split()),
            'total_chars': len(text),
            'avg_line_length': len(text) / max(len(lines), 1),
            'paragraphs': len([l for l in lines if l.strip()]),
        }
        
        return structure
    
    @staticmethod
    def _clean_text(text: str) -> str:
        """清理文本"""
        # 移除特殊字符但保留标点
        text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)
        # 移除多余空白
        text = re.sub(r'\s+', ' ', text)
        return text.strip()


class KnowledgeExtractor:
    """知识提取 - 结构化信息"""
    
    def __init__(self):
        self.summarizer = TextSummarizer()
    
    def extract_knowledge_points(self, text: str) -> List[Dict]:
        """
        提取知识点
        
        Returns:
            知识点列表，每个包含 {title, content, keywords, source_page}
        """
        # 分句
        sentences = text.split('。')
        
        knowledge_points = []
        for i, sent in enumerate(sentences):
            if len(sent.strip()) < 20:
                continue
            
            keywords = self.summarizer.extract_keywords(sent, top_k=3)
            
            knowledge_points.append({
                'content': sent.strip(),
                'keywords': keywords,
                'position': i,
            })
        
        return knowledge_points
    
    def create_mindmap_structure(self, 
                                 title: str,
                                 sections: List[Dict]) -> Dict:
        """
        创建思维导图结构
        
        Args:
            title: 标题
            sections: 章节列表
            
        Returns:
            思维导图结构 (树形字典)
        """
        mindmap = {
            'name': title,
            'children': []
        }
        
        for section in sections:
            branch = {
                'name': section.get('title', ''),
                'children': []
            }
            
            # 提取该部分的关键词作为子节点
            content = section.get('content', '')
            keywords = self.summarizer.extract_keywords(content, top_k=3)
            
            for keyword in keywords:
                branch['children'].append({
                    'name': keyword,
                    'children': []
                })
            
            mindmap['children'].append(branch)
        
        return mindmap


# 使用示例
if __name__ == "__main__":
    sample_text = """
    人工智能是计算机科学的一个分支。它试图了解智能的实质，
    并生产出一种新的能以人类智能相似的方式做出反应的智能机器。
    """
    
    summarizer = TextSummarizer()
    
    # 摘要
    summary = summarizer.summarize(sample_text)
    print(f"摘要: {summary}\n")
    
    # 关键词
    keywords = summarizer.extract_keywords(sample_text)
    print(f"关键词: {keywords}\n")
    
    # 句子提取
    sentences = summarizer.extract_sentences(sample_text)
    print(f"主要句子: {sentences}\n")
    
    # 结构分析
    structure = summarizer.analyze_structure(sample_text)
    print(f"结构分析: {structure}")
