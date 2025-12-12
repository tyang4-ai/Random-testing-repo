import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// ==================== 文章管理 API ====================

/**
 * 获取所有文章
 */
export const getAllArticles = async () => {
  const response = await api.get('/api/articles/')
  return response.data
}

/**
 * 获取单篇文章
 */
export const getArticle = async (id) => {
  const response = await api.get(`/api/articles/${id}`)
  return response.data
}

/**
 * 创建新文章
 */
export const createArticle = async (articleData) => {
  const response = await api.post('/api/articles/', articleData)
  return response.data
}

/**
 * 更新文章
 */
export const updateArticle = async (id, articleData) => {
  const response = await api.put(`/api/articles/${id}`, articleData)
  return response.data
}

/**
 * 删除文章
 */
export const deleteArticle = async (id) => {
  const response = await api.delete(`/api/articles/${id}`)
  return response.data
}

/**
 * 获取所有分类
 */
export const getCategories = async () => {
  const response = await api.get('/api/articles/categories/list')
  return response.data
}

/**
 * 获取所有文章类型
 */
export const getArticleTypes = async () => {
  const response = await api.get('/api/articles/types/list')
  return response.data
}

// ==================== 搜索与报告 API ====================

/**
 * 语义搜索文章
 */
export const searchArticles = async (query, topK = 5) => {
  const response = await api.post('/api/search/', {
    query,
    top_k: topK,
  })
  return response.data
}

/**
 * 生成研究报告
 */
export const generateReport = async (query, articleIds) => {
  const response = await api.post('/api/search/report', {
    query,
    article_ids: articleIds,
  })
  return response.data
}

/**
 * 检查服务状态
 */
export const checkServiceStatus = async () => {
  const response = await api.get('/api/search/status')
  return response.data
}

export default api
