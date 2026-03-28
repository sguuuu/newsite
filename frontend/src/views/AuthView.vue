<template>
  <div>
    <AppHeader />
    <section class="section" style="min-height: calc(100vh - 80px); background: var(--light-gray); display:flex; align-items:center;">
      <div class="container" style="max-width: 540px; width:100%;">
        <div style="background: white; border-radius: 16px; padding: 40px; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">

          <!-- ── Подтверждение сброса пароля (пришли по ссылке из письма) ── -->
          <div v-if="resetMode === 'confirm'">
            <h2 style="color:var(--primary-dark); margin-top:0; margin-bottom:24px;">Новый пароль</h2>
            <form @submit.prevent="handleResetConfirm" novalidate>
              <div class="form-group">
                <label :style="resetErrors.new_password ? 'color:#ef4444' : ''">Новый пароль</label>
                <input v-model="resetConfirmForm.new_password" type="password" class="form-input" placeholder="Минимум 8 символов"
                  :style="resetErrors.new_password ? 'border-color:#ef4444' : ''"
                  @input="delete resetErrors.new_password">
                <span v-if="resetErrors.new_password" style="color:#ef4444;font-size:12px;margin-top:4px;display:block;">{{ resetErrors.new_password }}</span>
              </div>
              <div class="form-group">
                <label :style="resetErrors.confirm ? 'color:#ef4444' : ''">Повторите пароль</label>
                <input v-model="resetConfirmForm.confirm" type="password" class="form-input" placeholder="Повторите пароль"
                  :style="resetErrors.confirm ? 'border-color:#ef4444' : ''"
                  @input="delete resetErrors.confirm">
                <span v-if="resetErrors.confirm" style="color:#ef4444;font-size:12px;margin-top:4px;display:block;">{{ resetErrors.confirm }}</span>
              </div>
              <div v-if="resetError" style="color:#ef4444; font-size:14px; margin-bottom:15px; padding: 10px; background:#fef2f2; border-radius:8px;">{{ resetError }}</div>
              <div v-if="resetSuccess" style="color:#065f46; font-size:14px; margin-bottom:15px; padding: 10px; background:#d1fae5; border-radius:8px;">{{ resetSuccess }}</div>
              <button v-if="!resetSuccess" type="submit" class="btn btn-primary" style="width:100%; background:var(--primary-blue); color:white;" :disabled="resetLoading">
                {{ resetLoading ? 'Сохраняем...' : 'Сохранить пароль' }}
              </button>
              <button v-else type="button" class="btn btn-primary" style="width:100%; background:var(--primary-blue); color:white;" @click="activeTab = 'login'; resetMode = ''">
                Войти
              </button>
            </form>
          </div>

          <!-- ── Запрос сброса пароля ── -->
          <div v-else-if="resetMode === 'request'">
            <button @click="resetMode = ''" style="border:none;background:none;cursor:pointer;color:var(--primary-blue);font-size:14px;padding:0;margin-bottom:20px;">← Назад</button>
            <h2 style="color:var(--primary-dark); margin-top:0; margin-bottom:8px;">Восстановление пароля</h2>
            <p style="color:var(--text-gray); font-size:14px; margin-bottom:24px;">Введите email — отправим ссылку для сброса пароля.</p>
            <form @submit.prevent="handleResetRequest" novalidate>
              <div class="form-group">
                <label>Email</label>
                <input v-model="resetEmail" type="email" class="form-input" placeholder="your@email.com" required>
              </div>
              <div v-if="resetError" style="color:#ef4444; font-size:14px; margin-bottom:15px; padding: 10px; background:#fef2f2; border-radius:8px;">{{ resetError }}</div>
              <div v-if="resetSuccess" style="color:#065f46; font-size:14px; margin-bottom:15px; padding: 10px; background:#d1fae5; border-radius:8px;">{{ resetSuccess }}</div>
              <button type="submit" class="btn btn-primary" style="width:100%; background:var(--primary-blue); color:white;" :disabled="resetLoading || !!resetSuccess">
                {{ resetLoading ? 'Отправляем...' : 'Отправить ссылку' }}
              </button>
            </form>
          </div>

          <!-- ── Обычный вход / регистрация ── -->
          <template v-else>
            <!-- Tabs -->
            <div style="display:flex; border-bottom: 2px solid #e5e7eb; margin-bottom: 30px;">
              <button
                v-for="tab in ['login','register']" :key="tab"
                @click="activeTab = tab"
                :style="{ padding:'12px 24px', border:'none', background:'none', cursor:'pointer', fontWeight: activeTab===tab ? 600 : 400, color: activeTab===tab ? 'var(--primary-blue)' : 'var(--text-gray)', borderBottom: activeTab===tab ? '2px solid var(--primary-blue)' : '2px solid transparent', marginBottom:'-2px', fontSize:'15px' }"
              >{{ tab === 'login' ? 'Войти' : 'Регистрация' }}</button>
            </div>

            <!-- Login -->
            <form v-if="activeTab === 'login'" @submit.prevent="handleLogin">
              <div class="form-group">
                <label>Email</label>
                <input v-model="loginForm.email" type="email" class="form-input" placeholder="your@email.com" required>
              </div>
              <div class="form-group">
                <label>Пароль</label>
                <div style="position:relative;">
                  <input v-model="loginForm.password" :type="showLoginPassword ? 'text' : 'password'" class="form-input" placeholder="Введите пароль" style="padding-right:44px" required>
                  <button type="button" @click="showLoginPassword = !showLoginPassword" style="position:absolute;right:10px;top:50%;transform:translateY(-50%);background:none;border:none;cursor:pointer;color:var(--text-gray);padding:4px;">
                    {{ showLoginPassword ? '🙈' : '👁' }}
                  </button>
                </div>
              </div>
              <div v-if="error" style="color:#ef4444; font-size:14px; margin-bottom:15px; padding: 10px; background:#fef2f2; border-radius:8px;">{{ error }}</div>
              <button type="submit" class="btn btn-primary" style="width:100%; background: var(--primary-blue); color: white;" :disabled="loginLoading">
                {{ loginLoading ? 'Входим...' : 'Войти' }}
              </button>
              <div style="text-align:center; margin-top:16px;">
                <button type="button" @click="openResetRequest" style="border:none;background:none;cursor:pointer;color:var(--primary-blue);font-size:14px;text-decoration:underline;">
                  Забыли пароль?
                </button>
              </div>
            </form>

            <!-- Register -->
            <form v-else @submit.prevent="handleRegister" novalidate>
              <div style="margin-bottom: 20px;">
                <label style="display:block; font-weight:500; font-size:14px; margin-bottom:8px;">Тип пользователя</label>
                <div style="display:flex; gap:10px; flex-wrap:wrap;">
                  <label v-for="r in roles" :key="r.value" style="display:flex; align-items:center; gap:6px; cursor:pointer; padding: 8px 16px; border: 2px solid; border-radius:8px; font-size:14px; transition: all 0.2s;"
                    :style="{ borderColor: regForm.role === r.value ? 'var(--primary-blue)' : '#e5e7eb', background: regForm.role === r.value ? '#eff6ff' : 'white', color: regForm.role === r.value ? 'var(--primary-blue)' : 'var(--text-dark)' }">
                    <input type="radio" v-model="regForm.role" :value="r.value" style="display:none">
                    {{ r.label }}
                  </label>
                </div>
              </div>
              <div class="form-row">
                <div class="form-group" style="margin-bottom:0;">
                  <label :style="fieldErrors.last_name ? 'color:#ef4444' : ''">Фамилия</label>
                  <input v-model="regForm.last_name" type="text" class="form-input" placeholder="Иванов"
                    :style="fieldErrors.last_name ? 'border-color:#ef4444' : ''"
                    @input="clearFieldError('last_name')">
                  <span style="color:#ef4444;font-size:12px;margin-top:4px;display:block;min-height:18px;">{{ fieldErrors.last_name ? 'Обязательное поле' : '' }}</span>
                </div>
                <div class="form-group" style="margin-bottom:0;">
                  <label :style="fieldErrors.first_name ? 'color:#ef4444' : ''">Имя</label>
                  <input v-model="regForm.first_name" type="text" class="form-input" placeholder="Иван"
                    :style="fieldErrors.first_name ? 'border-color:#ef4444' : ''"
                    @input="clearFieldError('first_name')">
                  <span style="color:#ef4444;font-size:12px;margin-top:4px;display:block;min-height:18px;">{{ fieldErrors.first_name ? 'Обязательное поле' : '' }}</span>
                </div>
              </div>
              <div class="form-group">
                <label>Отчество</label>
                <input v-model="regForm.patronymic" type="text" class="form-input" placeholder="Иванович">
              </div>
              <div class="form-group" style="margin-bottom:0;">
                <label :style="fieldErrors.email ? 'color:#ef4444' : ''">Email</label>
                <input v-model="regForm.email" type="email" class="form-input" placeholder="your@email.com"
                  :style="fieldErrors.email ? 'border-color:#ef4444' : ''"
                  @input="clearFieldError('email')">
                <span style="color:#ef4444;font-size:12px;margin-top:4px;display:block;min-height:18px;">{{ fieldErrors.email || '' }}</span>
              </div>
              <div class="form-group">
                <label>Учреждение</label>
                <input v-model="regForm.institution" type="text" class="form-input" placeholder="Школа №1, г. Сочи">
              </div>
              <div v-if="['participant', 'teacher'].includes(regForm.role)" class="form-group" style="margin-bottom:0;">
                <label :style="fieldErrors.birth_date ? 'color:#ef4444' : ''">Дата рождения *</label>
                <input v-model="regForm.birth_date" type="date" class="form-input"
                  :style="fieldErrors.birth_date ? 'border-color:#ef4444' : ''"
                  @input="clearFieldError('birth_date')">
                <span style="color:#ef4444;font-size:12px;margin-top:4px;display:block;min-height:18px;">{{ fieldErrors.birth_date || '' }}</span>
              </div>
              <div class="form-row">
                <div class="form-group" style="margin-bottom:0;">
                  <label :style="fieldErrors.password ? 'color:#ef4444' : ''">Пароль</label>
                  <div style="position:relative;">
                    <input v-model="regForm.password" :type="showPassword ? 'text' : 'password'" class="form-input" placeholder="Минимум 8 символов"
                      :style="fieldErrors.password ? 'border-color:#ef4444;padding-right:44px' : 'padding-right:44px'"
                      @input="clearFieldError('password')">
                    <button type="button" @click="showPassword = !showPassword" style="position:absolute;right:10px;top:50%;transform:translateY(-50%);background:none;border:none;cursor:pointer;color:var(--text-gray);padding:4px;">
                      {{ showPassword ? '🙈' : '👁' }}
                    </button>
                  </div>
                  <span style="color:#ef4444;font-size:12px;margin-top:4px;display:block;min-height:18px;">{{ fieldErrors.password || '' }}</span>
                </div>
                <div class="form-group" style="margin-bottom:0;">
                  <label :style="fieldErrors.password_confirm ? 'color:#ef4444' : ''">Повторить пароль</label>
                  <div style="position:relative;">
                    <input v-model="regForm.password_confirm" :type="showPasswordConfirm ? 'text' : 'password'" class="form-input" placeholder="Повторите пароль"
                      :style="fieldErrors.password_confirm ? 'border-color:#ef4444;padding-right:44px' : 'padding-right:44px'"
                      @input="clearFieldError('password_confirm')">
                    <button type="button" @click="showPasswordConfirm = !showPasswordConfirm" style="position:absolute;right:10px;top:50%;transform:translateY(-50%);background:none;border:none;cursor:pointer;color:var(--text-gray);padding:4px;">
                      {{ showPasswordConfirm ? '🙈' : '👁' }}
                    </button>
                  </div>
                  <span style="color:#ef4444;font-size:12px;margin-top:4px;display:block;min-height:18px;">{{ fieldErrors.password_confirm ? 'Обязательное поле' : '' }}</span>
                </div>
              </div>
              <div style="margin-bottom:20px; padding:14px; border-radius:10px; transition: all 0.2s;"
                :style="fieldErrors.consent_given ? 'background:#fef2f2; border:1px solid #fca5a5;' : 'background:#f8fafc; border:1px solid #e5e7eb;'">
                <label style="display:flex; align-items:flex-start; gap:10px; cursor:pointer;">
                  <input type="checkbox" v-model="regForm.consent_given" style="margin-top:3px; flex-shrink:0; width:16px; height:16px; cursor:pointer;"
                    @change="clearFieldError('consent_given')">
                  <span style="font-size:13px; line-height:1.5; color:var(--text-dark);">
                    Я даю согласие на обработку персональных данных в соответствии с
                    <a href="/documents?type=privacy" target="_blank" style="color:var(--primary-blue); text-decoration:underline;">Политикой конфиденциальности</a>.
                  </span>
                </label>
                <span v-if="fieldErrors.consent_given" style="color:#ef4444;font-size:12px;margin-top:6px;display:block;padding-left:26px;">Необходимо дать согласие</span>
              </div>
              <div v-if="error" style="color:#ef4444; font-size:14px; margin-bottom:15px; padding: 10px; background:#fef2f2; border-radius:8px;">{{ error }}</div>
              <div v-if="success" style="color:#065f46; font-size:14px; margin-bottom:15px; padding: 10px; background:#d1fae5; border-radius:8px;">{{ success }}</div>
              <button type="submit" class="btn btn-primary" style="width:100%; background: var(--primary-blue); color: white;" :disabled="regLoading">
                {{ regLoading ? 'Регистрируем...' : 'Зарегистрироваться' }}
              </button>
            </form>
          </template>

        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import AppHeader from '@/components/AppHeader.vue'
import { useAuthStore } from '@/stores/auth.js'
import api from '@/api/index.js'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const activeTab = ref('login')
const error = ref('')
const success = ref('')
const loginLoading = ref(false)
const regLoading = ref(false)

// Режим сброса пароля: '' | 'request' | 'confirm'
const resetMode = ref('')
const resetEmail = ref('')
const resetLoading = ref(false)
const resetError = ref('')
const resetSuccess = ref('')
const resetErrors = ref({})
const resetConfirmForm = ref({ new_password: '', confirm: '' })

const loginForm = ref({ email: '', password: '' })
const regForm = ref({ role: 'participant', first_name: '', last_name: '', patronymic: '', email: '', institution: '', birth_date: '', password: '', password_confirm: '', consent_given: false })
const showLoginPassword = ref(false)
const showPassword = ref(false)
const showPasswordConfirm = ref(false)
const fieldErrors = ref({})

const roles = [
  { value: 'participant', label: 'Участник' },
  { value: 'teacher', label: 'Педагог' },
  { value: 'jury', label: 'Жюри' }
]

const roleRedirects = { admin: '/dashboard/admin', teacher: '/dashboard/teacher', participant: '/dashboard/participant', jury: '/dashboard/jury' }

// Если пришли по ссылке из письма (?uid=...&token=...)
onMounted(() => {
  if (route.query.uid && route.query.token) {
    resetConfirmForm.value = { new_password: '', confirm: '' }
    resetMode.value = 'confirm'
  }
})

function openResetRequest() {
  resetMode.value = 'request'
  resetEmail.value = ''
  resetError.value = ''
  resetSuccess.value = ''
}

function clearFieldError(field) {
  if (fieldErrors.value[field]) delete fieldErrors.value[field]
}

async function handleLogin() {
  error.value = ''
  loginLoading.value = true
  try {
    const user = await auth.login(loginForm.value.email, loginForm.value.password)
    const redirect = new URLSearchParams(window.location.search).get('redirect')
    router.push(redirect || roleRedirects[user.role] || '/')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Неверный email или пароль'
  } finally {
    loginLoading.value = false
  }
}

async function handleRegister() {
  error.value = ''
  success.value = ''
  fieldErrors.value = {}

  const f = regForm.value
  let hasErrors = false
  if (!f.first_name.trim()) { fieldErrors.value.first_name = true; hasErrors = true }
  if (!f.last_name.trim()) { fieldErrors.value.last_name = true; hasErrors = true }
  if (!f.email.trim()) { fieldErrors.value.email = 'Обязательное поле'; hasErrors = true }
  else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.email)) { fieldErrors.value.email = 'Некорректный email'; hasErrors = true }
  if (!f.password) { fieldErrors.value.password = 'Обязательное поле'; hasErrors = true }
  else if (f.password.length < 8) { fieldErrors.value.password = 'Минимум 8 символов'; hasErrors = true }
  if (!f.password_confirm) { fieldErrors.value.password_confirm = true; hasErrors = true }
  if (!f.consent_given) { fieldErrors.value.consent_given = true; hasErrors = true }
  if (['participant', 'teacher'].includes(f.role) && !f.birth_date) { fieldErrors.value.birth_date = 'Обязательное поле'; hasErrors = true }
  if (hasErrors) return

  if (f.password !== f.password_confirm) {
    error.value = 'Пароли не совпадают'
    return
  }

  regLoading.value = true
  try {
    const payload = { ...f, birth_date: f.birth_date || null }
    const resp = await auth.register(payload)
    const data = resp.data
    success.value = data.detail || 'Регистрация успешна!'
    if (!data.needs_approval) {
      // Участник — сразу переводим на вход
      activeTab.value = 'login'
      loginForm.value.email = f.email
    }
    // Педагог/жюри — остаёмся на форме, показываем сообщение об ожидании
  } catch (e) {
    const data = e.response?.data
    if (data?.email) { fieldErrors.value.email = data.email[0]; return }
    if (data && typeof data === 'object') {
      error.value = data.detail || Object.values(data).flat().join(' ')
    } else if (!e.response) {
      error.value = 'Нет связи с сервером. Убедитесь, что сервер запущен.'
    } else {
      error.value = 'Ошибка регистрации. Попробуйте снова.'
    }
  } finally {
    regLoading.value = false
  }
}

async function handleResetRequest() {
  resetError.value = ''
  resetSuccess.value = ''
  if (!resetEmail.value.trim()) { resetError.value = 'Введите email'; return }
  resetLoading.value = true
  try {
    await api.post('/api/auth/password-reset/', { email: resetEmail.value.trim() })
    resetSuccess.value = 'Если такой email зарегистрирован — письмо отправлено. Проверьте почту.'
  } catch {
    resetError.value = 'Ошибка отправки. Попробуйте позже.'
  } finally {
    resetLoading.value = false
  }
}

async function handleResetConfirm() {
  resetError.value = ''
  resetErrors.value = {}
  const f = resetConfirmForm.value
  if (!f.new_password) { resetErrors.value.new_password = 'Обязательное поле'; return }
  if (f.new_password.length < 8) { resetErrors.value.new_password = 'Минимум 8 символов'; return }
  if (!f.confirm) { resetErrors.value.confirm = 'Обязательное поле'; return }
  if (f.new_password !== f.confirm) { resetErrors.value.confirm = 'Пароли не совпадают'; return }

  resetLoading.value = true
  try {
    await api.post('/api/auth/password-reset/confirm/', {
      uid: route.query.uid,
      token: route.query.token,
      new_password: f.new_password,
    })
    resetSuccess.value = 'Пароль успешно изменён!'
  } catch (e) {
    resetError.value = e.response?.data?.detail || 'Ссылка устарела. Запросите новую.'
  } finally {
    resetLoading.value = false
  }
}
</script>
