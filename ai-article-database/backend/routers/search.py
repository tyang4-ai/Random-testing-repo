"""
搜索与报告生成 API (用户接口)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Article
from schemas import SearchRequest, SearchResult, ReportRequest, ReportResponse, ArticleResponse
from services.search import search_articles
from services.llm import generate_research_report, check_ollama_status, get_available_models, get_best_available_model

router = APIRouter(prefix="/api/search", tags=["搜索与报告"])


@router.post("/", response_model=List[SearchResult])
def search(request: SearchRequest, db: Session = Depends(get_db)):
    """
    语义搜索文章

    根据用户输入的关键词进行语义搜索，返回最相关的文章列表
    """
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="搜索关键词不能为空")

    # 执行语义搜索
    results = search_articles(db, request.query, request.top_k)

    # 转换为响应格式
    search_results = []
    for article, score in results:
        search_results.append(SearchResult(
            article=ArticleResponse(
                id=article.id,
                title=article.title,
                date=article.date,
                source=article.source,
                author=article.author,
                category=article.category,
                full_text=article.full_text,
                keywords=article.keywords,
                ai_summary=article.ai_summary,
                article_type=article.article_type,
            ),
            score=round(score, 4)
        ))

    return search_results


@router.post("/report", response_model=ReportResponse)
def generate_report(request: ReportRequest, db: Session = Depends(get_db)):
    """
    生成研究报告

    基于选定的文章生成综合研究报告
    """
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="研究主题不能为空")

    if not request.article_ids:
        raise HTTPException(status_code=400, detail="请选择至少一篇文章")

    # 检查 Ollama 服务
    if not check_ollama_status():
        raise HTTPException(
            status_code=503,
            detail="AI 服务未启动。请运行 'ollama serve' 启动 Ollama 服务"
        )

    # 获取选定的文章
    articles = db.query(Article).filter(Article.id.in_(request.article_ids)).all()

    if not articles:
        raise HTTPException(status_code=404, detail="未找到选定的文章")

    # 转换为字典列表
    articles_data = [article.to_dict() for article in articles]

    # 生成报告
    report = generate_research_report(request.query, articles_data)

    # 构建响应
    article_responses = [
        ArticleResponse(
            id=article.id,
            title=article.title,
            date=article.date,
            source=article.source,
            author=article.author,
            category=article.category,
            full_text=article.full_text,
            keywords=article.keywords,
            ai_summary=article.ai_summary,
            article_type=article.article_type,
        )
        for article in articles
    ]

    return ReportResponse(report=report, articles=article_responses)


@router.get("/status")
def get_service_status():
    """检查服务状态"""
    ollama_running = check_ollama_status()
    available_models = get_available_models() if ollama_running else []
    current_model = get_best_available_model() if ollama_running else None

    if not ollama_running:
        message = "警告: Ollama 服务未启动。请运行 'ollama serve'"
    elif not available_models:
        message = "警告: 没有可用的AI模型。请运行 'ollama pull qwen2:7b' 下载模型"
    else:
        message = f"服务正常运行，使用模型: {current_model}"

    return {
        "database": True,
        "ollama": ollama_running,
        "available_models": available_models,
        "current_model": current_model,
        "message": message
    }
