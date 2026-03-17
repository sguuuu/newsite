<template>
  <div>
    <AppHeader />
    <div class="dashboard-container">
      <aside class="sidebar">
        <div class="sidebar-header">
          <div class="user-avatar">{{ initials }}</div>
          <h3>{{ auth.user?.full_name || auth.user?.first_name || 'Педагог' }}</h3>
          <p class="user-role">Педагог</p>
        </div>
        <nav class="sidebar-nav">
          <button v-for="tab in tabs" :key="tab.id" class="sidebar-link" :class="{ active: activeTab === tab.id }" @click="activeTab = tab.id">
            <svg class="icon"><use :href="'#ic-' + tab.icon"/></svg>{{ tab.label }}
          </button>
        </nav>
      </aside>

      <main class="dashboard-main">

        <!-- Обзор -->
        <div v-show="activeTab === 'overview'">
          <div class="dashboard-header">
            <div><h1>Кабинет педагога</h1><p>Добро пожаловать, {{ auth.user?.first_name }}!</p></div>
          </div>
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-icon" style="background:#dbeafe;color:#1e40af"><svg class="icon"><use href="#ic-users"/></svg></div>
              <div class="stat-info"><h3>{{ students.length }}</h3><p>Мои ученики</p></div>
            </div>
            <div class="stat-card">
              <div class="stat-icon" style="background:#d1fae5;color:#065f46"><svg class="icon"><use href="#ic-calendar"/></svg></div>
              <div class="stat-info"><h3>{{ activeEvents }}</h3><p>Активных мероприятий</p></div>
            </div>
            <div class="stat-card">
              <div class="stat-icon" style="background:#fef3c7;color:#92400e"><svg class="icon"><use href="#ic-check-circle"/></svg></div>
              <div class="stat-info"><h3>{{ submittedCount }}</h3><p>Работ подано</p></div>
            </div>
            <div class="stat-card">
              <div class="stat-icon" style="background:#fce7f3;color:#9f1239"><svg class="icon"><use href="#ic-trophy"/></svg></div>
              <div class="stat-info"><h3>{{ prizesCount }}</h3><p>Призёров</p></div>
            </div>
          </div>
          <div class="section-grid">
            <div class="section-card">
              <h2>Последние активности учеников</h2>
              <div v-for="s in studentSubmissions.slice(0,4)" :key="s.id" class="user-item">
                <div class="user-avatar small">{{ s.student_initials || 'УЧ' }}</div>
                <div><h4>{{ s.student_name }}</h4><p>{{ s.event_title }} • {{ subStatusLabel(s.status) }}</p></div>
              </div>
              <div v-if="!studentSubmissions.length" style="color:var(--text-gray);text-align:center;padding:20px;">Нет активностей</div>
            </div>
            <div class="section-card">
              <h2>Уведомления</h2>
              <div v-for="n in notifications.slice(0,4)" :key="n.id" class="notification-item" :class="{ unread: !n.is_read }">
                <div><h4>{{ n.title }}</h4><p>{{ n.message }}</p><span class="notif-time">{{ timeAgo(n.created_at) }}</span></div>
              </div>
              <div v-if="!notifications.length" style="color:var(--text-gray);text-align:center;padding:20px;">Нет уведомлений</div>
            </div>
          </div>
        </div>

        <!-- Ученики -->
        <div v-show="activeTab === 'students'">
          <div class="dashboard-header">
            <h1>Мои ученики</h1>
            <span style="color:var(--text-gray);font-size:15px;">{{ students.length }} человек</span>
          </div>
          <div class="users-table">
            <div class="table-header" style="grid-template-columns:2fr 2fr 1fr 1fr 1fr;">
              <div>Ученик</div><div>Email</div><div>Учреждение</div><div>Работ</div><div>Призов</div>
            </div>
            <div v-for="s in students" :key="s.id" class="user-row" style="grid-template-columns:2fr 2fr 1fr 1fr 1fr;">
              <div class="user-cell">
                <div class="user-avatar small">{{ studentInitials(s) }}</div>
                <span>{{ s.full_name || s.email }}</span>
              </div>
              <div style="font-size:14px;color:var(--text-gray);">{{ s.email }}</div>
              <div style="font-size:14px;">{{ s.institution || '—' }}</div>
              <div>{{ s.submission_count || 0 }}</div>
              <div>{{ s.prize_count || 0 }}</div>
            </div>
            <div v-if="!students.length" style="padding:30px;text-align:center;color:var(--text-gray);">Учеников не найдено</div>
          </div>
        </div>

        <!-- Мероприятия -->
        <div v-show="activeTab === 'events'">
          <div class="dashboard-header"><h1>Мероприятия учеников</h1></div>
          <div class="admin-events-grid">
            <div v-for="ev in events" :key="ev.id" class="admin-event-card">
              <div class="event-header">
                <div><h3>{{ ev.title }}</h3><p>{{ typeLabel(ev.event_type) }} • {{ formatDate(ev.start_date) }}</p></div>
                <span class="event-badge" :class="statusClass(ev.status)">{{ statusLabel(ev.status) }}</span>
              </div>
              <div class="event-stats">
                <div class="stat-item"><span class="stat-label">Участников</span><span class="stat-value">{{ ev.participant_count || 0 }}</span></div>
                <div class="stat-item"><span class="stat-label">Моих учеников</span><span class="stat-value">0</span></div>
              </div>
              <div class="event-actions">
                <button class="btn-small btn-outline" @click="$router.push('/events/' + ev.id)">Подробнее</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Профиль -->
        <div v-show="activeTab === 'profile'">
          <div class="dashboard-header"><h1>Мой профиль</h1></div>
          <div class="profile-section">
            <h2>Личные данные</h2>
            <form class="profile-form" @submit.prevent="saveProfile">
              <div class="form-row">
                <div class="form-group"><label>Фамилия</label><input v-model="profileForm.last_name" type="text" class="form-input"></div>
                <div class="form-group"><label>Имя</label><input v-model="profileForm.first_name" type="text" class="form-input"></div>
              </div>
              <div class="form-group"><label>Должность / Класс</label><input v-model="profileForm.grade_or_position" type="text" class="form-input"></div>
              <div class="form-group"><label>Учреждение</label><input v-model="profileForm.institution" type="text" class="form-input"></div>
              <div v-if="saved" style="color:#065f46;padding:10px;background:#d1fae5;border-radius:8px;margin-bottom:15px;">Сохранено!</div>
              <button type="submit" class="btn" style="background:var(--primary-blue);color:white;">Сохранить</button>
            </form>
          </div>
        </div>

      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AppHeader from '@/components/AppHeader.vue'
import { useAuthStore } from '@/stores/auth.js'
import api from '@/api/index.js'

const auth = useAuthStore()
const activeTab = ref('overview')
const tabs = [
  { id: 'overview', label: 'Обзор', icon: 'chart-bar' },
  { id: 'students', label: 'Мои ученики', icon: 'users' },
  { id: 'events', label: 'Мероприятия', icon: 'calendar' },
  { id: 'profile', label: 'Профиль', icon: 'user' }
]
const initials = computed(() => {
  const u = auth.user
  return u ? ((u.first_name?.[0] || '') + (u.last_name?.[0] || '')).toUpperCase() || 'П' : 'П'
})
const students = ref([])
const events = ref([])
const studentSubmissions = ref([])
const notifications = ref([])
const saved = ref(false)
const profileForm = ref({
  first_name: auth.user?.first_name || '', last_name: auth.user?.last_name || '',
  grade_or_position: auth.user?.grade_or_position || '', institution: auth.user?.institution || ''
})
const activeEvents = computed(() => events.value.filter(e => e.status === 'active').length)
const submittedCount = computed(() => studentSubmissions.value.length)
const prizesCount = ref(0)

onMounted(async () => {
  await Promise.allSettled([
    api.get('/api/auth/users/?role=participant').then(r => { students.value = r.data.results || r.data }).catch(() => {}),
    api.get('/api/events/').then(r => { events.value = r.data.results || r.data }).catch(() => {}),
    api.get('/api/submissions/').then(r => { studentSubmissions.value = r.data.results || r.data }).catch(() => {}),
    api.get('/api/notifications/').then(r => { notifications.value = r.data.results || r.data }).catch(() => {})
  ])
})

async function saveProfile() {
  try { await auth.updateProfile(profileForm.value); saved.value = true; setTimeout(() => saved.value = false, 3000) } catch {}
}

function studentInitials(s) { return ((s.first_name?.[0] || '') + (s.last_name?.[0] || '')).toUpperCase() || 'У' }
function formatDate(d) { return d ? new Date(d).toLocaleDateString('ru-RU') : '—' }
function statusClass(s) { return { active: 'status-active', upcoming: 'status-soon', completed: 'status-completed' }[s] || 'status-pending' }
function statusLabel(s) { return { active: 'Активно', upcoming: 'Скоро', completed: 'Завершено' }[s] || s }
function typeLabel(t) { return { olympiad: 'Олимпиада', competition: 'Конкурс' }[t] || t }
function subStatusLabel(s) { return { submitted: 'Отправлено', evaluated: 'Проверено', under_review: 'На проверке' }[s] || s }
function timeAgo(d) {
  if (!d) return ''
  const h = Math.floor((Date.now() - new Date(d)) / 3600000)
  return h < 24 ? `${h} ч. назад` : `${Math.floor(h / 24)} дн. назад`
}
</script>
