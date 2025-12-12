"""
LLM 服务 (通过 Ollama)
支持多种模型: DeepSeek, Qwen, Llama, Gemma 等
"""
import requests
import json
from typing import List, Dict, Optional

OLLAMA_BASE_URL = "http://localhost:11434"

# 按优先级排列的支持模型列表
SUPPORTED_MODELS = [
    "deepseek-v2",
    "deepseek-coder:6.7b",
    "qwen2:7b",
    "qwen2:1.5b",
    "qwen:7b",
    "llama3:8b",
    "llama3.1:8b",
    "gemma2:9b",
    "gemma:7b",
    "mistral:7b",
]

# 缓存当前可用的模型
_current_model = None


def check_ollama_status() -> bool:
    """检查 Ollama 服务是否运行"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False


def get_available_models() -> List[str]:
    """获取已安装的模型列表"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            return [m["name"] for m in models]
    except:
        pass
    return []


def get_best_available_model() -> Optional[str]:
    """获取最佳可用模型"""
    global _current_model

    if _current_model:
        return _current_model

    available = get_available_models()
    if not available:
        return None

    # 按优先级查找
    for model in SUPPORTED_MODELS:
        for avail in available:
            if model in avail or avail in model:
                _current_model = avail
                print(f"使用模型: {_current_model}")
                return _current_model

    # 如果没有找到优先模型，使用第一个可用的
    _current_model = available[0]
    print(f"使用模型: {_current_model}")
    return _current_model


def generate_text(prompt: str, model: str = None) -> str:
    """
    使用 LLM 生成文本 (自动选择最佳可用模型)

    Args:
        prompt: 提示词
        model: 模型名称 (可选，默认自动选择)

    Returns:
        生成的文本
    """
    # 自动选择模型
    if model is None:
        model = get_best_available_model()
        if model is None:
            return "错误: 没有找到可用的AI模型。请先运行 'ollama pull qwen2:7b' 下载模型"

    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_predict": 4096,
                }
            },
            timeout=180  # 3分钟超时 (较小模型可能更慢)
        )

        if response.status_code == 200:
            return response.json().get("response", "")
        else:
            return f"错误: Ollama 返回状态码 {response.status_code}"
    except requests.exceptions.ConnectionError:
        return "错误: 无法连接到 Ollama 服务。请确保 Ollama 正在运行 (ollama serve)"
    except requests.exceptions.Timeout:
        return "错误: 请求超时，请稍后重试"
    except Exception as e:
        return f"错误: {str(e)}"


def generate_article_summary(full_text: str) -> str:
    """
    为文章生成一句话摘要

    Args:
        full_text: 文章全文

    Returns:
        一句话摘要
    """
    prompt = f"""请阅读以下文章，并用一句话概括其核心内容。要求：
1. 不超过50个字
2. 准确概括文章主旨
3. 语言简洁明了

文章内容：
{full_text[:3000]}  # 限制长度

一句话摘要："""

    return generate_text(prompt)


def extract_keywords(full_text: str) -> List[str]:
    """
    从文章中提取关键词

    Args:
        full_text: 文章全文

    Returns:
        关键词列表
    """
    prompt = f"""请从以下文章中提取5-8个最重要的关键词。要求：
1. 关键词应该是名词或名词短语
2. 关键词应该能代表文章的主题
3. 只返回关键词，用逗号分隔

文章内容：
{full_text[:3000]}

关键词："""

    result = generate_text(prompt)
    # 解析关键词
    keywords = [kw.strip() for kw in result.split("，") if kw.strip()]
    if not keywords:
        keywords = [kw.strip() for kw in result.split(",") if kw.strip()]
    return keywords[:8]


def generate_research_report(query: str, articles: List[Dict]) -> str:
    """
    基于检索到的文章生成研究报告

    Args:
        query: 用户搜索查询
        articles: 相关文章列表

    Returns:
        研究报告文本
    """
    # 构建文章摘要
    articles_context = ""
    for i, article in enumerate(articles, 1):
        articles_context += f"""
【文献{i}】
标题：{article['title']}
来源：{article['source']}
日期：{article['date']}
类型：{article['article_type']}
摘要：{article['ai_summary']}
内容摘录：{article['full_text'][:1000]}...

"""

    prompt = f"""你是一位专业的环境保护研究员。请基于以下检索到的文献资料，针对用户的研究主题"{query}"撰写一份专业的研究报告。

检索到的相关文献：
{articles_context}

请按照以下格式撰写研究报告：

# 研究报告：{query}

## 一、摘要
[用200字左右概述本报告的主要内容和结论]

## 二、研究背景
[介绍该主题的背景、重要性和研究意义]

## 三、现状分析
[基于文献资料分析当前状况，引用具体文献]

## 四、主要发现
[列出3-5个主要发现，每个发现都要引用相关文献]

## 五、案例分析
[选取1-2个典型案例进行详细分析]

## 六、结论与建议
[总结主要结论，提出3-5条具体建议]

## 七、参考文献
[列出所引用的文献]

请确保：
1. 内容专业、客观
2. 引用文献时标注来源
3. 建议具有可操作性
4. 语言正式、学术化

研究报告："""

    return generate_text(prompt)
