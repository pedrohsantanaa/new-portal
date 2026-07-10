<template>
  <div class="user-form-page">
    <div class="form-top-actions">
      <button type="button" class="btn-cancel" @click="router.push('/users')">Cancelar</button>
      <button type="button" class="btn-save" :disabled="saving" @click="handleSave">
        {{ saving ? 'Salvando...' : (isEdit ? 'Salvar alterações' : 'Criar usuário') }}
      </button>
    </div>

    <div v-if="loading" class="loading">Carregando usuário...</div>

    <div v-else class="form-layout">
      <!-- Dados do usuário -->
      <div class="form-main">
        <div class="sidebar-card">
          <h3>Dados do usuário</h3>

          <div class="field">
            <label>Nome completo</label>
            <input v-model="form.name" type="text" placeholder="Nome do usuário" />
          </div>

          <div class="field">
            <label>E-mail <span class="required">*</span></label>
            <input v-model="form.email" type="email" placeholder="email@exemplo.com" required />
          </div>

          <div class="field">
            <label>{{ isEdit ? 'Nova senha (deixe vazio para manter)' : 'Senha' }} <span v-if="!isEdit" class="required">*</span></label>
            <input v-model="form.password" type="password" :placeholder="isEdit ? '••••••••' : 'Digite a senha'" :required="!isEdit" />
          </div>

          <div class="field-checkbox">
            <label>
              <input type="checkbox" v-model="form.is_active" />
              Usuário ativo
            </label>
          </div>
        </div>
      </div>

      <!-- Permissões -->
      <div class="form-sidebar">
        <div class="sidebar-card">
          <h3>Permissões de acesso</h3>
          <p class="perms-description">Selecione quais telas este usuário pode acessar:</p>

          <div class="permissions-grid">
            <label v-for="perm in availablePermissions" :key="perm.id" class="perm-checkbox">
              <input
                type="checkbox"
                :value="perm.id"
                v-model="form.permission_ids"
              />
              <div class="perm-info">
                <span class="perm-name">{{ perm.name }}</span>
                <span class="perm-code">{{ perm.codename }}</span>
              </div>
            </label>
          </div>

          <div class="perm-legend">
            <span>Nenhuma permissão = usuário não acessa o painel</span>
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
const availablePermissions = ref([])

const form = ref({
  name: '',
  email: '',
  password: '',
  is_active: true,
  permission_ids: [],
})

onMounted(async () => {
  try {
    const { data: perms } = await api.get('/api/users/permissions')
    availablePermissions.value = perms
  } catch (err) {
  }

  if (isEdit.value) {
    loading.value = true
    try {
      const { data } = await api.get(`/api/users/${route.params.id}`)
      form.value = {
        name: data.name || '',
        email: data.email,
        password: '',
        is_active: data.is_active,
        permission_ids: data.permissions.map(p => p.id),
      }
    } catch (err) {
      error.value = 'Erro ao carregar usuário'
    } finally {
      loading.value = false
    }
  }
})

async function handleSave() {
  if (!form.value.email.trim()) {
    error.value = 'E-mail é obrigatório'
    return
  }
  if (!isEdit.value && !form.value.password) {
    error.value = 'Senha é obrigatória'
    return
  }

  saving.value = true
  error.value = ''

  try {
    const payload = {
      name: form.value.name.trim() || null,
      email: form.value.email.trim(),
      is_active: form.value.is_active,
      permission_ids: form.value.permission_ids,
    }

    if (form.value.password) {
      payload.password = form.value.password
    }

    if (isEdit.value) {
      await api.put(`/api/users/${route.params.id}`, payload)
    } else {
      await api.post('/api/users/', payload)
    }
    router.push('/users')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erro ao salvar usuário'
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
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}
@media (max-width: 900px) {
  .form-layout {
    grid-template-columns: 1fr;
  }
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
  margin: 0 0 16px;
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
.field input[type="email"],
.field input[type="password"] {
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
.field input:focus {
  border-color: #011a4f;
}
.required {
  color: #dc2626;
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
.perms-description {
  font-size: 13px;
  color: #64748b;
  margin: -8px 0 16px;
}
.permissions-grid {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.perm-checkbox {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}
.perm-checkbox:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
}
.perm-checkbox input[type="checkbox"] {
  width: 16px;
  height: 16px;
  accent-color: #011a4f;
  flex-shrink: 0;
}
.perm-info {
  display: flex;
  flex-direction: column;
}
.perm-name {
  font-size: 14px;
  font-weight: 500;
  color: #1e293b;
}
.perm-code {
  font-size: 11px;
  color: #94a3b8;
}
.perm-legend {
  margin-top: 12px;
  font-size: 12px;
  color: #94a3b8;
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
