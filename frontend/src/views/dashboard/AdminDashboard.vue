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
                <button class="btn-small btn-outline" @click="openStagesModal(ev)" style="border-color:var(--primary-blue);color:var(--primary-blue);">Этапы и задания</button>
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
                    <option v-for="ev in activeAdminEvents" :key="ev.id" :value="ev.id">{{ ev.title }}</option>
                  </select>
                </div>
                <div class="form-group">
                  <label>Эксперт</label>
                  <select v-model="juryForm.jury" class="form-input">
                    <option value="">Выберите эксперта...</option>
                    <option v-for="j in juryUsers" :key="j.id" :value="j.id">{{ j.full_name || j.email }}</option>
                  </select>
                </div>
                <div v-if="juryError" style="color:#991b1b;background:#fef2f2;padding:8px 12px;border-radius:8px;font-size:13px;margin-bottom:8px;">{{ juryError }}</div>
                <button type="submit" class="btn btn-primary" style="background:var(--primary-blue);color:white;">Назначить</button>
              </form>
            </div>
            <div class="section-card">
              <h2>Текущие назначения</h2>
              <div class="assignments-list">
                <div v-for="a in juryAssignments" :key="a.id" class="assignment-item">
                  <div><h4>{{ a.jury?.full_name || a.jury?.email }}</h4><p>{{ a.event_title }}</p></div>
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

        <!-- ====== ДОКУМЕНТЫ ====== -->
        <div v-show="activeTab === 'documents'">
          <div class="dashboard-header">
            <h1>Официальные документы</h1>
          </div>

          <!-- Форма загрузки -->
          <div class="section-card" style="margin-bottom:28px;">
            <h2 style="margin-bottom:16px;">Загрузить документ</h2>
            <form @submit.prevent="uploadDocument" style="display:flex;flex-direction:column;gap:14px;">
              <div class="form-row form-row-2">
                <div class="form-group">
                  <label>Название *</label>
                  <input v-model="docForm.title" type="text" class="form-input" required placeholder="Название документа">
                </div>
                <div class="form-group">
                  <label>Тип документа</label>
                  <select v-model="docForm.doc_type" class="form-input">
                    <option value="regulation">Положение</option>
                    <option value="template">Шаблон работы</option>
                    <option value="criteria">Критерии оценивания</option>
                    <option value="methodology">Метод. материалы</option>
                    <option value="privacy">Политика конф.</option>
                    <option value="other">Прочее</option>
                  </select>
                </div>
              </div>
              <div class="form-row form-row-2">
                <div class="form-group">
                  <label>Мероприятие <span style="color:var(--text-gray);font-weight:400;">(необязательно)</span></label>
                  <select v-model="docForm.event" class="form-input">
                    <option :value="null">— Без мероприятия —</option>
                    <option v-for="ev in adminEvents" :key="ev.id" :value="ev.id">{{ ev.title }}</option>
                  </select>
                </div>
                <div class="form-group">
                  <label>Описание</label>
                  <input v-model="docForm.description" type="text" class="form-input" placeholder="Краткое описание (необязательно)">
                </div>
              </div>
              <div class="form-group">
                <label>Файл *</label>
                <input type="file" class="form-input" @change="onDocFileChange" accept=".pdf,.doc,.docx,.xls,.xlsx,.zip,.rar" required>
                <p style="font-size:12px;color:var(--text-gray);margin-top:4px;">PDF, Word, Excel, архивы. Макс. 10 МБ.</p>
              </div>
              <div v-if="docError" style="color:#991b1b;background:#fef2f2;padding:10px;border-radius:8px;font-size:14px;">{{ docError }}</div>
              <div v-if="docSuccess" style="color:#065f46;background:#d1fae5;padding:10px;border-radius:8px;font-size:14px;">{{ docSuccess }}</div>
              <button type="submit" class="btn" style="background:var(--primary-blue);color:white;width:fit-content;" :disabled="docLoading">
                {{ docLoading ? 'Загружаем...' : 'Загрузить документ' }}
              </button>
            </form>
          </div>

          <!-- Список документов -->
          <div class="section-card">
            <h2 style="margin-bottom:16px;">Загруженные документы ({{ documents.length }})</h2>
            <div v-if="!documents.length" style="text-align:center;padding:40px;color:var(--text-gray);">Документов ещё нет</div>
            <div v-for="doc in documents" :key="doc.id"
              style="display:flex;justify-content:space-between;align-items:center;padding:14px 18px;background:#f8fafc;border-radius:10px;border:1px solid #e2e8f0;margin-bottom:10px;">
              <div style="flex:1;min-width:0;">
                <div style="font-weight:600;font-size:14px;">{{ doc.title }}</div>
                <div style="font-size:12px;color:var(--text-gray);margin-top:2px;">
                  {{ docTypeLabel(doc.doc_type) }}
                  <span v-if="doc.event_title"> · {{ doc.event_title }}</span>
                  · {{ doc.file_size_display }}
                </div>
              </div>
              <div style="display:flex;gap:8px;margin-left:12px;flex-shrink:0;">
                <a :href="'/api/documents/' + doc.id + '/download/'" style="display:inline-flex;align-items:center;gap:4px;padding:6px 14px;background:var(--primary-blue);color:white;border-radius:8px;font-size:13px;text-decoration:none;">Скачать</a>
                <button class="btn-icon btn-icon-danger" @click="deleteDocument(doc.id)"><svg class="icon"><use href="#ic-trash"/></svg></button>
              </div>
            </div>
          </div>
        </div>

        <!-- ====== РАБОТЫ ====== -->
        <div v-show="activeTab === 'submissions'">
          <div class="dashboard-header">
            <h1>Работы участников</h1>
          </div>
          <div class="filter-section">
            <select v-model="submissionEventFilter" style="max-width:300px;">
              <option value="">Все мероприятия</option>
              <option v-for="ev in adminEvents" :key="ev.id" :value="ev.id">{{ ev.title }}</option>
            </select>
            <select v-model="submissionStatusFilter">
              <option value="">Все статусы</option>
              <option value="draft">Черновик</option>
              <option value="submitted">Отправлено</option>
              <option value="under_review">На проверке</option>
              <option value="evaluated">Проверено</option>
            </select>
          </div>
          <div class="users-table" style="margin-top:16px;">
            <div class="table-header" style="grid-template-columns:2fr 2fr 1.5fr 1fr 1fr 1fr;">
              <div>Участник</div><div>Мероприятие</div><div>Файл</div><div>Дата</div><div>Статус</div><div>Действия</div>
            </div>
            <div v-for="s in filteredSubmissions" :key="s.id" class="user-row" style="grid-template-columns:2fr 2fr 1.5fr 1fr 1fr 1fr;">
              <div class="user-cell">
                <div class="user-avatar small">{{ (s.participant?.full_name?.[0] || '?').toUpperCase() }}</div>
                <span>{{ s.participant?.full_name || s.participant?.email || '—' }}</span>
              </div>
              <div style="font-size:14px;">{{ s.event_title || '—' }}</div>
              <div style="font-size:13px;color:var(--text-gray);">{{ s.original_filename || '—' }}</div>
              <div style="font-size:13px;">{{ s.submitted_at ? formatDate(s.submitted_at) : formatDate(s.created_at) }}</div>
              <div><span class="event-badge" :class="subStatusClass(s.status)">{{ subStatusLabel(s.status) }}</span></div>
              <div style="display:flex;gap:6px;">
                <a v-if="s.file" :href="s.file" target="_blank" style="display:inline-flex;align-items:center;padding:4px 10px;background:var(--primary-blue);color:white;border-radius:6px;font-size:12px;text-decoration:none;">Скачать</a>
              </div>
            </div>
            <div v-if="!filteredSubmissions.length" style="padding:30px;text-align:center;color:var(--text-gray);">Работ не найдено</div>
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

  <!-- ====== МОДАЛКА: ЭТАПЫ И ЗАДАНИЯ ====== -->
  <div v-if="showStagesModal" class="modal-overlay" @click.self="closeStagesModal">
    <div class="modal-box" style="max-width:750px;">
      <div class="modal-head">
        <h2>Этапы и задания: {{ stagesEvent?.title }}</h2>
        <button class="modal-close" @click="closeStagesModal">✕</button>
      </div>

      <!-- Stage form -->
      <div style="background:#f8fafc;border-radius:10px;padding:20px;margin-bottom:24px;">
        <h3 style="font-size:15px;font-weight:600;margin-bottom:14px;">{{ editingStage ? 'Редактировать этап' : 'Добавить этап' }}</h3>
        <div class="form-row">
          <div class="form-group" style="flex:2">
            <label>Название этапа *</label>
            <input v-model="stageForm.title" type="text" class="form-input" placeholder="Например: Отборочный тур">
          </div>
          <div class="form-group">
            <label>Порядок</label>
            <input v-model.number="stageForm.order" type="number" min="1" class="form-input">
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Дата начала</label>
            <input v-model="stageForm.start_date" type="date" class="form-input">
          </div>
          <div class="form-group">
            <label>Дата окончания</label>
            <input v-model="stageForm.end_date" type="date" class="form-input">
          </div>
        </div>
        <div class="form-group">
          <label>Описание</label>
          <textarea v-model="stageForm.description" class="form-input" rows="2" placeholder="Краткое описание этапа..."></textarea>
        </div>
        <div style="display:flex;gap:10px;margin-top:4px;">
          <button class="btn" style="background:var(--primary-blue);color:white;" @click="saveStage">{{ editingStage ? 'Сохранить' : 'Добавить этап' }}</button>
          <button v-if="editingStage" class="btn btn-outline" @click="cancelEditStage">Отмена</button>
        </div>
      </div>

      <!-- Stages list -->
      <div v-if="!stages.length" style="text-align:center;padding:30px;color:var(--text-gray);">Этапов ещё нет</div>
      <div v-for="stage in stages" :key="stage.id" style="border:1px solid #e5e7eb;border-radius:12px;margin-bottom:16px;overflow:hidden;">
        <!-- Stage header -->
        <div style="background:#f1f5f9;padding:14px 18px;display:flex;justify-content:space-between;align-items:center;">
          <div>
            <span style="font-weight:600;color:var(--primary-dark);">Этап {{ stage.order }}: {{ stage.title }}</span>
            <span v-if="stage.start_date" style="font-size:13px;color:var(--text-gray);margin-left:12px;">{{ formatDate(stage.start_date) }} — {{ formatDate(stage.end_date) }}</span>
          </div>
          <div style="display:flex;gap:8px;">
            <button class="btn-icon" @click="startEditStage(stage)"><svg class="icon"><use href="#ic-edit"/></svg></button>
            <button class="btn-icon btn-icon-danger" @click="deleteStage(stage.id)"><svg class="icon"><use href="#ic-trash"/></svg></button>
          </div>
        </div>
        <div v-if="stage.description" style="padding:8px 18px;font-size:13px;color:var(--text-gray);border-bottom:1px solid #e5e7eb;">{{ stage.description }}</div>

        <!-- Tasks -->
        <div style="padding:14px 18px;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
            <span style="font-size:14px;font-weight:600;">Задания</span>
            <button class="btn-small btn-outline" style="font-size:12px;" @click="openAddTask(stage)">+ Добавить задание</button>
          </div>
          <div v-if="!stage.tasks?.length" style="font-size:13px;color:var(--text-gray);padding:6px 0;">Заданий нет</div>
          <div v-for="task in stage.tasks" :key="task.id" style="background:#fafafa;border-radius:8px;padding:12px 14px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:flex-start;">
            <div style="flex:1;">
              <div style="font-weight:600;font-size:14px;margin-bottom:4px;">{{ task.order }}. {{ task.title }}</div>
              <div style="font-size:13px;color:var(--text-gray);line-height:1.5;">{{ task.description }}</div>
              <div style="font-size:12px;color:var(--primary-blue);margin-top:4px;">Макс. балл: {{ task.max_score }}</div>
            </div>
            <div style="display:flex;gap:6px;margin-left:12px;flex-shrink:0;">
              <button class="btn-icon" @click="startEditTask(task, stage)"><svg class="icon"><use href="#ic-edit"/></svg></button>
              <button class="btn-icon btn-icon-danger" @click="deleteTask(task.id, stage)"><svg class="icon"><use href="#ic-trash"/></svg></button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- ====== МОДАЛКА: ЗАДАНИЕ ====== -->
  <div v-if="showTaskModal" class="modal-overlay" @click.self="showTaskModal = false">
    <div class="modal-box" style="max-width:560px;">
      <div class="modal-head">
        <h2>{{ editingTask ? 'Редактировать задание' : 'Добавить задание' }}</h2>
        <button class="modal-close" @click="showTaskModal = false">✕</button>
      </div>
      <div class="modal-form">
        <div class="form-row">
          <div class="form-group" style="flex:3">
            <label>Название задания *</label>
            <input v-model="taskForm.title" type="text" class="form-input" placeholder="Название задания">
          </div>
          <div class="form-group">
            <label>Порядок</label>
            <input v-model.number="taskForm.order" type="number" min="1" class="form-input">
          </div>
        </div>
        <div class="form-group">
          <label>Условие задания *</label>
          <textarea v-model="taskForm.description" class="form-input" rows="5" placeholder="Подробное условие задания..."></textarea>
        </div>
        <div class="form-group">
          <label>Максимальный балл</label>
          <input v-model.number="taskForm.max_score" type="number" min="1" max="1000" class="form-input">
        </div>
        <div class="form-group">
          <label>Файл задания <span style="font-weight:400;color:var(--text-gray);">(необязательно)</span></label>
          <input type="file" class="form-input" @change="onTaskFileChange"
            accept=".pdf,.doc,.docx,.xls,.xlsx,.zip,.rar,.txt,.png,.jpg,.jpeg">
          <p style="font-size:12px;color:var(--text-gray);margin-top:4px;">PDF, Word, Excel, изображения, архивы. Макс. размер: 10 МБ.</p>
          <div v-if="editingTask?.file" style="margin-top:6px;font-size:13px;display:flex;align-items:center;gap:8px;">
            <span style="color:var(--text-gray);">Текущий файл:</span>
            <a :href="editingTask.file" target="_blank" style="color:var(--primary-blue);text-decoration:underline;">скачать</a>
          </div>
        </div>
        <div v-if="taskError" style="color:#ef4444;background:#fef2f2;padding:10px;border-radius:8px;margin-bottom:12px;">{{ taskError }}</div>
        <div style="display:flex;gap:10px;">
          <button class="btn" style="background:var(--primary-blue);color:white;flex:1;" @click="saveTask">{{ editingTask ? 'Сохранить' : 'Добавить' }}</button>
          <button class="btn btn-outline" @click="showTaskModal = false">Отмена</button>
        </div>
      </div>
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
        <div v-if="userForm.role === 'participant'" class="form-row">
          <div class="form-group">
            <label>Педагог (куратор)</label>
            <select v-model="userForm.teacher_id" class="form-input">
              <option :value="null">— Не назначен —</option>
              <option v-for="t in teacherUsers" :key="t.id" :value="t.id">{{ t.full_name || t.email }}</option>
            </select>
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
  { id: 'documents', label: 'Документы', icon: 'file' },
  { id: 'submissions', label: 'Работы', icon: 'upload' },
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
const activeAdminEvents = computed(() => adminEvents.value.filter(e => e.status !== 'completed' && e.status !== 'cancelled'))

// ---- Jury ----
const juryUsers = ref([])
const teacherUsers = ref([])
const juryAssignments = ref([])
const juryForm = ref({ event: '', jury: '' })

// ---- Documents ----
const documents = ref([])
const docForm = ref({ title: '', doc_type: 'regulation', event: null, description: '' })
const docLoading = ref(false)
const docError = ref('')
const docSuccess = ref('')

// ---- Submissions (admin view) ----
const allSubmissions = ref([])
const submissionEventFilter = ref('')
const submissionStatusFilter = ref('')
const filteredSubmissions = computed(() => allSubmissions.value.filter(s => {
  if (submissionEventFilter.value && s.event !== submissionEventFilter.value && s.event?.id !== submissionEventFilter.value) return false
  if (submissionStatusFilter.value && s.status !== submissionStatusFilter.value) return false
  return true
}))

// ---- Settings ----
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

// ── Stages & Tasks ────────────────────────────────────────────────────────────
const showStagesModal = ref(false)
const stagesEvent = ref(null)
const stages = ref([])
const editingStage = ref(null)
const stageForm = ref({ title: '', description: '', order: 1, start_date: '', end_date: '' })

const showTaskModal = ref(false)
const editingTask = ref(null)
const taskStage = ref(null)
const taskForm = ref({ title: '', description: '', order: 1, max_score: 100 })
const taskError = ref('')

async function openStagesModal(ev) {
  stagesEvent.value = ev
  editingStage.value = null
  stageForm.value = { title: '', description: '', order: 1, start_date: '', end_date: '' }
  await loadStages(ev.id)
  showStagesModal.value = true
}

function closeStagesModal() {
  showStagesModal.value = false
  stagesEvent.value = null
  stages.value = []
}

async function loadStages(eventId) {
  try {
    const r = await api.get(`/api/events/stages/?event=${eventId}`)
    stages.value = r.data.results || r.data
  } catch {}
}

async function saveStage() {
  if (!stageForm.value.title.trim()) return
  try {
    const payload = { ...stageForm.value, event: stagesEvent.value.id }
    if (!payload.start_date) delete payload.start_date
    if (!payload.end_date) delete payload.end_date
    if (editingStage.value) {
      const r = await api.put(`/api/events/stages/${editingStage.value.id}/`, payload)
      const idx = stages.value.findIndex(s => s.id === editingStage.value.id)
      if (idx !== -1) stages.value[idx] = { ...stages.value[idx], ...r.data }
    } else {
      const r = await api.post('/api/events/stages/', payload)
      stages.value.push({ ...r.data, tasks: [] })
    }
    cancelEditStage()
  } catch {}
}

function startEditStage(stage) {
  editingStage.value = stage
  stageForm.value = {
    title: stage.title,
    description: stage.description || '',
    order: stage.order,
    start_date: stage.start_date || '',
    end_date: stage.end_date || ''
  }
}

function cancelEditStage() {
  editingStage.value = null
  stageForm.value = { title: '', description: '', order: stages.value.length + 1, start_date: '', end_date: '' }
}

async function deleteStage(stageId) {
  if (!confirm('Удалить этап? Все задания этапа будут удалены.')) return
  try {
    await api.delete(`/api/events/stages/${stageId}/`)
    stages.value = stages.value.filter(s => s.id !== stageId)
  } catch {}
}

function onTaskFileChange(e) {
  const file = e.target.files[0] || null
  if (file && file.size > 10 * 1024 * 1024) {
    taskError.value = 'Файл превышает 10 МБ. Выберите файл меньшего размера.'
    e.target.value = ''
    taskForm.value.file = null
    return
  }
  taskError.value = ''
  taskForm.value.file = file
}

function openAddTask(stage) {
  taskStage.value = stage
  editingTask.value = null
  taskForm.value = { title: '', description: '', order: (stage.tasks?.length || 0) + 1, max_score: 100, file: null }
  taskError.value = ''
  showTaskModal.value = true
}

function startEditTask(task, stage) {
  taskStage.value = stage
  editingTask.value = task
  taskForm.value = { title: task.title, description: task.description, order: task.order, max_score: task.max_score, file: null }
  taskError.value = ''
  showTaskModal.value = true
}

async function saveTask() {
  taskError.value = ''
  if (!taskForm.value.title.trim() || !taskForm.value.description.trim()) {
    taskError.value = 'Заполните название и условие задания'
    return
  }
  try {
    const fd = new FormData()
    fd.append('stage', taskStage.value.id)
    fd.append('title', taskForm.value.title)
    fd.append('description', taskForm.value.description)
    fd.append('order', taskForm.value.order)
    fd.append('max_score', taskForm.value.max_score)
    if (taskForm.value.file) fd.append('file', taskForm.value.file)
    const headers = { 'Content-Type': 'multipart/form-data' }
    if (editingTask.value) {
      const r = await api.patch(`/api/events/tasks/${editingTask.value.id}/`, fd, { headers })
      const idx = taskStage.value.tasks.findIndex(t => t.id === editingTask.value.id)
      if (idx !== -1) taskStage.value.tasks[idx] = r.data
    } else {
      const r = await api.post('/api/events/tasks/', fd, { headers })
      if (!taskStage.value.tasks) taskStage.value.tasks = []
      taskStage.value.tasks.push(r.data)
    }
    showTaskModal.value = false
  } catch (e) {
    taskError.value = e.response?.data?.detail || 'Ошибка при сохранении'
  }
}

async function deleteTask(taskId, stage) {
  if (!confirm('Удалить задание?')) return
  try {
    await api.delete(`/api/events/tasks/${taskId}/`)
    stage.tasks = stage.tasks.filter(t => t.id !== taskId)
  } catch {}
}

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
    loadJury(),
    loadDocuments(),
    loadSubmissions()
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
    const [jRes, tRes, aRes] = await Promise.all([
      api.get('/api/auth/users/?role=jury'),
      api.get('/api/auth/users/?role=teacher'),
      api.get('/api/events/jury-assignments/')
    ])
    juryUsers.value = jRes.data.results || jRes.data
    teacherUsers.value = tRes.data.results || tRes.data
    juryAssignments.value = aRes.data.results || aRes.data
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

const juryError = ref('')

async function assignJury() {
  juryError.value = ''
  if (!juryForm.value.event || !juryForm.value.jury) {
    juryError.value = 'Выберите мероприятие и эксперта'
    return
  }
  try {
    const res = await api.post(`/api/events/${juryForm.value.event}/assign_jury/`, { jury_id: juryForm.value.jury })
    juryAssignments.value.push(res.data)
    juryForm.value = { event: '', jury: '' }
  } catch (e) {
    juryError.value = e.response?.data?.detail || e.response?.data?.non_field_errors?.[0] || 'Ошибка при назначении'
  }
}

async function removeAssignment(id) {
  try {
    await api.delete(`/api/events/jury-assignments/${id}/`)
    juryAssignments.value = juryAssignments.value.filter(a => a.id !== id)
  } catch {}
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
  userForm.value = { first_name: '', last_name: '', patronymic: '', email: '', phone: '', role: 'participant', status: 'active', institution: '', grade_or_position: '', teacher_id: null, password: '' }
  modalError.value = ''
  showUserModal.value = true
}
function openEditUser(u) {
  editingUser.value = u
  userForm.value = { first_name: u.first_name || '', last_name: u.last_name || '', patronymic: u.patronymic || '', email: u.email, phone: u.phone || '', role: u.role, status: u.status || 'active', institution: u.institution || '', grade_or_position: u.grade_or_position || '', teacher_id: u.teacher_id || null }
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
      // Назначить педагога отдельным запросом если участник
      if (userForm.value.role === 'participant') {
        await api.post(`/api/auth/users/${editingUser.value.id}/assign_teacher/`, { teacher_id: userForm.value.teacher_id }).catch(() => {})
      }
    } else {
      const res = await api.post('/api/auth/register/', { ...userForm.value, password_confirm: userForm.value.password })
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

// ---- Documents functions ----
async function loadDocuments() {
  try {
    const res = await api.get('/api/documents/')
    documents.value = res.data.results || res.data
  } catch {}
}

function onDocFileChange(e) {
  docForm.value._file = e.target.files[0] || null
}

async function uploadDocument() {
  docError.value = ''
  docSuccess.value = ''
  if (!docForm.value.title.trim() || !docForm.value._file) {
    docError.value = 'Укажите название и выберите файл'
    return
  }
  docLoading.value = true
  try {
    const fd = new FormData()
    fd.append('title', docForm.value.title)
    fd.append('doc_type', docForm.value.doc_type)
    fd.append('description', docForm.value.description || '')
    if (docForm.value.event) fd.append('event', docForm.value.event)
    fd.append('file', docForm.value._file)
    const res = await api.post('/api/documents/', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
    documents.value.unshift(res.data)
    docSuccess.value = 'Документ успешно загружен!'
    docForm.value = { title: '', doc_type: 'regulation', event: null, description: '' }
  } catch (e) {
    docError.value = e.response?.data?.detail || Object.values(e.response?.data || {}).flat().join(' ') || 'Ошибка загрузки'
  } finally {
    docLoading.value = false
  }
}

async function deleteDocument(id) {
  if (!confirm('Удалить документ?')) return
  try {
    await api.delete(`/api/documents/${id}/`)
    documents.value = documents.value.filter(d => d.id !== id)
  } catch {}
}

function docTypeLabel(t) {
  return { regulation: 'Положение', template: 'Шаблон работы', criteria: 'Критерии', methodology: 'Метод. материалы', privacy: 'Политика конф.', other: 'Прочее' }[t] || t
}

// ---- Submissions functions ----
async function loadSubmissions() {
  try {
    const res = await api.get('/api/submissions/')
    allSubmissions.value = res.data.results || res.data
  } catch {}
}

function subStatusClass(s) { return { draft: 'status-pending', submitted: 'status-soon', under_review: 'status-soon', evaluated: 'status-active' }[s] || 'status-pending' }
function subStatusLabel(s) { return { draft: 'Черновик', submitted: 'Отправлено', under_review: 'На проверке', evaluated: 'Проверено' }[s] || s }

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
