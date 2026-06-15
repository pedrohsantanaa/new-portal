<template>
  <div class="page">
    <div class="page-header">
      <h1>{{ isEdit ? 'Editar Notícia' : 'Nova Notícia' }}</h1>
      <router-link to="/news" class="btn-back">← Voltar</router-link>
    </div>

    <form @submit.prevent="handleSave" class="form-card">
      <div class="field">
        <label>Título</label>
        <input v-model="form.title" type="text" required />
      </div>

      <div class="field">
        <label>Categoria</label>
        <select v-model="form.category" required>
          <option value="">Selecione</option>
          <option value="Crédito">Crédito</option>
          <option value="Programa">Programa</option>
          <option value="Evento">Evento</option>
          <option value="Empreendedorismo">Empreendedorismo</option>
        </select>
      </div>

      <div class="field">
        <label>Resumo</label>
        <textarea v-model="form.summary" rows="2" required></textarea>
      </div>

      <div class="field">
        <label>Conteúdo</label>
        <textarea v-model="form.content" rows="10" required></textarea>
      </div>

      <!-- Upload de Imagem -->
      <div class="field">
        <label>Imagem da Notícia</label>

        <div class="image-upload-area" v-if="!imagePreview && !form.image_url">
          <input
            type="file"
            ref="fileInput"
            accept="image/jpeg,image/png,image/webp,image/gif"
            @change="handleFileSelect"
            class="file-input"
          />
          <div class="upload-placeholder" @click="$refs.fileInput.click()">
            <span class="upload-icon">📷</span>
            <span class="upload-text">Clique para enviar uma imagem</span>
            <span class="upload-hint">JPG, PNG ou WebP • Máx. 5MB</span>
          </div>
        </div>

        <!-- Preview da imagem -->
        <div v-if="imagePreview" class="image-preview">
          <img :src="imagePreview" alt="Preview" />
          <button type="button" class="remove-image" @click="removeImage">✕</button>
        </div>

        <!-- URL alternativa -->
        <div class="url-input">
          <input
            v-model="form.image_url"
            type="text"
            placeholder="Ou cole a URL da imagem aqui"
            @input="clearFileSelection"
          />
        </div>

        <!-- Erro de upload -->
        <div v-if="uploadError" class="upload-error">{{ uploadError }}</div>
      </div>

      <div class="field checkbox-field">
        <label>
          <input v-model="form.published" type="checkbox" />
          Publicar imediatamente
        </label>
      </div>

      <div class="form-actions">
        <button type="submit" class="btn-primary" :disabled="saving">
          {{ saving ? 'Salvando...' : 'Salvar' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => !!route.params.slug)
const currentNews = ref(null)
const saving = ref(false)

const form = ref({
  title: '',
  category: '',
  summary: '',
  content: '',
  image_url: '',
  published: false,
})

const selectedFile = ref(null)
const imagePreview = ref('')
const uploadError = ref('')
const fileInput = ref(null)

function handleFileSelect(event) {
  const file = event.target.files[0]
  if (!file) return

  uploadError.value = ''

  if (file.size > 5 * 1024 * 1024) {
    uploadError.value = 'Arquivo muito grande. Máximo: 5MB'
    return
  }

  const allowedTypes = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']
  if (!allowedTypes.includes(file.type)) {
    uploadError.value = 'Tipo de arquivo não permitido. Use JPG, PNG ou WebP'
    return
  }

  selectedFile.value = file
  imagePreview.value = URL.createObjectURL(file)
  form.value.image_url = ''
}

function removeImage() {
  selectedFile.value = null
  imagePreview.value = ''
  form.value.image_url = ''
  uploadError.value = ''
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

function clearFileSelection() {
  if (form.value.image_url) {
    selectedFile.value = null
    imagePreview.value = ''
  }
}

async function uploadImage() {
  if (!selectedFile.value) return form.value.image_url

  const formData = new FormData()
  formData.append('file', selectedFile.value)

  const { data } = await api.post('/api/upload/', formData, {
    params: { folder: 'news' },
    headers: { 'Content-Type': 'multipart/form-data' },
  })

  return data.url
}

onMounted(async () => {
  if (isEdit.value) {
    try {
      const { data } = await api.get(`/api/news/${route.params.slug}`)
      currentNews.value = data
      form.value = {
        title: data.title,
        category: data.category,
        summary: data.summary,
        content: data.content,
        image_url: data.image_url || '',
        published: data.published,
      }
    } catch (e) {
      alert('Erro ao carregar notícia')
      router.push('/news')
    }
  }
})

async function handleSave() {
  saving.value = true
  uploadError.value = ''
  try {
    if (selectedFile.value) {
      form.value.image_url = await uploadImage()
    }

    if (isEdit.value) {
      await api.put(`/api/news/${currentNews.value.id}`, form.value)
    } else {
      await api.post('/api/news/', form.value)
    }
    router.push('/news')
  } catch (e) {
    alert(e.response?.data?.detail || 'Erro ao salvar')
  } finally {
    saving.value = false
  }
}
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

.btn-back {
  color: #64748b;
  font-weight: 500;
}

.btn-back:hover {
  color: #011a4f;
}

.form-card {
  background: white;
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  max-width: 700px;
}

.field {
  margin-bottom: 20px;
}

.field label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 6px;
  color: #334155;
}

.field input,
.field select,
.field textarea {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 15px;
  font-family: inherit;
}

.field input:focus,
.field select:focus,
.field textarea:focus {
  outline: none;
  border-color: #083ea8;
}

/* Upload de Imagem */
.image-upload-area {
  position: relative;
}

.file-input {
  position: absolute;
  opacity: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  border: 2px dashed #e2e8f0;
  border-radius: 12px;
  background: #f8fafc;
  cursor: pointer;
  transition: all 0.2s ease;
}

.upload-placeholder:hover {
  border-color: #083ea8;
  background: #f1f5f9;
}

.upload-icon {
  font-size: 36px;
  margin-bottom: 12px;
}

.upload-text {
  font-size: 15px;
  font-weight: 600;
  color: #334155;
}

.upload-hint {
  font-size: 13px;
  color: #64748b;
  margin-top: 4px;
}

.image-preview {
  position: relative;
  display: inline-block;
}

.image-preview img {
  width: 100%;
  max-height: 300px;
  object-fit: cover;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.remove-image {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 32px;
  height: 32px;
  background: #dc2626;
  color: white;
  border: none;
  border-radius: 50%;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.remove-image:hover {
  background: #b91c1c;
}

.url-input {
  margin-top: 12px;
}

.upload-error {
  margin-top: 8px;
  color: #dc2626;
  font-size: 13px;
}

.checkbox-field label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 400;
}

.checkbox-field input {
  width: auto;
}

.btn-primary {
  background: #011a4f;
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
}

.btn-primary:hover {
  background: #083ea8;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
