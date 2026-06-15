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
        <textarea v-model="form.details" rows="6"></textarea>
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
        <label>URL do Ícone (opcional)</label>
        <input v-model="form.icon_url" type="text" placeholder="/icons/..." />
      </div>

      <div class="field checkbox-field">
        <label>
          <input v-model="form.active" type="checkbox" />
          Ativo
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

const isEdit = computed(() => !!route.params.id)
const saving = ref(false)

const form = ref({
  title: '',
  description: '',
  details: '',
  color: '#EEF4FF',
  order: 0,
  icon_url: '',
  active: true,
})

onMounted(async () => {
  if (isEdit.value) {
    try {
      const { data } = await api.get(`/api/credit-lines/${route.params.id}`)
      form.value = {
        title: data.title,
        description: data.description,
        details: data.details || '',
        color: data.color,
        order: data.order,
        icon_url: data.icon_url || '',
        active: data.active,
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
    if (isEdit.value) {
      await api.put(`/api/credit-lines/${route.params.id}`, form.value)
    } else {
      await api.post('/api/credit-lines/', form.value)
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
