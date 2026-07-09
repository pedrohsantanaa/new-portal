<template>
  <div class="carousel-form-page">
    <div class="form-top-actions">
      <button type="button" class="btn-cancel" @click="router.push('/carousel')">Cancelar</button>
      <button type="button" class="btn-save" :disabled="saving" @click="handleSave">
        {{ saving ? 'Salvando...' : (isEdit ? 'Salvar alterações' : 'Criar slide') }}
      </button>
    </div>

    <div v-if="loading" class="loading">Carregando slide...</div>

    <div v-else class="form-layout">
      <div class="form-main">
        <div class="sidebar-card">
          <h3>Detalhes do Slide</h3>

          <div class="field">
            <label>Imagem <span class="required">*</span></label>
            <div
              class="dropzone"
              :class="{ 'has-image': form.image_url, dragging: isDragging }"
              @click="triggerFileInput"
              @dragover.prevent="isDragging = true"
              @dragleave="isDragging = false"
              @drop.prevent="handleDrop"
            >
              <img v-if="form.image_url" :src="resolveMediaUrl(form.image_url)" alt="Preview" class="image-preview" />
              <div v-else class="dropzone-content">
                <Upload :size="32" />
                <p>Arraste ou clique para enviar imagem</p>
                <span>PNG, JPG ou WebP. Máximo: 5MB.</span>
              </div>
            </div>
            <input ref="fileInput" type="file" accept="image/jpeg,image/png,image/webp" style="display: none" @change="handleFileSelect" />
            <span v-if="uploadError" class="error-text">{{ uploadError }}</span>
            <span v-if="uploadingImage" class="hint">Enviando imagem...</span>
          </div>

          <div class="field">
            <label>Título</label>
            <input v-model="form.title" type="text" placeholder="Título exibido sobre a imagem (opcional)" />
          </div>

          <div class="field">
            <label>Descrição</label>
            <textarea v-model="form.description" rows="2" placeholder="Descrição exibida abaixo do título (opcional)"></textarea>
          </div>

          <div class="field">
            <label>Link do Botão</label>
            <input v-model="form.link" type="text" placeholder="URL para onde o botão redireciona (ex: /noticias)" />
          </div>

          <div class="field">
            <label>Texto do Botão</label>
            <input v-model="form.btn_label" type="text" placeholder="Texto exibido no botão (ex: Saiba Mais)" />
          </div>

          <div class="field">
            <label>Classe do Botão</label>
            <div class="radio-group">
              <label class="radio-option">
                <input type="radio" v-model="form.btn_class" value="btn-orange" />
                <span class="radio-preview btn-orange-preview">btn-orange</span>
              </label>
              <label class="radio-option">
                <input type="radio" v-model="form.btn_class" value="btn-light" />
                <span class="radio-preview btn-light-preview">btn-light</span>
              </label>
            </div>
          </div>

          <div class="field">
            <label>Ordem</label>
            <input v-model.number="form.order" type="number" min="0" />
            <span class="hint">Define a ordem de exibição no carrossel</span>
          </div>

          <div class="field-checkbox">
            <label>
              <input type="checkbox" v-model="form.active" />
              Slide ativo
            </label>
            <span class="hint">Slides inativos não aparecem no carrossel</span>
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
import { Upload } from 'lucide-vue-next'
import api, { API_BASE_URL } from '@/services/api'

const router = useRouter()
const route = useRoute()

const isEdit = computed(() => !!route.params.id)
const loading = ref(false)
const saving = ref(false)
const error = ref('')
const uploadingImage = ref(false)
const uploadError = ref('')
const isDragging = ref(false)
const fileInput = ref(null)

const form = ref({
  image_url: '',
  title: '',
  description: '',
  link: '',
  btn_label: '',
  btn_class: 'btn-orange',
  order: 0,
  active: true,
})

function resolveMediaUrl(url) {
  if (!url) return ''
  if (/^https?:\/\//i.test(url)) return url
  return API_BASE_URL ? `${API_BASE_URL}${url}` : url
}

function triggerFileInput() {
  fileInput.value?.click()
}

function handleFileSelect(e) {
  const file = e.target.files[0]
  if (file) uploadImage(file)
}

function handleDrop(e) {
  isDragging.value = false
  const file = e.dataTransfer.files[0]
  if (file) uploadImage(file)
}

async function uploadImage(file) {
  uploadError.value = ''
  if (!file.type.startsWith('image/')) {
    uploadError.value = 'Selecione um arquivo de imagem válido.'
    return
  }
  if (file.size > 5 * 1024 * 1024) {
    uploadError.value = 'Arquivo muito grande. Máximo: 5MB.'
    return
  }
  const formData = new FormData()
  formData.append('file', file)
  uploadingImage.value = true
  try {
    const { data } = await api.post('/api/upload?folder=carousel', formData)
    form.value.image_url = data.url
  } catch (err) {
    uploadError.value = err.response?.data?.detail || 'Erro ao fazer upload da imagem.'
  } finally {
    uploadingImage.value = false
  }
}

onMounted(async () => {
  if (isEdit.value) {
    loading.value = true
    try {
      const { data } = await api.get(`/api/carousel-slides/${route.params.id}`)
      form.value = {
        image_url: data.image_url,
        title: data.title || '',
        description: data.description || '',
        link: data.link || '',
        btn_label: data.btn_label || '',
        btn_class: data.btn_class,
        order: data.order,
        active: data.active,
      }
    } catch (err) {
      error.value = 'Erro ao carregar slide'
      console.error(err)
    } finally {
      loading.value = false
    }
  }
})

async function handleSave() {
  if (!form.value.image_url) {
    error.value = 'A imagem é obrigatória'
    return
  }

  saving.value = true
  error.value = ''

  try {
    const payload = {
      image_url: form.value.image_url,
      title: form.value.title.trim() || null,
      description: form.value.description.trim() || null,
      link: form.value.link.trim() || null,
      btn_label: form.value.btn_label.trim() || null,
      btn_class: form.value.btn_class,
      order: form.value.order,
      active: form.value.active,
    }

    if (isEdit.value) {
      await api.put(`/api/carousel-slides/${route.params.id}`, payload)
    } else {
      await api.post('/api/carousel-slides/', payload)
    }
    router.push('/carousel')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erro ao salvar slide'
    console.error(err)
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
  grid-template-columns: 1fr;
  gap: 24px;
  max-width: 700px;
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
.field textarea {
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
.field textarea:focus {
  border-color: #011a4f;
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
.error-text {
  display: block;
  font-size: 12px;
  color: #dc2626;
  margin-top: 4px;
}
.dropzone {
  border: 2px dashed #e2e8f0;
  border-radius: 8px;
  padding: 24px;
  text-align: center;
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s;
}
.dropzone:hover {
  border-color: #011a4f;
  background: #f8fafc;
}
.dropzone.dragging {
  border-color: #011a4f;
  background: #eff6ff;
}
.dropzone.has-image {
  padding: 8px;
  border-style: solid;
  border-color: #e2e8f0;
}
.dropzone-content p {
  margin: 8px 0 4px;
  font-size: 14px;
  color: #475569;
}
.dropzone-content span {
  font-size: 12px;
  color: #94a3b8;
}
.image-preview {
  max-width: 100%;
  max-height: 200px;
  border-radius: 6px;
  object-fit: contain;
}
.radio-group {
  display: flex;
  gap: 12px;
}
.radio-option {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}
.radio-option input[type="radio"] {
  accent-color: #011a4f;
}
.radio-preview {
  padding: 6px 14px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
}
.btn-orange-preview {
  background: #ffc107;
  color: #000;
}
.btn-light-preview {
  background: #ffffff;
  color: #011a4f;
  border: 1px solid #e2e8f0;
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
.error-message {
  margin-top: 16px;
  padding: 12px 16px;
  background: #fef2f2;
  color: #dc2626;
  border-radius: 8px;
  font-size: 14px;
}
</style>
