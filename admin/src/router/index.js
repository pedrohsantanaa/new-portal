import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import Login from '@/views/Login.vue'
import Dashboard from '@/views/Dashboard.vue'
import NewsList from '@/views/NewsList.vue'
import NewsForm from '@/views/NewsForm.vue'
import CreditLinesList from '@/views/CreditLinesList.vue'
import CreditLineForm from '@/views/CreditLineForm.vue'

const routes = [
  { path: '/login', name: 'Login', component: Login, meta: { guest: true } },
  {
    path: '/',
    component: () => import('@/components/AdminLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', name: 'Dashboard', component: Dashboard },
      { path: 'news', name: 'NewsList', component: NewsList },
      { path: 'news/new', name: 'NewsNew', component: NewsForm },
      { path: 'news/:slug/edit', name: 'NewsEdit', component: NewsForm },
      { path: 'credit-lines', name: 'CreditLinesList', component: CreditLinesList },
      { path: 'credit-lines/new', name: 'CreditLineNew', component: CreditLineForm },
      { path: 'credit-lines/:id/edit', name: 'CreditLineEdit', component: CreditLineForm },
    ],
  },
]

const router = createRouter({
  history: createWebHistory('/admin'),
  routes,
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next('/login')
  } else if (to.meta.guest && auth.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router
