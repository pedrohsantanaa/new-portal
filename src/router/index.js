import { createRouter, createWebHistory } from 'vue-router'

import Home from '@/views/Home.vue'
import NewsPage from '@/views/NewsPage.vue'
import NewsDetailPage from '@/views/NewsDetailPage.vue'
import InfoAccessPage from '@/views/InfoAccessPage.vue'
import CreditLinesPage from '@/views/CreditLinesPage.vue'
import CreditLineDetailPage from '@/views/CreditLineDetailPage.vue'
import InstitutionalPage from '@/views/InstitutionalPage.vue'

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
  {
    path: '/linhas-de-credito',
    name: 'CreditLines',
    component: CreditLinesPage,
  },
  {
    path: '/linhas-de-credito/:slug',
    name: 'CreditLineDetail',
    component: CreditLineDetailPage,
  },
  {
    path: '/institucional',
    name: 'Institutional',
    component: InstitutionalPage,
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
