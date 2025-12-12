"""
语义搜索服务
"""
from typing import List, Tuple
from sqlalchemy.orm import Session
from database import get_article_collection
from services.embedding import generate_query_embedding, generate_embedding
from models import Article


def add_article_to_index(article_id: int, title: str, full_text: str, keywords: List[str], ai_summary: str):
    """
    将文章添加到向量索引

    Args:
        article_id: 文章ID
        title: 标题
        full_text: 全文
        keywords: 关键词列表
        ai_summary: AI摘要
    """
    collection = get_article_collection()

    # 组合文本用于生成嵌入向量
    # 标题和关键词权重更高，重复添加
    combined_text = f"{title} {title} {' '.join(keywords)} {' '.join(keywords)} {ai_summary} {full_text[:2000]}"

    # 生成向量
    embedding = generate_embedding(combined_text)

    # 添加到 ChromaDB
    collection.add(
        ids=[str(article_id)],
        embeddings=[embedding],
        metadatas=[{"article_id": article_id}],
        documents=[combined_text[:1000]]  # 存储部分文本用于调试
    )

    print(f"文章 {article_id} 已添加到向量索引")


def remove_article_from_index(article_id: int):
    """
    从向量索引中删除文章

    Args:
        article_id: 文章ID
    """
    collection = get_article_collection()
    try:
        collection.delete(ids=[str(article_id)])
        print(f"文章 {article_id} 已从向量索引删除")
    except Exception as e:
        print(f"删除文章 {article_id} 失败: {e}")


def update_article_in_index(article_id: int, title: str, full_text: str, keywords: List[str], ai_summary: str):
    """
    更新向量索引中的文章

    Args:
        article_id: 文章ID
        title: 标题
        full_text: 全文
        keywords: 关键词列表
        ai_summary: AI摘要
    """
    # 先删除旧的
    remove_article_from_index(article_id)
    # 再添加新的
    add_article_to_index(article_id, title, full_text, keywords, ai_summary)


def semantic_search(query: str, top_k: int = 5) -> List[Tuple[int, float]]:
    """
    执行语义搜索

    Args:
        query: 搜索查询
        top_k: 返回结果数量

    Returns:
        [(article_id, score), ...] 按相关度排序
    """
    collection = get_article_collection()

    # 检查集合是否为空
    if collection.count() == 0:
        return []

    # 生成查询向量
    query_embedding = generate_query_embedding(query)

    # 执行搜索
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count()),
        include=["distances"]
    )

    # 解析结果
    search_results = []
    if results and results['ids'] and len(results['ids']) > 0:
        for i, article_id_str in enumerate(results['ids'][0]):
            article_id = int(article_id_str)
            # ChromaDB 返回距离，转换为相似度分数 (1 - distance)
            distance = results['distances'][0][i] if results['distances'] else 0
            score = 1 - distance  # 余弦距离转相似度
            search_results.append((article_id, score))

    return search_results


def search_articles(db: Session, query: str, top_k: int = 5) -> List[Tuple[Article, float]]:
    """
    搜索文章并返回完整文章对象

    Args:
        db: 数据库会话
        query: 搜索查询
        top_k: 返回结果数量

    Returns:
        [(Article, score), ...] 按相关度排序
    """
    # 执行语义搜索
    search_results = semantic_search(query, top_k)

    # 获取完整文章
    articles_with_scores = []
    for article_id, score in search_results:
        article = db.query(Article).filter(Article.id == article_id).first()
        if article:
            articles_with_scores.append((article, score))

    return articles_with_scores
