<template>
  <div class="carousel-page">
    <div class="page-header">
      <div>
        <h1>Carousel Hero</h1>
        <p class="subtitle">Gerencie os slides do banner principal</p>
      </div>
      <router-link v-if="canAccess('settings')" to="/carousel/new" class="btn-primary">
        <Plus :size="18" /> Novo slide
      </router-link>
    </div>

    <div v-if="loading" class="loading">Carregando slides...</div>

    <div v-else class="table-wrapper">
      <table class="data-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Imagem</th>
            <th>Título</th>
            <th>Botão</th>
            <th>Classe</th>
            <th>Status</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="slide in slides" :key="slide.id">
            <td>{{ slide.order }}</td>
            <td>
              <img :src="slide.image_url" class="thumb" :alt="slide.title || 'Slide'" />
            </td>
            <td>{{ slide.title || '—' }}</td>
            <td>{{ slide.btn_label || '—' }}</td>
            <td><code>{{ slide.btn_class }}</code></td>
            <td>
              <span class="badge" :class="slide.active ? 'badge-success' : 'badge-muted'">
                {{ slide.active ? 'Ativo' : 'Inativo' }}
              </span>
            </td>
            <td class="actions">
              <router-link v-if="canAccess('settings')" :to="`/carousel/${slide.id}/edit`" class="btn-icon" title="Editar">
                <Pencil :size="16" />
              </router-link>
              <button v-if="canAccess('settings')" class="btn-icon btn-danger" title="Excluir" @click="confirmDelete(slide)">
                <Trash2 :size="16" />
              </button>
            </td>
          </tr>
          <tr v-if="slides.length === 0">
            <td colspan="7" class="empty-row">Nenhum slide encontrado</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="showDeleteModal" class="modal-overlay" @click="showDeleteModal = false">
      <div class="modal" @click.stop>
        <h3>Excluir slide</h3>
        <p>Tem certeza que deseja excluir este slide?</p>
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
import { Plus, Pencil, Trash2 } from 'lucide-vue-next'
import { canAccess } from '@/utils/permissions'
import api from '@/services/api'

const slides = ref([])
const loading = ref(true)
const showDeleteModal = ref(false)
const deleteTarget = ref(null)
const deleting = ref(false)

async function loadSlides() {
  loading.value = true
  try {
    const { data } = await api.get('/api/carousel-slides/')
    slides.value = data.items
  } catch (err) {
    console.error('Erro ao carregar slides:', err)
  } finally {
    loading.value = false
  }
}

function confirmDelete(slide) {
  deleteTarget.value = slide
  showDeleteModal.value = true
}

async function handleDelete() {
  if (!deleteTarget.value) return
  deleting.value = true
  try {
    await api.delete(`/api/carousel-slides/${deleteTarget.value.id}`)
    showDeleteModal.value = false
    deleteTarget.value = null
    await loadSlides()
  } catch (err) {
    console.error('Erro ao excluir slide:', err)
  } finally {
    deleting.value = false
  }
}

onMounted(loadSlides)
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
.thumb {
  width: 80px;
  height: 45px;
  object-fit: cover;
  border-radius: 6px;
}
.data-table code {
  background: #f1f5f9;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
  color: #64748b;
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
