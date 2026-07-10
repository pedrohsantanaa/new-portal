<template>
  <div class="sale-items-page">
    <div class="page-header">
      <div>
        <h1>Vendas Diretas</h1>
        <p class="subtitle">Gerencie imóveis e veículos disponíveis para venda</p>
      </div>
      <router-link v-if="canAccess('settings')" to="/sale-items/new" class="btn-primary">
        <Plus :size="18" /> Novo item
      </router-link>
    </div>

    <div class="filters-bar">
      <div class="filter-tabs">
        <button :class="{ active: filterType === '' }" @click="filterType = ''; loadItems()">Todos</button>
        <button :class="{ active: filterType === 'imovel' }" @click="filterType = 'imovel'; loadItems()">Imóveis</button>
        <button :class="{ active: filterType === 'veiculo' }" @click="filterType = 'veiculo'; loadItems()">Veículos</button>
      </div>
      <div class="search-box">
        <Search :size="18" />
        <input v-model="search" type="text" placeholder="Buscar por título ou cidade..." @input="debouncedSearch" />
      </div>
    </div>

    <div v-if="loading" class="loading">Carregando itens...</div>

    <div v-else class="table-wrapper">
      <table class="data-table">
        <thead>
          <tr>
            <th>Tipo</th>
            <th>Título</th>
            <th>Cidade</th>
            <th>Preço</th>
            <th>Destaque</th>
            <th>Status</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td>
              <span class="type-badge" :class="item.item_type === 'imovel' ? 'badge-blue' : 'badge-green'">
                {{ item.item_type === 'imovel' ? 'Imóvel' : 'Veículo' }}
              </span>
            </td>
            <td>{{ item.title }}</td>
            <td>{{ item.city || '—' }}</td>
            <td>R$ {{ formatPrice(item.price) }}</td>
            <td>
              <span class="badge" :class="item.featured ? 'badge-warning' : 'badge-muted'">
                {{ item.featured ? 'Sim' : 'Não' }}
              </span>
            </td>
            <td>
              <span class="badge" :class="item.active ? 'badge-success' : 'badge-muted'">
                {{ item.active ? 'Ativo' : 'Inativo' }}
              </span>
            </td>
            <td class="actions">
              <router-link v-if="canAccess('settings')" :to="`/sale-items/${item.id}/edit`" class="btn-icon" title="Editar">
                <Pencil :size="16" />
              </router-link>
              <button v-if="canAccess('settings')" class="btn-icon btn-danger" title="Excluir" @click="confirmDelete(item)">
                <Trash2 :size="16" />
              </button>
            </td>
          </tr>
          <tr v-if="items.length === 0">
            <td colspan="7" class="empty-row">Nenhum item encontrado</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="totalPages > 1" class="pagination">
      <button :disabled="currentPage <= 1" @click="goToPage(currentPage - 1)">Anterior</button>
      <span>Página {{ currentPage }} de {{ totalPages }}</span>
      <button :disabled="currentPage >= totalPages" @click="goToPage(currentPage + 1)">Próxima</button>
    </div>

    <div v-if="showDeleteModal" class="modal-overlay" @click="showDeleteModal = false">
      <div class="modal" @click.stop>
        <h3>Excluir item</h3>
        <p>Tem certeza que deseja excluir <strong>{{ deleteTarget?.title }}</strong>?</p>
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

const items = ref([])
const loading = ref(true)
const search = ref('')
const filterType = ref('')
const currentPage = ref(1)
const totalPages = ref(1)
const showDeleteModal = ref(false)
const deleteTarget = ref(null)
const deleting = ref(false)

let searchTimeout = null

function debouncedSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => { currentPage.value = 1; loadItems() }, 300)
}

function formatPrice(value) {
  return new Intl.NumberFormat('pt-BR', { minimumFractionDigits: 2 }).format(value)
}

async function loadItems() {
  loading.value = true
  try {
    const params = { page: currentPage.value, limit: 20 }
    if (filterType.value) params.item_type = filterType.value
    if (search.value) params.search = search.value
    const { data } = await api.get('/api/sale-items/', { params })
    items.value = data.items
    totalPages.value = data.pages
  } catch (err) {
  } finally {
    loading.value = false
  }
}

function goToPage(page) {
  currentPage.value = page
  loadItems()
}

function confirmDelete(item) {
  deleteTarget.value = item
  showDeleteModal.value = true
}

async function handleDelete() {
  if (!deleteTarget.value) return
  deleting.value = true
  try {
    await api.delete(`/api/sale-items/${deleteTarget.value.id}`)
    showDeleteModal.value = false
    deleteTarget.value = null
    await loadItems()
  } catch (err) {
  } finally {
    deleting.value = false
  }
}

onMounted(loadItems)
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
.btn-primary:hover { background: #0a2d6a; }
.filters-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  align-items: center;
}
.filter-tabs {
  display: flex;
  gap: 4px;
  background: #f1f5f9;
  border-radius: 8px;
  padding: 4px;
}
.filter-tabs button {
  padding: 6px 16px;
  border: none;
  border-radius: 6px;
  background: transparent;
  font-size: 13px;
  font-weight: 500;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}
.filter-tabs button.active {
  background: white;
  color: #1e293b;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
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
.loading { text-align: center; padding: 40px; color: #64748b; }
.table-wrapper {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}
.data-table { width: 100%; border-collapse: collapse; }
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
.data-table tr:hover td { background: #f8fafc; }
.type-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}
.badge-blue { background: #dbeafe; color: #1e40af; }
.badge-green { background: #dcfce7; color: #166534; }
.badge { display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 500; }
.badge-success { background: #dcfce7; color: #166534; }
.badge-warning { background: #fef3c7; color: #92400e; }
.badge-muted { background: #f1f5f9; color: #64748b; }
.actions { display: flex; gap: 8px; }
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
.btn-icon:hover { background: #f8fafc; color: #1e293b; border-color: #cbd5e1; }
.btn-danger:hover { background: #fef2f2; color: #dc2626; border-color: #fecaca; }
.empty-row { text-align: center; color: #94a3b8; padding: 32px 16px !important; }
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 20px;
  font-size: 14px;
  color: #64748b;
}
.pagination button {
  padding: 8px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: white;
  color: #475569;
  font-size: 14px;
  cursor: pointer;
}
.pagination button:hover { background: #f8fafc; }
.pagination button:disabled { opacity: 0.5; cursor: not-allowed; }
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
.modal h3 { margin: 0 0 12px; font-size: 18px; font-weight: 600; color: #1e293b; }
.modal p { margin: 0 0 8px; color: #475569; font-size: 14px; }
.modal-warning { color: #94a3b8; font-size: 13px; }
.modal-actions { display: flex; gap: 12px; justify-content: flex-end; margin-top: 20px; }
.btn-cancel {
  padding: 8px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: white;
  color: #475569;
  font-size: 14px;
  cursor: pointer;
}
.btn-cancel:hover { background: #f8fafc; }
.btn-delete {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  background: #dc2626;
  color: white;
  font-size: 14px;
  cursor: pointer;
}
.btn-delete:hover { background: #b91c1c; }
.btn-delete:disabled { opacity: 0.6; cursor: not-allowed; }
</style>
