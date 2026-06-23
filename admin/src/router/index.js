import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import Login from '@/views/Login.vue'
import Dashboard from '@/views/Dashboard.vue'
import NewsList from '@/views/NewsList.vue'
import NewsForm from '@/views/NewsForm.vue'
import CreditLinesList from '@/views/CreditLinesList.vue'
import CreditLineForm from '@/views/CreditLineForm.vue'
import CategoryList from '@/views/CategoryList.vue'
import CategoryForm from '@/views/CategoryForm.vue'
import UserList from '@/views/UserList.vue'
import UserForm from '@/views/UserForm.vue'
import InfoCategoryList from '@/views/InfoCategoryList.vue'
import InfoCategoryForm from '@/views/InfoCategoryForm.vue'
import InfoDocumentList from '@/views/InfoDocumentList.vue'
import InfoDocumentForm from '@/views/InfoDocumentForm.vue'

const routes = [
  { path: '/login', name: 'Login', component: Login, meta: { guest: true } },
  {
    path: '/',
    component: () => import('@/components/AdminLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', name: 'Dashboard', component: Dashboard },
      { path: 'news', name: 'NewsList', component: NewsList, meta: { permission: 'news' } },
      { path: 'news/new', name: 'NewsNew', component: NewsForm, meta: { permission: 'news' } },
      { path: 'news/:slug/edit', name: 'NewsEdit', component: NewsForm, meta: { permission: 'news' } },
      { path: 'credit-lines', name: 'CreditLinesList', component: CreditLinesList, meta: { permission: 'credit_lines' } },
      { path: 'credit-lines/new', name: 'CreditLineNew', component: CreditLineForm, meta: { permission: 'credit_lines' } },
      { path: 'credit-lines/:id/edit', name: 'CreditLineEdit', component: CreditLineForm, meta: { permission: 'credit_lines' } },
      { path: 'categories', name: 'CategoryList', component: CategoryList, meta: { permission: 'categories' } },
      { path: 'categories/new', name: 'CategoryNew', component: CategoryForm, meta: { permission: 'categories' } },
      { path: 'categories/:id/edit', name: 'CategoryEdit', component: CategoryForm, meta: { permission: 'categories' } },
      { path: 'users', name: 'UserList', component: UserList, meta: { permission: 'users' } },
      { path: 'users/new', name: 'UserNew', component: UserForm, meta: { permission: 'users' } },
      { path: 'users/:id/edit', name: 'UserEdit', component: UserForm, meta: { permission: 'users' } },
      { path: 'info-access', name: 'InfoCategoryList', component: InfoCategoryList, meta: { permission: 'info_access' } },
      { path: 'info-access/new', name: 'InfoCategoryNew', component: InfoCategoryForm, meta: { permission: 'info_access' } },
      { path: 'info-access/:id/edit', name: 'InfoCategoryEdit', component: InfoCategoryForm, meta: { permission: 'info_access' } },
      { path: 'info-documents', name: 'InfoDocumentList', component: InfoDocumentList, meta: { permission: 'info_access' } },
      { path: 'info-documents/new', name: 'InfoDocumentNew', component: InfoDocumentForm, meta: { permission: 'info_access' } },
      { path: 'info-documents/:id/edit', name: 'InfoDocumentEdit', component: InfoDocumentForm, meta: { permission: 'info_access' } },
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
  } else if (to.meta.permission && !auth.hasPermission(to.meta.permission)) {
    next('/')
  } else {
    next()
  }
})

export default router
