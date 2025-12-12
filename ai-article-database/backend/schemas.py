"""
Pydantic 数据验证模型
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class ArticleCreate(BaseModel):
    """创建文章的请求模型"""
    title: str
    date: date
    source: str
    author: str
    category: str
    full_text: str
    keywords: List[str]
    ai_summary: str
    article_type: str


class ArticleUpdate(BaseModel):
    """更新文章的请求模型"""
    title: Optional[str] = None
    date: Optional[date] = None
    source: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    full_text: Optional[str] = None
    keywords: Optional[List[str]] = None
    ai_summary: Optional[str] = None
    article_type: Optional[str] = None


class ArticleResponse(BaseModel):
    """文章响应模型"""
    id: int
    title: str
    date: date
    source: str
    author: str
    category: str
    full_text: str
    keywords: List[str]
    ai_summary: str
    article_type: str

    class Config:
        from_attributes = True


class SearchRequest(BaseModel):
    """搜索请求模型"""
    query: str
    top_k: int = 5


class SearchResult(BaseModel):
    """搜索结果模型"""
    article: ArticleResponse
    score: float


class ReportRequest(BaseModel):
    """报告生成请求模型"""
    query: str
    article_ids: List[int]


class ReportResponse(BaseModel):
    """报告响应模型"""
    report: str
    articles: List[ArticleResponse]
