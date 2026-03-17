import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api/index.js'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  const accessToken = ref(localStorage.getItem('access_token') || null)
  const refreshToken = ref(localStorage.getItem('refresh_token') || null)

  const isAuthenticated = computed(() => !!accessToken.value && !!user.value)

  function setTokens(access, refresh) {
    accessToken.value = access
    refreshToken.value = refresh
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
    api.defaults.headers.common['Authorization'] = `Bearer ${access}`
  }

  function setUser(userData) {
    user.value = userData
    localStorage.setItem('user', JSON.stringify(userData))
  }

  async function login(email, password) {
    const resp = await api.post('/api/auth/login/', { email, password })
    setTokens(resp.data.access, resp.data.refresh)
    const profile = await api.get('/api/auth/profile/')
    setUser(profile.data)
    return profile.data
  }

  async function register(data) {
    return await api.post('/api/auth/register/', data)
  }

  async function logout() {
    try {
      await api.post('/api/auth/logout/', { refresh: refreshToken.value })
    } catch {}
    accessToken.value = null
    refreshToken.value = null
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    delete api.defaults.headers.common['Authorization']
  }

  async function updateProfile(data) {
    const resp = await api.put('/api/auth/profile/', data)
    setUser(resp.data)
    return resp.data
  }

  // Восстанавливаем заголовок при перезагрузке
  if (accessToken.value) {
    api.defaults.headers.common['Authorization'] = `Bearer ${accessToken.value}`
  }

  return { user, accessToken, isAuthenticated, login, register, logout, updateProfile, setUser, setTokens }
})
