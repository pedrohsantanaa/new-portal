<template>
  <div class="users-page">
    <div class="page-header">
      <div>
        <h1>Usuários</h1>
        <p class="subtitle">Gerencie os usuários do painel administrativo</p>
      </div>
      <router-link v-if="canAccess('users')" to="/users/new" class="btn-primary">
        <Plus :size="18" /> Novo usuário
      </router-link>
    </div>

    <div class="filters-bar">
      <div class="search-box">
        <Search :size="18" />
        <input v-model="search" type="text" placeholder="Buscar por nome ou e-mail..." @input="debouncedSearch" />
      </div>
    </div>

    <div v-if="loading" class="loading">Carregando usuários...</div>

    <div v-else class="table-wrapper">
      <table class="data-table">
        <thead>
          <tr>
            <th>Nome</th>
            <th>E-mail</th>
            <th>Status</th>
            <th>Permissões</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.name || '—' }}</td>
            <td>{{ user.email }}</td>
            <td>
              <span class="badge" :class="user.is_active ? 'badge-success' : 'badge-muted'">
                {{ user.is_active ? 'Ativo' : 'Inativo' }}
              </span>
            </td>
            <td>
              <div class="permission-tags">
                <span v-for="perm in user.permissions" :key="perm.id" class="perm-tag">
                  {{ perm.name }}
                </span>
                <span v-if="user.permissions.length === 0" class="no-perms">Nenhuma</span>
              </div>
            </td>
            <td class="actions">
              <router-link v-if="canAccess('users')" :to="`/users/${user.id}/edit`" class="btn-icon" title="Editar">
                <Pencil :size="16" />
              </router-link>
              <button v-if="canAccess('users')" class="btn-icon btn-danger" title="Excluir" @click="confirmDelete(user)" :disabled="user.id === currentUserId">
                <Trash2 :size="16" />
              </button>
            </td>
          </tr>
          <tr v-if="users.length === 0">
            <td colspan="5" class="empty-row">Nenhum usuário encontrado</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="showDeleteModal" class="modal-overlay" @click="showDeleteModal = false">
      <div class="modal" @click.stop>
        <h3>Excluir usuário</h3>
        <p>Tem certeza que deseja excluir o usuário <strong>{{ deleteTarget?.email }}</strong>?</p>
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
import { ref, computed, onMounted } from 'vue'
import { Plus, Search, Pencil, Trash2 } from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'
import { canAccess } from '@/utils/permissions'
import api from '@/services/api'

const auth = useAuthStore()
const currentUserId = computed(() => auth.user?.id)

const users = ref([])
const loading = ref(true)
const search = ref('')
const showDeleteModal = ref(false)
const deleteTarget = ref(null)
const deleting = ref(false)

let searchTimeout = null

function debouncedSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => loadUsers(), 300)
}

async function loadUsers() {
  loading.value = true
  try {
    const params = { limit: 50 }
    if (search.value) params.search = search.value
    const { data } = await api.get('/api/users/', { params })
    users.value = data
  } catch (err) {
    console.error('Erro ao carregar usuários:', err)
  } finally {
    loading.value = false
  }
}

function confirmDelete(user) {
  deleteTarget.value = user
  showDeleteModal.value = true
}

async function handleDelete() {
  if (!deleteTarget.value) return
  deleting.value = true
  try {
    await api.delete(`/api/users/${deleteTarget.value.id}`)
    showDeleteModal.value = false
    deleteTarget.value = null
    await loadUsers()
  } catch (err) {
    console.error('Erro ao excluir usuário:', err)
  } finally {
    deleting.value = false
  }
}

onMounted(loadUsers)
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
.badge-muted {
  background: #f1f5f9;
  color: #64748b;
}
.permission-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}
.perm-tag {
  display: inline-block;
  padding: 2px 8px;
  background: #eff6ff;
  color: #1e40af;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 500;
}
.no-perms {
  color: #94a3b8;
  font-size: 13px;
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
.btn-icon:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
.btn-danger:hover:not(:disabled) {
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
