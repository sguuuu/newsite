import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '',
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' }
})

// Авто-обновление токена при 401
api.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      const refresh = localStorage.getItem('refresh_token')
      if (refresh && !error.config._retry) {
        error.config._retry = true
        try {
          const res = await axios.post('/api/auth/token/refresh/', { refresh })
          const newAccess = res.data.access
          localStorage.setItem('access_token', newAccess)
          api.defaults.headers.common['Authorization'] = `Bearer ${newAccess}`
          error.config.headers['Authorization'] = `Bearer ${newAccess}`
          return api.request(error.config)
        } catch {
          localStorage.clear()
          window.location.href = '/auth'
        }
      }
    }
    return Promise.reject(error)
  }
)

export default api
