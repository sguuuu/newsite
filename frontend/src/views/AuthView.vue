<template>
  <div>
    <AppHeader />
    <section class="section" style="min-height: calc(100vh - 80px); background: var(--light-gray); display:flex; align-items:center;">
      <div class="container" style="max-width: 540px; width:100%;">
        <div style="background: white; border-radius: 16px; padding: 40px; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">

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
              <input v-model="loginForm.password" type="password" class="form-input" placeholder="Введите пароль" required>
            </div>
            <div v-if="error" style="color:#ef4444; font-size:14px; margin-bottom:15px; padding: 10px; background:#fef2f2; border-radius:8px;">{{ error }}</div>
            <button type="submit" class="btn btn-primary" style="width:100%; background: var(--primary-blue); color: white;" :disabled="loginLoading">
              {{ loginLoading ? 'Входим...' : 'Войти' }}
            </button>
          </form>

          <!-- Register -->
          <form v-else @submit.prevent="handleRegister">
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
              <div class="form-group">
                <label>Имя</label>
                <input v-model="regForm.first_name" type="text" class="form-input" placeholder="Иван" required>
              </div>
              <div class="form-group">
                <label>Фамилия</label>
                <input v-model="regForm.last_name" type="text" class="form-input" placeholder="Иванов" required>
              </div>
            </div>
            <div class="form-group">
              <label>Отчество</label>
              <input v-model="regForm.patronymic" type="text" class="form-input" placeholder="Иванович">
            </div>
            <div class="form-group">
              <label>Email</label>
              <input v-model="regForm.email" type="email" class="form-input" placeholder="your@email.com" required>
            </div>
            <div class="form-group">
              <label>Учреждение</label>
              <input v-model="regForm.institution" type="text" class="form-input" placeholder="Школа №1, г. Сочи">
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>Пароль</label>
                <input v-model="regForm.password" type="password" class="form-input" placeholder="Минимум 8 символов" required>
              </div>
              <div class="form-group">
                <label>Повторить пароль</label>
                <input v-model="regForm.password2" type="password" class="form-input" placeholder="Повторите пароль" required>
              </div>
            </div>
            <!-- Согласие на обработку персональных данных -->
            <div style="margin-bottom:20px; padding:14px; background:#f8fafc; border:1px solid #e5e7eb; border-radius:10px;">
              <label style="display:flex; align-items:flex-start; gap:10px; cursor:pointer;">
                <input type="checkbox" v-model="regForm.consent_given" style="margin-top:3px; flex-shrink:0; width:16px; height:16px; cursor:pointer;" required>
                <span style="font-size:13px; line-height:1.5; color:var(--text-dark);">
                  Я даю согласие на обработку персональных данных в соответствии с
                  <a href="/documents?type=privacy" target="_blank" style="color:var(--primary-blue); text-decoration:underline;">Политикой конфиденциальности</a>.
                  С документом можно ознакомиться перед регистрацией.
                </span>
              </label>
            </div>
            <div v-if="error" style="color:#ef4444; font-size:14px; margin-bottom:15px; padding: 10px; background:#fef2f2; border-radius:8px;">{{ error }}</div>
            <div v-if="success" style="color:#065f46; font-size:14px; margin-bottom:15px; padding: 10px; background:#d1fae5; border-radius:8px;">{{ success }}</div>
            <button type="submit" class="btn btn-primary" style="width:100%; background: var(--primary-blue); color: white;" :disabled="regLoading || !regForm.consent_given">
              {{ regLoading ? 'Регистрируем...' : 'Зарегистрироваться' }}
            </button>
          </form>

        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AppHeader from '@/components/AppHeader.vue'
import { useAuthStore } from '@/stores/auth.js'

const router = useRouter()
const auth = useAuthStore()
const activeTab = ref('login')
const error = ref('')
const success = ref('')
const loginLoading = ref(false)
const regLoading = ref(false)

const loginForm = ref({ email: '', password: '' })
const regForm = ref({ role: 'participant', first_name: '', last_name: '', patronymic: '', email: '', institution: '', password: '', password2: '', consent_given: false })

const roles = [
  { value: 'participant', label: 'Участник' },
  { value: 'teacher', label: 'Педагог' },
  { value: 'jury', label: 'Жюри' }
]

const roleRedirects = { admin: '/dashboard/admin', teacher: '/dashboard/teacher', participant: '/dashboard/participant', jury: '/dashboard/jury' }

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
  if (regForm.value.password !== regForm.value.password2) {
    error.value = 'Пароли не совпадают'
    return
  }
  if (!regForm.value.consent_given) {
    error.value = 'Необходимо дать согласие на обработку персональных данных'
    return
  }
  regLoading.value = true
  try {
    await auth.register(regForm.value)
    success.value = 'Регистрация успешна! Войдите в систему.'
    activeTab.value = 'login'
    loginForm.value.email = regForm.value.email
  } catch (e) {
    const data = e.response?.data
    error.value = typeof data === 'object' ? Object.values(data).flat().join(' ') : 'Ошибка регистрации'
  } finally {
    regLoading.value = false
  }
}
</script>
