<template>
  <div class="admin-layout" :class="{ 'sidebar-open': sidebarOpen }">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="logo">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          <span>Portal Institucional Fomento</span>
        </div>
      </div>

      <nav class="sidebar-nav">
        <router-link to="/" class="nav-item" @click="sidebarOpen = false">
          <LayoutDashboard :size="20" />
          <span>Dashboard</span>
        </router-link>

        <div class="nav-group">
          <button class="nav-item nav-group-toggle" :class="{ active: isContentActive }" @click="contentExpanded = !contentExpanded">
            <FolderOpen :size="20" />
            <span>Conteúdo</span>
            <ChevronDown :size="16" class="chevron" :class="{ rotated: contentExpanded }" />
          </button>
          <div class="nav-submenu" v-show="contentExpanded">
            <!-- <router-link to="/pages" class="nav-subitem" @click="sidebarOpen = false">Páginas</router-link> -->
            <router-link to="/news" class="nav-subitem" @click="sidebarOpen = false">Notícias</router-link>
            <!-- <router-link to="/events" class="nav-subitem" @click="sidebarOpen = false">Eventos</router-link> -->
            <!-- <router-link to="/publications" class="nav-subitem" @click="sidebarOpen = false">Publicações</router-link> -->
            <!-- <router-link to="/media" class="nav-subitem" @click="sidebarOpen = false">Mídia</router-link> -->
          </div>
        </div>

        <div class="nav-group">
          <button class="nav-item nav-group-toggle" :class="{ active: isUsersActive }" @click="usersExpanded = !usersExpanded">
            <Users :size="20" />
            <span>Usuários</span>
            <ChevronDown :size="16" class="chevron" :class="{ rotated: usersExpanded }" />
          </button>
          <div class="nav-submenu" v-show="usersExpanded">
            <router-link to="/users" class="nav-subitem" @click="sidebarOpen = false">Lista de usuários</router-link>
          </div>
        </div>

        <div class="nav-group">
          <button class="nav-item nav-group-toggle" :class="{ active: isCategoriesActive }" @click="categoriesExpanded = !categoriesExpanded">
            <Tag :size="20" />
            <span>Categorias</span>
            <ChevronDown :size="16" class="chevron" :class="{ rotated: categoriesExpanded }" />
          </button>
          <div class="nav-submenu" v-show="categoriesExpanded">
            <router-link to="/categories" class="nav-subitem" @click="sidebarOpen = false">Gerenciar</router-link>
          </div>
        </div>
<!-- 
        <router-link to="/menus" class="nav-item" @click="sidebarOpen = false">
          <Menu :size="20" />
          <span>Menus</span>
        </router-link> -->

        <div class="nav-group">
          <button class="nav-item nav-group-toggle" :class="{ active: isSettingsActive }" @click="settingsExpanded = !settingsExpanded">
            <Settings :size="20" />
            <span>Configurações</span>
            <ChevronDown :size="16" class="chevron" :class="{ rotated: settingsExpanded }" />
          </button>
          <div class="nav-submenu" v-show="settingsExpanded">
            <router-link to="/settings/general" class="nav-subitem" @click="sidebarOpen = false">Geral</router-link>
          </div>
        </div>
<!-- 
        <router-link to="/reports" class="nav-item" @click="sidebarOpen = false">
          <BarChart3 :size="20" />
          <span>Relatórios</span>
        </router-link> -->
      </nav>

      <div class="sidebar-footer">
        <div class="user-info" v-if="auth.user">
          <div class="user-avatar">{{ auth.user.email?.charAt(0).toUpperCase() || 'U' }}</div>
          <div class="user-details">
            <span class="user-name">{{ auth.user.email }}</span>
            <span class="user-role">Administrador</span>
          </div>
          <button class="btn-logout" @click="handleLogout" title="Sair">
            <LogOut :size="18" />
          </button>
        </div>
      </div>
    </aside>

    <!-- Overlay mobile -->
    <div class="sidebar-overlay" v-if="sidebarOpen" @click="sidebarOpen = false"></div>

    <!-- Main -->
    <div class="main-wrapper">
      <!-- Topbar -->
      <header class="topbar">
        <div class="topbar-left">
          <button class="btn-hamburger" @click="sidebarOpen = !sidebarOpen">
            <Menu :size="22" />
          </button>
          <nav class="breadcrumb">
            <router-link to="/" class="breadcrumb-item">Início</router-link>
            <template v-for="(crumb, i) in breadcrumbs" :key="i">
              <span class="breadcrumb-sep">&gt;</span>
              <router-link v-if="crumb.to" :to="crumb.to" class="breadcrumb-item">{{ crumb.label }}</router-link>
              <span v-else class="breadcrumb-item current">{{ crumb.label }}</span>
            </template>
          </nav>
        </div>
        <div class="topbar-right">
          <a href="/" target="_blank" class="btn-ver-site">
            Ver site <ExternalLink :size="14" />
          </a>
          <button class="btn-notification">
            <Bell :size="20" />
            <span class="notif-dot"></span>
          </button>
        </div>
      </header>

      <!-- Content -->
      <main class="main-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import {
  LayoutDashboard, FolderOpen, ChevronDown, Users, Tag, Menu,
  Settings, BarChart3, LogOut, ExternalLink, Bell
} from 'lucide-vue-next'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const sidebarOpen = ref(false)
const contentExpanded = ref(true)
const usersExpanded = ref(false)
const categoriesExpanded = ref(false)
const settingsExpanded = ref(false)

const isContentActive = computed(() => {
  const path = route.path
  return path.startsWith('/news') || path.startsWith('/pages') || path.startsWith('/events') || path.startsWith('/publications') || path.startsWith('/media')
})
const isUsersActive = computed(() => route.path.startsWith('/users'))
const isCategoriesActive = computed(() => route.path.startsWith('/categories'))
const isSettingsActive = computed(() => route.path.startsWith('/settings'))

const breadcrumbs = computed(() => {
  const crumbs = []
  const path = route.path
  if (path === '/') return crumbs
  if (path.startsWith('/news')) {
    crumbs.push({ label: 'Notícias', to: '/news' })
    if (path.includes('/new')) crumbs.push({ label: 'Nova notícia' })
    else if (path.includes('/edit')) crumbs.push({ label: 'Editar notícia' })
  } else if (path.startsWith('/credit-lines')) {
    crumbs.push({ label: 'Linhas de Crédito', to: '/credit-lines' })
    if (path.includes('/new')) crumbs.push({ label: 'Nova linha' })
    else if (path.includes('/edit')) crumbs.push({ label: 'Editar linha' })
  } else if (path.startsWith('/users')) {
    crumbs.push({ label: 'Usuários' })
  } else if (path.startsWith('/categories')) {
    crumbs.push({ label: 'Categorias' })
  } else if (path.startsWith('/settings')) {
    crumbs.push({ label: 'Configurações' })
  } else if (path.startsWith('/reports')) {
    crumbs.push({ label: 'Relatórios' })
  }
  return crumbs
})

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
}

/* SIDEBAR */
.sidebar {
  width: 260px;
  background: #011a4f;
  color: white;
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 100;
  transition: transform 0.3s ease;
}

.sidebar-header {
  padding: 20px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 16px;
  font-weight: 700;
}

.sidebar-nav {
  flex: 1;
  padding: 12px;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  width: 100%;
  border: none;
  background: none;
  text-align: left;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.nav-item.router-link-exact-active,
.nav-item.active {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  font-weight: 600;
}

.chevron {
  margin-left: auto;
  transition: transform 0.2s;
}

.chevron.rotated {
  transform: rotate(180deg);
}

.nav-submenu {
  padding-left: 20px;
}

.nav-subitem {
  display: block;
  padding: 8px 14px;
  border-radius: 6px;
  color: rgba(255, 255, 255, 0.6);
  font-size: 13px;
  transition: all 0.2s;
}

.nav-subitem:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.nav-subitem.router-link-exact-active {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  font-weight: 600;
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
  flex-shrink: 0;
}

.user-details {
  flex: 1;
  min-width: 0;
}

.user-name {
  display: block;
  font-size: 13px;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  display: block;
  font-size: 11px;
  color: rgba(255, 255, 255, 0.5);
}

.btn-logout {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  padding: 6px;
  border-radius: 6px;
  transition: all 0.2s;
}

.btn-logout:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

/* OVERLAY */
.sidebar-overlay {
  display: none;
}

/* MAIN */
.main-wrapper {
  flex: 1;
  margin-left: 260px;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* TOPBAR */
.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 32px;
  background: white;
  border-bottom: 1px solid #e2e8f0;
  position: sticky;
  top: 0;
  z-index: 50;
}

.topbar-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.btn-hamburger {
  display: none;
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 4px;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.breadcrumb-item {
  color: #64748b;
}

.breadcrumb-item.current {
  color: #1e293b;
  font-weight: 500;
}

.breadcrumb-sep {
  color: #cbd5e1;
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.btn-ver-site {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: white;
  color: #1e293b;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-ver-site:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.btn-notification {
  position: relative;
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 6px;
}

.notif-dot {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 8px;
  height: 8px;
  background: #dc2626;
  border-radius: 50%;
}

/* CONTENT */
.main-content {
  flex: 1;
  padding: 32px;
  background: #f1f5f9;
}

/* RESPONSIVE */
@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
  }

  .sidebar-open .sidebar {
    transform: translateX(0);
  }

  .sidebar-overlay {
    display: block;
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: 90;
  }

  .main-wrapper {
    margin-left: 0;
  }

  .btn-hamburger {
    display: flex;
  }

  .main-content {
    padding: 16px;
  }

  .topbar {
    padding: 12px 16px;
  }
}
</style>
