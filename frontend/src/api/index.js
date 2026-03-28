import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '',
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' }
})

// Очередь запросов, ожидающих обновления токена
let isRefreshing = false
let refreshQueue = []

function processQueue(error, token = null) {
  refreshQueue.forEach(({ resolve, reject }) => {
    if (error) reject(error)
    else resolve(token)
  })
  refreshQueue = []
}

// Авто-обновление токена при 401 с защитой от гонки параллельных запросов
api.interceptors.response.use(
  response => response,
  async error => {
    const original = error.config
    if (error.response?.status !== 401 || original._retry) {
      return Promise.reject(error)
    }

    // Если рефреш уже идёт — встаём в очередь
    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        refreshQueue.push({ resolve, reject })
      }).then(token => {
        original.headers['Authorization'] = `Bearer ${token}`
        return api.request(original)
      })
    }

    original._retry = true
    isRefreshing = true

    const refresh = localStorage.getItem('refresh_token')
    if (!refresh) {
      isRefreshing = false
      localStorage.clear()
      window.location.href = '/auth'
      return Promise.reject(error)
    }

    try {
      const res = await axios.post('/api/auth/token/refresh/', { refresh })
      const newAccess = res.data.access
      const newRefresh = res.data.refresh  // сохраняем ротированный refresh-токен
      localStorage.setItem('access_token', newAccess)
      if (newRefresh) localStorage.setItem('refresh_token', newRefresh)
      api.defaults.headers.common['Authorization'] = `Bearer ${newAccess}`
      original.headers['Authorization'] = `Bearer ${newAccess}`
      processQueue(null, newAccess)
      return api.request(original)
    } catch (refreshError) {
      processQueue(refreshError, null)
      localStorage.clear()
      window.location.href = '/auth'
      return Promise.reject(refreshError)
    } finally {
      isRefreshing = false
    }
  }
)

export default api
