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
              <div class="stat-info"><h3>{{ totalEvents }}</h3><p>Участий в мероприятиях</p></div>
            </div>
            <div class="stat-card">
              <div class="stat-icon" style="background:#fef3c7;color:#92400e"><svg class="icon"><use href="#ic-check-circle"/></svg></div>
              <div class="stat-info"><h3>{{ totalSubmissions }}</h3><p>Сданных работ</p></div>
            </div>
          </div>
          <div class="section-grid">
            <div class="section-card">
              <h2>Последние активности учеников</h2>
              <div v-for="s in recentActivity.slice(0,5)" :key="s.id" class="user-item">
                <div class="user-avatar small">{{ s.initials || 'У' }}</div>
                <div>
                  <h4>{{ s.full_name }}</h4>
                  <p>{{ s.event_title }} · <span :style="subStatusColor(s.status)">{{ subStatusLabel(s.status) }}</span></p>
                </div>
              </div>
              <div v-if="!recentActivity.length" style="color:var(--text-gray);text-align:center;padding:20px;">Нет активностей</div>
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
            <span style="color:var(--text-gray);font-size:15px;">{{ students.length }} чел.</span>
          </div>

          <!-- Входящие заявки -->
          <div v-if="incomingRequests.length" class="section-card" style="margin-bottom:28px;border-left:4px solid var(--primary-blue);">
            <h2 style="margin-bottom:14px;">Заявки на прикрепление <span style="background:#dbeafe;color:#1d4ed8;font-size:13px;padding:2px 10px;border-radius:20px;margin-left:8px;">{{ incomingRequests.length }}</span></h2>
            <div v-for="req in incomingRequests" :key="req.id"
                 style="display:flex;align-items:center;justify-content:space-between;padding:14px 16px;background:#f8fafc;border-radius:10px;margin-bottom:10px;gap:12px;flex-wrap:wrap;">
              <div>
                <div style="font-weight:600;color:var(--primary-dark);">{{ req.participant_name }}</div>
                <div style="font-size:13px;color:var(--text-gray);margin-top:2px;">
                  {{ req.participant_institution }}{{ req.participant_grade ? ' · ' + req.participant_grade : '' }}
                </div>
                <div v-if="req.message" style="font-size:13px;color:var(--text-gray);font-style:italic;margin-top:4px;">"{{ req.message }}"</div>
              </div>
              <div style="display:flex;gap:8px;flex-shrink:0;">
                <button @click="approveRequest(req.id)"
                  style="padding:7px 16px;background:#16a34a;color:white;border:none;border-radius:8px;cursor:pointer;font-size:14px;font-weight:600;">
                  ✓ Принять
                </button>
                <button @click="rejectRequest(req.id)"
                  style="padding:7px 16px;background:none;border:1px solid #ef4444;color:#ef4444;border-radius:8px;cursor:pointer;font-size:14px;">
                  Отклонить
                </button>
              </div>
            </div>
          </div>

          <!-- Список учеников -->
          <div v-if="!students.length" style="text-align:center;padding:60px;color:var(--text-gray);">
            <p>У вас пока нет учеников</p>
            <p style="font-size:14px;margin-top:8px;">Ученики сами отправляют заявку на прикрепление через свой профиль</p>
          </div>

          <div v-for="s in students" :key="s.id" style="border:1px solid #e5e7eb;border-radius:12px;margin-bottom:14px;overflow:hidden;">
            <!-- Student header -->
            <div style="display:flex;justify-content:space-between;align-items:center;padding:16px 20px;background:#f8fafc;cursor:pointer;"
              @click="toggleStudent(s.id)">
              <div style="display:flex;align-items:center;gap:12px;">
                <div class="user-avatar small">{{ s.initials || 'У' }}</div>
                <div>
                  <div style="font-weight:600;color:var(--primary-dark);">{{ s.full_name }}</div>
                  <div style="font-size:13px;color:var(--text-gray);">{{ s.institution }}{{ s.grade_or_position ? ' · ' + s.grade_or_position : '' }}</div>
                </div>
              </div>
              <div style="display:flex;align-items:center;gap:16px;">
                <div style="text-align:center;">
                  <div style="font-weight:600;font-size:16px;color:var(--primary-blue);">{{ s.events?.length || 0 }}</div>
                  <div style="font-size:11px;color:var(--text-gray);">мероприятий</div>
                </div>
                <div style="text-align:center;">
                  <div style="font-weight:600;font-size:16px;color:#065f46;">{{ s.submissions?.length || 0 }}</div>
                  <div style="font-size:11px;color:var(--text-gray);">работ</div>
                </div>
                <button class="btn-icon btn-icon-danger" title="Отвязать" style="margin-left:8px;"
                  @click.stop="removeStudent(s.id)">
                  <svg class="icon"><use href="#ic-close"/></svg>
                </button>
                <svg class="icon" style="color:var(--text-gray);transition:transform 0.2s;"
                  :style="expandedStudent === s.id ? 'transform:rotate(180deg)' : ''">
                  <use href="#ic-chart-bar"/>
                </svg>
              </div>
            </div>

            <!-- Expanded: events + submissions -->
            <div v-if="expandedStudent === s.id" style="padding:16px 20px;">
              <!-- Events -->
              <div style="margin-bottom:16px;">
                <h4 style="font-size:14px;font-weight:600;margin-bottom:10px;color:var(--text-gray);">МЕРОПРИЯТИЯ</h4>
                <div v-if="!s.events?.length" style="font-size:13px;color:var(--text-gray);">Не участвует ни в одном мероприятии</div>
                <div v-for="ev in s.events" :key="ev.id" style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                  <span class="event-badge" :class="statusClass(ev.status)" style="font-size:11px;">{{ statusLabel(ev.status) }}</span>
                  <span style="font-size:14px;">{{ ev.title }}</span>
                </div>
              </div>
              <!-- Submissions -->
              <div>
                <h4 style="font-size:14px;font-weight:600;margin-bottom:10px;color:var(--text-gray);">РАБОТЫ</h4>
                <div v-if="!s.submissions?.length" style="font-size:13px;color:var(--text-gray);">Работ не подавалось</div>
                <div v-for="sub in s.submissions" :key="sub.id"
                  style="background:#f9fafb;border-radius:8px;padding:10px 14px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center;">
                  <div>
                    <div style="font-size:14px;font-weight:500;">{{ sub.event_title }}</div>
                    <div style="font-size:12px;color:var(--text-gray);margin-top:2px;">
                      {{ sub.submitted_at ? 'Сдано: ' + formatDate(sub.submitted_at) : 'Черновик' }}
                    </div>
                  </div>
                  <div style="display:flex;align-items:center;gap:10px;">
                    <span class="event-badge" :class="subStatusClass(sub.status)" style="font-size:11px;">{{ subStatusLabel(sub.status) }}</span>
                    <span v-if="sub.score !== null" style="font-weight:600;color:var(--primary-blue);">{{ sub.score }}/100</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Аналитика -->
        <div v-show="activeTab === 'analytics'">
          <div class="dashboard-header">
            <div><h1>Аналитика моих учеников</h1><p>Статистика по мероприятиям и работам ваших учеников</p></div>
          </div>
          <AnalyticsPanel v-if="activeTab === 'analytics'" />
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
              <div class="form-group"><label>Должность</label><input v-model="profileForm.grade_or_position" type="text" class="form-input"></div>
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
import AnalyticsPanel from '@/components/AnalyticsPanel.vue'
import { useAuthStore } from '@/stores/auth.js'
import api from '@/api/index.js'

const auth = useAuthStore()
const activeTab = ref('overview')
const tabs = [
  { id: 'overview', label: 'Обзор', icon: 'chart-bar' },
  { id: 'students', label: 'Мои ученики', icon: 'users' },
  { id: 'analytics', label: 'Аналитика', icon: 'chart-bar' },
  { id: 'profile', label: 'Профиль', icon: 'user' }
]
const initials = computed(() => {
  const u = auth.user
  return u ? ((u.first_name?.[0] || '') + (u.last_name?.[0] || '')).toUpperCase() || 'П' : 'П'
})

const students = ref([])
const notifications = ref([])
const expandedStudent = ref(null)
const saved = ref(false)
const incomingRequests = ref([])

const profileForm = ref({
  first_name: auth.user?.first_name || '',
  last_name: auth.user?.last_name || '',
  grade_or_position: auth.user?.grade_or_position || '',
  institution: auth.user?.institution || ''
})

const totalEvents = computed(() => students.value.reduce((sum, s) => sum + (s.events?.length || 0), 0))
const totalSubmissions = computed(() => students.value.reduce((sum, s) => sum + (s.submissions?.length || 0), 0))

const recentActivity = computed(() => {
  const all = []
  for (const s of students.value) {
    for (const sub of s.submissions || []) {
      all.push({ id: `${s.id}-${sub.id}`, full_name: s.full_name, initials: s.initials, ...sub })
    }
  }
  return all.sort((a, b) => new Date(b.submitted_at || 0) - new Date(a.submitted_at || 0))
})

onMounted(async () => {
  await Promise.allSettled([
    api.get('/api/auth/my-students/').then(r => { students.value = r.data }).catch(() => {}),
    api.get('/api/notifications/').then(r => { notifications.value = r.data.results || r.data }).catch(() => {}),
    api.get('/api/auth/teacher-requests/').then(r => { incomingRequests.value = r.data.results || r.data }).catch(() => {}),
  ])
})

function toggleStudent(id) {
  expandedStudent.value = expandedStudent.value === id ? null : id
}

async function approveRequest(id) {
  try {
    await api.post(`/api/auth/teacher-requests/${id}/approve/`)
    incomingRequests.value = incomingRequests.value.filter(r => r.id !== id)
    const res = await api.get('/api/auth/my-students/')
    students.value = res.data
  } catch {}
}

async function rejectRequest(id) {
  try {
    await api.post(`/api/auth/teacher-requests/${id}/reject/`)
    incomingRequests.value = incomingRequests.value.filter(r => r.id !== id)
  } catch {}
}

async function removeStudent(id) {
  if (!confirm('Отвязать ученика? Он останется на платформе, но перестанет быть в вашем списке.')) return
  try {
    await api.delete(`/api/auth/my-students/${id}/remove/`)
    students.value = students.value.filter(s => s.id !== id)
  } catch {}
}

async function saveProfile() {
  try { await auth.updateProfile(profileForm.value); saved.value = true; setTimeout(() => saved.value = false, 3000) } catch {}
}

function formatDate(d) { return d ? new Date(d).toLocaleDateString('ru-RU') : '—' }
function statusClass(s) { return { active: 'status-active', upcoming: 'status-soon', completed: 'status-completed' }[s] || 'status-pending' }
function statusLabel(s) { return { active: 'Активно', upcoming: 'Скоро', completed: 'Завершено', draft: 'Черновик' }[s] || s }
function subStatusClass(s) { return { submitted: 'status-soon', under_review: 'status-soon', evaluated: 'status-active', draft: 'status-pending' }[s] || 'status-pending' }
function subStatusLabel(s) { return { draft: 'Черновик', submitted: 'Отправлено', under_review: 'На проверке', evaluated: 'Проверено' }[s] || s }
function subStatusColor(s) { return { evaluated: 'color:#065f46', submitted: 'color:#92400e', under_review: 'color:#1e40af' }[s] || '' }
function timeAgo(d) {
  if (!d) return ''
  const h = Math.floor((Date.now() - new Date(d)) / 3600000)
  return h < 24 ? `${h} ч. назад` : `${Math.floor(h / 24)} дн. назад`
}
</script>
