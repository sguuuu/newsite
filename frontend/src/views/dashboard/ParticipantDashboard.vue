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
            <svg class="icon"><use :href="'#ic-' + tab.icon"/></svg>
            {{ tab.label }}
            <span v-if="tab.badge" style="margin-left:auto;background:#ef4444;color:white;font-size:11px;font-weight:700;padding:1px 6px;border-radius:10px;">{{ tab.badge }}</span>
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
          </div>
          <div class="section-grid">
            <div class="section-card">
              <h2>Ближайшие мероприятия</h2>
              <div v-for="ev in myEvents.filter(ev => !['completed','cancelled'].includes(effectiveStatus(ev))).slice(0,3)" :key="ev.id" class="event-item">
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

          <!-- История участий -->
          <div v-if="completedMyEvents.length" class="section-card" style="margin-top:24px;">
            <h2 style="margin-bottom:16px;">Мои конкурсы — история участий</h2>
            <div v-for="ev in completedMyEvents" :key="ev.id"
              style="display:flex;justify-content:space-between;align-items:center;padding:12px 0;border-bottom:1px solid #f1f5f9;">
              <div>
                <div style="font-weight:600;font-size:14px;color:var(--primary-dark);">{{ ev.title }}</div>
                <div style="font-size:12px;color:var(--text-gray);margin-top:2px;">{{ formatDate(ev.start_date) }} — {{ formatDate(ev.end_date) }}</div>
              </div>
              <div style="display:flex;align-items:center;gap:12px;">
                <span v-if="submissionForEvent(ev.id)" style="font-size:13px;font-weight:600;"
                  :style="submissionForEvent(ev.id).score !== null ? 'color:var(--primary-blue)' : 'color:var(--text-gray)'">
                  {{ submissionForEvent(ev.id).score !== null ? submissionForEvent(ev.id).score + '/100' : subStatusLabel(submissionForEvent(ev.id).status) }}
                </span>
                <span v-else style="font-size:12px;color:var(--text-gray);">Без работы</span>
                <span class="event-badge" style="background:#fee2e2;color:#991b1b;">Завершено</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Мои мероприятия -->
        <div v-show="activeTab === 'events'">
          <div class="dashboard-header"><h1>Мои мероприятия</h1></div>

          <!-- Активные и предстоящие -->
          <template v-if="activeMyEvents.length">
            <div v-for="ev in activeMyEvents" :key="ev.id" class="event-item">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div>
                  <span class="event-badge" :class="statusClass(effectiveStatus(ev))" style="margin-bottom:8px;display:inline-block">{{ statusLabel(effectiveStatus(ev)) }}</span>
                  <h4>{{ ev.title }}</h4>
                  <p>{{ formatDate(ev.start_date) }} — {{ formatDate(ev.end_date) }}</p>
                </div>
                <button class="btn-small btn-outline" @click="$router.push('/events/' + ev.id)">Подробнее</button>
              </div>
            </div>
          </template>
          <div v-else-if="!myEvents.length" style="text-align:center;padding:60px;color:var(--text-gray);">
            <p>Вы ещё не зарегистрированы ни на одно мероприятие</p>
            <button class="btn" style="background:var(--primary-blue);color:white;margin-top:20px;" @click="$router.push('/events')">Найти мероприятие</button>
          </div>

          <!-- Завершённые -->
          <template v-if="completedMyEvents.length">
            <div style="margin-top:30px;margin-bottom:12px;display:flex;align-items:center;gap:10px;">
              <h3 style="font-size:16px;font-weight:600;color:#991b1b;">Завершённые мероприятия</h3>
              <span style="display:inline-block;width:8px;height:8px;background:#991b1b;border-radius:50%;"></span>
            </div>
            <div v-for="ev in completedMyEvents" :key="ev.id" class="event-item" style="border-left:3px solid #fca5a5;opacity:0.85;">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div>
                  <span class="event-badge" style="background:#fee2e2;color:#991b1b;margin-bottom:8px;display:inline-block;">Завершено</span>
                  <h4>{{ ev.title }}</h4>
                  <p>{{ formatDate(ev.start_date) }} — {{ formatDate(ev.end_date) }}</p>
                </div>
                <button class="btn-small btn-outline" @click="$router.push('/events/' + ev.id)">Подробнее</button>
              </div>
            </div>
          </template>
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
                  Допустимые форматы: PDF, Word (.doc/.docx), Excel (.xls/.xlsx), ZIP, RAR. Макс. размер: 10 МБ.
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
              <div v-if="s.status === 'draft'" style="margin-top:12px;display:flex;gap:10px;align-items:center;flex-wrap:wrap;">
                <button class="btn btn-outline" style="font-size:13px;padding:6px 16px;" @click="submitWork(s)" :disabled="s._submitting">
                  {{ s._submitting ? 'Отправляем...' : 'Подать официально' }}
                </button>
                <button class="btn btn-outline" style="font-size:13px;padding:6px 16px;border-color:#ef4444;color:#ef4444;" @click="deleteDraft(s)" :disabled="s._deleting">
                  {{ s._deleting ? 'Удаляем...' : 'Удалить черновик' }}
                </button>
                <span style="font-size:12px;color:var(--text-gray);">Черновик — работа ещё не отправлена на проверку</span>
              </div>
              <!-- Кнопка «Обновить работу» для отправленных (не проверенных) -->
              <div v-if="['submitted','under_review'].includes(s.status)" style="margin-top:12px;">
                <div v-if="resubmitId !== s.id">
                  <button class="btn btn-outline" style="font-size:13px;padding:6px 16px;" @click="resubmitId = s.id">
                    Обновить файл работы
                  </button>
                </div>
                <div v-else style="display:flex;flex-direction:column;gap:10px;background:#f8fafc;padding:14px;border-radius:10px;">
                  <p style="font-size:13px;color:var(--text-gray);margin:0;">Выберите новый файл. Текущий будет заменён, работа останется на проверке.</p>
                  <input type="file" class="form-input" @change="onResubmitFile" accept=".pdf,.doc,.docx,.xls,.xlsx,.zip,.rar" style="font-size:13px;" />
                  <div v-if="resubmitError" style="color:#991b1b;font-size:13px;">{{ resubmitError }}</div>
                  <div style="display:flex;gap:8px;">
                    <button class="btn" style="background:var(--primary-blue);color:white;font-size:13px;padding:6px 18px;"
                      @click="resubmitWork(s)" :disabled="!resubmitFile || s._resubmitting">
                      {{ s._resubmitting ? 'Заменяем...' : 'Заменить файл' }}
                    </button>
                    <button class="btn btn-outline" style="font-size:13px;padding:6px 14px;" @click="resubmitId = null; resubmitFile = null; resubmitError = ''">Отмена</button>
                  </div>
                </div>
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

        <!-- Задания -->
        <div v-show="activeTab === 'tasks'">
          <div class="dashboard-header"><h1>Задания</h1></div>

          <!-- Event selector -->
          <div style="margin-bottom:24px;">
            <label style="font-size:14px;font-weight:600;display:block;margin-bottom:8px;">Выберите мероприятие</label>
            <select v-model="selectedTasksEvent" class="form-input" style="max-width:400px;" @change="loadEventStages">
              <option value="">— Выберите мероприятие —</option>
              <option v-for="ev in activeMyEvents" :key="ev.id" :value="ev.id">{{ ev.title }}</option>
            </select>
          </div>

          <div v-if="stagesLoading" style="text-align:center;padding:40px;color:var(--text-gray);">Загрузка...</div>
          <div v-else-if="!selectedTasksEvent" style="text-align:center;padding:60px;color:var(--text-gray);">Выберите мероприятие для просмотра заданий</div>
          <div v-else-if="!eventStages.length" style="text-align:center;padding:60px;color:var(--text-gray);">Заданий для этого мероприятия пока нет</div>

          <div v-for="stage in eventStages" :key="stage.id" style="margin-bottom:24px;border:1px solid #e5e7eb;border-radius:12px;overflow:hidden;">
            <div style="background:var(--gradient-hero);padding:16px 20px;color:white;">
              <div style="font-weight:700;font-size:16px;">Этап {{ stage.order }}: {{ stage.title }}</div>
              <div v-if="stage.start_date" style="font-size:13px;opacity:0.85;margin-top:4px;">{{ formatDate(stage.start_date) }} — {{ formatDate(stage.end_date) }}</div>
              <div v-if="stage.description" style="font-size:13px;opacity:0.85;margin-top:4px;">{{ stage.description }}</div>
            </div>
            <div v-if="!stage.tasks?.length" style="padding:20px;font-size:14px;color:var(--text-gray);text-align:center;">Заданий нет</div>
            <div v-for="task in stage.tasks" :key="task.id" style="padding:18px 20px;border-top:1px solid #e5e7eb;">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">
                <h4 style="font-size:15px;font-weight:600;color:var(--primary-dark);">{{ task.order }}. {{ task.title }}</h4>
                <span style="background:#eff6ff;color:#1e40af;font-size:12px;padding:3px 10px;border-radius:20px;white-space:nowrap;margin-left:12px;">{{ task.max_score }} баллов</span>
              </div>
              <p style="font-size:14px;color:var(--text-dark);line-height:1.7;white-space:pre-wrap;">{{ task.description }}</p>
              <a v-if="task.file" :href="task.file" target="_blank"
                style="display:inline-flex;align-items:center;gap:6px;margin-top:10px;font-size:13px;color:var(--primary-blue);text-decoration:none;background:#eff6ff;padding:6px 14px;border-radius:8px;">
                <svg class="icon icon-sm"><use href="#ic-download"/></svg>Скачать файл задания
              </a>
            </div>
          </div>

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

        <!-- Документы для регистрации -->
        <div v-show="activeTab === 'documents'">
          <div class="dashboard-header">
            <h1>Документы для регистрации</h1>
            <p style="color:var(--text-gray);font-size:14px;">Загрузите необходимые документы для участия в мероприятиях</p>
          </div>

          <div v-if="pendingRegistrations.length === 0 && myDocs.length === 0" style="text-align:center;padding:60px;color:var(--text-gray);">
            Нет регистраций, требующих документов
          </div>

          <!-- Регистрации ожидающие документов -->
          <div v-for="reg in pendingRegistrations" :key="reg.id" class="section-card" style="margin-bottom:20px;border-left:4px solid #f59e0b;">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:16px;">
              <div>
                <h3 style="font-size:17px;color:var(--primary-dark);">{{ reg.event_title }}</h3>
                <span class="event-badge status-soon" style="margin-top:6px;display:inline-block;">Ожидает документы</span>
              </div>
            </div>

            <!-- Уже загруженные документы -->
            <div v-if="reg.documents?.length" style="margin-bottom:16px;">
              <p style="font-size:14px;font-weight:600;margin-bottom:8px;">Загруженные документы:</p>
              <div v-for="doc in reg.documents" :key="doc.id" style="display:flex;align-items:center;gap:10px;padding:10px 14px;background:#f8fafc;border-radius:8px;margin-bottom:8px;">
                <span style="flex:1;font-size:14px;">{{ docTypeLabel(doc.doc_type) }}</span>
                <span class="status-badge" :class="doc.status">{{ docStatusLabel(doc.status) }}</span>
                <span v-if="doc.admin_note" style="font-size:12px;color:#b45309;background:#fef3c7;padding:2px 8px;border-radius:6px;">{{ doc.admin_note }}</span>
              </div>
            </div>

            <!-- Форма загрузки документа -->
            <div style="background:#f8fafc;border-radius:10px;padding:16px;">
              <p style="font-size:14px;font-weight:600;margin-bottom:12px;">Загрузить документ:</p>
              <div v-if="isMinorParticipant && reg.requires_application" class="form-group">
                <label>Тип документа</label>
                <select v-model="docUploadForm[reg.id].doc_type" class="form-input">
                  <option value="parental_consent">Согласие родителей/законного представителя</option>
                  <option value="application">Заявка на участие</option>
                </select>
              </div>
              <div v-else class="form-group">
                <label>Тип документа</label>
                <div style="padding:10px 14px;background:#eff6ff;border-radius:8px;font-size:14px;color:var(--primary-blue);font-weight:500;">
                  {{ isMinorParticipant ? 'Согласие родителей/законного представителя' : 'Заявка на участие' }}
                </div>
              </div>
              <div v-if="docUploadForm[reg.id].doc_type === 'parental_consent'" class="form-row">
                <div class="form-group">
                  <label>ФИО родителя/законного представителя *</label>
                  <input v-model="docUploadForm[reg.id].parent_full_name" type="text" class="form-input" placeholder="Иванова Мария Петровна">
                </div>
                <div class="form-group">
                  <label>Телефон родителя</label>
                  <input v-model="docUploadForm[reg.id].parent_phone" type="tel" class="form-input" placeholder="+7 (999) 000-00-00">
                </div>
              </div>
              <div class="form-group">
                <label>Файл документа *</label>
                <input type="file" class="form-input" @change="e => onDocFileChange(e, reg.id)" accept=".pdf,.doc,.docx,.jpg,.jpeg,.png">
                <p style="font-size:12px;color:var(--text-gray);margin-top:4px;">PDF, Word, изображения. Макс. 10 МБ.</p>
              </div>
              <div class="form-group">
                <label>Примечание <span style="font-weight:400;color:var(--text-gray);">(необязательно)</span></label>
                <input v-model="docUploadForm[reg.id].comment" type="text" class="form-input" placeholder="Дополнительная информация...">
              </div>
              <div v-if="docUploadErrors[reg.id]" style="color:#991b1b;background:#fef2f2;padding:10px;border-radius:8px;font-size:14px;margin-bottom:10px;">{{ docUploadErrors[reg.id] }}</div>
              <div v-if="docUploadSuccess[reg.id]" style="color:#065f46;background:#d1fae5;padding:10px;border-radius:8px;font-size:14px;margin-bottom:10px;">{{ docUploadSuccess[reg.id] }}</div>
              <button class="btn" style="background:var(--primary-blue);color:white;" @click="uploadDocument(reg.id)" :disabled="docUploading[reg.id]">
                {{ docUploading[reg.id] ? 'Загружаем...' : 'Загрузить документ' }}
              </button>
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
                <div class="form-group"><label>Отчество</label><input v-model="profileForm.patronymic" type="text" class="form-input"></div>
              </div>
              <div class="form-row">
                <div class="form-group"><label>Email</label><input v-model="profileForm.email" type="email" class="form-input" disabled style="background:#f9fafb;"></div>
                <div class="form-group"><label>Телефон</label><input v-model="profileForm.phone" type="tel" class="form-input"></div>
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label>Дата рождения</label>
                  <input v-model="profileForm.birth_date" type="date" class="form-input"
                    :disabled="profileBirthDateLocked" :style="profileBirthDateLocked ? 'background:#f9fafb;' : ''">
                  <p style="font-size:12px;color:var(--text-gray);margin-top:4px;">
                    <span v-if="profileBirthDateLocked">Дата рождения установлена и не может быть изменена.</span>
                    <span v-else>Укажите дату рождения. После сохранения изменить её будет невозможно.</span>
                  </p>
                </div>
                <div v-if="profileAge !== null" class="form-group" style="display:flex;align-items:center;">
                  <div style="padding:12px 20px;background:#eff6ff;border-radius:10px;text-align:center;">
                    <div style="font-size:28px;font-weight:700;color:var(--primary-blue);">{{ profileAge }}</div>
                    <div style="font-size:13px;color:var(--text-gray);">лет</div>
                  </div>
                </div>
              </div>
              <div class="form-group"><label>Учреждение</label><input v-model="profileForm.institution" type="text" class="form-input"></div>
              <!-- Педагог — система заявок -->
              <div class="form-group">
                <label>Мой педагог (куратор)</label>

                <!-- Уже прикреплён -->
                <div v-if="profileForm.teacher_id" style="display:flex;align-items:center;justify-content:space-between;padding:12px 16px;background:#eff6ff;border-radius:10px;border:1px solid #bfdbfe;">
                  <div>
                    <div style="font-weight:600;color:var(--primary-dark);">{{ profileForm.teacher_name || 'Педагог' }}</div>
                    <div style="font-size:12px;color:var(--text-gray);">Педагог видит ваш прогресс в мероприятиях</div>
                  </div>
                  <button type="button" @click="detachTeacher" style="padding:6px 14px;background:none;border:1px solid #ef4444;color:#ef4444;border-radius:8px;cursor:pointer;font-size:13px;">Отвязаться</button>
                </div>

                <!-- Есть ожидающая заявка -->
                <div v-else-if="pendingTeacherRequest" style="padding:12px 16px;background:#fffbeb;border-radius:10px;border:1px solid #fcd34d;">
                  <div style="font-weight:600;color:#92400e;margin-bottom:4px;">Заявка отправлена — ожидает подтверждения</div>
                  <div style="font-size:13px;color:#78350f;">{{ pendingTeacherRequest.teacher_name }} · {{ pendingTeacherRequest.teacher_institution }}</div>
                  <button type="button" @click="cancelTeacherRequest(pendingTeacherRequest.id)" style="margin-top:10px;padding:5px 12px;background:none;border:1px solid #d97706;color:#d97706;border-radius:6px;cursor:pointer;font-size:13px;">Отозвать заявку</button>
                </div>

                <!-- Нет педагога — выбор из списка -->
                <div v-else>
                  <select v-model="selectedTeacherId" class="form-input" style="margin-bottom:8px;">
                    <option :value="null">— Выберите педагога —</option>
                    <option v-for="t in teachersList" :key="t.id" :value="t.id">{{ t.full_name }}{{ t.institution ? ' · ' + t.institution : '' }}</option>
                  </select>
                  <div style="display:flex;gap:8px;align-items:flex-start;">
                    <input v-model="teacherRequestMessage" type="text" class="form-input" placeholder="Сообщение педагогу (необязательно)" style="flex:1;">
                    <button type="button" @click="sendTeacherRequest" :disabled="!selectedTeacherId || sendingTeacherReq"
                      style="padding:10px 18px;background:var(--primary-blue);color:white;border:none;border-radius:8px;cursor:pointer;font-size:14px;white-space:nowrap;">
                      {{ sendingTeacherReq ? '...' : 'Подать заявку' }}
                    </button>
                  </div>
                  <p style="font-size:12px;color:var(--text-gray);margin-top:6px;">Педагог получит заявку и подтвердит прикрепление. Ваш email педагогу не передаётся.</p>
                  <div v-if="teacherReqError" style="color:#991b1b;font-size:13px;margin-top:6px;">{{ teacherReqError }}</div>
                  <div v-if="teacherReqSuccess" style="color:#065f46;font-size:13px;margin-top:6px;">{{ teacherReqSuccess }}</div>
                </div>
              </div>
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

const tabs = computed(() => [
  { id: 'overview', label: 'Обзор', icon: 'chart-bar' },
  { id: 'events', label: 'Мои мероприятия', icon: 'calendar' },
  { id: 'tasks', label: 'Задания', icon: 'document' },
  { id: 'submissions', label: 'Мои работы', icon: 'upload' },
  { id: 'documents', label: 'Документы', icon: 'file', badge: pendingDocsCount.value || null },
  { id: 'profile', label: 'Профиль', icon: 'user' }
])

const initials = computed(() => {
  const u = auth.user
  return u ? ((u.first_name?.[0] || '') + (u.last_name?.[0] || '')).toUpperCase() || 'У' : 'У'
})

const myEvents = ref([])
const submissions = ref([])
const notifications = ref([])
const results = ref([])
const myDocs = ref([])
const pendingRegistrations = ref([])

// Форма загрузки документов (по reg.id)
const docUploadForm = ref({})
const docUploadErrors = ref({})
const docUploadSuccess = ref({})
const docUploading = ref({})

// Upload form
const uploadForm = ref({ event_id: '', file: null })
const uploadLoading = ref(false)
const uploadError = ref('')
const uploadSuccess = ref('')
const activeEvents = computed(() => myEvents.value.filter(ev => ['active', 'upcoming'].includes(effectiveStatus(ev))))

const selectedTasksEvent = ref('')
const eventStages = ref([])
const stagesLoading = ref(false)

async function loadEventStages() {
  if (!selectedTasksEvent.value) { eventStages.value = []; return }
  stagesLoading.value = true
  try {
    const r = await api.get(`/api/events/stages/?event=${selectedTasksEvent.value}`)
    eventStages.value = r.data.results || r.data
  } catch {
    eventStages.value = []
  } finally {
    stagesLoading.value = false
  }
}

function onFileChange(e) {
  const file = e.target.files[0] || null
  if (file && file.size > 10 * 1024 * 1024) {
    uploadError.value = 'Файл превышает 10 МБ. Выберите файл меньшего размера.'
    e.target.value = ''
    uploadForm.value.file = null
    return
  }
  uploadError.value = ''
  uploadForm.value.file = file
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

async function deleteDraft(s) {
  if (!confirm('Удалить черновик? Файл будет удалён безвозвратно.')) return
  s._deleting = true
  try {
    await api.delete(`/api/submissions/${s.id}/`)
    submissions.value = submissions.value.filter(x => x.id !== s.id)
  } catch (e) {
    alert(e.response?.data?.detail || 'Ошибка при удалении')
    s._deleting = false
  }
}

const resubmitId = ref(null)
const resubmitFile = ref(null)
const resubmitError = ref('')

function onResubmitFile(e) {
  const file = e.target.files[0] || null
  resubmitError.value = ''
  if (file && file.size > 10 * 1024 * 1024) {
    resubmitError.value = 'Файл превышает 10 МБ.'
    e.target.value = ''
    resubmitFile.value = null
    return
  }
  resubmitFile.value = file
}

async function resubmitWork(s) {
  if (!resubmitFile.value) return
  s._resubmitting = true
  resubmitError.value = ''
  try {
    const fd = new FormData()
    fd.append('file', resubmitFile.value)
    const r = await api.post(`/api/submissions/${s.id}/resubmit/`, fd, { headers: { 'Content-Type': 'multipart/form-data' } })
    Object.assign(s, r.data)
    resubmitId.value = null
    resubmitFile.value = null
  } catch (e) {
    resubmitError.value = e.response?.data?.detail || 'Ошибка при замене файла'
  } finally {
    s._resubmitting = false
  }
}

function submissionForEvent(eventId) {
  return submissions.value.find(s => s.event === eventId || s.event_id === eventId) || null
}

const profileSaved = ref(false)
const teachersList = ref([])
const pendingTeacherRequest = ref(null)
const selectedTeacherId = ref(null)
const teacherRequestMessage = ref('')
const sendingTeacherReq = ref(false)
const teacherReqError = ref('')
const teacherReqSuccess = ref('')
const profileForm = ref({
  first_name: auth.user?.first_name || '',
  last_name: auth.user?.last_name || '',
  patronymic: auth.user?.patronymic || '',
  email: auth.user?.email || '',
  phone: auth.user?.phone || '',
  institution: auth.user?.institution || '',
  teacher_id: auth.user?.teacher_id ?? null,
  birth_date: '',
})

const activeMyEvents = computed(() => myEvents.value.filter(ev => effectiveStatus(ev) !== 'completed' && effectiveStatus(ev) !== 'cancelled'))
const completedMyEvents = computed(() => myEvents.value.filter(ev => effectiveStatus(ev) === 'completed' || effectiveStatus(ev) === 'cancelled'))
const evaluatedCount = computed(() => submissions.value.filter(s => s.status === 'evaluated').length)
const pendingDocsCount = computed(() => pendingRegistrations.value.length)
const isMinorParticipant = computed(() => {
  const bd = profileForm.value.birth_date
  if (!bd) return false
  const today = new Date()
  const birth = new Date(bd)
  const age = today.getFullYear() - birth.getFullYear() - (
    (today.getMonth() < birth.getMonth() || (today.getMonth() === birth.getMonth() && today.getDate() < birth.getDate())) ? 1 : 0
  )
  return age < 18
})
const profileBirthDateLocked = ref(false)
const profileAge = computed(() => {
  const bd = profileForm.value.birth_date
  if (!bd) return null
  const today = new Date()
  const birth = new Date(bd)
  return today.getFullYear() - birth.getFullYear() - (
    (today.getMonth() < birth.getMonth() || (today.getMonth() === birth.getMonth() && today.getDate() < birth.getDate())) ? 1 : 0
  )
})
const prizes = computed(() => results.value.filter(r => r.place > 0 && r.place <= 3).length)
const gold = computed(() => results.value.filter(r => r.place === 1).length)
const silver = computed(() => results.value.filter(r => r.place === 2).length)
const bronze = computed(() => results.value.filter(r => r.place === 3).length)

onMounted(async () => {
  await Promise.allSettled([
    api.get('/api/events/?my=true').then(r => { myEvents.value = r.data.results || r.data }).catch(() => {}),
    api.get('/api/submissions/').then(r => { submissions.value = r.data.results || r.data }).catch(() => {}),
    api.get('/api/notifications/').then(r => { notifications.value = r.data.results || r.data }).catch(() => {}),
    api.get('/api/submissions/results/').then(r => { results.value = r.data.results || r.data }).catch(() => {}),
    api.get('/api/auth/teachers/').then(r => { teachersList.value = r.data.results || r.data }).catch(() => {}),
    api.get('/api/auth/teacher-requests/').then(r => {
      const reqs = r.data.results || r.data
      pendingTeacherRequest.value = reqs.find(r => r.status === 'pending') || null
    }).catch(() => {}),
    loadMyDocs(),
  ])
  // Подтягиваем birth_date из профиля
  try {
    const r = await api.get('/api/auth/profile/')
    profileForm.value.birth_date = r.data.birth_date || ''
    profileBirthDateLocked.value = r.data.birth_date_locked || false
  } catch {}
})

async function loadMyDocs() {
  try {
    const r = await api.get('/api/events/my-registrations/')
    const regs = r.data.results || r.data
    pendingRegistrations.value = regs.filter(reg => reg.status === 'pending_docs')
    // Инициализируем формы для каждой ожидающей регистрации
    for (const reg of pendingRegistrations.value) {
      if (!docUploadForm.value[reg.id]) {
        const defaultType = isMinorParticipant.value
          ? 'parental_consent'
          : 'application'
        docUploadForm.value[reg.id] = { doc_type: defaultType, parent_full_name: '', parent_phone: '', comment: '', file: null }
      }
    }
  } catch {}
}

function onDocFileChange(e, regId) {
  const file = e.target.files[0] || null
  if (file && file.size > 10 * 1024 * 1024) {
    docUploadErrors.value[regId] = 'Файл превышает 10 МБ.'
    e.target.value = ''
    return
  }
  docUploadErrors.value[regId] = ''
  docUploadForm.value[regId].file = file
}

async function uploadDocument(regId) {
  const form = docUploadForm.value[regId]
  docUploadErrors.value[regId] = ''
  docUploadSuccess.value[regId] = ''
  if (!form.file) { docUploadErrors.value[regId] = 'Выберите файл'; return }
  if (form.doc_type === 'parental_consent' && !form.parent_full_name.trim()) {
    docUploadErrors.value[regId] = 'Укажите ФИО родителя/законного представителя'
    return
  }
  docUploading.value[regId] = true
  try {
    const fd = new FormData()
    fd.append('registration', regId)
    fd.append('doc_type', form.doc_type)
    fd.append('file', form.file)
    if (form.parent_full_name) fd.append('parent_full_name', form.parent_full_name)
    if (form.parent_phone) fd.append('parent_phone', form.parent_phone)
    if (form.comment) fd.append('comment', form.comment)
    const r = await api.post('/api/events/reg-docs/', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
    docUploadSuccess.value[regId] = 'Документ загружен и отправлен на проверку администратору.'
    // Добавляем документ в список регистрации
    const reg = pendingRegistrations.value.find(x => x.id === regId)
    if (reg) { if (!reg.documents) reg.documents = []; reg.documents.push(r.data) }
    form.file = null; form.parent_full_name = ''; form.parent_phone = ''; form.comment = ''
  } catch (e) {
    docUploadErrors.value[regId] = e.response?.data?.detail || Object.values(e.response?.data || {}).flat().join(' ') || 'Ошибка загрузки'
  } finally {
    docUploading.value[regId] = false
  }
}

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

async function sendTeacherRequest() {
  if (!selectedTeacherId.value) return
  sendingTeacherReq.value = true
  teacherReqError.value = ''
  teacherReqSuccess.value = ''
  try {
    await api.post('/api/auth/teacher-requests/', {
      teacher_id: selectedTeacherId.value,
      message: teacherRequestMessage.value,
    })
    const reqs = (await api.get('/api/auth/teacher-requests/')).data
    const list = reqs.results || reqs
    pendingTeacherRequest.value = list.find(r => r.status === 'pending') || null
    teacherReqSuccess.value = 'Заявка отправлена! Ожидайте подтверждения педагога.'
    selectedTeacherId.value = null
    teacherRequestMessage.value = ''
  } catch (e) {
    teacherReqError.value = e.response?.data?.detail || 'Ошибка отправки заявки'
  } finally {
    sendingTeacherReq.value = false
  }
}

async function cancelTeacherRequest(id) {
  try {
    await api.delete(`/api/auth/teacher-requests/${id}/`)
    pendingTeacherRequest.value = null
  } catch {}
}

async function detachTeacher() {
  if (!confirm('Отвязаться от педагога?')) return
  try {
    await auth.updateProfile({ ...profileForm.value, teacher_id: null })
    profileForm.value.teacher_id = null
    profileForm.value.teacher_name = null
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
function docTypeLabel(t) {
  return { parental_consent: 'Согласие родителей', application: 'Заявка на участие', other: 'Прочее' }[t] || t
}
function docStatusLabel(s) {
  return { pending: 'На проверке', approved: 'Одобрено', rejected: 'Отклонено' }[s] || s
}
</script>
