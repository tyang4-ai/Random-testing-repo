"""
SQLAlchemy 数据模型
"""
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Article(Base):
    """文章模型"""
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, comment="标题")
    date = Column(Date, nullable=False, comment="发布日期")
    source = Column(String(200), nullable=False, comment="来源")
    author = Column(String(100), nullable=False, comment="作者")
    category = Column(String(100), nullable=False, comment="分类")
    full_text = Column(Text, nullable=False, comment="全文内容")
    keywords = Column(JSON, nullable=False, comment="关键词列表")
    ai_summary = Column(String(500), nullable=False, comment="AI一句话摘要")
    article_type = Column(String(50), nullable=False, comment="文章类型")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "date": self.date.isoformat() if self.date else None,
            "source": self.source,
            "author": self.author,
            "category": self.category,
            "full_text": self.full_text,
            "keywords": self.keywords,
            "ai_summary": self.ai_summary,
            "article_type": self.article_type,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
