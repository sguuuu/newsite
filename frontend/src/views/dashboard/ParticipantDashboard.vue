<template>
  <div>
    <AppHeader />
    <div class="dashboard-container">

      <!-- Sidebar -->
      <aside class="sidebar">
        <div class="sidebar-header">
          <div class="user-avatar">{{ initials }}</div>
          <h3>{{ auth.user?.full_name || auth.user?.first_name || 'Участник' }}</h3>
          <p class="user-role">Участник</p>
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
            <div><h1>Мой кабинет</h1><p>Добро пожаловать, {{ auth.user?.first_name || 'Участник' }}!</p></div>
          </div>
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-icon" style="background:#dbeafe;color:#1e40af"><svg class="icon"><use href="#ic-calendar"/></svg></div>
              <div class="stat-info"><h3>{{ myEvents.length }}</h3><p>Мои мероприятия</p></div>
            </div>
            <div class="stat-card">
              <div class="stat-icon" style="background:#d1fae5;color:#065f46"><svg class="icon"><use href="#ic-upload"/></svg></div>
              <div class="stat-info"><h3>{{ submissions.length }}</h3><p>Поданных работ</p></div>
            </div>
            <div class="stat-card">
              <div class="stat-icon" style="background:#fef3c7;color:#92400e"><svg class="icon"><use href="#ic-check-circle"/></svg></div>
              <div class="stat-info"><h3>{{ evaluatedCount }}</h3><p>Проверено</p></div>
            </div>
            <div class="stat-card">
              <div class="stat-icon" style="background:#fce7f3;color:#9f1239"><svg class="icon"><use href="#ic-trophy"/></svg></div>
              <div class="stat-info"><h3>{{ prizes }}</h3><p>Призовых мест</p></div>
            </div>
          </div>
          <div class="section-grid">
            <div class="section-card">
              <h2>Ближайшие мероприятия</h2>
              <div v-for="ev in myEvents.slice(0,3)" :key="ev.id" class="event-item">
                <span class="event-badge" :class="statusClass(effectiveStatus(ev))">{{ statusLabel(effectiveStatus(ev)) }}</span>
                <h4>{{ ev.title }}</h4>
                <p>Дедлайн: {{ formatDate(ev.registration_deadline) }}</p>
                <button class="btn-small btn-outline" @click="$router.push('/events/' + ev.id)">Перейти</button>
              </div>
              <div v-if="!myEvents.length" style="color:var(--text-gray);font-size:14px;padding:20px 0;text-align:center;">Нет активных мероприятий</div>
            </div>
            <div class="section-card">
              <h2>Последние уведомления</h2>
              <div v-for="n in notifications.slice(0,4)" :key="n.id" class="notification-item" :class="{ unread: !n.is_read }">
                <div><h4>{{ n.title }}</h4><p>{{ n.message }}</p><span class="notif-time">{{ timeAgo(n.created_at) }}</span></div>
              </div>
              <div v-if="!notifications.length" style="color:var(--text-gray);font-size:14px;padding:20px 0;text-align:center;">Нет уведомлений</div>
            </div>
          </div>
        </div>

        <!-- Мои мероприятия -->
        <div v-show="activeTab === 'events'">
          <div class="dashboard-header"><h1>Мои мероприятия</h1></div>
          <div v-for="ev in myEvents" :key="ev.id" class="event-item">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;">
              <div>
                <span class="event-badge" :class="statusClass(effectiveStatus(ev))" style="margin-bottom:8px;display:inline-block">{{ statusLabel(effectiveStatus(ev)) }}</span>
                <h4>{{ ev.title }}</h4>
                <p>{{ formatDate(ev.start_date) }} — {{ formatDate(ev.end_date) }}</p>
              </div>
              <button class="btn-small btn-outline" @click="$router.push('/events/' + ev.id)">Подробнее</button>
            </div>
          </div>
          <div v-if="!myEvents.length" style="text-align:center;padding:60px;color:var(--text-gray);">
            <p>Вы ещё не зарегистрированы ни на одно мероприятие</p>
            <button class="btn" style="background:var(--primary-blue);color:white;margin-top:20px;" @click="$router.push('/events')">Найти мероприятие</button>
          </div>
        </div>

        <!-- Мои работы -->
        <div v-show="activeTab === 'submissions'">
          <div class="dashboard-header"><h1>Мои работы</h1></div>

          <!-- Форма загрузки -->
          <div class="section-card" style="margin-bottom:30px;">
            <h2 style="margin-bottom:16px;">Загрузить работу</h2>
            <form @submit.prevent="uploadSubmission" style="display:flex;flex-direction:column;gap:14px;">
              <div class="form-group">
                <label>Мероприятие</label>
                <select v-model="uploadForm.event_id" class="form-input" required>
                  <option value="" disabled>Выберите мероприятие</option>
                  <option v-for="ev in activeEvents" :key="ev.id" :value="ev.id">{{ ev.title }}</option>
                </select>
              </div>
              <div class="form-group">
                <label>Файл работы</label>
                <input type="file" class="form-input" @change="onFileChange" accept=".pdf,.doc,.docx,.xls,.xlsx,.zip,.rar" required />
                <p style="font-size:12px;color:var(--text-gray);margin-top:4px;">
                  Допустимые форматы: PDF, Word (.doc/.docx), Excel (.xls/.xlsx), ZIP, RAR. Макс. размер: 20 МБ.
                </p>
              </div>
              <div v-if="uploadError" style="color:#991b1b;background:#fef2f2;padding:10px;border-radius:8px;font-size:14px;">{{ uploadError }}</div>
              <div v-if="uploadSuccess" style="color:#065f46;background:#d1fae5;padding:10px;border-radius:8px;font-size:14px;">{{ uploadSuccess }}</div>
              <button type="submit" class="btn" style="background:var(--primary-blue);color:white;width:fit-content;" :disabled="uploadLoading">
                {{ uploadLoading ? 'Загружаем...' : 'Загрузить работу' }}
              </button>
            </form>
          </div>

          <!-- Список работ -->
          <div class="submissions-list">
            <div v-for="s in submissions" :key="s.id" class="submission-card" :class="{ checked: s.status === 'evaluated' }">
              <div class="submission-header">
                <h3>{{ s.event_title || 'Мероприятие' }}</h3>
                <span class="event-badge" :class="subStatusClass(s.status)">{{ subStatusLabel(s.status) }}</span>
              </div>
              <div class="submission-info">
                Файл: {{ s.original_filename }} · {{ s.file_size_kb }} КБ · Загружено: {{ formatDate(s.created_at) }}
              </div>
              <!-- Кнопка «Подать официально» для черновиков -->
              <div v-if="s.status === 'draft'" style="margin-top:12px;display:flex;gap:10px;align-items:center;">
                <button class="btn btn-outline" style="font-size:13px;padding:6px 16px;" @click="submitWork(s)" :disabled="s._submitting">
                  {{ s._submitting ? 'Отправляем...' : 'Подать официально' }}
                </button>
                <span style="font-size:12px;color:var(--text-gray);">Черновик — работа ещё не отправлена на проверку</span>
              </div>
              <div v-if="s.status === 'evaluated'" class="submission-result" style="margin-top:15px;">
                <div class="score-display">
                  <span class="score">{{ s.score }}</span>
                  <span class="max-score">/100</span>
                </div>
                <div v-if="s.feedback" style="flex:1;padding:12px;background:#f9fafb;border-radius:8px;font-size:14px;color:var(--text-gray);">{{ s.feedback }}</div>
              </div>
            </div>
          </div>
          <div v-if="!submissions.length" style="text-align:center;padding:40px;color:var(--text-gray);">Вы ещё не загружали работы</div>
        </div>

        <!-- Результаты -->
        <div v-show="activeTab === 'results'">
          <div class="dashboard-header"><h1>Мои результаты</h1></div>
          <div class="achievements-grid">
            <div class="achievement-card gold"><div class="achievement-icon"><svg class="icon" style="width:40px;height:40px;color:#d97706"><use href="#ic-medal"/></svg></div><h3>{{ gold }}</h3><p>Золото</p></div>
            <div class="achievement-card silver"><div class="achievement-icon"><svg class="icon" style="width:40px;height:40px;color:#6b7280"><use href="#ic-medal"/></svg></div><h3>{{ silver }}</h3><p>Серебро</p></div>
            <div class="achievement-card bronze"><div class="achievement-icon"><svg class="icon" style="width:40px;height:40px;color:#b45309"><use href="#ic-medal"/></svg></div><h3>{{ bronze }}</h3><p>Бронза</p></div>
          </div>
          <div v-if="!results.length" style="text-align:center;padding:60px;color:var(--text-gray);">Результатов пока нет</div>
        </div>

        <!-- Уведомления -->
        <div v-show="activeTab === 'notifications'">
          <div class="dashboard-header">
            <h1>Уведомления</h1>
            <button class="btn btn-outline" @click="markAllRead">Прочитать все</button>
          </div>
          <div v-for="n in notifications" :key="n.id" class="notification-item" :class="{ unread: !n.is_read }" @click="markRead(n)">
            <div><h4>{{ n.title }}</h4><p>{{ n.message }}</p><span class="notif-time">{{ timeAgo(n.created_at) }}</span></div>
          </div>
          <div v-if="!notifications.length" style="text-align:center;padding:60px;color:var(--text-gray);">Нет уведомлений</div>
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
                <div class="form-group"><label>Отчество</label><input v-model="profileForm.patronymic" type="text" class="form-input"></div>
              </div>
              <div class="form-row">
                <div class="form-group"><label>Email</label><input v-model="profileForm.email" type="email" class="form-input" disabled style="background:#f9fafb;"></div>
                <div class="form-group"><label>Телефон</label><input v-model="profileForm.phone" type="tel" class="form-input"></div>
              </div>
              <div class="form-group"><label>Учреждение</label><input v-model="profileForm.institution" type="text" class="form-input"></div>
              <div v-if="profileSaved" style="color:#065f46;padding:10px;background:#d1fae5;border-radius:8px;margin-bottom:15px;">Профиль сохранён!</div>
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
  { id: 'events', label: 'Мои мероприятия', icon: 'calendar' },
  { id: 'submissions', label: 'Мои работы', icon: 'upload' },
  { id: 'results', label: 'Результаты', icon: 'trophy' },
  { id: 'notifications', label: 'Уведомления', icon: 'mail' },
  { id: 'profile', label: 'Профиль', icon: 'user' }
]

const initials = computed(() => {
  const u = auth.user
  return u ? ((u.first_name?.[0] || '') + (u.last_name?.[0] || '')).toUpperCase() || 'У' : 'У'
})

const myEvents = ref([])
const submissions = ref([])
const notifications = ref([])
const results = ref([])

// Upload form
const uploadForm = ref({ event_id: '', file: null })
const uploadLoading = ref(false)
const uploadError = ref('')
const uploadSuccess = ref('')
const activeEvents = computed(() => myEvents.value.filter(ev => ['active', 'upcoming'].includes(effectiveStatus(ev))))

function onFileChange(e) {
  uploadForm.value.file = e.target.files[0] || null
}

async function uploadSubmission() {
  uploadError.value = ''
  uploadSuccess.value = ''
  if (!uploadForm.value.event_id || !uploadForm.value.file) return
  uploadLoading.value = true
  try {
    const fd = new FormData()
    fd.append('event', uploadForm.value.event_id)
    fd.append('file', uploadForm.value.file)
    await api.post('/api/submissions/', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
    uploadSuccess.value = 'Работа успешно загружена! Статус: Черновик. Нажмите «Подать официально» когда будете готовы.'
    uploadForm.value = { event_id: '', file: null }
    const r = await api.get('/api/submissions/')
    submissions.value = r.data.results || r.data
  } catch (e) {
    uploadError.value = e.response?.data?.file?.[0] || e.response?.data?.detail || 'Ошибка при загрузке файла'
  } finally {
    uploadLoading.value = false
  }
}

async function submitWork(s) {
  s._submitting = true
  try {
    await api.post(`/api/submissions/${s.id}/submit/`)
    s.status = 'submitted'
  } catch (e) {
    alert(e.response?.data?.detail || 'Ошибка при отправке работы')
  } finally {
    s._submitting = false
  }
}

const profileSaved = ref(false)
const profileForm = ref({
  first_name: auth.user?.first_name || '',
  last_name: auth.user?.last_name || '',
  patronymic: auth.user?.patronymic || '',
  email: auth.user?.email || '',
  phone: auth.user?.phone || '',
  institution: auth.user?.institution || ''
})

const evaluatedCount = computed(() => submissions.value.filter(s => s.status === 'evaluated').length)
const prizes = computed(() => results.value.filter(r => r.place > 0 && r.place <= 3).length)
const gold = computed(() => results.value.filter(r => r.place === 1).length)
const silver = computed(() => results.value.filter(r => r.place === 2).length)
const bronze = computed(() => results.value.filter(r => r.place === 3).length)

onMounted(async () => {
  await Promise.allSettled([
    api.get('/api/events/?my=true').then(r => { myEvents.value = r.data.results || r.data }).catch(() => {}),
    api.get('/api/submissions/').then(r => { submissions.value = r.data.results || r.data }).catch(() => {}),
    api.get('/api/notifications/').then(r => { notifications.value = r.data.results || r.data }).catch(() => {}),
    api.get('/api/submissions/results/').then(r => { results.value = r.data.results || r.data }).catch(() => {})
  ])
})

async function markRead(n) {
  if (n.is_read) return
  try { await api.post(`/api/notifications/${n.id}/read/`); n.is_read = true } catch {}
}

async function markAllRead() {
  try { await api.post('/api/notifications/read-all/'); notifications.value.forEach(n => n.is_read = true) } catch {}
}

async function saveProfile() {
  try {
    await auth.updateProfile(profileForm.value)
    profileSaved.value = true
    setTimeout(() => profileSaved.value = false, 3000)
  } catch {}
}

function formatDate(d) { return d ? new Date(d).toLocaleDateString('ru-RU') : '—' }
function effectiveStatus(ev) {
  if (!ev) return 'unknown'
  if (ev.status === 'cancelled') return 'cancelled'
  const today = new Date(); today.setHours(0, 0, 0, 0)
  if (ev.end_date && new Date(ev.end_date) < today) return 'completed'
  if (ev.start_date && new Date(ev.start_date) <= today && ev.status !== 'completed') return 'active'
  return ev.status
}
function statusClass(s) { return { active: 'status-active', upcoming: 'status-soon', completed: 'status-completed', cancelled: 'status-completed' }[s] || 'status-pending' }
function statusLabel(s) { return { active: 'Активно', upcoming: 'Скоро', completed: 'Завершено', cancelled: 'Отменено', draft: 'Черновик' }[s] || s }
function subStatusClass(s) { return { draft: 'status-pending', submitted: 'status-soon', under_review: 'status-soon', evaluated: 'status-active' }[s] || 'status-pending' }
function subStatusLabel(s) { return { draft: 'Черновик', submitted: 'Отправлено', under_review: 'На проверке', evaluated: 'Проверено' }[s] || s }
function timeAgo(d) {
  if (!d) return ''
  const h = Math.floor((Date.now() - new Date(d)) / 3600000)
  return h < 24 ? `${h} ч. назад` : `${Math.floor(h / 24)} дн. назад`
}
</script>
