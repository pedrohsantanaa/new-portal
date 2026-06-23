import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const accessToken = ref(localStorage.getItem('access_token') || '')
  const refreshToken = ref(localStorage.getItem('refresh_token') || '')

  const isAuthenticated = computed(() => !!accessToken.value)

  function hasPermission(codename) {
    return user.value?.permissions?.some(p => p.codename === codename) ?? false
  }

  async function login(email, password) {
    const { data } = await api.post('/api/auth/login', { email, password })
    accessToken.value = data.access_token
    refreshToken.value = data.refresh_token
    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('refresh_token', data.refresh_token)
    api.defaults.headers.common['Authorization'] = `Bearer ${data.access_token}`
    await fetchUser()
  }

  async function fetchUser() {
    try {
      const { data } = await api.get('/api/auth/me')
      user.value = data
    } catch {
      logout()
    }
  }

  function logout() {
    user.value = null
    accessToken.value = ''
    refreshToken.value = ''
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    delete api.defaults.headers.common['Authorization']
  }

  function init() {
    if (accessToken.value) {
      api.defaults.headers.common['Authorization'] = `Bearer ${accessToken.value}`
      fetchUser()
    }
  }

  return { user, accessToken, refreshToken, isAuthenticated, hasPermission, login, fetchUser, logout, init }
})
