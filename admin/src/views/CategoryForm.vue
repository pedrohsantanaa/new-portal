<template>
  <div class="category-form-page">
    <div class="form-top-actions">
      <button type="button" class="btn-cancel" @click="router.push('/categories')">Cancelar</button>
      <button type="button" class="btn-save" :disabled="saving" @click="handleSave">
        {{ saving ? 'Salvando...' : (isEdit ? 'Salvar alterações' : 'Criar categoria') }}
      </button>
    </div>

    <div v-if="loading" class="loading">Carregando categoria...</div>

    <div v-else class="form-layout">
      <div class="form-main">
        <div class="sidebar-card">
          <h3>Detalhes</h3>

          <div class="field">
            <label>Nome <span class="required">*</span></label>
            <input v-model="form.name" type="text" placeholder="Ex: Crédito, Programa..." required />
          </div>

          <div class="field">
            <label>Slug</label>
            <input :value="slug" type="text" disabled class="slug-field" />
            <span class="hint">Gerado automaticamente a partir do nome</span>
          </div>

          <div class="field">
            <label>Descrição</label>
            <textarea v-model="form.description" rows="3" placeholder="Breve descrição da categoria (opcional)"></textarea>
          </div>

          <div class="field">
            <label>Ordem</label>
            <input v-model.number="form.order" type="number" min="0" />
            <span class="hint">Define a ordem de exibição</span>
          </div>

          <div class="field-checkbox">
            <label>
              <input type="checkbox" v-model="form.active" />
              Categoria ativa
            </label>
            <span class="hint">Categorias inativas não aparecem para seleção</span>
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
import api from '@/services/api'

const router = useRouter()
const route = useRoute()

const isEdit = computed(() => !!route.params.id)
const loading = ref(false)
const saving = ref(false)
const error = ref('')

const form = ref({
  name: '',
  description: '',
  order: 0,
  active: true,
})

const slug = computed(() => {
  return form.value.name
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^\w\s-]/g, '')
    .replace(/[\s_]+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '')
})

onMounted(async () => {
  if (isEdit.value) {
    loading.value = true
    try {
      const { data } = await api.get(`/api/categories/${route.params.id}`)
      form.value = {
        name: data.name,
        description: data.description || '',
        order: data.order,
        active: data.active,
      }
    } catch (err) {
      error.value = 'Erro ao carregar categoria'
      console.error(err)
    } finally {
      loading.value = false
    }
  }
})

async function handleSave() {
  if (!form.value.name.trim()) {
    error.value = 'Nome é obrigatório'
    return
  }

  saving.value = true
  error.value = ''

  try {
    const payload = {
      name: form.value.name.trim(),
      description: form.value.description.trim() || null,
      order: form.value.order,
      active: form.value.active,
    }

    if (isEdit.value) {
      await api.put(`/api/categories/${route.params.id}`, payload)
    } else {
      await api.post('/api/categories/', payload)
    }
    router.push('/categories')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erro ao salvar categoria'
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
.slug-field {
  background: #f8fafc !important;
  color: #64748b !important;
  cursor: not-allowed;
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
.error-message {
  margin-top: 16px;
  padding: 12px 16px;
  background: #fef2f2;
  color: #dc2626;
  border-radius: 8px;
  font-size: 14px;
}
</style>
