<template>
  <div>
    <AppHeader />
    <div class="dashboard-container">
      <aside class="sidebar">
        <div class="sidebar-header">
          <div class="user-avatar">{{ initials }}</div>
          <h3>{{ auth.user?.full_name || auth.user?.first_name || 'Эксперт' }}</h3>
          <p class="user-role">Эксперт жюри</p>
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
            <div><h1>Кабинет эксперта</h1><p>Добро пожаловать, {{ auth.user?.first_name }}!</p></div>
          </div>
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-icon" style="background:#dbeafe;color:#1e40af"><svg class="icon"><use href="#ic-clipboard"/></svg></div>
              <div class="stat-info"><h3>{{ assignments.length }}</h3><p>Назначений</p></div>
            </div>
            <div class="stat-card">
              <div class="stat-icon" style="background:#fef3c7;color:#92400e"><svg class="icon"><use href="#ic-clock"/></svg></div>
              <div class="stat-info"><h3>{{ pendingCount }}</h3><p>Ожидают проверки</p></div>
            </div>
            <div class="stat-card">
              <div class="stat-icon" style="background:#d1fae5;color:#065f46"><svg class="icon"><use href="#ic-check-circle"/></svg></div>
              <div class="stat-info"><h3>{{ doneCount }}</h3><p>Проверено</p></div>
            </div>
            <div class="stat-card">
              <div class="stat-icon" style="background:#fce7f3;color:#9f1239"><svg class="icon"><use href="#ic-chart-bar"/></svg></div>
              <div class="stat-info"><h3>{{ avgScore }}</h3><p>Средний балл</p></div>
            </div>
          </div>
          <div class="section-grid">
            <div class="section-card">
              <h2>Работы для проверки</h2>
              <div v-for="s in pendingSubmissions.slice(0,3)" :key="s.id" class="event-item">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                  <div>
                    <h4>{{ s.participant_name }}</h4>
                    <p>{{ s.event_title }}</p>
                  </div>
                  <button class="btn-small btn-primary" style="background:var(--primary-blue);color:white;" @click="openEval(s)">Проверить</button>
                </div>
              </div>
              <div v-if="!pendingSubmissions.length" style="color:var(--text-gray);text-align:center;padding:20px;">Нет работ для проверки</div>
            </div>
            <div class="section-card">
              <h2>Мои назначения</h2>
              <div v-for="a in assignments.slice(0,4)" :key="a.id" class="event-item">
                <h4>{{ a.event_title }}</h4>
                <p>{{ a.submissions_count || 0 }} работ назначено</p>
              </div>
              <div v-if="!assignments.length" style="color:var(--text-gray);text-align:center;padding:20px;">Нет назначений</div>
            </div>
          </div>
        </div>

        <!-- Работы для проверки -->
        <div v-show="activeTab === 'submissions'">
          <div class="dashboard-header"><h1>Работы для проверки</h1></div>
          <div class="submissions-list">
            <div v-for="s in submissions" :key="s.id" class="submission-card" :class="{ checked: s.status === 'evaluated' }">
              <div class="submission-header">
                <div>
                  <h3>{{ s.participant_name }}</h3>
                  <p style="color:var(--text-gray);font-size:14px;">{{ s.event_title }}</p>
                </div>
                <span class="event-badge" :class="subStatusClass(s.status)">{{ subStatusLabel(s.status) }}</span>
              </div>
              <div class="submission-info">Загружено: {{ formatDate(s.submitted_at || s.created_at) }}</div>
              <div style="display:flex;gap:10px;margin-top:15px;">
                <a v-if="s.file" :href="s.file" class="btn-small btn-outline" target="_blank">
                  <svg class="icon icon-sm" style="margin-right:4px;"><use href="#ic-download"/></svg>Скачать работу
                </a>
                <button v-if="s.status !== 'evaluated'" class="btn-small btn-primary" style="background:var(--primary-blue);color:white;" @click="openEval(s)">Оценить</button>
                <span v-else style="color:#065f46;font-weight:600;">Проверено: {{ s.score }}/100</span>
              </div>
            </div>
          </div>
          <div v-if="!submissions.length" style="text-align:center;padding:60px;color:var(--text-gray);">Нет работ</div>
        </div>

        <!-- История оценок -->
        <div v-show="activeTab === 'history'">
          <div class="dashboard-header"><h1>История оценок</h1></div>
          <div class="submissions-list">
            <div v-for="e in evaluations" :key="e.id" class="submission-card checked">
              <div class="submission-header">
                <div><h3>{{ e.participant_name }}</h3><p style="color:var(--text-gray);font-size:14px;">{{ e.event_title }}</p></div>
                <div class="score-display"><span class="score" style="font-size:32px;">{{ e.score }}</span><span class="max-score" style="font-size:18px;">/100</span></div>
              </div>
              <div v-if="e.feedback" style="background:#f9fafb;padding:12px;border-radius:8px;font-size:14px;color:var(--text-gray);margin-top:10px;">{{ e.feedback }}</div>
            </div>
          </div>
          <div v-if="!evaluations.length" style="text-align:center;padding:60px;color:var(--text-gray);">Нет оценённых работ</div>
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
              <div class="form-group"><label>Организация</label><input v-model="profileForm.institution" type="text" class="form-input"></div>
              <div v-if="saved" style="color:#065f46;padding:10px;background:#d1fae5;border-radius:8px;margin-bottom:15px;">Сохранено!</div>
              <button type="submit" class="btn" style="background:var(--primary-blue);color:white;">Сохранить</button>
            </form>
          </div>
        </div>

      </main>
    </div>

    <!-- Модальное окно оценки -->
    <div v-if="evalModal" style="position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:9999;display:flex;align-items:center;justify-content:center;padding:20px;">
      <div style="background:white;border-radius:16px;padding:35px;max-width:600px;width:100%;max-height:90vh;overflow-y:auto;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:25px;">
          <h2 style="color:var(--primary-dark);">Оценить работу</h2>
          <button @click="evalModal = false" style="border:none;background:none;cursor:pointer;font-size:24px;color:var(--text-gray);">✕</button>
        </div>
        <p style="margin-bottom:20px;color:var(--text-gray);">Участник: <strong>{{ evalTarget?.participant_name }}</strong></p>
        <div class="form-group">
          <label>Оценка (0–100)</label>
          <input v-model.number="evalForm.score" type="number" min="0" max="100" class="form-input" placeholder="0–100">
        </div>
        <div style="margin-bottom:20px;">
          <label style="font-weight:600;font-size:14px;display:block;margin-bottom:12px;">Критерии оценки</label>
          <div v-for="c in criteria" :key="c.key" style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
            <input type="checkbox" v-model="evalForm[c.key]" :id="c.key" style="width:18px;height:18px;cursor:pointer;">
            <label :for="c.key" style="cursor:pointer;font-size:14px;">{{ c.label }}</label>
          </div>
        </div>
        <div class="form-group">
          <label>Комментарий</label>
          <textarea v-model="evalForm.feedback" class="form-input" rows="4" placeholder="Подробный отзыв по работе..."></textarea>
        </div>
        <div v-if="evalError" style="color:#ef4444;padding:10px;background:#fef2f2;border-radius:8px;margin-bottom:15px;">{{ evalError }}</div>
        <div style="display:flex;gap:10px;">
          <button class="btn" style="background:var(--primary-blue);color:white;flex:1;" @click="submitEval(false)">Опубликовать</button>
          <button class="btn btn-outline" style="flex:1;" @click="submitEval(true)">Сохранить черновик</button>
        </div>
      </div>
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
  { id: 'submissions', label: 'Проверка работ', icon: 'pen' },
  { id: 'history', label: 'История', icon: 'clipboard' },
  { id: 'profile', label: 'Профиль', icon: 'user' }
]
const initials = computed(() => {
  const u = auth.user
  return u ? ((u.first_name?.[0] || '') + (u.last_name?.[0] || '')).toUpperCase() || 'Э' : 'Э'
})

const submissions = ref([])
const evaluations = ref([])
const assignments = ref([])
const saved = ref(false)
const evalModal = ref(false)
const evalTarget = ref(null)
const evalError = ref('')
const profileForm = ref({
  first_name: auth.user?.first_name || '', last_name: auth.user?.last_name || '',
  grade_or_position: auth.user?.grade_or_position || '', institution: auth.user?.institution || ''
})
const evalForm = ref({ score: '', feedback: '', criteria_completeness: false, criteria_accuracy: false, criteria_examples: false, criteria_grammar: false })

const criteria = [
  { key: 'criteria_completeness', label: 'Полнота ответа' },
  { key: 'criteria_accuracy', label: 'Точность данных' },
  { key: 'criteria_examples', label: 'Наличие примеров' },
  { key: 'criteria_grammar', label: 'Грамотность изложения' }
]

const pendingSubmissions = computed(() => submissions.value.filter(s => s.status !== 'evaluated'))
const pendingCount = computed(() => pendingSubmissions.value.length)
const doneCount = computed(() => submissions.value.filter(s => s.status === 'evaluated').length)
const avgScore = computed(() => {
  const scored = evaluations.value.filter(e => e.score !== null)
  if (!scored.length) return '—'
  return Math.round(scored.reduce((sum, e) => sum + e.score, 0) / scored.length)
})

onMounted(async () => {
  await Promise.allSettled([
    api.get('/api/submissions/').then(r => { submissions.value = r.data.results || r.data }).catch(() => {}),
    api.get('/api/submissions/evaluations/').then(r => { evaluations.value = r.data.results || r.data }).catch(() => {})
  ])
})

function openEval(s) {
  evalTarget.value = s
  evalForm.value = { score: '', feedback: '', criteria_completeness: false, criteria_accuracy: false, criteria_examples: false, criteria_grammar: false }
  evalError.value = ''
  evalModal.value = true
}

async function submitEval(isDraft) {
  if (!isDraft && (evalForm.value.score === '' || evalForm.value.score < 0 || evalForm.value.score > 100)) {
    evalError.value = 'Введите оценку от 0 до 100'
    return
  }
  try {
    const payload = { submission: evalTarget.value.id, is_draft: isDraft, ...evalForm.value }
    const res = await api.post('/api/submissions/evaluations/', payload)
    if (!isDraft) {
      await api.post(`/api/submissions/evaluations/${res.data.id}/finalize/`)
      const s = submissions.value.find(s => s.id === evalTarget.value.id)
      if (s) { s.status = 'evaluated'; s.score = evalForm.value.score }
    }
    evaluations.value.push(res.data)
    evalModal.value = false
  } catch (e) {
    evalError.value = e.response?.data?.detail || 'Ошибка при сохранении оценки'
  }
}

async function saveProfile() {
  try { await auth.updateProfile(profileForm.value); saved.value = true; setTimeout(() => saved.value = false, 3000) } catch {}
}

function formatDate(d) { return d ? new Date(d).toLocaleDateString('ru-RU') : '—' }
function subStatusClass(s) { return { submitted: 'status-soon', under_review: 'status-soon', evaluated: 'status-active' }[s] || 'status-pending' }
function subStatusLabel(s) { return { submitted: 'Отправлено', under_review: 'На проверке', evaluated: 'Проверено', draft: 'Черновик' }[s] || s }
</script>
