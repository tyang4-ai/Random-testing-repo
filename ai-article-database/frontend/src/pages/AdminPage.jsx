import React, { useState, useEffect } from 'react'
import { getAllArticles, createArticle, updateArticle, deleteArticle } from '../services/api'

// 预设的分类选项
const CATEGORIES = [
  '水污染治理',
  '大气污染防治',
  '土壤修复',
  '生态保护',
  '固废处理',
  '碳中和',
  '环境监测',
  '政策法规',
  '其他',
]

// 预设的文章类型选项
const ARTICLE_TYPES = [
  '新闻报道',
  '研究论文',
  '政府报告',
  '杂志文章',
  '案例分析',
  '政策解读',
]

function AdminPage() {
  const [articles, setArticles] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [editingArticle, setEditingArticle] = useState(null)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  // 表单状态
  const [formData, setFormData] = useState({
    title: '',
    date: '',
    source: '',
    author: '',
    category: '',
    full_text: '',
    keywords: '',
    ai_summary: '',
    article_type: '',
  })

  // 加载文章列表
  const loadArticles = async () => {
    setIsLoading(true)
    try {
      const data = await getAllArticles()
      setArticles(data)
    } catch (err) {
      setError('加载文章失败: ' + (err.response?.data?.detail || err.message))
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    loadArticles()
  }, [])

  // 打开新增模态框
  const openAddModal = () => {
    setFormData({
      title: '',
      date: new Date().toISOString().split('T')[0],
      source: '',
      author: '',
      category: CATEGORIES[0],
      full_text: '',
      keywords: '',
      ai_summary: '',
      article_type: ARTICLE_TYPES[0],
    })
    setEditingArticle(null)
    setShowModal(true)
    setError('')
  }

  // 打开编辑模态框
  const openEditModal = (article) => {
    setFormData({
      title: article.title,
      date: article.date,
      source: article.source,
      author: article.author,
      category: article.category,
      full_text: article.full_text,
      keywords: article.keywords.join(', '),
      ai_summary: article.ai_summary,
      article_type: article.article_type,
    })
    setEditingArticle(article)
    setShowModal(true)
    setError('')
  }

  // 关闭模态框
  const closeModal = () => {
    setShowModal(false)
    setEditingArticle(null)
    setError('')
  }

  // 处理表单输入
  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  // 提交表单
  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')

    // 验证必填字段
    if (!formData.title || !formData.date || !formData.source || !formData.full_text) {
      setError('请填写所有必填字段')
      return
    }

    // 准备数据
    const articleData = {
      ...formData,
      keywords: formData.keywords.split(/[,，]/).map(k => k.trim()).filter(k => k),
    }

    try {
      if (editingArticle) {
        await updateArticle(editingArticle.id, articleData)
        setSuccess('文章更新成功!')
      } else {
        await createArticle(articleData)
        setSuccess('文章添加成功!')
      }
      closeModal()
      loadArticles()
    } catch (err) {
      setError('操作失败: ' + (err.response?.data?.detail || err.message))
    }
  }

  // 删除文章
  const handleDelete = async (article) => {
    if (!window.confirm(`确定要删除文章"${article.title}"吗？此操作不可撤销。`)) {
      return
    }

    try {
      await deleteArticle(article.id)
      setSuccess('文章已删除')
      loadArticles()
    } catch (err) {
      setError('删除失败: ' + (err.response?.data?.detail || err.message))
    }
  }

  // 清除提示
  useEffect(() => {
    if (success) {
      const timer = setTimeout(() => setSuccess(''), 3000)
      return () => clearTimeout(timer)
    }
  }, [success])

  return (
    <div className="admin-page">
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <h2 className="card-title" style={{ marginBottom: 0 }}>⚙️ 文章管理</h2>
          <button className="btn btn-primary" onClick={openAddModal}>
            ➕ 添加文章
          </button>
        </div>

        {error && <div className="alert alert-error">{error}</div>}
        {success && <div className="alert alert-success">{success}</div>}

        {isLoading ? (
          <div className="loading">
            <div className="loading-spinner"></div>
            <p>加载中...</p>
          </div>
        ) : articles.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state-icon">📭</div>
            <h3>暂无文章</h3>
            <p style={{ marginTop: '0.5rem', color: '#666' }}>
              点击"添加文章"按钮开始添加环保文献
            </p>
          </div>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table className="table">
              <thead>
                <tr>
                  <th>标题</th>
                  <th>日期</th>
                  <th>来源</th>
                  <th>分类</th>
                  <th>类型</th>
                  <th>关键词</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                {articles.map(article => (
                  <tr key={article.id}>
                    <td style={{ maxWidth: '250px' }}>
                      <strong style={{ color: '#1a5f2a' }}>{article.title}</strong>
                      <p style={{ fontSize: '0.8rem', color: '#666', marginTop: '0.25rem' }}>
                        {article.ai_summary?.slice(0, 50)}...
                      </p>
                    </td>
                    <td style={{ whiteSpace: 'nowrap' }}>{article.date}</td>
                    <td>{article.source}</td>
                    <td>
                      <span className="keyword-tag">{article.category}</span>
                    </td>
                    <td>{article.article_type}</td>
                    <td style={{ maxWidth: '200px' }}>
                      <div className="article-keywords">
                        {article.keywords?.slice(0, 3).map((kw, idx) => (
                          <span key={idx} className="keyword-tag">{kw}</span>
                        ))}
                        {article.keywords?.length > 3 && (
                          <span style={{ color: '#999', fontSize: '0.8rem' }}>
                            +{article.keywords.length - 3}
                          </span>
                        )}
                      </div>
                    </td>
                    <td style={{ whiteSpace: 'nowrap' }}>
                      <button
                        className="btn btn-secondary btn-sm"
                        style={{ marginRight: '0.5rem' }}
                        onClick={() => openEditModal(article)}
                      >
                        ✏️ 编辑
                      </button>
                      <button
                        className="btn btn-danger btn-sm"
                        onClick={() => handleDelete(article)}
                      >
                        🗑️ 删除
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <div style={{ marginTop: '1rem', color: '#666', fontSize: '0.875rem' }}>
          共 {articles.length} 篇文章
        </div>
      </div>

      {/* 添加/编辑模态框 */}
      {showModal && (
        <div className="modal-overlay" onClick={closeModal}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h2>{editingArticle ? '编辑文章' : '添加新文章'}</h2>
              <button className="modal-close" onClick={closeModal}>&times;</button>
            </div>

            {error && <div className="alert alert-error">{error}</div>}

            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>标题 *</label>
                <input
                  type="text"
                  name="title"
                  value={formData.title}
                  onChange={handleInputChange}
                  placeholder="请输入文章标题"
                  required
                />
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                <div className="form-group">
                  <label>发布日期 *</label>
                  <input
                    type="date"
                    name="date"
                    value={formData.date}
                    onChange={handleInputChange}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>来源 *</label>
                  <input
                    type="text"
                    name="source"
                    value={formData.source}
                    onChange={handleInputChange}
                    placeholder="如：新华社、环保部"
                    required
                  />
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                <div className="form-group">
                  <label>作者</label>
                  <input
                    type="text"
                    name="author"
                    value={formData.author}
                    onChange={handleInputChange}
                    placeholder="作者姓名"
                  />
                </div>
                <div className="form-group">
                  <label>分类</label>
                  <select
                    name="category"
                    value={formData.category}
                    onChange={handleInputChange}
                  >
                    {CATEGORIES.map(cat => (
                      <option key={cat} value={cat}>{cat}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="form-group">
                <label>文章类型</label>
                <select
                  name="article_type"
                  value={formData.article_type}
                  onChange={handleInputChange}
                >
                  {ARTICLE_TYPES.map(type => (
                    <option key={type} value={type}>{type}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>关键词 (用逗号分隔)</label>
                <input
                  type="text"
                  name="keywords"
                  value={formData.keywords}
                  onChange={handleInputChange}
                  placeholder="如：长三角, 水污染, 治理"
                />
              </div>

              <div className="form-group">
                <label>AI摘要 (一句话)</label>
                <input
                  type="text"
                  name="ai_summary"
                  value={formData.ai_summary}
                  onChange={handleInputChange}
                  placeholder="用一句话概括文章核心内容"
                />
              </div>

              <div className="form-group">
                <label>全文内容 *</label>
                <textarea
                  name="full_text"
                  value={formData.full_text}
                  onChange={handleInputChange}
                  placeholder="请输入文章全文内容..."
                  style={{ minHeight: '200px' }}
                  required
                />
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '1rem', marginTop: '1.5rem' }}>
                <button type="button" className="btn btn-secondary" onClick={closeModal}>
                  取消
                </button>
                <button type="submit" className="btn btn-primary">
                  {editingArticle ? '保存修改' : '添加文章'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default AdminPage
