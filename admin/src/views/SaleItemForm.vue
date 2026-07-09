<template>
  <div class="sale-item-form-page">
    <div class="form-top-actions">
      <button type="button" class="btn-cancel" @click="router.push('/sale-items')">Cancelar</button>
      <button type="button" class="btn-save" :disabled="saving" @click="handleSave">
        {{ saving ? 'Salvando...' : (isEdit ? 'Salvar alterações' : 'Criar item') }}
      </button>
    </div>

    <div v-if="loading" class="loading">Carregando item...</div>

    <div v-else class="form-layout">
      <div class="form-main">
        <div class="sidebar-card">
          <h3>Detalhes do Item</h3>

          <div class="field">
            <label>Tipo <span class="required">*</span></label>
            <select v-model="form.item_type">
              <option value="imovel">Imóvel</option>
              <option value="veiculo">Veículo</option>
            </select>
          </div>

          <div class="field">
            <label>Título <span class="required">*</span></label>
            <input v-model="form.title" type="text" placeholder="Ex: Palmas, Toyota Hilux SRX" />
          </div>

          <div class="field">
            <label>Descrição</label>
            <textarea v-model="form.description" rows="2" placeholder="Breve descrição do item"></textarea>
          </div>

          <div class="field">
            <label>Detalhes (HTML)</label>
            <textarea v-model="form.details" rows="4" placeholder="Informações detalhadas em HTML"></textarea>
            <span class="hint">Conteúdo rico com formatação HTML</span>
          </div>

          <div class="field">
            <label>Imagem Principal</label>
            <div class="dropzone" :class="{ 'has-image': form.image_url }" @click="triggerFileInput">
              <img v-if="form.image_url" :src="resolveMediaUrl(form.image_url)" alt="Preview" class="image-preview" />
              <div v-else class="dropzone-content">
                <Upload :size="32" />
                <p>Clique para enviar imagem</p>
                <span>PNG, JPG ou WebP. Máximo: 5MB.</span>
              </div>
            </div>
            <input ref="fileInput" type="file" accept="image/jpeg,image/png,image/webp" style="display: none" @change="handleFileSelect" />
            <span v-if="uploadError" class="error-text">{{ uploadError }}</span>
          </div>

          <div class="field">
            <label>Outras Imagens (Galeria)</label>
            <div class="gallery-grid">
              <div v-for="(img, idx) in galleryImages" :key="idx" class="gallery-thumb">
                <img :src="resolveMediaUrl(img)" :alt="`Imagem ${idx + 1}`" />
                <button type="button" class="gallery-remove" @click="removeGalleryImage(idx)" aria-label="Remover imagem">✕</button>
              </div>
              <button type="button" class="gallery-add" @click="triggerGalleryInput" :disabled="galleryUploading">
                <Upload :size="20" />
                <span>{{ galleryUploading ? 'Enviando...' : 'Adicionar' }}</span>
              </button>
            </div>
            <input ref="galleryFileInput" type="file" accept="image/jpeg,image/png,image/webp" multiple style="display: none" @change="handleGalleryFileSelect" />
            <span class="hint">Imagens adicionais exibidas na galeria de detalhes. Máximo: 5MB cada.</span>
            <span v-if="galleryError" class="error-text">{{ galleryError }}</span>
          </div>

          <div class="field">
            <label>Cidade</label>
            <input v-model="form.city" type="text" placeholder="Ex: Palmas" />
          </div>

          <div class="field">
            <label>Telefone</label>
            <input v-model="form.phone" type="text" placeholder="Ex: (63) 99999-0000" />
          </div>

          <div class="field">
            <label>Preço (R$) <span class="required">*</span></label>
            <input v-model.number="form.price" type="number" min="0" step="0.01" />
          </div>

          <!-- Campos de Imóvel -->
          <template v-if="form.item_type === 'imovel'">
            <div class="field-row">
              <div class="field">
                <label>Tipo do Imóvel</label>
                <select v-model="form.property_type">
                  <option value="">Selecione</option>
                  <option value="Urbano">Urbano</option>
                  <option value="Rural">Rural</option>
                </select>
              </div>
              <div class="field">
                <label>Finalidade</label>
                <select v-model="form.purpose">
                  <option value="">Selecione</option>
                  <option value="Residencial">Residencial</option>
                  <option value="Comercial">Comercial</option>
                  <option value="Rural">Rural</option>
                </select>
              </div>
            </div>
            <div class="field">
              <label>Área (m²)</label>
              <input v-model.number="form.area_m2" type="number" min="0" />
            </div>
          </template>

          <!-- Campos de Veículo -->
          <template v-if="form.item_type === 'veiculo'">
            <div class="field-row">
              <div class="field">
                <label>Ano</label>
                <input v-model.number="form.year" type="number" min="1900" max="2099" />
              </div>
              <div class="field">
                <label>Combustível</label>
                <select v-model="form.fuel">
                  <option value="">Selecione</option>
                  <option value="Gasolina">Gasolina</option>
                  <option value="Etanol">Etanol</option>
                  <option value="Flex">Flex</option>
                  <option value="Diesel">Diesel</option>
                  <option value="Elétrico">Elétrico</option>
                  <option value="Híbrido">Híbrido</option>
                </select>
              </div>
            </div>
            <div class="field">
              <label>Câmbio</label>
              <select v-model="form.transmission">
                <option value="">Selecione</option>
                <option value="Manual">Manual</option>
                <option value="Automática">Automática</option>
              </select>
            </div>
          </template>

          <div class="field">
            <label>Ordem</label>
            <input v-model.number="form.order" type="number" min="0" />
          </div>

          <div class="field-checkbox">
            <label>
              <input type="checkbox" v-model="form.featured" />
              Item em destaque
            </label>
            <span class="hint">Itens em destaque aparecem na página principal</span>
          </div>

          <div class="field-checkbox">
            <label>
              <input type="checkbox" v-model="form.active" />
              Item ativo
            </label>
            <span class="hint">Itens inativos não aparecem no site</span>
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
const uploadError = ref('')
const fileInput = ref(null)
const galleryFileInput = ref(null)
const galleryImages = ref([])
const galleryUploading = ref(false)
const galleryError = ref('')

const form = ref({
  item_type: 'imovel',
  title: '',
  description: '',
  details: '',
  city: '',
  region: '',
  property_type: '',
  purpose: '',
  year: null,
  fuel: '',
  transmission: '',
  price: 0,
  area_m2: null,
  image_url: '',
  phone: '',
  featured: false,
  active: true,
  order: 0,
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
  try {
    const { data } = await api.post('/api/upload?folder=sale-items', formData)
    form.value.image_url = data.url
  } catch (err) {
    uploadError.value = err.response?.data?.detail || 'Erro ao fazer upload.'
  }
}

function triggerGalleryInput() {
  galleryFileInput.value?.click()
}

function handleGalleryFileSelect(e) {
  const files = Array.from(e.target.files)
  files.forEach(file => uploadGalleryImage(file))
  e.target.value = ''
}

async function uploadGalleryImage(file) {
  galleryError.value = ''
  if (!file.type.startsWith('image/')) {
    galleryError.value = 'Selecione um arquivo de imagem válido.'
    return
  }
  if (file.size > 5 * 1024 * 1024) {
    galleryError.value = 'Arquivo muito grande. Máximo: 5MB.'
    return
  }
  galleryUploading.value = true
  const formData = new FormData()
  formData.append('file', file)
  try {
    const { data } = await api.post('/api/upload?folder=sale-items', formData)
    galleryImages.value.push(data.url)
  } catch (err) {
    galleryError.value = err.response?.data?.detail || 'Erro ao fazer upload.'
  } finally {
    galleryUploading.value = false
  }
}

function removeGalleryImage(index) {
  galleryImages.value.splice(index, 1)
}

onMounted(async () => {
  if (isEdit.value) {
    loading.value = true
    try {
      const { data } = await api.get(`/api/sale-items/${route.params.id}`)
      form.value = {
        item_type: data.item_type,
        title: data.title,
        description: data.description || '',
        details: data.details || '',
        city: data.city || '',
        region: data.region || '',
        property_type: data.property_type || '',
        purpose: data.purpose || '',
        year: data.year,
        fuel: data.fuel || '',
        transmission: data.transmission || '',
        price: data.price,
        area_m2: data.area_m2,
        image_url: data.image_url || '',
        phone: data.phone || '',
        featured: data.featured,
        active: data.active,
        order: data.order,
      }
      if (data.gallery) {
        try {
          const parsed = typeof data.gallery === 'string' ? JSON.parse(data.gallery) : data.gallery
          galleryImages.value = Array.isArray(parsed) ? parsed : []
        } catch {
          galleryImages.value = []
        }
      }
    } catch (err) {
      error.value = 'Erro ao carregar item'
      console.error(err)
    } finally {
      loading.value = false
    }
  }
})

async function handleSave() {
  if (!form.value.title.trim()) {
    error.value = 'O título é obrigatório'
    return
  }
  if (!form.value.price || form.value.price <= 0) {
    error.value = 'O preço deve ser maior que zero'
    return
  }

  saving.value = true
  error.value = ''

  try {
    const payload = {
      item_type: form.value.item_type,
      title: form.value.title.trim(),
      description: form.value.description.trim() || null,
      details: form.value.details.trim() || null,
      city: form.value.city.trim() || null,
      region: form.value.region.trim() || null,
      property_type: form.value.item_type === 'imovel' ? form.value.property_type || null : null,
      purpose: form.value.item_type === 'imovel' ? form.value.purpose || null : null,
      year: form.value.item_type === 'veiculo' ? form.value.year : null,
      fuel: form.value.item_type === 'veiculo' ? form.value.fuel || null : null,
      transmission: form.value.item_type === 'veiculo' ? form.value.transmission || null : null,
      price: form.value.price,
      area_m2: form.value.item_type === 'imovel' ? form.value.area_m2 : null,
      image_url: form.value.image_url || null,
      gallery: galleryImages.value.length > 0 ? JSON.stringify(galleryImages.value) : null,
      phone: form.value.phone.trim() || null,
      featured: form.value.featured,
      active: form.value.active,
      order: form.value.order,
    }

    if (isEdit.value) {
      await api.put(`/api/sale-items/${route.params.id}`, payload)
    } else {
      await api.post('/api/sale-items/', payload)
    }
    router.push('/sale-items')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erro ao salvar item'
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
.btn-cancel:hover { background: #f8fafc; }
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
.btn-save:hover { background: #0a2d6a; }
.btn-save:disabled { opacity: 0.6; cursor: not-allowed; }
.loading { text-align: center; padding: 40px; color: #64748b; }
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
.field { margin-bottom: 16px; }
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
.field select:focus { border-color: #011a4f; }
.field-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}
.required { color: #dc2626; }
.hint { display: block; font-size: 12px; color: #94a3b8; margin-top: 4px; }
.error-text { display: block; font-size: 12px; color: #dc2626; margin-top: 4px; }
.dropzone {
  border: 2px dashed #e2e8f0;
  border-radius: 8px;
  padding: 24px;
  text-align: center;
  cursor: pointer;
  transition: border-color 0.2s;
}
.dropzone:hover { border-color: #011a4f; background: #f8fafc; }
.dropzone.has-image { padding: 8px; border-style: solid; }
.dropzone-content p { margin: 8px 0 4px; font-size: 14px; color: #475569; }
.dropzone-content span { font-size: 12px; color: #94a3b8; }
.image-preview { max-width: 100%; max-height: 200px; border-radius: 6px; object-fit: contain; }
.gallery-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.gallery-thumb {
  position: relative;
  width: 90px;
  height: 90px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
}
.gallery-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.gallery-remove {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 20px;
  height: 20px;
  border: none;
  border-radius: 50%;
  background: rgba(220, 38, 38, 0.9);
  color: white;
  font-size: 11px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s;
}
.gallery-thumb:hover .gallery-remove {
  opacity: 1;
}
.gallery-add {
  width: 90px;
  height: 90px;
  border: 2px dashed #e2e8f0;
  border-radius: 8px;
  background: transparent;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  color: #94a3b8;
  font-size: 11px;
  transition: all 0.2s;
}
.gallery-add:hover {
  border-color: #011a4f;
  color: #011a4f;
  background: #f8fafc;
}
.gallery-add:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.field-checkbox { margin-bottom: 16px; }
.field-checkbox label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #475569;
  cursor: pointer;
}
.field-checkbox input[type="checkbox"] { width: 16px; height: 16px; accent-color: #011a4f; }
.error-message {
  margin-top: 16px;
  padding: 12px 16px;
  background: #fef2f2;
  color: #dc2626;
  border-radius: 8px;
  font-size: 14px;
}
</style>
