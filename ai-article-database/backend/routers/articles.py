"""
文章管理 API (管理员接口)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database import get_db
from models import Article
from schemas import ArticleCreate, ArticleUpdate, ArticleResponse
from services.search import add_article_to_index, remove_article_from_index, update_article_in_index
from services.llm import generate_article_summary, extract_keywords

router = APIRouter(prefix="/api/articles", tags=["文章管理"])


@router.get("/", response_model=List[ArticleResponse])
def get_all_articles(db: Session = Depends(get_db)):
    """获取所有文章列表"""
    articles = db.query(Article).order_by(Article.created_at.desc()).all()
    return articles


@router.get("/{article_id}", response_model=ArticleResponse)
def get_article(article_id: int, db: Session = Depends(get_db)):
    """获取单篇文章详情"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    return article


@router.post("/", response_model=ArticleResponse)
def create_article(article_data: ArticleCreate, db: Session = Depends(get_db)):
    """创建新文章"""
    # 创建文章对象
    article = Article(
        title=article_data.title,
        date=article_data.date,
        source=article_data.source,
        author=article_data.author,
        category=article_data.category,
        full_text=article_data.full_text,
        keywords=article_data.keywords,
        ai_summary=article_data.ai_summary,
        article_type=article_data.article_type,
    )

    # 保存到数据库
    db.add(article)
    db.commit()
    db.refresh(article)

    # 添加到向量索引
    add_article_to_index(
        article.id,
        article.title,
        article.full_text,
        article.keywords,
        article.ai_summary
    )

    return article


@router.post("/auto-process", response_model=ArticleResponse)
def create_article_with_ai(
    title: str,
    date: str,
    source: str,
    author: str,
    category: str,
    full_text: str,
    article_type: str,
    db: Session = Depends(get_db)
):
    """
    创建文章并自动使用AI生成摘要和关键词
    """
    # AI 生成摘要
    ai_summary = generate_article_summary(full_text)

    # AI 提取关键词
    keywords = extract_keywords(full_text)

    # 创建文章
    article = Article(
        title=title,
        date=datetime.strptime(date, "%Y-%m-%d").date(),
        source=source,
        author=author,
        category=category,
        full_text=full_text,
        keywords=keywords,
        ai_summary=ai_summary,
        article_type=article_type,
    )

    db.add(article)
    db.commit()
    db.refresh(article)

    # 添加到向量索引
    add_article_to_index(
        article.id,
        article.title,
        article.full_text,
        article.keywords,
        article.ai_summary
    )

    return article


@router.put("/{article_id}", response_model=ArticleResponse)
def update_article(article_id: int, article_data: ArticleUpdate, db: Session = Depends(get_db)):
    """更新文章"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")

    # 更新字段
    update_data = article_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(article, field, value)

    db.commit()
    db.refresh(article)

    # 更新向量索引
    update_article_in_index(
        article.id,
        article.title,
        article.full_text,
        article.keywords,
        article.ai_summary
    )

    return article


@router.delete("/{article_id}")
def delete_article(article_id: int, db: Session = Depends(get_db)):
    """删除文章"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")

    # 从向量索引删除
    remove_article_from_index(article_id)

    # 从数据库删除
    db.delete(article)
    db.commit()

    return {"message": "文章已删除", "id": article_id}


@router.get("/categories/list")
def get_categories(db: Session = Depends(get_db)):
    """获取所有分类列表"""
    categories = db.query(Article.category).distinct().all()
    return [c[0] for c in categories]


@router.get("/types/list")
def get_article_types(db: Session = Depends(get_db)):
    """获取所有文章类型列表"""
    types = db.query(Article.article_type).distinct().all()
    return [t[0] for t in types]
