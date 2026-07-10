import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  { path: '/login', name: 'Login', component: () => import('@/views/Login.vue'), meta: { guest: true } },
  {
    path: '/',
    component: () => import('@/components/AdminLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', name: 'Dashboard', component: () => import('@/views/Dashboard.vue') },
      { path: 'news', name: 'NewsList', component: () => import('@/views/NewsList.vue'), meta: { permission: 'news' } },
      { path: 'news/new', name: 'NewsNew', component: () => import('@/views/NewsForm.vue'), meta: { permission: 'news' } },
      { path: 'news/:slug/edit', name: 'NewsEdit', component: () => import('@/views/NewsForm.vue'), meta: { permission: 'news' } },
      { path: 'credit-lines', name: 'CreditLinesList', component: () => import('@/views/CreditLinesList.vue'), meta: { permission: 'credit_lines' } },
      { path: 'credit-lines/new', name: 'CreditLineNew', component: () => import('@/views/CreditLineForm.vue'), meta: { permission: 'credit_lines' } },
      { path: 'credit-lines/:id/edit', name: 'CreditLineEdit', component: () => import('@/views/CreditLineForm.vue'), meta: { permission: 'credit_lines' } },
      { path: 'categories', name: 'CategoryList', component: () => import('@/views/CategoryList.vue'), meta: { permission: 'categories' } },
      { path: 'categories/new', name: 'CategoryNew', component: () => import('@/views/CategoryForm.vue'), meta: { permission: 'categories' } },
      { path: 'categories/:id/edit', name: 'CategoryEdit', component: () => import('@/views/CategoryForm.vue'), meta: { permission: 'categories' } },
      { path: 'users', name: 'UserList', component: () => import('@/views/UserList.vue'), meta: { permission: 'users' } },
      { path: 'users/new', name: 'UserNew', component: () => import('@/views/UserForm.vue'), meta: { permission: 'users' } },
      { path: 'users/:id/edit', name: 'UserEdit', component: () => import('@/views/UserForm.vue'), meta: { permission: 'users' } },
      { path: 'info-access', name: 'InfoCategoryList', component: () => import('@/views/InfoCategoryList.vue'), meta: { permission: 'info_access' } },
      { path: 'info-access/new', name: 'InfoCategoryNew', component: () => import('@/views/InfoCategoryForm.vue'), meta: { permission: 'info_access' } },
      { path: 'info-access/:id/edit', name: 'InfoCategoryEdit', component: () => import('@/views/InfoCategoryForm.vue'), meta: { permission: 'info_access' } },
      { path: 'info-documents', name: 'InfoDocumentList', component: () => import('@/views/InfoDocumentList.vue'), meta: { permission: 'info_access' } },
      { path: 'info-documents/new', name: 'InfoDocumentNew', component: () => import('@/views/InfoDocumentForm.vue'), meta: { permission: 'info_access' } },
      { path: 'info-documents/:id/edit', name: 'InfoDocumentEdit', component: () => import('@/views/InfoDocumentForm.vue'), meta: { permission: 'info_access' } },
      { path: 'settings', name: 'SiteSettings', component: () => import('@/views/SiteSettings.vue'), meta: { permission: 'settings' } },
      { path: 'carousel', name: 'CarouselList', component: () => import('@/views/CarouselList.vue'), meta: { permission: 'settings' } },
      { path: 'carousel/new', name: 'CarouselNew', component: () => import('@/views/CarouselForm.vue'), meta: { permission: 'settings' } },
      { path: 'carousel/:id/edit', name: 'CarouselEdit', component: () => import('@/views/CarouselForm.vue'), meta: { permission: 'settings' } },
      { path: 'sale-items', name: 'SaleItemList', component: () => import('@/views/SaleItemList.vue'), meta: { permission: 'settings' } },
      { path: 'sale-items/new', name: 'SaleItemNew', component: () => import('@/views/SaleItemForm.vue'), meta: { permission: 'settings' } },
      { path: 'sale-items/:id/edit', name: 'SaleItemEdit', component: () => import('@/views/SaleItemForm.vue'), meta: { permission: 'settings' } },
    ],
  },
  { path: '/:pathMatch(.*)*', redirect: '/' },
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
  } else if (to.meta.permission && !auth.hasPermission(to.meta.permission)) {
    next('/')
  } else {
    next()
  }
})

export default router
