<template>
  <div class="page">
    <div class="page-header">
      <h1>Linhas de Crédito</h1>
      <router-link v-if="canAccess('credit_lines')" to="/credit-lines/new" class="btn-primary">Nova Linha</router-link>
    </div>

    <div v-if="loading" class="loading">Carregando...</div>

    <div v-else class="table-wrapper">
      <table class="data-table">
        <thead>
          <tr>
            <th>Título</th>
            <th>Cor</th>
            <th>Ordem</th>
            <th>Status</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in creditLines" :key="item.id">
            <td>{{ item.title }}</td>
            <td>
              <span class="color-dot" :style="{ background: item.color }"></span>
            </td>
            <td>{{ item.order }}</td>
            <td>
              <span :class="['badge', item.active ? 'active' : 'inactive']">
                {{ item.active ? 'Ativo' : 'Inativo' }}
              </span>
            </td>
            <td class="actions">
              <router-link v-if="canAccess('credit_lines')" :to="`/credit-lines/${item.id}/edit`" class="btn-edit">Editar</router-link>
              <button v-if="canAccess('credit_lines')" @click="handleDelete(item.id)" class="btn-delete">Excluir</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'
import { canAccess } from '@/utils/permissions'

const creditLines = ref([])
const loading = ref(true)

async function loadCreditLines() {
  loading.value = true
  try {
    const { data } = await api.get('/api/credit-lines/?limit=50')
    creditLines.value = data.items
  } catch (e) {
    console.error('Erro ao carregar linhas', e)
  } finally {
    loading.value = false
  }
}

async function handleDelete(id) {
  if (!confirm('Tem certeza que deseja excluir esta linha de crédito?')) return
  try {
    await api.delete(`/api/credit-lines/${id}`)
    await loadCreditLines()
  } catch (e) {
    alert('Erro ao excluir linha de crédito')
  }
}

onMounted(loadCreditLines)
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-header h1 {
  color: #011a4f;
}

.btn-primary {
  background: #011a4f;
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
}

.btn-primary:hover {
  background: #083ea8;
}

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
  background: #f8fafc;
  padding: 14px 16px;
  text-align: left;
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
}

.data-table td {
  padding: 14px 16px;
  border-top: 1px solid #e2e8f0;
}

.color-dot {
  display: inline-block;
  width: 24px;
  height: 24px;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
}

.badge {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.badge.active {
  background: #dcfce7;
  color: #16a34a;
}

.badge.inactive {
  background: #fef2f2;
  color: #dc2626;
}

.actions {
  display: flex;
  gap: 8px;
}

.btn-edit {
  padding: 6px 12px;
  background: #e2e8f0;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
}

.btn-edit:hover {
  background: #cbd5e1;
}

.btn-delete {
  padding: 6px 12px;
  background: #fef2f2;
  color: #dc2626;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
}

.btn-delete:hover {
  background: #fee2e2;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #64748b;
}
</style>
