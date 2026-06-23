<template>
  <div class="categories-page">
    <div class="page-header">
      <div>
        <h1>Categorias de Acesso à Informação</h1>
        <p class="subtitle">Gerencie as categorias de documentos</p>
      </div>
      <router-link v-if="canAccess('info_access')" to="/info-access/new" class="btn-primary">
        <Plus :size="18" /> Nova categoria
      </router-link>
    </div>

    <div class="filters-bar">
      <div class="search-box">
        <Search :size="18" />
        <input v-model="search" type="text" placeholder="Buscar por nome..." @input="debouncedSearch" />
      </div>
    </div>

    <div v-if="loading" class="loading">Carregando categorias...</div>

    <div v-else class="table-wrapper">
      <table class="data-table">
        <thead>
          <tr>
            <th>Nome</th>
            <th>Slug</th>
            <th>Descrição</th>
            <th>Ícone</th>
            <th>Ordem</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="category in categories" :key="category.id">
            <td>{{ category.name }}</td>
            <td><code>{{ category.slug }}</code></td>
            <td>{{ category.description || '—' }}</td>
            <td><code>{{ category.icon || '—' }}</code></td>
            <td>{{ category.sort_order }}</td>
            <td class="actions">
              <router-link v-if="canAccess('info_access')" :to="`/info-access/${category.id}/edit`" class="btn-icon" title="Editar">
                <Pencil :size="16" />
              </router-link>
              <button v-if="canAccess('info_access')" class="btn-icon btn-danger" title="Excluir" @click="confirmDelete(category)">
                <Trash2 :size="16" />
              </button>
            </td>
          </tr>
          <tr v-if="categories.length === 0">
            <td colspan="6" class="empty-row">Nenhuma categoria encontrada</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="showDeleteModal" class="modal-overlay" @click="showDeleteModal = false">
      <div class="modal" @click.stop>
        <h3>Excluir categoria</h3>
        <p>Tem certeza que deseja excluir a categoria <strong>{{ deleteTarget?.name }}</strong>?</p>
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
import { Plus, Search, Pencil, Trash2 } from 'lucide-vue-next'
import { canAccess } from '@/utils/permissions'
import api from '@/services/api'

const categories = ref([])
const loading = ref(true)
const search = ref('')
const showDeleteModal = ref(false)
const deleteTarget = ref(null)
const deleting = ref(false)

let searchTimeout = null

function debouncedSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => loadCategories(), 300)
}

async function loadCategories() {
  loading.value = true
  try {
    const params = {}
    if (search.value) params.search = search.value
    const { data } = await api.get('/api/info-categories/all', { params })
    categories.value = data.items
  } catch (err) {
    console.error('Erro ao carregar categorias:', err)
  } finally {
    loading.value = false
  }
}

function confirmDelete(category) {
  deleteTarget.value = category
  showDeleteModal.value = true
}

async function handleDelete() {
  if (!deleteTarget.value) return
  deleting.value = true
  try {
    await api.delete(`/api/info-categories/${deleteTarget.value.id}`)
    showDeleteModal.value = false
    deleteTarget.value = null
    await loadCategories()
  } catch (err) {
    console.error('Erro ao excluir categoria:', err)
  } finally {
    deleting.value = false
  }
}

onMounted(loadCategories)
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
.data-table code {
  background: #f1f5f9;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
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
