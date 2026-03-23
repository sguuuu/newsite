import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api/index.js'

export const useNotificationsStore = defineStore('notifications', () => {
  const list = ref([])
  const unreadCount = ref(0)
  let pollInterval = null

  async function fetchAll() {
    try {
      const res = await api.get('/api/notifications/')
      list.value = res.data.results || res.data
      unreadCount.value = list.value.filter(n => !n.is_read).length
    } catch (e) {
      console.error('notifications fetch error:', e)
    }
  }

  async function checkDeadlines() {
    try {
      await api.post('/api/notifications/check-deadlines/')
    } catch {}
  }

  async function markRead(id) {
    // Оптимистичное обновление — сразу меняем UI
    list.value = list.value.map(n => n.id === id ? { ...n, is_read: true } : n)
    unreadCount.value = list.value.filter(n => !n.is_read).length
    try {
      await api.post(`/api/notifications/${id}/read/`)
    } catch (e) {
      console.error('markRead error:', e)
      // откатываем при ошибке
      await fetchAll()
    }
  }

function startPolling() {
    checkDeadlines().then(fetchAll)
    pollInterval = setInterval(() => {
      checkDeadlines().then(fetchAll)
    }, 60000)
  }

  function stopPolling() {
    if (pollInterval) { clearInterval(pollInterval); pollInterval = null }
    list.value = []
    unreadCount.value = 0
  }

  return { list, unreadCount, fetchAll, markRead, startPolling, stopPolling }
})
