<template>
  <div class="documents-page">
    <div class="page-header">
      <div>
        <h1>Documentos</h1>
        <p class="subtitle">Gerencie os documentos do Acesso à Informação</p>
      </div>
      <router-link v-if="canAccess('info_access')" to="/info-documents/new" class="btn-primary">
        <Plus :size="18" /> Novo documento
      </router-link>
    </div>

    <div class="filters-bar">
      <div class="search-box">
        <Search :size="18" />
        <input v-model="search" type="text" placeholder="Buscar por título..." @input="debouncedSearch" />
      </div>
      <select v-model="filterCategory" @change="loadDocuments" class="filter-select">
        <option value="">Todas as categorias</option>
        <option v-for="cat in allCategories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
      </select>
      <select v-model="filterYear" @change="loadDocuments" class="filter-select filter-year">
        <option value="">Todos os anos</option>
        <option v-for="year in years" :key="year" :value="year">{{ year }}</option>
      </select>
    </div>

    <div v-if="loading" class="loading">Carregando documentos...</div>

    <div v-else class="table-wrapper">
      <table class="data-table">
        <thead>
          <tr>
            <th>Título</th>
            <th>Categoria</th>
            <th>Tipo</th>
            <th>Ano/Mês</th>
            <th>Destaque</th>
            <th>Status</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="doc in documents" :key="doc.id">
            <td class="title-cell">{{ doc.title }}</td>
            <td>{{ doc.category_name || '—' }}</td>
            <td>
              <span class="badge-type" :class="'badge-' + doc.file_type">
                {{ doc.file_type.toUpperCase() }}
              </span>
            </td>
            <td>{{ doc.year }}{{ doc.month ? '/' + String(doc.month).padStart(2, '0') : '' }}</td>
            <td>
              <span class="badge" :class="doc.is_highlight ? 'badge-warning' : 'badge-muted'">
                {{ doc.is_highlight ? 'Sim' : 'Não' }}
              </span>
            </td>
            <td>
              <span class="badge" :class="doc.published ? 'badge-success' : 'badge-muted'">
                {{ doc.published ? 'Publicado' : 'Rascunho' }}
              </span>
            </td>
            <td class="actions">
              <a :href="doc.file_url" target="_blank" class="btn-icon" title="Visualizar">
                <Eye :size="16" />
              </a>
              <router-link v-if="canAccess('info_access')" :to="`/info-documents/${doc.id}/edit`" class="btn-icon" title="Editar">
                <Pencil :size="16" />
              </router-link>
              <button v-if="canAccess('info_access')" class="btn-icon btn-danger" title="Excluir" @click="confirmDelete(doc)">
                <Trash2 :size="16" />
              </button>
            </td>
          </tr>
          <tr v-if="documents.length === 0">
            <td colspan="7" class="empty-row">Nenhum documento encontrado</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="totalPages > 1" class="pagination">
      <button class="page-btn" :disabled="currentPage <= 1" @click="goToPage(currentPage - 1)">Anterior</button>
      <span class="page-info">Página {{ currentPage }} de {{ totalPages }}</span>
      <button class="page-btn" :disabled="currentPage >= totalPages" @click="goToPage(currentPage + 1)">Próxima</button>
    </div>

    <div v-if="showDeleteModal" class="modal-overlay" @click="showDeleteModal = false">
      <div class="modal" @click.stop>
        <h3>Excluir documento</h3>
        <p>Tem certeza que deseja excluir o documento <strong>{{ deleteTarget?.title }}</strong>?</p>
        <p class="modal-warning">Esta ação não pode ser desfeita.</p>
        <div class="modal-actions">
          <button class="btn-cancel" @click="showDeleteModal = false">Cancelar</button>
          <button class="btn-delete" @click="handleDelete" :disabled="deleting">
            {{ deleting ? 'Excluindo...' : 'Excluir' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus, Search, Pencil, Trash2, Eye } from 'lucide-vue-next'
import { canAccess } from '@/utils/permissions'
import api from '@/services/api'

const documents = ref([])
const allCategories = ref([])
const years = ref([])
const loading = ref(true)
const search = ref('')
const filterCategory = ref('')
const filterYear = ref('')
const currentPage = ref(1)
const totalPages = ref(1)
const showDeleteModal = ref(false)
const deleteTarget = ref(null)
const deleting = ref(false)

let searchTimeout = null

function debouncedSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => { currentPage.value = 1; loadDocuments() }, 300)
}

async function loadDocuments() {
  loading.value = true
  try {
    const params = { page: currentPage.value, limit: 20 }
    if (search.value) params.search = search.value
    if (filterCategory.value) params.category_id = filterCategory.value
    if (filterYear.value) params.year = filterYear.value
    const { data } = await api.get('/api/info-documents/all', { params })
    documents.value = data.items
    totalPages.value = data.pages
  } catch (err) {
  } finally {
    loading.value = false
  }
}

async function loadFilters() {
  try {
    const [catsRes, yearsRes] = await Promise.all([
      api.get('/api/info-categories/all'),
      api.get('/api/info-documents/years'),
    ])
    allCategories.value = catsRes.data.items
    years.value = yearsRes.data.years
  } catch (err) {
  }
}

function goToPage(page) {
  currentPage.value = page
  loadDocuments()
}

function confirmDelete(doc) {
  deleteTarget.value = doc
  showDeleteModal.value = true
}

async function handleDelete() {
  if (!deleteTarget.value) return
  deleting.value = true
  try {
    await api.delete(`/api/info-documents/${deleteTarget.value.id}`)
    showDeleteModal.value = false
    deleteTarget.value = null
    await loadDocuments()
  } catch (err) {
  } finally {
    deleting.value = false
  }
}

onMounted(() => {
  loadFilters()
  loadDocuments()
})
</script>

<style scoped>
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
  margin: 0;
}
.subtitle {
  color: #64748b;
  font-size: 14px;
  margin: 4px 0 0;
}
.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: #011a4f;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  text-decoration: none;
  transition: background 0.2s;
}
.btn-primary:hover {
  background: #0a2d6a;
}
.filters-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}
.search-box {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  flex: 1;
  max-width: 400px;
}
.search-box input {
  border: none;
  outline: none;
  font-size: 14px;
  width: 100%;
  background: transparent;
}
.filter-select {
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  color: #475569;
  background: white;
  cursor: pointer;
}
.filter-year {
  width: 120px;
}
.loading {
  text-align: center;
  padding: 40px;
  color: #64748b;
}
.table-wrapper {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}
.data-table {
  width: 100%;
  border-collapse: collapse;
}
.data-table th {
  text-align: left;
  padding: 12px 16px;
  background: #f8fafc;
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.data-table td {
  padding: 14px 16px;
  border-top: 1px solid #f1f5f9;
  font-size: 14px;
  color: #334155;
}
.data-table tr:hover td {
  background: #f8fafc;
}
.title-cell {
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.badge-type {
  display: inline-block;
  padding: 3px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
}
.badge-pdf {
  background: #fef2f2;
  color: #dc2626;
}
.badge-xlsx {
  background: #dcfce7;
  color: #166534;
}
.badge-csv {
  background: #dbeafe;
  color: #1e40af;
}
.badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}
.badge-success {
  background: #dcfce7;
  color: #166534;
}
.badge-warning {
  background: #fef3c7;
  color: #92400e;
}
.badge-muted {
  background: #f1f5f9;
  color: #64748b;
}
.actions {
  display: flex;
  gap: 8px;
}
.btn-icon {
  display: inline-flex;
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
.btn-icon:hover {
  background: #f8fafc;
  color: #1e293b;
  border-color: #cbd5e1;
}
.btn-danger:hover {
  background: #fef2f2;
  color: #dc2626;
  border-color: #fecaca;
}
.empty-row {
  text-align: center;
  color: #94a3b8;
  padding: 32px 16px !important;
}
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-top: 20px;
}
.page-btn {
  padding: 8px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: white;
  color: #475569;
  font-size: 14px;
  cursor: pointer;
}
.page-btn:hover:not(:disabled) {
  background: #f8fafc;
}
.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.page-info {
  font-size: 14px;
  color: #64748b;
}
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 200;
}
.modal {
  background: white;
  border-radius: 12px;
  padding: 24px;
  width: 100%;
  max-width: 420px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}
.modal h3 {
  margin: 0 0 12px;
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
}
.modal p {
  margin: 0 0 8px;
  color: #475569;
  font-size: 14px;
}
.modal-warning {
  color: #94a3b8;
  font-size: 13px;
}
.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 20px;
}
.btn-cancel {
  padding: 8px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: white;
  color: #475569;
  font-size: 14px;
  cursor: pointer;
}
.btn-cancel:hover {
  background: #f8fafc;
}
.btn-delete {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  background: #dc2626;
  color: white;
  font-size: 14px;
  cursor: pointer;
}
.btn-delete:hover {
  background: #b91c1c;
}
.btn-delete:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
