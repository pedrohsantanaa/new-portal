import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
  },
  {
    path: '/noticias',
    name: 'NewsPage',
    component: () => import('@/views/NewsPage.vue'),
  },
  {
    path: '/noticias/:slug',
    name: 'NewsDetail',
    component: () => import('@/views/NewsDetailPage.vue'),
  },
  {
    path: '/acesso-a-informacao',
    name: 'InfoAccess',
    component: () => import('@/views/InfoAccessPage.vue'),
  },
  {
    path: '/linhas-de-credito',
    name: 'CreditLines',
    component: () => import('@/views/CreditLinesPage.vue'),
  },
  {
    path: '/linhas-de-credito/:slug',
    name: 'CreditLineDetail',
    component: () => import('@/views/CreditLineDetailPage.vue'),
  },
  {
    path: '/institucional',
    name: 'Institutional',
    component: () => import('@/views/InstitutionalPage.vue'),
  },
  {
    path: '/vendas-diretas',
    name: 'VendasDiretas',
    component: () => import('@/views/VendasDiretasPage.vue'),
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/Home.vue'),
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
