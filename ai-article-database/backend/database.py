"""
数据库配置 - SQLite + ChromaDB
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import chromadb
from chromadb.config import Settings

# 数据库文件路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

# SQLite 配置
SQLITE_URL = f"sqlite:///{os.path.join(DATA_DIR, 'articles.db')}"
engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ChromaDB 配置 (向量数据库)
CHROMA_DIR = os.path.join(DATA_DIR, "chroma_db")
chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)

# 获取或创建文章向量集合
def get_article_collection():
    """获取文章向量集合"""
    return chroma_client.get_or_create_collection(
        name="articles",
        metadata={"hnsw:space": "cosine"}  # 使用余弦相似度
    )


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """初始化数据库表"""
    from models import Base
    Base.metadata.create_all(bind=engine)
    print("数据库初始化完成")
