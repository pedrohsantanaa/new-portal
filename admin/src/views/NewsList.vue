<template>
  <div class="page">
    <div class="page-header">
      <h1>Notícias</h1>
      <router-link to="/news/new" class="btn-primary">Nova Notícia</router-link>
    </div>

    <div v-if="loading" class="loading">Carregando...</div>

    <div v-else class="table-wrapper">
      <table class="data-table">
        <thead>
          <tr>
            <th>Título</th>
            <th>Categoria</th>
            <th>Status</th>
            <th>Data</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in news" :key="item.id">
            <td>{{ item.title }}</td>
            <td>{{ item.category }}</td>
            <td>
              <span :class="['badge', item.published ? 'published' : 'draft']">
                {{ item.published ? 'Publicado' : 'Rascunho' }}
              </span>
            </td>
            <td>{{ formatDate(item.created_at) }}</td>
            <td class="actions">
              <router-link :to="`/news/${item.id}/edit`" class="btn-edit">Editar</router-link>
              <button @click="handleDelete(item.id)" class="btn-delete">Excluir</button>
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

const news = ref([])
const loading = ref(true)

async function loadNews() {
  loading.value = true
  try {
    const { data } = await api.get('/api/news/?limit=50')
    news.value = data.items
  } catch (e) {
    console.error('Erro ao carregar notícias', e)
  } finally {
    loading.value = false
  }
}

async function handleDelete(id) {
  if (!confirm('Tem certeza que deseja excluir esta notícia?')) return
  try {
    await api.delete(`/api/news/${id}`)
    await loadNews()
  } catch (e) {
    alert('Erro ao excluir notícia')
  }
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('pt-BR')
}

onMounted(loadNews)
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
  transition: background 0.2s;
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

.badge {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.badge.published {
  background: #dcfce7;
  color: #16a34a;
}

.badge.draft {
  background: #f1f5f9;
  color: #64748b;
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
