<template>
  <div>
    <AppHeader />
    <div class="dashboard-container">

      <!-- Sidebar -->
      <aside class="sidebar">
        <div class="sidebar-header">
          <div class="user-avatar">{{ initials }}</div>
          <h3>{{ auth.user?.full_name || 'Администратор' }}</h3>
          <p class="user-role">Администратор</p>
        </div>
        <nav class="sidebar-nav">
          <button v-for="tab in tabs" :key="tab.id"
            class="sidebar-link" :class="{ active: activeTab === tab.id }"
            @click="activeTab = tab.id">
            <svg class="icon" aria-hidden="true"><use :href="'#ic-' + tab.icon"/></svg>
            {{ tab.label }}
          </button>
        </nav>
      </aside>

      <!-- Main content -->
      <main class="dashboard-main">

        <!-- ====== ОБЗОР ====== -->
        <div v-show="activeTab === 'overview'">
          <div class="dashboard-header">
            <div>
              <h1>Обзор платформы</h1>
              <p>Актуальное состояние системы и ключевые показатели</p>
            </div>
          </div>

          <!-- Stat cards -->
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-icon" style="background:#dbeafe;color:#1e40af">
                <svg class="icon" aria-hidden="true"><use href="#ic-users"/></svg>
              </div>
              <div class="stat-info">
                <h3>{{ stats.total_users || '—' }}</h3>
                <p>Всего пользователей</p>
                <span style="color:#10b981;font-size:13px;">↑ +24 за неделю</span>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon" style="background:#d1fae5;color:#065f46">
                <svg class="icon" aria-hidden="true"><use href="#ic-calendar"/></svg>
              </div>
              <div class="stat-info">
                <h3>{{ stats.active_events || '—' }}</h3>
                <p>Активных мероприятий</p>
                <span style="color:#10b981;font-size:13px;">↑ +3 за месяц</span>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon" style="background:#fef3c7;color:#92400e">
                <svg class="icon" aria-hidden="true"><use href="#ic-check-circle"/></svg>
              </div>
              <div class="stat-info">
                <h3>{{ stats.completed_submissions || '—' }}</h3>
                <p>Завершённых работ</p>
                <span style="color:#10b981;font-size:13px;">↑ +156 за месяц</span>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon" style="background:#fce7f3;color:#9f1239">
                <svg class="icon" aria-hidden="true"><use href="#ic-scale"/></svg>
              </div>
              <div class="stat-info">
                <h3>{{ stats.jury_count || '—' }}</h3>
                <p>Экспертов жюри</p>
                <span style="color:#10b981;font-size:13px;">↑ +5 за месяц</span>
              </div>
            </div>
          </div>

          <!-- Role distribution + Popular events -->
          <div class="section-grid">

            <!-- Распределение по ролям — НОВЫЙ ДИЗАЙН -->
            <div class="section-card">
              <h2>Распределение по ролям</h2>
              <div class="roles-cards-grid">
                <div class="role-stat-card role-stat-card--participants">
                  <div class="role-stat-icon">
                    <svg class="icon icon-lg" aria-hidden="true"><use href="#ic-users"/></svg>
                  </div>
                  <div class="role-stat-number">{{ roleStats.participants }}</div>
                  <div class="role-stat-label">Участники</div>
                  <div class="role-stat-bar">
                    <div class="role-stat-fill" :style="{ width: roleStats.participantsPct + '%' }"></div>
                  </div>
                  <div class="role-stat-percent">{{ roleStats.participantsPct }}%</div>
                </div>
                <div class="role-stat-card role-stat-card--teachers">
                  <div class="role-stat-icon">
                    <svg class="icon icon-lg" aria-hidden="true"><use href="#ic-user"/></svg>
                  </div>
                  <div class="role-stat-number">{{ roleStats.teachers }}</div>
                  <div class="role-stat-label">Педагоги</div>
                  <div class="role-stat-bar">
                    <div class="role-stat-fill" :style="{ width: roleStats.teachersPct + '%' }"></div>
                  </div>
                  <div class="role-stat-percent">{{ roleStats.teachersPct }}%</div>
                </div>
                <div class="role-stat-card role-stat-card--jury">
                  <div class="role-stat-icon">
                    <svg class="icon icon-lg" aria-hidden="true"><use href="#ic-scale"/></svg>
                  </div>
                  <div class="role-stat-number">{{ roleStats.jury }}</div>
                  <div class="role-stat-label">Эксперты</div>
                  <div class="role-stat-bar">
                    <div class="role-stat-fill" :style="{ width: roleStats.juryPct + '%' }"></div>
                  </div>
                  <div class="role-stat-percent">{{ roleStats.juryPct }}%</div>
                </div>
              </div>
            </div>

            <!-- Популярные мероприятия -->
            <div class="section-card">
              <h2>Популярные мероприятия</h2>
              <div class="popular-events">
                <div v-for="(ev, i) in popularEvents" :key="ev.id" class="popular-item">
                  <span class="popular-item-name">
                    <span style="color:var(--text-gray); margin-right:8px;">{{ i + 1 }}.</span>{{ ev.title }}
                  </span>
                  <span class="popular-count">{{ ev.participant_count }} уч.</span>
                </div>
                <div v-if="!popularEvents.length" style="color:var(--text-gray); font-size:14px; padding:20px 0; text-align:center;">Нет данных</div>
              </div>
            </div>
          </div>

          <!-- Activity + Recent registrations -->
          <div class="section-grid">
            <div class="section-card">
              <h2>Активность пользователей</h2>
              <div class="chart-placeholder">
                <svg class="icon icon-lg" aria-hidden="true" style="color:#93c5fd"><use href="#ic-chart-bar"/></svg>
                <p>График активности за последние 30 дней</p>
              </div>
            </div>
            <div class="section-card">
              <h2>Последние регистрации</h2>
              <div class="recent-users">
                <div v-for="u in recentUsers" :key="u.id" class="user-item">
                  <div class="user-avatar small">{{ userInitials(u) }}</div>
                  <div>
                    <h4>{{ u.full_name || u.email }}</h4>
                    <p>{{ roleLabel(u.role) }} • {{ timeAgo(u.date_joined) }}</p>
                  </div>
                </div>
                <div v-if="!recentUsers.length" style="color:var(--text-gray); font-size:14px; text-align:center; padding:20px 0;">Нет данных</div>
              </div>
            </div>
          </div>
        </div>

        <!-- ====== ПОЛЬЗОВАТЕЛИ ====== -->
        <div v-show="activeTab === 'users'">
          <div class="dashboard-header">
            <h1>Управление пользователями</h1>
            <button class="btn btn-primary" style="background:var(--primary-blue);color:white;" @click="openCreateUser">+ Создать пользователя</button>
          </div>
          <div class="filter-section">
            <input v-model="userSearch" type="text" placeholder="Поиск по имени или email...">
            <select v-model="userRoleFilter">
              <option value="">Все роли</option>
              <option value="participant">Участник</option>
              <option value="teacher">Педагог</option>
              <option value="jury">Жюри</option>
              <option value="admin">Администратор</option>
            </select>
            <select v-model="userStatusFilter">
              <option value="">Все статусы</option>
              <option value="active">Активные</option>
              <option value="blocked">Заблокированные</option>
            </select>
          </div>
          <div class="users-table">
            <div class="table-header">
              <div>Пользователь</div><div>Роль</div><div>Email</div>
              <div>Дата регистрации</div><div>Статус</div><div>Действия</div>
            </div>
            <div v-for="u in filteredUsers" :key="u.id" class="user-row">
              <div class="user-cell">
                <div class="user-avatar small">{{ userInitials(u) }}</div>
                <span>{{ u.full_name || u.email }}</span>
              </div>
              <div><span class="role-badge" :class="u.role">{{ roleLabel(u.role) }}</span></div>
              <div style="font-size:14px; color:var(--text-gray);">{{ u.email }}</div>
              <div style="font-size:14px;">{{ formatDate(u.date_joined) }}</div>
              <div><span class="status-badge" :class="u.status">{{ statusLabel(u.status) }}</span></div>
              <div class="action-buttons" style="display:flex;gap:8px;">
                <button class="btn-icon" title="Редактировать" @click="openEditUser(u)"><svg class="icon"><use href="#ic-edit"/></svg></button>
                <button class="btn-icon btn-icon-danger" title="Удалить" @click="deleteUser(u.id)"><svg class="icon"><use href="#ic-trash"/></svg></button>
              </div>
            </div>
            <div v-if="!filteredUsers.length" style="padding:30px; text-align:center; color:var(--text-gray);">Пользователей не найдено</div>
          </div>
        </div>

        <!-- ====== МЕРОПРИЯТИЯ ====== -->
        <div v-show="activeTab === 'events'">
          <div class="dashboard-header">
            <h1>Управление мероприятиями</h1>
            <button class="btn btn-primary" style="background:var(--primary-blue);color:white;" @click="openCreateEvent">+ Создать мероприятие</button>
          </div>
          <div class="filter-tabs">
            <button class="filter-tab" :class="{ active: eventFilter === '' }" @click="eventFilter = ''">Все</button>
            <button class="filter-tab" :class="{ active: eventFilter === 'active' }" @click="eventFilter = 'active'">Активные</button>
            <button class="filter-tab" :class="{ active: eventFilter === 'upcoming' }" @click="eventFilter = 'upcoming'">Предстоящие</button>
            <button class="filter-tab" :class="{ active: eventFilter === 'completed' }" @click="eventFilter = 'completed'">Завершённые</button>
          </div>
          <div class="admin-events-grid">
            <div v-for="ev in filteredEvents" :key="ev.id" class="admin-event-card">
              <div class="event-header">
                <div>
                  <h3>{{ ev.title }}</h3>
                  <p>{{ typeLabel(ev.event_type) }} • {{ formatDate(ev.start_date) }}</p>
                </div>
                <span class="event-badge" :class="statusClass(ev.status)">{{ eventStatusLabel(ev.status) }}</span>
              </div>
              <div class="event-stats">
                <div class="stat-item"><span class="stat-label">Участников</span><span class="stat-value">{{ ev.participant_count || 0 }}</span></div>
                <div class="stat-item"><span class="stat-label">Работ сдано</span><span class="stat-value">0</span></div>
                <div class="stat-item"><span class="stat-label">Проверено</span><span class="stat-value">0</span></div>
              </div>
              <div class="event-actions">
                <button class="btn-small btn-outline" @click="openEditEvent(ev)">Редактировать</button>
                <button class="btn-small btn-danger" @click="deleteEvent(ev.id)">Удалить</button>
              </div>
            </div>
            <div v-if="!filteredEvents.length" style="padding:30px; text-align:center; color:var(--text-gray); grid-column:1/-1;">Мероприятий не найдено</div>
          </div>
        </div>

        <!-- ====== ЖЮРИ ====== -->
        <div v-show="activeTab === 'jury'">
          <div class="dashboard-header">
            <h1>Управление жюри</h1>
            <p>Назначение экспертов на мероприятия</p>
          </div>
          <div class="jury-management">
            <div class="section-card">
              <h2>Назначить жюри</h2>
              <form style="margin-top:20px;" @submit.prevent="assignJury">
                <div class="form-group">
                  <label>Мероприятие</label>
                  <select v-model="juryForm.event" class="form-input">
                    <option value="">Выберите мероприятие...</option>
                    <option v-for="ev in adminEvents" :key="ev.id" :value="ev.id">{{ ev.title }}</option>
                  </select>
                </div>
                <div class="form-group">
                  <label>Эксперт</label>
                  <select v-model="juryForm.jury" class="form-input">
                    <option value="">Выберите эксперта...</option>
                    <option v-for="j in juryUsers" :key="j.id" :value="j.id">{{ j.full_name || j.email }}</option>
                  </select>
                </div>
                <button type="submit" class="btn btn-primary" style="background:var(--primary-blue);color:white;">Назначить</button>
              </form>
            </div>
            <div class="section-card">
              <h2>Текущие назначения</h2>
              <div class="assignments-list">
                <div v-for="a in juryAssignments" :key="a.id" class="assignment-item">
                  <div><h4>{{ a.jury_name }}</h4><p>{{ a.event_title }}</p></div>
                  <button class="btn-icon btn-icon-danger" @click="removeAssignment(a.id)"><svg class="icon"><use href="#ic-close"/></svg></button>
                </div>
                <div v-if="!juryAssignments.length" style="color:var(--text-gray); text-align:center; padding:20px;">Нет назначений</div>
              </div>
            </div>
          </div>
        </div>

        <!-- ====== КОНТЕНТ ====== -->
        <div v-show="activeTab === 'content'">
          <div class="dashboard-header">
            <h1>Управление контентом</h1>
            <p>Редактирование страниц сайта</p>
          </div>
          <div class="content-sections">
            <div v-for="c in contentItems" :key="c.key" class="content-card">
              <h3>{{ c.title }}</h3>
              <p>{{ c.desc }}</p>
              <a :href="c.adminUrl" target="_blank" class="btn-outline" style="padding:8px 20px; border-radius:8px; border:2px solid var(--primary-blue); color:var(--primary-blue); background:none; cursor:pointer; font-size:14px; text-decoration:none; display:inline-block;">Редактировать</a>
            </div>
          </div>
        </div>

        <!-- ====== СТАТИСТИКА ====== -->
        <div v-show="activeTab === 'statistics'">
          <div class="dashboard-header">
            <h1>Статистика платформы</h1>
            <button class="btn btn-outline" style="display:inline-flex;align-items:center;gap:8px;" @click="exportReport">
              <svg class="icon icon-sm"><use href="#ic-export"/></svg>
              Экспорт отчёта
            </button>
          </div>
          <div class="stats-overview">
            <div class="section-card">
              <h2>Регистрации по месяцам</h2>
              <div class="chart-placeholder">
                <svg class="icon icon-lg" style="color:#93c5fd"><use href="#ic-chart-line"/></svg>
                <p>Динамика регистраций за последние 12 месяцев</p>
              </div>
            </div>
            <div class="section-card">
              <h2>Сводка по мероприятиям</h2>
              <div class="chart-placeholder">
                <svg class="icon icon-lg" style="color:#93c5fd"><use href="#ic-chart-bar"/></svg>
                <p>Сравнение мероприятий по числу участников и работ</p>
              </div>
            </div>
          </div>
        </div>

        <!-- ====== НАСТРОЙКИ ====== -->
        <div v-show="activeTab === 'settings'">
          <div class="dashboard-header">
            <h1>Настройки платформы</h1>
            <p>Общие параметры системы</p>
          </div>
          <div class="settings-section">
            <div class="section-card">
              <h2>Email-уведомления</h2>
              <div class="settings-list">
                <div v-for="s in emailSettings" :key="s.key" class="setting-item">
                  <label class="switch">
                    <input type="checkbox" v-model="s.value">
                    <span class="slider"></span>
                  </label>
                  <div class="setting-info"><h4>{{ s.title }}</h4><p>{{ s.desc }}</p></div>
                </div>
              </div>
            </div>
            <div class="section-card" style="margin-top:30px;">
              <h2>Безопасность</h2>
              <div class="settings-list">
                <div class="setting-item">
                  <label class="switch"><input type="checkbox" v-model="twoFactor"><span class="slider"></span></label>
                  <div class="setting-info"><h4>Двухфакторная аутентификация</h4><p>Требовать 2FA для администраторов</p></div>
                </div>
              </div>
            </div>
            <div style="margin-top:25px;">
              <button class="btn" style="background:var(--primary-blue);color:white;">Сохранить настройки</button>
            </div>
          </div>
        </div>

      </main>
    </div>
  </div>

  <!-- ====== МОДАЛКА: МЕРОПРИЯТИЕ ====== -->
  <div v-if="showEventModal" class="modal-overlay" @click.self="closeEventModal">
    <div class="modal-box">
      <div class="modal-head">
        <h2>{{ editingEvent ? 'Редактировать мероприятие' : 'Создать мероприятие' }}</h2>
        <button class="modal-close" @click="closeEventModal">✕</button>
      </div>
      <form @submit.prevent="saveEvent" class="modal-form">
        <div class="form-row">
          <div class="form-group">
            <label>Название *</label>
            <input v-model="eventForm.title" type="text" class="form-input" required placeholder="Название мероприятия">
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Краткое описание</label>
            <input v-model="eventForm.short_description" type="text" class="form-input" placeholder="Одна строка для списка">
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Полное описание *</label>
            <textarea v-model="eventForm.description" class="form-input" rows="4" required placeholder="Подробное описание..."></textarea>
          </div>
        </div>
        <div class="form-row form-row-3">
          <div class="form-group">
            <label>Тип</label>
            <select v-model="eventForm.event_type" class="form-input">
              <option value="olympiad">Олимпиада</option>
              <option value="competition">Конкурс</option>
            </select>
          </div>
          <div class="form-group">
            <label>Формат</label>
            <select v-model="eventForm.format" class="form-input">
              <option value="online">Онлайн</option>
              <option value="offline">Очно</option>
              <option value="hybrid">Смешанный</option>
            </select>
          </div>
          <div class="form-group">
            <label>Статус</label>
            <select v-model="eventForm.status" class="form-input">
              <option value="draft">Черновик</option>
              <option value="upcoming">Предстоящее</option>
              <option value="active">Активное</option>
              <option value="completed">Завершённое</option>
              <option value="cancelled">Отменено</option>
            </select>
          </div>
        </div>
        <div class="form-row form-row-3">
          <div class="form-group">
            <label>Дата начала *</label>
            <input v-model="eventForm.start_date" type="date" class="form-input" required>
          </div>
          <div class="form-group">
            <label>Дата окончания *</label>
            <input v-model="eventForm.end_date" type="date" class="form-input" required>
          </div>
          <div class="form-group">
            <label>Дедлайн регистрации *</label>
            <input v-model="eventForm.registration_deadline" type="date" class="form-input" required>
          </div>
        </div>
        <div class="form-row form-row-3">
          <div class="form-group">
            <label>Макс. участников</label>
            <input v-model="eventForm.max_participants" type="number" class="form-input" placeholder="Без лимита">
          </div>
          <div class="form-group">
            <label>Мин. возраст</label>
            <input v-model="eventForm.age_min" type="number" class="form-input" placeholder="—">
          </div>
          <div class="form-group">
            <label>Макс. возраст</label>
            <input v-model="eventForm.age_max" type="number" class="form-input" placeholder="—">
          </div>
        </div>
        <p v-if="modalError" class="modal-error">{{ modalError }}</p>
        <div class="modal-actions">
          <button type="button" class="btn-modal-cancel" @click="closeEventModal">Отмена</button>
          <button type="submit" class="btn-modal-submit" :disabled="modalLoading">
            {{ modalLoading ? 'Сохранение...' : (editingEvent ? 'Сохранить' : 'Создать') }}
          </button>
        </div>
      </form>
    </div>
  </div>

  <!-- ====== МОДАЛКА: ПОЛЬЗОВАТЕЛЬ ====== -->
  <div v-if="showUserModal" class="modal-overlay" @click.self="closeUserModal">
    <div class="modal-box">
      <div class="modal-head">
        <h2>{{ editingUser ? 'Редактировать пользователя' : 'Создать пользователя' }}</h2>
        <button class="modal-close" @click="closeUserModal">✕</button>
      </div>
      <form @submit.prevent="saveUser" class="modal-form">
        <div class="form-row form-row-3">
          <div class="form-group">
            <label>Фамилия *</label>
            <input v-model="userForm.last_name" type="text" class="form-input" required>
          </div>
          <div class="form-group">
            <label>Имя *</label>
            <input v-model="userForm.first_name" type="text" class="form-input" required>
          </div>
          <div class="form-group">
            <label>Отчество</label>
            <input v-model="userForm.patronymic" type="text" class="form-input">
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Email *</label>
            <input v-model="userForm.email" type="email" class="form-input" required :disabled="!!editingUser">
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Телефон</label>
            <input v-model="userForm.phone" type="tel" class="form-input" placeholder="+7 (___) ___-__-__">
          </div>
        </div>
        <div class="form-row form-row-2">
          <div class="form-group">
            <label>Роль</label>
            <select v-model="userForm.role" class="form-input">
              <option value="participant">Участник</option>
              <option value="teacher">Педагог</option>
              <option value="jury">Жюри</option>
              <option value="admin">Администратор</option>
            </select>
          </div>
          <div class="form-group">
            <label>Статус</label>
            <select v-model="userForm.status" class="form-input">
              <option value="active">Активен</option>
              <option value="blocked">Заблокирован</option>
              <option value="pending">Ожидает подтверждения</option>
            </select>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Учреждение</label>
            <input v-model="userForm.institution" type="text" class="form-input" placeholder="Школа / организация">
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Класс / Должность</label>
            <input v-model="userForm.grade_or_position" type="text" class="form-input" placeholder="Например: 10А или Учитель математики">
          </div>
        </div>
        <div v-if="!editingUser" class="form-row">
          <div class="form-group">
            <label>Пароль *</label>
            <input v-model="userForm.password" type="password" class="form-input" required placeholder="Минимум 8 символов">
          </div>
        </div>
        <p v-if="modalError" class="modal-error">{{ modalError }}</p>
        <div class="modal-actions">
          <button type="button" class="btn-modal-cancel" @click="closeUserModal">Отмена</button>
          <button type="submit" class="btn-modal-submit" :disabled="modalLoading">
            {{ modalLoading ? 'Сохранение...' : (editingUser ? 'Сохранить' : 'Создать') }}
          </button>
        </div>
      </form>
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
  { id: 'users', label: 'Пользователи', icon: 'users' },
  { id: 'events', label: 'Мероприятия', icon: 'calendar' },
  { id: 'jury', label: 'Жюри', icon: 'scale' },
  { id: 'content', label: 'Контент', icon: 'document' },
  { id: 'statistics', label: 'Статистика', icon: 'chart-line' },
  { id: 'settings', label: 'Настройки', icon: 'settings' }
]

const initials = computed(() => {
  const u = auth.user
  return u ? ((u.first_name?.[0] || '') + (u.last_name?.[0] || '')).toUpperCase() || 'А' : 'А'
})

// ---- Overview data ----
const stats = ref({ total_users: null, active_events: null, completed_submissions: null, jury_count: null })
const roleStats = ref({ participants: 935, participantsPct: 75, teachers: 250, teachersPct: 20, jury: 62, juryPct: 5 })
const popularEvents = ref([])
const recentUsers = ref([])

// ---- Users ----
const users = ref([])
const userSearch = ref('')
const userRoleFilter = ref('')
const userStatusFilter = ref('')
const showCreateUser = ref(false)

const filteredUsers = computed(() => users.value.filter(u => {
  const q = userSearch.value.toLowerCase()
  if (q && !((u.full_name || '').toLowerCase().includes(q) || u.email.toLowerCase().includes(q))) return false
  if (userRoleFilter.value && u.role !== userRoleFilter.value) return false
  if (userStatusFilter.value && u.status !== userStatusFilter.value) return false
  return true
}))

// ---- Events ----
const adminEvents = ref([])
const eventFilter = ref('')
const showEventModal = ref(false)
const editingEvent = ref(null)
const eventForm = ref({})

const filteredEvents = computed(() =>
  eventFilter.value ? adminEvents.value.filter(e => e.status === eventFilter.value) : adminEvents.value
)

// ---- Jury ----
const juryUsers = ref([])
const juryAssignments = ref([])
const juryForm = ref({ event: '', jury: '' })

// ---- Settings ----
const twoFactor = ref(true)
const emailSettings = ref([
  { key: 'reg', title: 'Уведомления о регистрации', desc: 'Отправлять email при регистрации пользователей', value: true },
  { key: 'deadline', title: 'Напоминания о дедлайнах', desc: 'Автоматические напоминания участникам', value: true }
])

const contentItems = [
  { key: 'events', title: 'Мероприятия', desc: 'Создание и редактирование мероприятий, олимпиад, конкурсов', adminUrl: 'http://localhost:8000/admin/events/event/' },
  { key: 'docs', title: 'Официальные документы', desc: 'Загрузка и управление документами для участников', adminUrl: 'http://localhost:8000/admin/documents/document/' },
  { key: 'users', title: 'Пользователи', desc: 'Управление учётными записями участников, педагогов и жюри', adminUrl: 'http://localhost:8000/admin/users/user/' },
  { key: 'submissions', title: 'Работы участников', desc: 'Просмотр и управление присланными работами', adminUrl: 'http://localhost:8000/admin/submissions/submission/' }
]

// ---- Modal shared ----
const modalLoading = ref(false)
const modalError = ref('')

// ---- User modal ----
const showUserModal = ref(false)
const editingUser = ref(null)
const userForm = ref({})

onMounted(async () => {
  await Promise.allSettled([
    loadStats(),
    loadUsers(),
    loadEvents(),
    loadJury()
  ])
})

async function loadStats() {
  try {
    const res = await api.get('/api/auth/users/stats/')
    const d = res.data
    stats.value.total_users = d.total || d.total_users
    stats.value.jury_count = d.jury
    const total = (d.participant || 0) + (d.teacher || 0) + (d.jury || 0)
    if (total) {
      roleStats.value = {
        participants: d.participant || 0,
        participantsPct: Math.round((d.participant || 0) / total * 100),
        teachers: d.teacher || 0,
        teachersPct: Math.round((d.teacher || 0) / total * 100),
        jury: d.jury || 0,
        juryPct: Math.round((d.jury || 0) / total * 100)
      }
    }
  } catch {}
  try {
    const res = await api.get('/api/events/?status=active')
    const list = res.data.results || res.data
    stats.value.active_events = Array.isArray(list) ? list.length : (res.data.count || 0)
    popularEvents.value = [...list].sort((a, b) => (b.participant_count || 0) - (a.participant_count || 0)).slice(0, 5)
  } catch {}
}

async function loadUsers() {
  try {
    const res = await api.get('/api/auth/users/')
    users.value = res.data.results || res.data
    recentUsers.value = [...users.value].sort((a, b) => new Date(b.date_joined) - new Date(a.date_joined)).slice(0, 5)
  } catch {}
}

async function loadEvents() {
  try {
    const res = await api.get('/api/events/')
    adminEvents.value = res.data.results || res.data
  } catch {}
}

async function loadJury() {
  try {
    const res = await api.get('/api/auth/users/?role=jury')
    juryUsers.value = res.data.results || res.data
  } catch {}
}

async function deleteUser(id) {
  if (!confirm('Удалить пользователя?')) return
  try {
    await api.delete(`/api/auth/users/${id}/`)
    users.value = users.value.filter(u => u.id !== id)
  } catch {}
}

async function deleteEvent(id) {
  if (!confirm('Удалить мероприятие?')) return
  try {
    await api.delete(`/api/events/${id}/`)
    adminEvents.value = adminEvents.value.filter(e => e.id !== id)
  } catch {}
}

async function assignJury() {
  if (!juryForm.value.event || !juryForm.value.jury) return
  try {
    await api.post(`/api/events/${juryForm.value.event}/assign_jury/`, { jury_id: juryForm.value.jury })
    const ev = adminEvents.value.find(e => e.id === juryForm.value.event)
    const j = juryUsers.value.find(u => u.id === juryForm.value.jury)
    if (ev && j) juryAssignments.value.push({ id: Date.now(), event_title: ev.title, jury_name: j.full_name || j.email })
    juryForm.value = { event: '', jury: '' }
  } catch {}
}

function removeAssignment(id) {
  juryAssignments.value = juryAssignments.value.filter(a => a.id !== id)
}

// ---- Event modal ----
function openCreateEvent() {
  editingEvent.value = null
  eventForm.value = { title: '', description: '', short_description: '', event_type: 'olympiad', format: 'online', status: 'draft', start_date: '', end_date: '', registration_deadline: '', max_participants: null, age_min: null, age_max: null }
  modalError.value = ''
  showEventModal.value = true
}
function openEditEvent(ev) {
  editingEvent.value = ev
  eventForm.value = { title: ev.title, description: ev.description || '', short_description: ev.short_description || '', event_type: ev.event_type, format: ev.format || 'online', status: ev.status, start_date: ev.start_date || '', end_date: ev.end_date || '', registration_deadline: ev.registration_deadline || '', max_participants: ev.max_participants || null, age_min: ev.age_min || null, age_max: ev.age_max || null }
  modalError.value = ''
  showEventModal.value = true
}
function closeEventModal() { showEventModal.value = false }

async function saveEvent() {
  modalLoading.value = true
  modalError.value = ''
  try {
    if (editingEvent.value) {
      const res = await api.patch(`/api/events/${editingEvent.value.id}/`, eventForm.value)
      const idx = adminEvents.value.findIndex(e => e.id === editingEvent.value.id)
      if (idx !== -1) adminEvents.value[idx] = { ...adminEvents.value[idx], ...res.data }
    } else {
      const res = await api.post('/api/events/', eventForm.value)
      adminEvents.value.unshift(res.data)
    }
    closeEventModal()
  } catch (e) {
    const data = e.response?.data
    modalError.value = data ? Object.values(data).flat().join(' ') : 'Ошибка сохранения'
  } finally {
    modalLoading.value = false
  }
}

// ---- User modal ----
function openCreateUser() {
  editingUser.value = null
  userForm.value = { first_name: '', last_name: '', patronymic: '', email: '', phone: '', role: 'participant', status: 'active', institution: '', grade_or_position: '', password: '' }
  modalError.value = ''
  showUserModal.value = true
}
function openEditUser(u) {
  editingUser.value = u
  userForm.value = { first_name: u.first_name || '', last_name: u.last_name || '', patronymic: u.patronymic || '', email: u.email, phone: u.phone || '', role: u.role, status: u.status || 'active', institution: u.institution || '', grade_or_position: u.grade_or_position || '' }
  modalError.value = ''
  showUserModal.value = true
}
function closeUserModal() { showUserModal.value = false }

async function saveUser() {
  modalLoading.value = true
  modalError.value = ''
  try {
    if (editingUser.value) {
      const res = await api.patch(`/api/auth/users/${editingUser.value.id}/`, userForm.value)
      const idx = users.value.findIndex(u => u.id === editingUser.value.id)
      if (idx !== -1) users.value[idx] = { ...users.value[idx], ...res.data }
    } else {
      const res = await api.post('/api/auth/register/', { ...userForm.value, re_password: userForm.value.password })
      users.value.unshift(res.data)
    }
    closeUserModal()
  } catch (e) {
    const data = e.response?.data
    modalError.value = data ? Object.values(data).flat().join(' ') : 'Ошибка сохранения'
  } finally {
    modalLoading.value = false
  }
}

function exportReport() { alert('Экспорт отчёта (функционал в разработке)') }

function userInitials(u) {
  return ((u.first_name?.[0] || '') + (u.last_name?.[0] || '')).toUpperCase() || u.email?.[0]?.toUpperCase() || 'У'
}

function roleLabel(r) { return { admin: 'Администратор', teacher: 'Педагог', participant: 'Участник', jury: 'Жюри' }[r] || r }
function statusLabel(s) { return { active: 'Активен', blocked: 'Заблокирован', pending: 'Ожидание' }[s] || s }
function typeLabel(t) { return { olympiad: 'Олимпиада', competition: 'Конкурс' }[t] || t }
function statusClass(s) { return { active: 'status-active', upcoming: 'status-soon', completed: 'status-completed', draft: 'status-pending' }[s] || 'status-pending' }
function eventStatusLabel(s) { return { active: 'Активно', upcoming: 'Скоро', completed: 'Завершено', draft: 'Черновик' }[s] || s }
function formatDate(d) { return d ? new Date(d).toLocaleDateString('ru-RU') : '—' }
function timeAgo(d) {
  if (!d) return ''
  const diff = Date.now() - new Date(d)
  const h = Math.floor(diff / 3600000)
  if (h < 24) return `${h} ч. назад`
  return `${Math.floor(h / 24)} дн. назад`
}
</script>
