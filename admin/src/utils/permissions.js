import { useAuthStore } from '@/stores/auth'

export function canAccess(codename) {
  const auth = useAuthStore()
  return auth.hasPermission(codename)
}
