import axios from 'axios'

export const API_BASE_URL = (import.meta.env.VITE_API_URL || '').replace(/\/+$/, '')

export function buildApiUrl(path) {
  return API_BASE_URL ? `${API_BASE_URL}${path}` : path
}

const api = axios.create({
  baseURL: API_BASE_URL || '',
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  if (config.method === 'get') {
    config.params = { ...config.params, _t: Date.now() }
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    if (!originalRequest) return Promise.reject(error)
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        try {
          const { data } = await axios.post(buildApiUrl('/api/auth/refresh'), { refresh_token: refreshToken })
          localStorage.setItem('access_token', data.access_token)
          localStorage.setItem('refresh_token', data.refresh_token)
          originalRequest.headers.Authorization = `Bearer ${data.access_token}`
          return api(originalRequest)
        } catch {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          window.location.href = '/login'
        }
      }
    }
    return Promise.reject(error)
  }
)

export default api
