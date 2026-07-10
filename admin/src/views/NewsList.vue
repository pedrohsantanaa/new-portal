<template>
  <div class="news-list-page">
    <!-- Header -->
    <div class="page-header">
      <div>
        <h1>Notícias</h1>
        <p class="subtitle">Gerencie todas as notícias do portal</p>
      </div>
      <router-link v-if="canAccess('news')" to="/news/new" class="btn-primary">
        <Plus :size="18" /> Nova notícia
      </router-link>
    </div>

    <!-- Filtros -->
    <div class="filters-bar">
      <div class="search-box">
        <Search :size="18" />
        <input v-model="search" type="text" placeholder="Buscar por título..." @input="debouncedSearch" />
      </div>
      <select v-model="filterCategory" @change="loadNews(1)">
        <option value="">Todas as categorias</option>
        <option v-for="cat in categories" :key="cat.id" :value="cat.name">{{ cat.name }}</option>
      </select>
      <select v-model="filterStatus" @change="loadNews(1)">
        <option value="">Todos os status</option>
        <option value="published">Publicada</option>
        <option value="draft">Rascunho</option>
      </select>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading">Carregando notícias...</div>

    <!-- Tabela -->
    <div v-else class="table-wrapper">
      <table class="data-table">
        <thead>
          <tr>
            <th>Título</th>
            <th>Categoria</th>
            <th>Autor</th>
            <th>Status</th>
            <th>Data de publicação</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="news.length === 0">
            <td colspan="6" class="empty-row">Nenhuma notícia encontrada.</td>
          </tr>
          <tr v-for="item in news" :key="item.id">
            <td class="td-title">{{ item.title }}</td>
            <td><span class="badge-category">{{ item.category }}</span></td>
            <td>{{ item.author || '—' }}</td>
            <td>
              <span :class="['badge-status', item.published ? 'published' : 'draft']">
                {{ item.published ? 'Publicada' : 'Rascunho' }}
              </span>
            </td>
            <td>{{ formatDate(item.published_at || item.created_at) }}</td>
            <td class="td-actions">
              <router-link v-if="canAccess('news')" :to="`/news/${item.slug}/edit`" class="btn-action btn-edit" title="Editar">
                <Pencil :size="15" />
              </router-link>
              <a :href="`/noticias/${item.slug}`" target="_blank" class="btn-action btn-view" title="Visualizar" v-if="item.published">
                <ExternalLink :size="15" />
              </a>
              <button v-if="canAccess('news')" class="btn-action btn-delete" @click="handleDelete(item)" title="Excluir">
                <Trash2 :size="15" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Paginação -->
    <div v-if="totalPages > 1" class="pagination">
      <button class="page-btn" :disabled="currentPage <= 1" @click="loadNews(currentPage - 1)">
        ← Anterior
      </button>
      <div class="page-numbers">
        <button
          v-for="p in visiblePages"
          :key="p"
          :class="['page-num', { active: p === currentPage }]"
          @click="loadNews(p)"
        >{{ p }}</button>
      </div>
      <button class="page-btn" :disabled="currentPage >= totalPages" @click="loadNews(currentPage + 1)">
        Próxima →
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'
import { canAccess } from '@/utils/permissions'
import { Plus, Search, Pencil, ExternalLink, Trash2 } from 'lucide-vue-next'

const news = ref([])
const categories = ref([])
const loading = ref(true)
const currentPage = ref(1)
const totalPages = ref(1)
const totalItems = ref(0)
const search = ref('')
const filterCategory = ref('')
const filterStatus = ref('')
const limit = 10

let searchTimeout = null

const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, currentPage.value - 2)
  const end = Math.min(totalPages.value, start + 4)
  for (let i = start; i <= end; i++) pages.push(i)
  return pages
})

function debouncedSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => loadNews(1), 300)
}

async function loadNews(page = 1) {
  loading.value = true
  currentPage.value = page
  try {
    const params = { page, limit }
    if (search.value) params.search = search.value
    if (filterCategory.value) params.category = filterCategory.value
    if (filterStatus.value === 'published') params.published_only = true
    const { data } = await api.get('/api/news/', { params })
    news.value = data.items
    totalPages.value = data.pages
    totalItems.value = data.total
  } catch (e) {
  } finally {
    loading.value = false
  }
}

async function handleDelete(item) {
  if (!confirm(`Tem certeza que deseja excluir "${item.title}"?`)) return
  try {
    await api.delete(`/api/news/${item.id}`)
    await loadNews(currentPage.value)
  } catch {
    alert('Erro ao excluir notícia')
  }
}

function formatDate(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

onMounted(async () => {
  try {
    const { data } = await api.get('/api/categories/')
    categories.value = data
  } catch (err) {
  }
  loadNews(1)
})
</script>

<style scoped>
.news-list-page {
  max-width: 1200px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.page-header h1 {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
}

.subtitle {
  font-size: 14px;
  color: #64748b;
  margin-top: 4px;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: #083ea8;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  text-decoration: none;
}

.btn-primary:hover {
  background: #062d7a;
}

/* FILTERS */
.filters-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.search-box {
  flex: 1;
  min-width: 200px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 14px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
}

.search-box input {
  flex: 1;
  border: none;
  padding: 10px 0;
  font-size: 14px;
  outline: none;
  background: transparent;
}

.filters-bar select {
  padding: 10px 14px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  color: #1e293b;
  background: white;
  cursor: pointer;
}

.filters-bar select:focus {
  outline: none;
  border-color: #083ea8;
}

/* TABLE */
.table-wrapper {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  padding: 14px 16px;
  text-align: left;
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.data-table td {
  padding: 14px 16px;
  font-size: 14px;
  color: #334155;
  border-bottom: 1px solid #f1f5f9;
}

.data-table tr:last-child td {
  border-bottom: none;
}

.data-table tr:hover td {
  background: #f8fafc;
}

.td-title {
  font-weight: 600;
  color: #1e293b;
  max-width: 280px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.badge-category {
  display: inline-block;
  padding: 4px 10px;
  background: #eff6ff;
  color: #083ea8;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.badge-status {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.badge-status.published {
  background: #f0fdf4;
  color: #16a34a;
}

.badge-status.draft {
  background: #fefce8;
  color: #ca8a04;
}

.td-actions {
  display: flex;
  gap: 6px;
}

.btn-action {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  background: white;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
}

.btn-action:hover {
  background: #f1f5f9;
}

.btn-edit:hover {
  color: #083ea8;
  border-color: #083ea8;
}

.btn-view:hover {
  color: #16a34a;
  border-color: #16a34a;
}

.btn-delete:hover {
  color: #dc2626;
  border-color: #dc2626;
  background: #fef2f2;
}

.empty-row {
  text-align: center;
  padding: 40px 16px !important;
  color: #94a3b8;
}

/* LOADING */
.loading {
  text-align: center;
  padding: 60px 20px;
  color: #64748b;
  font-size: 15px;
}

/* PAGINATION */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  margin-top: 24px;
}

.page-btn {
  padding: 8px 16px;
  border: 1px solid #e2e8f0;
  background: white;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #334155;
  cursor: pointer;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled) {
  border-color: #083ea8;
  color: #083ea8;
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-numbers {
  display: flex;
  gap: 4px;
}

.page-num {
  width: 36px;
  height: 36px;
  border: none;
  background: white;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}

.page-num:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.page-num.active {
  background: #083ea8;
  color: white;
}
</style>
