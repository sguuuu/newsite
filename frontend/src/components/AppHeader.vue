<template>
  <header class="header">
    <div class="container">
      <div class="header-content">
        <RouterLink to="/" class="logo">
          <img :src="logoSrc" alt="СочиГУ" class="logo-icon" @error="handleLogoError" ref="logoImg">
          <span class="logo-text">Школа<br>финансовой культуры</span>
        </RouterLink>

        <nav class="nav">
          <ul class="nav-list">
            <li><RouterLink to="/" class="nav-link" :class="{ active: route.path === '/' }">Главная</RouterLink></li>
            <li><RouterLink to="/events" class="nav-link" :class="{ active: route.path.startsWith('/events') }">Мероприятия</RouterLink></li>
            <li><RouterLink to="/documents" class="nav-link" :class="{ active: route.path === '/documents' }">Документы</RouterLink></li>
            <li><RouterLink to="/about" class="nav-link" :class="{ active: route.path === '/about' }">О школе</RouterLink></li>
            <li><RouterLink to="/contacts" class="nav-link" :class="{ active: route.path === '/contacts' }">Контакты</RouterLink></li>
          </ul>
        </nav>

        <div v-if="auth.isAuthenticated" class="user-menu">
          <!-- Колокольчик -->
          <div class="notif-bell-wrap" ref="bellWrap">
            <button class="notif-bell-btn" @click="togglePanel" :class="{ active: panelOpen }" title="Уведомления">
              <svg style="width:20px;height:20px"><use href="#ic-bell"/></svg>
              <span v-if="notifStore.unreadCount > 0" class="notif-badge">
                {{ notifStore.unreadCount > 9 ? '9+' : notifStore.unreadCount }}
              </span>
            </button>

            <!-- Дропдаун -->
            <div v-if="panelOpen" class="notif-panel">
              <div class="notif-panel-header">
                <span style="font-weight:600; color:var(--primary-dark);">Уведомления</span>
              </div>

              <div v-if="notifStore.list.length === 0" style="padding:30px 20px; text-align:center; color:var(--text-gray); font-size:14px;">
                Нет уведомлений
              </div>

              <div v-else class="notif-list">
                <div
                  v-for="n in notifStore.list" :key="n.id"
                  class="notif-item"
                  :class="{ unread: !n.is_read }"
                  @click="handleNotifClick(n)"
                >
                  <div class="notif-icon" :class="'notif-icon--' + n.notif_type">
                    <svg style="width:14px;height:14px"><use :href="notifIcon(n.notif_type)"/></svg>
                  </div>
                  <div style="flex:1; min-width:0;">
                    <div style="font-weight:600; font-size:14px; color:var(--text-dark); margin-bottom:2px;">{{ n.title }}</div>
                    <div style="font-size:13px; color:var(--text-gray); line-height:1.4; white-space:normal;">{{ n.message }}</div>
                    <div style="font-size:12px; color:#94a3b8; margin-top:4px;">{{ formatTime(n.created_at) }}</div>
                  </div>
                  <div v-if="!n.is_read" style="width:8px;height:8px;border-radius:50%;background:var(--primary-blue);flex-shrink:0;margin-top:4px;"></div>
                </div>
              </div>
            </div>
          </div>

          <div class="user-avatar-sm" aria-hidden="true">{{ userInitials }}</div>
          <span class="user-name">{{ auth.user?.first_name || 'Пользователь' }}</span>
          <RouterLink :to="dashboardPath" class="btn-login">Профиль</RouterLink>
          <button class="btn-login btn-logout" @click="handleLogout">Выход</button>
        </div>
        <button v-else class="btn-login" @click="router.push('/auth')">Войти</button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed, ref, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'
import { useNotificationsStore } from '@/stores/notifications.js'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const notifStore = useNotificationsStore()

const logoImg = ref(null)
const logoSrc = '/images/sochgu-logo.png'
const panelOpen = ref(false)
const bellWrap = ref(null)

const userInitials = computed(() => {
  if (!auth.user) return 'У'
  return ((auth.user.first_name?.[0] || '') + (auth.user.last_name?.[0] || '')).toUpperCase() || 'У'
})

const dashboardPath = computed(() => {
  const map = { admin: '/dashboard/admin', teacher: '/dashboard/teacher', participant: '/dashboard/participant', jury: '/dashboard/jury' }
  return map[auth.user?.role] || '/dashboard'
})

function togglePanel() {
  panelOpen.value = !panelOpen.value
}

function handleNotifClick(n) {
  if (!n.is_read) notifStore.markRead(n.id)
}

// Закрыть дропдаун при клике вне
function onClickOutside(e) {
  if (bellWrap.value && !bellWrap.value.contains(e.target)) {
    panelOpen.value = false
  }
}

// Запускаем/останавливаем поллинг при авторизации
watch(() => auth.isAuthenticated, (val) => {
  if (val) notifStore.startPolling()
  else notifStore.stopPolling()
}, { immediate: true })

onMounted(() => document.addEventListener('click', onClickOutside))
onBeforeUnmount(() => document.removeEventListener('click', onClickOutside))

function handleLogoError() {
  if (logoImg.value) logoImg.value.style.display = 'none'
}

async function handleLogout() {
  notifStore.stopPolling()
  await auth.logout()
  router.push('/')
}

function notifIcon(type) {
  return {
    registration: '#ic-check-circle',
    submission: '#ic-upload',
    evaluation: '#ic-award',
    deadline: '#ic-clock',
    assignment: '#ic-clipboard',
    system: '#ic-bell',
  }[type] || '#ic-bell'
}

function formatTime(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  const now = new Date()
  const diff = Math.floor((now - d) / 60000)
  if (diff < 1) return 'только что'
  if (diff < 60) return `${diff} мин. назад`
  if (diff < 1440) return `${Math.floor(diff / 60)} ч. назад`
  return d.toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' })
}
</script>

<style scoped>
.notif-bell-wrap {
  position: relative;
}

.notif-bell-btn {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border: none;
  background: rgba(255,255,255,0.1);
  border-radius: 10px;
  cursor: pointer;
  color: white;
  transition: background 0.2s;
}
.notif-bell-btn:hover,
.notif-bell-btn.active {
  background: rgba(255,255,255,0.2);
}

.notif-badge {
  position: absolute;
  top: 4px;
  right: 4px;
  min-width: 16px;
  height: 16px;
  padding: 0 3px;
  background: #ef4444;
  color: white;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

.notif-panel {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  width: 340px;
  background: white;
  border-radius: 14px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.15);
  z-index: 1000;
  overflow: hidden;
}

.notif-panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 16px;
  border-bottom: 1px solid #f1f5f9;
}


.notif-list {
  max-height: 380px;
  overflow-y: auto;
}

.notif-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px 16px;
  cursor: pointer;
  border-bottom: 1px solid #f8fafc;
  transition: background 0.15s;
}
.notif-item:last-child { border-bottom: none; }
.notif-item:hover { background: #f8fafc; }
.notif-item.unread { background: #f0f7ff; }
.notif-item.unread:hover { background: #e0f0ff; }

.notif-icon {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-top: 2px;
}
.notif-icon--registration { background: #d1fae5; color: #065f46; }
.notif-icon--submission   { background: #eff6ff; color: #1e40af; }
.notif-icon--evaluation   { background: #fef3c7; color: #92400e; }
.notif-icon--deadline     { background: #fee2e2; color: #991b1b; }
.notif-icon--assignment   { background: #f3e8ff; color: #6b21a8; }
.notif-icon--system       { background: #f1f5f9; color: #64748b; }
</style>
