<template>
  <div class="document-form-page">
    <div class="form-top-actions">
      <button type="button" class="btn-cancel" @click="router.push('/info-documents')">Cancelar</button>
      <button type="button" class="btn-save" :disabled="saving || uploading" @click="handleSave">
        {{ saving ? 'Salvando...' : (isEdit ? 'Salvar alterações' : 'Criar documento') }}
      </button>
    </div>

    <div v-if="loading" class="loading">Carregando documento...</div>

    <div v-else class="form-layout">
      <div class="form-main">
        <div class="sidebar-card">
          <h3>Detalhes do documento</h3>

          <div class="field">
            <label>Título <span class="required">*</span></label>
            <input v-model="form.title" type="text" placeholder="Ex: Edital de Chamamento Nº 001/2026" required />
          </div>

          <div class="field">
            <label>Categoria <span class="required">*</span></label>
            <select v-model="form.category_id" required>
              <option value="">Selecione uma categoria</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
            </select>
          </div>

          <div class="field-row">
            <div class="field">
              <label>Ano <span class="required">*</span></label>
              <input v-model.number="form.year" type="number" min="2000" max="2099" required />
            </div>
            <div class="field">
              <label>Mês</label>
              <select v-model="form.month">
                <option :value="null">Todos</option>
                <option v-for="m in 12" :key="m" :value="m">{{ m }}</option>
              </select>
            </div>
          </div>

          <div class="field">
            <label>Arquivo <span class="required">*</span></label>
            <div
              class="file-dropzone"
              :class="{ active: dragActive, 'has-file': form.file_url }"
              @click="triggerFileInput"
              @dragover.prevent="dragActive = true"
              @dragleave="dragActive = false"
              @drop.prevent="handleDrop"
            >
              <template v-if="form.file_url">
                <div class="file-preview">
                  <File :size="24" />
                  <span class="file-name">{{ form.file_url.split('/').pop() }}</span>
                  <span class="file-type-badge" :class="'badge-' + form.file_type">{{ form.file_type?.toUpperCase() }}</span>
                  <button class="btn-remove" @click.stop="removeFile">✕</button>
                </div>
              </template>
              <template v-else>
                <Upload :size="32" />
                <p>Arraste o arquivo aqui ou <strong>clique para selecionar</strong></p>
                <span class="hint">PDF, XLSX ou CSV — Máximo 10MB</span>
              </template>
            </div>
            <input ref="fileInput" type="file" accept=".pdf,.xlsx,.csv" style="display:none" @change="onFileSelect" />
            <div v-if="uploading" class="upload-progress">Enviando arquivo...</div>
            <div v-if="uploadError" class="upload-error">{{ uploadError }}</div>
          </div>
        </div>
      </div>

      <div class="form-sidebar">
        <div class="sidebar-card">
          <h3>Publicação</h3>
          <div class="field-checkbox">
            <label>
              <input type="checkbox" v-model="form.is_highlight" />
              Documento em destaque
            </label>
            <span class="hint">Aparece na seção "Documentos em destaque"</span>
          </div>
          <div class="field-checkbox">
            <label>
              <input type="checkbox" v-model="form.published" />
              Publicado
            </label>
            <span class="hint">Documento visível no site</span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="error" class="error-message">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Upload, File } from 'lucide-vue-next'
import api from '@/services/api'

const router = useRouter()
const route = useRoute()

const isEdit = computed(() => !!route.params.id)
const loading = ref(false)
const saving = ref(false)
const uploading = ref(false)
const uploadError = ref('')
const error = ref('')
const dragActive = ref(false)
const fileInput = ref(null)
const categories = ref([])

const currentYear = new Date().getFullYear()
const currentMonth = new Date().getMonth() + 1

const form = ref({
  title: '',
  category_id: '',
  file_url: '',
  file_type: '',
  file_size: null,
  year: currentYear,
  month: currentMonth,
  is_highlight: false,
  published: false,
})

function triggerFileInput() {
  fileInput.value?.click()
}

function handleDrop(e) {
  dragActive.value = false
  const file = e.dataTransfer.files[0]
  if (file) uploadFile(file)
}

function onFileSelect(e) {
  const file = e.target.files[0]
  if (file) uploadFile(file)
}

async function uploadFile(file) {
  const allowedTypes = [
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'text/csv',
  ]
  if (!allowedTypes.includes(file.type)) {
    uploadError.value = 'Tipo de arquivo não permitido. Use PDF, XLSX ou CSV.'
    return
  }
  if (file.size > 10 * 1024 * 1024) {
    uploadError.value = 'Arquivo muito grande. Máximo 10MB.'
    return
  }

  uploading.value = true
  uploadError.value = ''

  try {
    const formData = new FormData()
    formData.append('file', file)
    const { data } = await api.post('/api/upload?folder=info-documents', formData)

    const typeMap = {
      'application/pdf': 'pdf',
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'xlsx',
      'text/csv': 'csv',
    }

    form.value.file_url = data.url
    form.value.file_type = typeMap[file.type] || file.name.split('.').pop()
    form.value.file_size = data.size
  } catch (err) {
    uploadError.value = err.response?.data?.detail || 'Erro ao fazer upload do arquivo.'
  } finally {
    uploading.value = false
  }
}

function removeFile() {
  form.value.file_url = ''
  form.value.file_type = ''
  form.value.file_size = null
  uploadError.value = ''
}

onMounted(async () => {
  try {
    const { data } = await api.get('/api/info-categories/all')
    categories.value = data.items
  } catch (err) {
  }

  if (isEdit.value) {
    loading.value = true
    try {
      const { data } = await api.get(`/api/info-documents/${route.params.id}`)
      form.value = {
        title: data.title,
        category_id: data.category_id,
        file_url: data.file_url,
        file_type: data.file_type,
        file_size: data.file_size,
        year: data.year,
        month: data.month,
        is_highlight: data.is_highlight,
        published: data.published,
      }
    } catch (err) {
      error.value = 'Erro ao carregar documento'
    } finally {
      loading.value = false
    }
  }
})

async function handleSave() {
  if (!form.value.title.trim()) {
    error.value = 'Título é obrigatório'
    return
  }
  if (!form.value.category_id) {
    error.value = 'Categoria é obrigatória'
    return
  }
  if (!form.value.file_url) {
    error.value = 'Arquivo é obrigatório'
    return
  }

  saving.value = true
  error.value = ''

  try {
    const payload = {
      title: form.value.title.trim(),
      category_id: Number(form.value.category_id),
      file_url: form.value.file_url,
      file_type: form.value.file_type,
      file_size: form.value.file_size,
      year: form.value.year,
      month: form.value.month,
      is_highlight: form.value.is_highlight,
      published: form.value.published,
    }

    if (isEdit.value) {
      await api.put(`/api/info-documents/${route.params.id}`, payload)
    } else {
      await api.post('/api/info-documents/', payload)
    }
    router.push('/info-documents')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erro ao salvar documento'
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.form-top-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-bottom: 24px;
}
.btn-cancel {
  padding: 10px 20px;
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
.btn-save {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  background: #011a4f;
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
}
.btn-save:hover {
  background: #0a2d6a;
}
.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.loading {
  text-align: center;
  padding: 40px;
  color: #64748b;
}
.form-layout {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 24px;
}
.sidebar-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}
.sidebar-card h3 {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 20px;
}
.field {
  margin-bottom: 16px;
}
.field label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: #475569;
  margin-bottom: 6px;
}
.field input[type="text"],
.field input[type="number"],
.field textarea,
.field select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  color: #1e293b;
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
}
.field input:focus,
.field textarea:focus,
.field select:focus {
  border-color: #011a4f;
}
.field-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}
.required {
  color: #dc2626;
}
.hint {
  display: block;
  font-size: 12px;
  color: #94a3b8;
  margin-top: 4px;
}
.field-checkbox {
  margin-bottom: 16px;
}
.field-checkbox label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #475569;
  cursor: pointer;
}
.field-checkbox input[type="checkbox"] {
  width: 16px;
  height: 16px;
  accent-color: #011a4f;
}
.file-dropzone {
  border: 2px dashed #e2e8f0;
  border-radius: 12px;
  padding: 32px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  color: #64748b;
}
.file-dropzone:hover,
.file-dropzone.active {
  border-color: #011a4f;
  background: #f8fafc;
}
.file-dropzone.has-file {
  border-color: #16a34a;
  background: #f0fdf4;
  padding: 16px;
}
.file-dropzone p {
  margin: 8px 0 4px;
  font-size: 14px;
}
.file-preview {
  display: flex;
  align-items: center;
  gap: 12px;
}
.file-name {
  flex: 1;
  text-align: left;
  font-size: 14px;
  color: #1e293b;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.file-type-badge {
  padding: 2px 8px;
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
.btn-remove {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  font-size: 16px;
  padding: 4px;
}
.btn-remove:hover {
  color: #dc2626;
}
.upload-progress {
  margin-top: 8px;
  font-size: 13px;
  color: #083ea8;
}
.upload-error {
  margin-top: 8px;
  font-size: 13px;
  color: #dc2626;
}
.error-message {
  margin-top: 16px;
  padding: 12px 16px;
  background: #fef2f2;
  color: #dc2626;
  border-radius: 8px;
  font-size: 14px;
}
.form-sidebar {
  position: sticky;
  top: 80px;
  align-self: start;
}
@media (max-width: 768px) {
  .form-layout {
    grid-template-columns: 1fr;
  }
  .form-sidebar {
    position: static;
  }
}
</style>
