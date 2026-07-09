import { ref, onMounted } from 'vue'
import api from '@/services/api'

const settings = ref([])
const loaded = ref(false)

export function useSiteSettings() {
  async function fetchSettings() {
    if (loaded.value) return
    try {
      const { data } = await api.get('/api/site-settings/public')
      settings.value = data
      loaded.value = true
    } catch {
      settings.value = []
      loaded.value = true
    }
  }

  function isVisible(key) {
    const setting = settings.value.find(s => s.key === key)
    return setting ? setting.value : true
  }

  onMounted(fetchSettings)

  return { settings, isVisible, fetchSettings }
}
