"""
BGE 中文向量嵌入服务
"""
from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

# 全局模型实例
_model = None


def get_embedding_model():
    """获取或初始化 BGE 模型"""
    global _model
    if _model is None:
        print("正在加载 BGE 中文嵌入模型...")
        # 使用 BGE-large-zh-v1.5，针对中文优化
        _model = SentenceTransformer('BAAI/bge-large-zh-v1.5')
        print("BGE 模型加载完成")
    return _model


def generate_embedding(text: str) -> List[float]:
    """
    为单个文本生成向量嵌入

    Args:
        text: 要嵌入的文本

    Returns:
        向量列表
    """
    model = get_embedding_model()
    # BGE 模型建议对查询添加前缀
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()


def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """
    为多个文本生成向量嵌入

    Args:
        texts: 文本列表

    Returns:
        向量列表的列表
    """
    model = get_embedding_model()
    embeddings = model.encode(texts, normalize_embeddings=True)
    return embeddings.tolist()


def generate_query_embedding(query: str) -> List[float]:
    """
    为搜索查询生成向量嵌入
    BGE 模型建议对查询文本添加特定前缀以提高检索效果

    Args:
        query: 搜索查询文本

    Returns:
        向量列表
    """
    model = get_embedding_model()
    # BGE 推荐的查询前缀
    query_with_prefix = f"为这个句子生成表示以用于检索相关文章：{query}"
    embedding = model.encode(query_with_prefix, normalize_embeddings=True)
    return embedding.tolist()
