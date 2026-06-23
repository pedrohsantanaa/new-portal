import { createRouter, createWebHistory } from 'vue-router'

import Home from '@/views/Home.vue'
import NewsPage from '@/views/NewsPage.vue'
import NewsDetailPage from '@/views/NewsDetailPage.vue'
import InfoAccessPage from '@/views/InfoAccessPage.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/noticias',
    name: 'NewsPage',
    component: NewsPage,
  },
  {
    path: '/noticias/:slug',
    name: 'NewsDetail',
    component: NewsDetailPage,
  },
  {
    path: '/acesso-a-informacao',
    name: 'InfoAccess',
    component: InfoAccessPage,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    if (to.hash) return { el: to.hash, behavior: 'smooth' }
    return { top: 0, behavior: 'smooth' }
  },
})

export default router
