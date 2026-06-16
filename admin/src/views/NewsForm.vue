<template>
  <div class="news-form-page">
    <!-- Top actions -->
    <div class="form-top-actions">
      <button type="button" class="btn-cancel" @click="router.push('/news')">Cancelar</button>
      <button type="button" class="btn-draft" :disabled="saving || uploadingImage" @click="handleSaveDraft">Salvar rascunho</button>
      <div class="publish-group">
        <button type="button" class="btn-publish" :disabled="saving || uploadingImage" @click="handlePublish">Publicar</button>
        <button type="button" class="btn-publish-arrow" :disabled="saving || uploadingImage" @click="showPublishMenu = !showPublishMenu">▾</button>
        <div class="publish-menu" v-if="showPublishMenu">
          <button @click="handlePublish">Publicar agora</button>
          <button @click="handleSchedule">Agendar publicação</button>
        </div>
      </div>
    </div>

    <!-- Layout 2 colunas -->
    <div class="form-layout">
      <!-- Coluna principal -->
      <div class="form-main">
        <!-- Título -->
        <div class="field">
          <label>Título da notícia <span class="required">*</span></label>
          <input v-model="form.title" type="text" placeholder="Digite o título da notícia" required />
        </div>

        <!-- Subtítulo / Resumo -->
        <div class="field">
          <label>Subtítulo / Resumo</label>
          <textarea v-model="form.summary" rows="3" maxlength="160" placeholder="Breve descrição da notícia (opcional)"></textarea>
          <span class="char-counter">{{ form.summary.length }}/160</span>
        </div>

        <!-- Imagem de destaque -->
        <div class="field">
          <label>Imagem de destaque</label>
          <div
            class="image-dropzone"
            :class="{ 'has-image': form.image_url, 'is-uploading': uploadingImage }"
            @click="triggerFileInput"
            @dragover.prevent="dragActive = true"
            @dragleave="dragActive = false"
            @drop.prevent="handleDrop"
          >
            <template v-if="form.image_url">
              <img :src="resolveMediaUrl(form.image_url)" alt="Preview" class="image-preview" />
              <button type="button" class="btn-remove-image" :disabled="uploadingImage" @click.stop="removeImage">Remover</button>
            </template>
            <template v-else>
              <div class="dropzone-content">
                <ImageIcon :size="40" />
                <p>Clique para selecionar uma imagem</p>
                <span>Ou arraste e solte aqui</span>
                <span class="hint">Tamanho recomendado: 1200x630px</span>
              </div>
            </template>
            <div v-if="uploadingImage" class="upload-overlay">Enviando imagem...</div>
          </div>
          <p v-if="uploadError" class="upload-error">{{ uploadError }}</p>
          <input ref="fileInput" type="file" accept="image/jpeg,image/png,image/webp" class="hidden-input" @change="onFileSelect" />
        </div>

        <!-- Corpo da notícia -->
        <div class="field">
          <label>Corpo da notícia <span class="required">*</span></label>
          <div class="editor-wrapper">
            <Editor
              v-model="form.content"
              :init="editorConfig"
            />
          </div>
        </div>

        <!-- Anexos -->

      </div>

      <!-- Sidebar direita -->
      <div class="form-sidebar">
        <!-- Publicação -->
        <div class="sidebar-card">
          <h3>Publicação</h3>

          <div class="field">
            <label>Status</label>
            <select v-model="form.published">
              <option :value="false">Rascunho</option>
              <option :value="true">Publicada</option>
            </select>
          </div>

          <div class="field">
            <label>Categoria <span class="required">*</span></label>
            <select v-model="form.category" required>
              <option value="" disabled>Selecione uma categoria</option>
              <option value="Crédito">Crédito</option>
              <option value="Programa">Programa</option>
              <option value="Evento">Evento</option>
              <option value="Empreendedorismo">Empreendedorismo</option>
            </select>
          </div>

          <div class="field">
            <label>Autor <span class="required">*</span></label>
            <input v-model="form.author" type="text" placeholder="Nome do autor" />
          </div>

          <div class="field">
            <label>Data de publicação</label>
            <input v-model="scheduledDate" type="datetime-local" />
          </div>

        </div>

        <!-- SEO -->
        <div class="sidebar-card">
          <h3>SEO <span class="optional">(opcional)</span></h3>

          <div class="field">
            <label>Título para SEO</label>
            <input v-model="form.seo_title" type="text" maxlength="60" placeholder="Título para mecanismos de busca" />
            <span class="char-counter">{{ (form.seo_title || '').length }}/60</span>
          </div>

          <div class="field">
            <label>Descrição para SEO</label>
            <textarea v-model="form.seo_description" rows="3" maxlength="160" placeholder="Breve descrição para mecanismos de busca"></textarea>
            <span class="char-counter">{{ (form.seo_description || '').length }}/160</span>
          </div>


        </div>
      </div>
    </div>

    <!-- Bottom bar -->
    <div class="form-bottom-bar">
      <span class="save-indicator" v-if="lastSaved">Último salvamento: agora há pouco</span>
      <span class="save-indicator" v-else>&nbsp;</span>
      <div class="bottom-actions">
        <button type="button" class="btn-cancel" @click="router.push('/news')">Cancelar</button>
        <button type="button" class="btn-draft" :disabled="saving || uploadingImage" @click="handleSaveDraft">Salvar rascunho</button>
        <div class="publish-group">
          <button type="button" class="btn-publish" :disabled="saving || uploadingImage" @click="handlePublish">Publicar</button>
          <button type="button" class="btn-publish-arrow" :disabled="saving || uploadingImage" @click="showPublishMenu = !showPublishMenu">▾</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Editor from '@tinymce/tinymce-vue'
import tinymce from 'tinymce'
import 'tinymce/themes/silver'
import 'tinymce/icons/default'
import 'tinymce/models/dom'
import 'tinymce/plugins/advlist'
import 'tinymce/plugins/autolink'
import 'tinymce/plugins/lists'
import 'tinymce/plugins/link'
import 'tinymce/plugins/image'
import 'tinymce/plugins/charmap'
import 'tinymce/plugins/anchor'
import 'tinymce/plugins/searchreplace'
import 'tinymce/plugins/visualblocks'
import 'tinymce/plugins/code'
import 'tinymce/plugins/fullscreen'
import 'tinymce/plugins/insertdatetime'
import 'tinymce/plugins/media'
import 'tinymce/plugins/table'
import 'tinymce/plugins/help'
import 'tinymce/plugins/wordcount'
import 'tinymce/skins/ui/oxide/skin.min.css'
import contentUiCss from 'tinymce/skins/ui/oxide/content.min.css?inline'
import contentCss from 'tinymce/skins/content/default/content.min.css?inline'
import api, { API_BASE_URL } from '@/services/api'
import { Image as ImageIcon, Paperclip, FileText } from 'lucide-vue-next'

if (typeof window !== 'undefined') {
  window.tinymce = tinymce
}

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => !!route.params.slug)
const currentNews = ref(null)
const saving = ref(false)
const lastSaved = ref(false)
const showPublishMenu = ref(false)
const dragActive = ref(false)
const uploadingImage = ref(false)
const uploadError = ref('')
const fileInput = ref(null)
const attachmentInput = ref(null)
const selectedFile = ref(null)
const attachments = ref([])
const scheduledDate = ref('')

const form = ref({
  title: '',
  slug: '',
  category: '',
  summary: '',
  content: '',
  image_url: '',
  published: false,
  author: '',
  visibility: 'public',
  scheduled_at: null,
  tags: [],
  categories: [],
  seo_title: '',
  seo_description: '',
  seo_keywords: '',
  pinnedTop: false,
  highlighted: false,
})

const editorConfig = {
  license_key: 'gpl',
  skin: false,
  content_css: false,
  height: 500,
  menubar: 'file edit insert view format table tools help',
  plugins: [
    'advlist', 'autolink', 'lists', 'link', 'image', 'charmap',
    'anchor', 'searchreplace', 'visualblocks', 'code', 'fullscreen',
    'insertdatetime', 'media', 'table', 'help', 'wordcount'
  ],
  toolbar: 'undo redo | blocks | bold italic underline | alignleft aligncenter alignright alignjustify | bullist numlist | link image table | removeformat code | help',
  content_style: `${contentUiCss}\n${contentCss}\nbody { font-family: system-ui, -apple-system, sans-serif; font-size: 15px; line-height: 1.7; }`,
  placeholder: 'Escreva o conteúdo da notícia aqui...',
  block_formats: 'Paragraph=p;Heading 2=h2;Heading 3=h3;Heading 4=h4',
  images_upload_handler: (blobInfo) => {
    return new Promise((resolve, reject) => {
      const formData = new FormData()
      formData.append('file', blobInfo.blob(), blobInfo.filename())
      api.post('/api/upload?folder=news', formData)
        .then((response) => resolve(resolveMediaUrl(response.data.url)))
        .catch((error) => reject(error))
    })
  },
  setup: (editor) => {
    editor.on('keyup', () => {
      wordCount.value = editor.plugins.wordcount?.body.getWordCount() || 0
    })
  },
}

const wordCount = ref(0)

function generateSlug(title) {
  return title
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^\w\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '')
}

let slugManuallyEdited = false

watch(() => form.value.title, (newTitle) => {
  if (!slugManuallyEdited && newTitle) {
    form.value.slug = generateSlug(newTitle)
  }
})

function triggerFileInput() {
  if (!form.value.image_url && !uploadingImage.value) fileInput.value?.click()
}

function triggerAttachmentInput() {
  attachmentInput.value?.click()
}

function onFileSelect(event) {
  const file = event.target.files[0]
  if (!file) return
  uploadImage(file)
  event.target.value = ''
}

function handleDrop(event) {
  dragActive.value = false
  if (uploadingImage.value) return
  const file = event.dataTransfer.files[0]
  if (file && file.type.startsWith('image/')) {
    uploadImage(file)
  }
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
    const { data } = await api.post('/api/upload?folder=news', formData)
    form.value.image_url = data.url
    selectedFile.value = null
  } catch (error) {
    console.error('Erro ao fazer upload da imagem:', error)
    uploadError.value = error.response?.data?.detail || 'Erro ao fazer upload da imagem.'
  } finally {
    uploadingImage.value = false
  }
}

function removeImage() {
  uploadError.value = ''
  form.value.image_url = ''
  selectedFile.value = null
}

function resolveMediaUrl(url) {
  if (!url) return ''
  if (/^https?:\/\//i.test(url)) return url
  return API_BASE_URL ? `${API_BASE_URL}${url}` : url
}

function onAttachmentSelect(event) {
  const files = Array.from(event.target.files)
  attachments.value.push(...files)
  event.target.value = ''
}

function removeAttachment(index) {
  attachments.value.splice(index, 1)
}

async function handleSave(published = false) {
  if (uploadingImage.value) {
    alert('Aguarde o upload da imagem finalizar antes de salvar.')
    return
  }
  if (!form.value.title || !form.value.category) {
    alert('Preencha os campos obrigatórios: Título e Categoria')
    return
  }
  saving.value = true
  try {
    form.value.published = published
    if (scheduledDate.value && !published) {
      form.value.scheduled_at = new Date(scheduledDate.value).toISOString()
    }

    const payload = {
      title: form.value.title,
      slug: form.value.slug,
      category: form.value.category,
      summary: form.value.summary || '',
      content: form.value.content,
      image_url: form.value.image_url,
      published: form.value.published,
      author: form.value.author,
      tags: form.value.tags,
      categories: form.value.categories,
      visibility: form.value.visibility,
      scheduled_at: form.value.scheduled_at,
      seo_title: form.value.seo_title,
      seo_description: form.value.seo_description,
      seo_keywords: form.value.seo_keywords,
    }

    if (isEdit.value) {
      await api.put(`/api/news/${currentNews.value.id}`, payload)
    } else {
      await api.post('/api/news/', payload)
    }
    lastSaved.value = true
    setTimeout(() => { lastSaved.value = false }, 3000)

    if (published) {
      router.push('/news')
    }
  } catch (e) {
    alert(e.response?.data?.detail || 'Erro ao salvar')
  } finally {
    saving.value = false
  }
}

function handleSaveDraft() {
  handleSave(false)
}

function handlePublish() {
  showPublishMenu.value = false
  handleSave(true)
}

function handleSchedule() {
  showPublishMenu.value = false
  if (!scheduledDate.value) {
    alert('Selecione uma data de publicação')
    return
  }
  handleSave(false)
}

onMounted(async () => {
  if (isEdit.value) {
    try {
      const { data } = await api.get(`/api/news/${route.params.slug}`)
      currentNews.value = data
      slugManuallyEdited = true
      form.value = {
        title: data.title || '',
        slug: data.slug || '',
        category: data.category || '',
        summary: data.summary || '',
        content: data.content || '',
        image_url: data.image_url || '',
        published: data.published || false,
        author: data.author || '',
        visibility: data.visibility || 'public',
        scheduled_at: data.scheduled_at || null,
        tags: data.tags || [],
        categories: data.categories || [],
        seo_title: data.seo_title || '',
        seo_description: data.seo_description || '',
        seo_keywords: data.seo_keywords || '',
        pinnedTop: false,
        highlighted: false,
      }
      if (data.scheduled_at) {
        scheduledDate.value = new Date(data.scheduled_at).toISOString().slice(0, 16)
      }
    } catch {
      alert('Erro ao carregar notícia')
      router.push('/news')
    }
  }
})
</script>

<style scoped>
.news-form-page {
  max-width: 1400px;
  margin: 0 auto;
}

/* TOP ACTIONS */
.form-top-actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 10px;
  margin-bottom: 24px;
}

/* BUTTONS */
.btn-cancel {
  padding: 10px 20px;
  background: white;
  color: #64748b;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.btn-draft {
  padding: 10px 20px;
  background: white;
  color: #1e293b;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-draft:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.publish-group {
  position: relative;
  display: flex;
}

.btn-publish {
  padding: 10px 20px;
  background: #083ea8;
  color: white;
  border: none;
  border-radius: 8px 0 0 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-publish:hover {
  background: #062d7a;
}

.btn-publish-arrow {
  padding: 10px 12px;
  background: #083ea8;
  color: white;
  border: none;
  border-radius: 0 8px 8px 0;
  font-size: 12px;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-publish-arrow:hover {
  background: #062d7a;
}

.publish-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 4px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  z-index: 10;
  overflow: hidden;
  min-width: 180px;
}

.publish-menu button {
  display: block;
  width: 100%;
  padding: 10px 16px;
  background: none;
  border: none;
  text-align: left;
  font-size: 14px;
  color: #334155;
  cursor: pointer;
  transition: background 0.15s;
}

.publish-menu button:hover {
  background: #f1f5f9;
}

/* LAYOUT */
.form-layout {
  display: flex;
  gap: 24px;
  align-items: flex-start;
}

.form-main {
  flex: 7;
  min-width: 0;
}

.form-sidebar {
  flex: 3;
  min-width: 280px;
  max-width: 320px;
  position: sticky;
  top: 80px;
}

/* SIDEBAR CARD */
.sidebar-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  margin-bottom: 16px;
}

.sidebar-card h3 {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 20px;
}

/* FIELDS */
.field {
  margin-bottom: 20px;
}

.field label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 6px;
}

.required {
  color: #dc2626;
}

.optional {
  color: #94a3b8;
  font-weight: 400;
  font-size: 13px;
}

.field input[type="text"],
.field input[type="datetime-local"],
.field textarea,
.field select {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 15px;
  font-family: inherit;
  color: #1e293b;
  transition: border-color 0.2s;
  background: white;
}

.field input:focus,
.field textarea:focus,
.field select:focus {
  outline: none;
  border-color: #083ea8;
}

.field textarea {
  resize: vertical;
  min-height: 80px;
}

.char-counter {
  display: block;
  text-align: right;
  font-size: 12px;
  color: #94a3b8;
  margin-top: 4px;
}

/* IMAGE DROPZONE */
.image-dropzone {
  border: 2px dashed #e2e8f0;
  border-radius: 12px;
  padding: 40px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  background: #f8fafc;
}

.image-dropzone:hover,
.image-dropzone.has-image {
  border-color: #083ea8;
}

.image-dropzone.has-image {
  padding: 0;
  border-style: solid;
  overflow: hidden;
  position: relative;
}

.image-dropzone.is-uploading {
  pointer-events: none;
  opacity: 0.85;
}

.dropzone-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: #64748b;
}

.dropzone-content p {
  font-weight: 500;
  color: #334155;
}

.dropzone-content span {
  font-size: 13px;
  color: #94a3b8;
}

.dropzone-content .hint {
  font-size: 12px;
  margin-top: 4px;
}

.image-preview {
  width: 100%;
  height: 200px;
  object-fit: cover;
  display: block;
}

.btn-remove-image {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 6px 12px;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-remove-image:hover {
  background: rgba(0, 0, 0, 0.8);
}

.upload-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.82);
  color: #083ea8;
  font-size: 14px;
  font-weight: 700;
}

.upload-error {
  margin-top: 8px;
  color: #dc2626;
  font-size: 13px;
}

.btn-draft:disabled,
.btn-publish:disabled,
.btn-publish-arrow:disabled,
.btn-remove-image:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.hidden-input {
  display: none;
}

/* EDITOR */
.editor-wrapper {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
}

/* ATTACHMENTS */
.attachments-area {
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn-select-files {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: white;
  color: #1e293b;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-select-files:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.attachment-hint {
  font-size: 13px;
  color: #94a3b8;
}

.attachments-list {
  margin-top: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.attachment-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: #f1f5f9;
  border-radius: 6px;
  font-size: 13px;
  color: #334155;
}

.attachment-item span {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.attachment-item button {
  background: none;
  border: none;
  color: #94a3b8;
  font-size: 16px;
  cursor: pointer;
  padding: 0;
}

.attachment-item button:hover {
  color: #dc2626;
}

/* CHECKBOX */
.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #334155;
  cursor: pointer;
  margin-bottom: 8px;
}

.checkbox-label input[type="checkbox"] {
  width: 16px;
  height: 16px;
  accent-color: #083ea8;
}

/* SLUG */
.slug-input-group {
  display: flex;
  align-items: center;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
}

.slug-prefix {
  padding: 10px 12px;
  background: #f1f5f9;
  font-size: 13px;
  color: #64748b;
  white-space: nowrap;
  border-right: 1px solid #e2e8f0;
}

.slug-input {
  border: none !important;
  border-radius: 0 !important;
  flex: 1;
  min-width: 0;
}

.slug-input:focus {
  outline: none;
}

/* BOTTOM BAR */
.form-bottom-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 0;
  margin-top: 24px;
  border-top: 1px solid #e2e8f0;
}

.save-indicator {
  font-size: 13px;
  color: #16a34a;
}

.bottom-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

/* RESPONSIVE */
@media (max-width: 992px) {
  .form-layout {
    flex-direction: column;
  }

  .form-sidebar {
    max-width: 100%;
    position: static;
  }
}

@media (max-width: 768px) {
  .form-top-actions {
    flex-wrap: wrap;
  }

  .form-bottom-bar {
    flex-direction: column;
    gap: 12px;
  }
}
</style>
