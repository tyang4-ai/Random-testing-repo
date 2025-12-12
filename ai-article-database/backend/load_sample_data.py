"""
加载示例数据脚本
运行此脚本将10篇示例环保文章导入数据库
"""
import json
import os
import sys
from datetime import datetime

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import init_db, SessionLocal, get_article_collection
from models import Article
from services.search import add_article_to_index


def load_sample_articles():
    """加载示例文章到数据库"""
    # 初始化数据库
    init_db()

    # 读取示例数据
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_articles.json')

    if not os.path.exists(data_path):
        print(f"错误: 找不到示例数据文件 {data_path}")
        return

    with open(data_path, 'r', encoding='utf-8') as f:
        articles_data = json.load(f)

    print(f"找到 {len(articles_data)} 篇示例文章")

    # 创建数据库会话
    db = SessionLocal()

    try:
        # 检查是否已有数据
        existing_count = db.query(Article).count()
        if existing_count > 0:
            print(f"数据库中已有 {existing_count} 篇文章")
            response = input("是否清空现有数据并重新导入? (y/n): ")
            if response.lower() == 'y':
                # 清空现有数据
                db.query(Article).delete()
                db.commit()
                # 清空向量索引
                collection = get_article_collection()
                # 获取所有ID并删除
                all_ids = collection.get()['ids']
                if all_ids:
                    collection.delete(ids=all_ids)
                print("已清空现有数据")
            else:
                print("取消导入")
                return

        # 导入文章
        print("\n开始导入文章...")
        print("(首次运行需要下载BGE模型，可能需要几分钟时间)\n")

        for i, article_data in enumerate(articles_data, 1):
            print(f"[{i}/{len(articles_data)}] 导入: {article_data['title'][:30]}...")

            # 创建文章对象
            article = Article(
                title=article_data['title'],
                date=datetime.strptime(article_data['date'], '%Y-%m-%d').date(),
                source=article_data['source'],
                author=article_data['author'],
                category=article_data['category'],
                full_text=article_data['full_text'],
                keywords=article_data['keywords'],
                ai_summary=article_data['ai_summary'],
                article_type=article_data['article_type'],
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

            print(f"    ✓ 已导入 (ID: {article.id})")

        print(f"\n✅ 成功导入 {len(articles_data)} 篇文章!")
        print("现在可以启动后端服务进行测试了")

    except Exception as e:
        print(f"\n❌ 导入失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == '__main__':
    print("=" * 50)
    print("环保文献智能数据库 - 示例数据导入工具")
    print("=" * 50)
    print()
    load_sample_articles()
