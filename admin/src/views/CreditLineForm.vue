<template>
  <div class="page">
    <div class="page-header">
      <h1>{{ isEdit ? 'Editar Linha de Crédito' : 'Nova Linha de Crédito' }}</h1>
      <router-link to="/credit-lines" class="btn-back">← Voltar</router-link>
    </div>

    <form @submit.prevent="handleSave" class="form-card">
      <div class="field">
        <label>Título</label>
        <input v-model="form.title" type="text" required />
      </div>

      <div class="field">
        <label>Descrição Curta</label>
        <textarea v-model="form.description" rows="2" required></textarea>
      </div>

      <div class="field">
        <label>Detalhes (opcional)</label>
        <div class="editor-wrapper">
          <Editor v-model="form.details" :init="editorConfig" />
        </div>
      </div>

      <div class="field-row">
        <div class="field">
          <label>Cor de Fundo</label>
          <div class="color-input">
            <input v-model="form.color" type="color" />
            <input v-model="form.color" type="text" placeholder="#EEF4FF" />
          </div>
        </div>

        <div class="field">
          <label>Ordem</label>
          <input v-model.number="form.order" type="number" min="0" />
        </div>
      </div>

      <div class="field">
        <label>Ícone (opcional)</label>
        <div
          class="file-dropzone icon-dropzone"
          :class="{ active: iconDragActive, 'has-file': form.icon_url }"
          @click="triggerIconInput"
          @dragover.prevent="iconDragActive = true"
          @dragleave="iconDragActive = false"
          @drop.prevent="handleIconDrop"
        >
          <template v-if="form.icon_url">
            <div class="file-preview">
              <img :src="form.icon_url" alt="Ícone" class="icon-preview-img" />
              <span class="file-name">{{ form.icon_url.split('/').pop() }}</span>
              <button type="button" class="btn-remove-file" @click.stop="removeIcon">✕</button>
            </div>
          </template>
          <template v-else>
            <div class="dropzone-content">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
              <p>Clique ou arraste o ícone</p>
              <span class="hint">PNG, SVG ou WebP — Máximo 5MB</span>
            </div>
          </template>
        </div>
        <input ref="iconInput" type="file" accept="image/jpeg,image/png,image/webp,image/svg+xml" style="display:none" @change="onIconSelect" />
        <div v-if="uploadingIcon" class="upload-progress">Enviando ícone...</div>
        <div v-if="iconError" class="upload-error">{{ iconError }}</div>
      </div>

      <div class="field checkbox-field">
        <label>
          <input v-model="form.active" type="checkbox" />
          Ativo
        </label>
      </div>

      <hr class="section-divider" />

      <div class="field">
        <label class="section-label">Documentos Necessários</label>
        <p class="section-hint">Documentos que o usuário precisa apresentar para solicitar o crédito.</p>
        <div v-for="(doc, index) in form.documents" :key="index" class="document-item">
          <div class="document-header">
            <input v-model="doc.label" type="text" placeholder="Nome do documento (ex: Contrato Social)" />
            <button type="button" class="btn-remove" @click="removeDocument('documents', index)">✕</button>
          </div>
          <div
            class="file-dropzone"
            :class="{ active: doc._dragActive, 'has-file': doc.file_url }"
            @click="triggerDocInput(index)"
            @dragover.prevent="doc._dragActive = true"
            @dragleave="doc._dragActive = false"
            @drop.prevent="handleDocDrop($event, index)"
          >
            <template v-if="doc.file_url">
              <div class="file-preview">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                <span class="file-name">{{ doc.file_url.split('/').pop() }}</span>
                <button type="button" class="btn-remove-file" @click.stop="removeDocFile(index)">✕</button>
              </div>
            </template>
            <template v-else>
              <div class="dropzone-content">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
                <p>Arraste o arquivo ou <strong>clique para selecionar</strong></p>
                <span class="hint">PDF, DOCX ou XLSX — Máximo 10MB</span>
              </div>
            </template>
          </div>
          <input :ref="el => docInputRefs[index] = el" type="file" accept=".pdf,.doc,.docx,.xls,.xlsx" style="display:none" @change="onDocSelect($event, index)" />
          <div v-if="doc._uploading" class="upload-progress">Enviando arquivo...</div>
          <div v-if="doc._error" class="upload-error">{{ doc._error }}</div>
        </div>
        <button type="button" class="btn-add" @click="addDocument('documents')">+ Adicionar Documento</button>
      </div>

      <hr class="section-divider" />

      <div class="field">
        <label class="section-label">Sistema Externo - HTML</label>
        <p class="section-hint">Cole o HTML do sistema externo de solicitação de crédito. Será exibido na própria página.</p>
        <textarea
          v-model="form.external_html"
          class="html-textarea"
          rows="10"
          placeholder='<iframe src="https://sistema.exemplo.com/solicitacao" width="100%" height="600"></iframe>'
        ></textarea>
      </div>

      <div class="form-actions">
        <button type="submit" class="btn-primary" :disabled="saving || uploadingIcon">
          {{ saving ? 'Salvando...' : 'Salvar' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
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
import api from '@/services/api'

if (typeof window !== 'undefined') {
  window.tinymce = tinymce
}

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => !!route.params.id)
const saving = ref(false)

const editorConfig = {
  license_key: 'gpl',
  skin: false,
  content_css: false,
  height: 400,
  menubar: 'file edit insert view format table tools help',
  plugins: [
    'advlist', 'autolink', 'lists', 'link', 'image', 'charmap',
    'anchor', 'searchreplace', 'visualblocks', 'code', 'fullscreen',
    'insertdatetime', 'media', 'table', 'help', 'wordcount'
  ],
  toolbar: 'undo redo | blocks | bold italic underline | alignleft aligncenter alignright alignjustify | bullist numlist | link image table | removeformat code | help',
  content_style: `${contentUiCss}\n${contentCss}\nbody { font-family: system-ui, -apple-system, sans-serif; font-size: 15px; line-height: 1.7; }`,
  placeholder: 'Descreva os detalhes da linha de crédito...',
  block_formats: 'Paragraph=p;Heading 2=h2;Heading 3=h3;Heading 4=h4',
}

const form = ref({
  title: '',
  description: '',
  details: '',
  color: '#EEF4FF',
  order: 0,
  icon_url: '',
  active: true,
  documents: [],
  external_html: '',
})

const iconDragActive = ref(false)
const uploadingIcon = ref(false)
const iconError = ref('')
const iconInput = ref(null)

const docInputRefs = reactive({})

function triggerIconInput() {
  if (!form.value.icon_url && !uploadingIcon.value) iconInput.value?.click()
}

function onIconSelect(event) {
  const file = event.target.files[0]
  if (file) uploadIcon(file)
  event.target.value = ''
}

function handleIconDrop(event) {
  iconDragActive.value = false
  if (uploadingIcon.value) return
  const file = event.dataTransfer.files[0]
  if (file && file.type.startsWith('image/')) uploadIcon(file)
}

async function uploadIcon(file) {
  iconError.value = ''
  if (!file.type.startsWith('image/')) {
    iconError.value = 'Selecione um arquivo de imagem válido.'
    return
  }
  if (file.size > 5 * 1024 * 1024) {
    iconError.value = 'Arquivo muito grande. Máximo: 5MB.'
    return
  }
  const formData = new FormData()
  formData.append('file', file)
  uploadingIcon.value = true
  try {
    const { data } = await api.post('/api/upload?folder=credit-lines', formData)
    form.value.icon_url = data.url
  } catch (error) {
    iconError.value = error.response?.data?.detail || 'Erro ao fazer upload do ícone.'
  } finally {
    uploadingIcon.value = false
  }
}

function removeIcon() {
  form.value.icon_url = ''
  iconError.value = ''
}

function addDocument(type) {
  form.value[type].push({ label: '', file_url: '', _dragActive: false, _uploading: false, _error: '' })
}

function removeDocument(type, index) {
  form.value[type].splice(index, 1)
}

function triggerDocInput(index) {
  if (!form.value.documents[index].file_url) docInputRefs[index]?.click()
}

function onDocSelect(event, index) {
  const file = event.target.files[0]
  if (file) uploadDoc(file, index)
  event.target.value = ''
}

function handleDocDrop(event, index) {
  form.value.documents[index]._dragActive = false
  if (form.value.documents[index]._uploading) return
  const file = event.dataTransfer.files[0]
  if (file) uploadDoc(file, index)
}

async function uploadDoc(file, index) {
  const doc = form.value.documents[index]
  doc._error = ''
  const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
  if (!allowedTypes.includes(file.type)) {
    doc._error = 'Tipo não permitido. Use PDF, DOCX ou XLSX.'
    return
  }
  if (file.size > 10 * 1024 * 1024) {
    doc._error = 'Arquivo muito grande. Máximo: 10MB.'
    return
  }
  doc._uploading = true
  try {
    const formData = new FormData()
    formData.append('file', file)
    const { data } = await api.post('/api/upload?folder=credit-lines', formData)
    doc.file_url = data.url
  } catch (error) {
    doc._error = error.response?.data?.detail || 'Erro ao enviar arquivo.'
  } finally {
    doc._uploading = false
  }
}

function removeDocFile(index) {
  form.value.documents[index].file_url = ''
}

function cleanDocuments(docs) {
  return docs.map(d => ({ label: d.label, file_url: d.file_url }))
}

onMounted(async () => {
  if (isEdit.value) {
    try {
      const { data } = await api.get(`/api/credit-lines/by-id/${route.params.id}`)
      const docs = (data.documents || []).map(d => ({ ...d, _dragActive: false, _uploading: false, _error: '' }))
      form.value = {
        title: data.title,
        description: data.description,
        details: data.details || '',
        color: data.color,
        order: data.order,
        icon_url: data.icon_url || '',
        active: data.active,
        documents: docs,
        external_html: data.external_html || '',
      }
    } catch (e) {
      alert('Erro ao carregar linha de crédito')
      router.push('/credit-lines')
    }
  }
})

async function handleSave() {
  saving.value = true
  try {
    const payload = {
      title: form.value.title,
      description: form.value.description,
      details: form.value.details,
      color: form.value.color,
      order: form.value.order,
      icon_url: form.value.icon_url,
      active: form.value.active,
      documents: cleanDocuments(form.value.documents),
      external_html: form.value.external_html,
    }
    if (isEdit.value) {
      await api.put(`/api/credit-lines/${route.params.id}`, payload)
    } else {
      await api.post('/api/credit-lines/', payload)
    }
    router.push('/credit-lines')
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

.field input[type="text"],
.field input[type="number"],
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

.field-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.color-input {
  display: flex;
  gap: 8px;
  align-items: center;
}

.color-input input[type="color"] {
  width: 44px;
  height: 40px;
  padding: 2px;
  cursor: pointer;
  border-radius: 6px;
}

.color-input input[type="text"] {
  flex: 1;
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

.section-divider {
  border: none;
  border-top: 1px solid #e2e8f0;
  margin: 32px 0;
}

.section-label {
  font-size: 16px !important;
  font-weight: 700 !important;
  color: #011a4f !important;
  margin-bottom: 4px !important;
}

.section-hint {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 16px;
}

.file-dropzone {
  border: 2px dashed #e2e8f0;
  border-radius: 12px;
  padding: 24px;
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
  border-style: solid;
  padding: 12px 16px;
}

.dropzone-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.dropzone-content p {
  font-size: 14px;
  color: #334155;
  margin: 0;
}

.dropzone-content .hint {
  font-size: 12px;
  color: #94a3b8;
}

.file-preview {
  display: flex;
  align-items: center;
  gap: 12px;
}

.icon-preview-img {
  width: 48px;
  height: 48px;
  object-fit: contain;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
  background: white;
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

.btn-remove-file {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  font-size: 16px;
  padding: 4px;
}

.btn-remove-file:hover {
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

.document-item {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 16px;
  margin-bottom: 12px;
}

.document-header {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.document-header input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
  background: white;
}

.document-header input:focus {
  outline: none;
  border-color: #083ea8;
}

.btn-remove {
  width: 32px;
  height: 32px;
  min-width: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-remove:hover {
  background: #fee2e2;
  border-color: #dc2626;
}

.document-item .file-dropzone {
  padding: 16px;
}

.btn-add {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 8px 16px;
  background: #f8fafc;
  color: #083ea8;
  border: 1px dashed #083ea8;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-add:hover {
  background: #eff6ff;
  border-style: solid;
}

.html-textarea {
  font-family: 'Courier New', Courier, monospace;
  font-size: 13px;
  line-height: 1.5;
  resize: vertical;
  min-height: 150px;
  background: #1e293b;
  color: #e2e8f0;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #334155;
}

.html-textarea:focus {
  outline: none;
  border-color: #083ea8;
}

.editor-wrapper {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
}

.form-actions {
  margin-top: 32px;
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

@media (max-width: 640px) {
  .field-row {
    grid-template-columns: 1fr;
  }
}
</style>
