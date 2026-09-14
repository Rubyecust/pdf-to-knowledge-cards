"""
工具函数模块
"""

import os
from pathlib import Path
from typing import List, Dict
import json


class DirectoryManager:
    """目录管理工具"""
    
    @staticmethod
    def ensure_dir(path: str) -> str:
        """确保目录存在"""
        Path(path).mkdir(parents=True, exist_ok=True)
        return path
    
    @staticmethod
    def get_files(directory: str, extension: str = None) -> List[str]:
        """获取目录下的文件"""
        files = []
        for file in Path(directory).iterdir():
            if file.is_file():
                if extension is None or file.suffix == extension:
                    files.append(str(file))
        return files


class ConfigManager:
    """配置文件管理"""
    
    @staticmethod
    def load_json(path: str) -> dict:
        """加载 JSON 配置文件"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return {}
    
    @staticmethod
    def save_json(data: dict, path: str) -> bool:
        """保存 JSON 配置文件"""
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存配置文件失败: {e}")
            return False


class TextProcessor:
    """文本处理工具"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """清理文本"""
        # 移除多余空白
        lines = [line.strip() for line in text.split('\n')]
        # 移除空行
        lines = [line for line in lines if line]
        return '\n'.join(lines)
    
    @staticmethod
    def truncate_text(text: str, max_length: int) -> str:
        """截断文本"""
        if len(text) <= max_length:
            return text
        return text[:max_length] + "..."
    
    @staticmethod
    def split_paragraphs(text: str) -> List[str]:
        """分割段落"""
        paragraphs = text.split('\n\n')
        return [p.strip() for p in paragraphs if p.strip()]


class Logger:
    """简单的日志记录"""
    
    @staticmethod
    def info(message: str):
        print(f"[INFO] {message}")
    
    @staticmethod
    def success(message: str):
        print(f"[✓] {message}")
    
    @staticmethod
    def warning(message: str):
        print(f"[⚠] {message}")
    
    @staticmethod
    def error(message: str):
        print(f"[✗] {message}")
