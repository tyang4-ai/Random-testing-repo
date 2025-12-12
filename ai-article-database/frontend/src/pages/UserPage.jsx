import React, { useState, useEffect } from 'react'
import { searchArticles, generateReport, checkServiceStatus } from '../services/api'

function UserPage() {
  const [query, setQuery] = useState('')
  const [searchResults, setSearchResults] = useState([])
  const [selectedArticles, setSelectedArticles] = useState([])
  const [report, setReport] = useState('')
  const [isSearching, setIsSearching] = useState(false)
  const [isGenerating, setIsGenerating] = useState(false)
  const [serviceStatus, setServiceStatus] = useState(null)
  const [error, setError] = useState('')

  // 检查服务状态
  useEffect(() => {
    const checkStatus = async () => {
      try {
        const status = await checkServiceStatus()
        setServiceStatus(status)
      } catch (err) {
        setServiceStatus({ database: false, ollama: false })
      }
    }
    checkStatus()
  }, [])

  // 执行搜索
  const handleSearch = async () => {
    if (!query.trim()) {
      setError('请输入搜索关键词')
      return
    }

    setIsSearching(true)
    setError('')
    setSearchResults([])
    setSelectedArticles([])
    setReport('')

    try {
      const results = await searchArticles(query, 10)
      setSearchResults(results)
      if (results.length === 0) {
        setError('未找到相关文章，请尝试其他关键词')
      }
    } catch (err) {
      setError('搜索失败: ' + (err.response?.data?.detail || err.message))
    } finally {
      setIsSearching(false)
    }
  }

  // 切换文章选择
  const toggleArticleSelection = (articleId) => {
    setSelectedArticles(prev => {
      if (prev.includes(articleId)) {
        return prev.filter(id => id !== articleId)
      } else {
        return [...prev, articleId]
      }
    })
  }

  // 全选/取消全选
  const toggleSelectAll = () => {
    if (selectedArticles.length === searchResults.length) {
      setSelectedArticles([])
    } else {
      setSelectedArticles(searchResults.map(r => r.article.id))
    }
  }

  // 生成报告
  const handleGenerateReport = async () => {
    if (selectedArticles.length === 0) {
      setError('请至少选择一篇文章')
      return
    }

    setIsGenerating(true)
    setError('')
    setReport('')

    try {
      const result = await generateReport(query, selectedArticles)
      setReport(result.report)
    } catch (err) {
      setError('报告生成失败: ' + (err.response?.data?.detail || err.message))
    } finally {
      setIsGenerating(false)
    }
  }

  // 处理回车键搜索
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }

  return (
    <div className="user-page">
      {/* 服务状态提示 */}
      {serviceStatus && !serviceStatus.ollama && (
        <div className="alert alert-error">
          ⚠️ AI服务未启动。请在终端运行 <code>ollama serve</code> 启动Ollama服务后再试。
        </div>
      )}
      {serviceStatus && serviceStatus.ollama && !serviceStatus.current_model && (
        <div className="alert alert-error">
          ⚠️ 没有可用的AI模型。请运行 <code>ollama pull qwen2:7b</code> 下载模型。
        </div>
      )}
      {serviceStatus && serviceStatus.current_model && (
        <div className="alert alert-info">
          ✓ AI服务正常运行，当前模型: {serviceStatus.current_model}
        </div>
      )}

      {/* 搜索区域 */}
      <div className="card">
        <h2 className="card-title">🔍 智能文献检索</h2>
        <p style={{ color: '#666', marginBottom: '1rem' }}>
          输入您想要研究的关键词，系统将为您找到最相关的环保文献，并生成综合研究报告。
        </p>
        <div className="search-box">
          <input
            type="text"
            placeholder="请输入关键词，如：长三角 水污染 治理..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={handleKeyPress}
          />
          <button
            className="btn btn-primary"
            onClick={handleSearch}
            disabled={isSearching}
          >
            {isSearching ? '搜索中...' : '🔍 搜索'}
          </button>
        </div>

        {error && <div className="alert alert-error">{error}</div>}
      </div>

      {/* 搜索结果 */}
      {searchResults.length > 0 && (
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h2 className="card-title" style={{ marginBottom: 0 }}>
              📄 搜索结果 ({searchResults.length}篇)
            </h2>
            <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
              <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
                <input
                  type="checkbox"
                  checked={selectedArticles.length === searchResults.length}
                  onChange={toggleSelectAll}
                />
                全选
              </label>
              <button
                className="btn btn-primary"
                onClick={handleGenerateReport}
                disabled={selectedArticles.length === 0 || isGenerating}
              >
                {isGenerating ? '生成中...' : `📝 生成报告 (${selectedArticles.length}篇)`}
              </button>
            </div>
          </div>

          <div className="article-list">
            {searchResults.map((result) => (
              <div
                key={result.article.id}
                className="checkbox-item"
                onClick={() => toggleArticleSelection(result.article.id)}
              >
                <input
                  type="checkbox"
                  checked={selectedArticles.includes(result.article.id)}
                  onChange={() => {}}
                />
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <h3 style={{ color: '#1a5f2a', marginBottom: '0.5rem' }}>
                      {result.article.title}
                    </h3>
                    <span className="relevance-score">
                      相关度: {(result.score * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="article-meta">
                    <span>📅 {result.article.date}</span>
                    <span>📰 {result.article.source}</span>
                    <span>✍️ {result.article.author}</span>
                    <span>📁 {result.article.category}</span>
                    <span>📑 {result.article.article_type}</span>
                  </div>
                  <p className="article-summary">{result.article.ai_summary}</p>
                  <div className="article-keywords">
                    {result.article.keywords.map((keyword, idx) => (
                      <span key={idx} className="keyword-tag">{keyword}</span>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 加载状态 */}
      {isSearching && (
        <div className="card">
          <div className="loading">
            <div className="loading-spinner"></div>
            <p>正在搜索相关文献...</p>
          </div>
        </div>
      )}

      {isGenerating && (
        <div className="card">
          <div className="loading">
            <div className="loading-spinner"></div>
            <p>AI正在分析文献并生成研究报告，请稍候...</p>
            <p style={{ fontSize: '0.875rem', color: '#999', marginTop: '0.5rem' }}>
              (这可能需要1-2分钟)
            </p>
          </div>
        </div>
      )}

      {/* 研究报告 */}
      {report && (
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h2 className="card-title" style={{ marginBottom: 0 }}>📋 研究报告</h2>
            <button
              className="btn btn-secondary btn-sm"
              onClick={() => {
                const blob = new Blob([report], { type: 'text/markdown' })
                const url = URL.createObjectURL(blob)
                const a = document.createElement('a')
                a.href = url
                a.download = `研究报告_${query}_${new Date().toISOString().split('T')[0]}.md`
                a.click()
              }}
            >
              📥 下载报告
            </button>
          </div>
          <div className="report-container">
            <div className="report-content">
              {report.split('\n').map((line, index) => {
                if (line.startsWith('# ')) {
                  return <h1 key={index}>{line.replace('# ', '')}</h1>
                } else if (line.startsWith('## ')) {
                  return <h2 key={index}>{line.replace('## ', '')}</h2>
                } else if (line.startsWith('- ')) {
                  return <li key={index} style={{ marginLeft: '1.5rem' }}>{line.replace('- ', '')}</li>
                } else if (line.trim() === '') {
                  return <br key={index} />
                } else {
                  return <p key={index} style={{ marginBottom: '0.5rem' }}>{line}</p>
                }
              })}
            </div>
          </div>
        </div>
      )}

      {/* 空状态 */}
      {!isSearching && searchResults.length === 0 && !error && (
        <div className="card">
          <div className="empty-state">
            <div className="empty-state-icon">🔍</div>
            <h3>开始您的文献研究</h3>
            <p style={{ marginTop: '0.5rem', color: '#666' }}>
              输入关键词搜索相关环保文献，选择文章后可生成综合研究报告
            </p>
            <div style={{ marginTop: '1rem', color: '#999', fontSize: '0.875rem' }}>
              <p>试试搜索：</p>
              <p>• 长三角 水污染</p>
              <p>• 苏州河 生态修复</p>
              <p>• 碳中和 政策</p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default UserPage
