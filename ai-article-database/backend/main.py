"""
AI 文章数据库 - FastAPI 后端主入口
环境保护文献智能检索与报告生成系统
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from database import init_db
from routers import articles, search

# 创建 FastAPI 应用
app = FastAPI(
    title="环保文献智能数据库",
    description="基于AI的环境保护文献检索与研究报告生成系统",
    version="1.0.0",
)

# 配置 CORS (允许前端访问)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(articles.router)
app.include_router(search.router)


@app.on_event("startup")
async def startup_event():
    """应用启动时初始化数据库"""
    init_db()
    print("=" * 50)
    print("环保文献智能数据库启动成功!")
    print("后端API地址: http://localhost:8000")
    print("API文档地址: http://localhost:8000/docs")
    print("=" * 50)


@app.get("/")
def root():
    """根路径 - 欢迎信息"""
    return {
        "message": "欢迎使用环保文献智能数据库",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "文章管理": "/api/articles",
            "搜索报告": "/api/search",
        }
    }


@app.get("/health")
def health_check():
    """健康检查"""
    return {"status": "healthy", "message": "服务运行正常"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
