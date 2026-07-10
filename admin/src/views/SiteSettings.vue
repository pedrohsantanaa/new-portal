<template>
  <div class="settings-page">
    <div class="page-header">
      <div>
        <h1>Configurações do Site</h1>
        <p class="subtitle">Controle a visibilidade de seções e páginas do portal</p>
      </div>
      <button class="btn-save" :disabled="saving" @click="handleSave">
        {{ saving ? 'Salvando...' : 'Salvar Alterações' }}
      </button>
    </div>

    <div v-if="loading" class="loading">Carregando configurações...</div>

    <div v-else class="settings-groups">
      <div class="settings-group">
        <h2>Seções da Home</h2>
        <p class="group-description">Controle quais seções aparecem na página inicial</p>
        <div class="settings-list">
          <label v-for="setting in homeSettings" :key="setting.key" class="setting-toggle">
            <div class="toggle-info">
              <span class="toggle-label">{{ setting.label }}</span>
              <span class="toggle-key">{{ setting.key }}</span>
            </div>
            <div class="toggle-switch">
              <input type="checkbox" v-model="setting.value" />
              <span class="toggle-slider"></span>
            </div>
          </label>
        </div>
      </div>

      <div class="settings-group">
        <h2>Páginas</h2>
        <p class="group-description">Controle quais páginas estão disponíveis no site</p>
        <div class="settings-list">
          <label v-for="setting in pageSettings" :key="setting.key" class="setting-toggle">
            <div class="toggle-info">
              <span class="toggle-label">{{ setting.label }}</span>
              <span class="toggle-key">{{ setting.key }}</span>
            </div>
            <div class="toggle-switch">
              <input type="checkbox" v-model="setting.value" />
              <span class="toggle-slider"></span>
            </div>
          </label>
        </div>
      </div>

      <div class="settings-group">
        <h2>Menu de Navegação</h2>
        <p class="group-description">Controle quais links aparecem no menu principal</p>
        <div class="settings-list">
          <label v-for="setting in navSettings" :key="setting.key" class="setting-toggle">
            <div class="toggle-info">
              <span class="toggle-label">{{ setting.label }}</span>
              <span class="toggle-key">{{ setting.key }}</span>
            </div>
            <div class="toggle-switch">
              <input type="checkbox" v-model="setting.value" />
              <span class="toggle-slider"></span>
            </div>
          </label>
        </div>
      </div>
    </div>

    <div v-if="successMessage" class="toast-success">{{ successMessage }}</div>
    <div v-if="error" class="toast-error">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'

const settings = ref([])
const loading = ref(true)
const saving = ref(false)
const error = ref('')
const successMessage = ref('')

const homeSettings = computed(() => settings.value.filter(s => s.group === 'home'))
const pageSettings = computed(() => settings.value.filter(s => s.group === 'pages'))
const navSettings = computed(() => settings.value.filter(s => s.group === 'nav'))

async function loadSettings() {
  loading.value = true
  try {
    const { data } = await api.get('/api/site-settings/')
    settings.value = data.map(s => ({ ...s }))
  } catch (err) {
    error.value = 'Erro ao carregar configurações'
  } finally {
    loading.value = false
  }
}

async function handleSave() {
  saving.value = true
  error.value = ''
  successMessage.value = ''

  try {
    const payload = {
      settings: settings.value.map(s => ({ key: s.key, value: s.value }))
    }
    await api.put('/api/site-settings/', payload)
    successMessage.value = 'Configurações salvas com sucesso!'
    setTimeout(() => { successMessage.value = '' }, 3000)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erro ao salvar configurações'
  } finally {
    saving.value = false
  }
}

onMounted(loadSettings)
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
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
.btn-save {
  padding: 10px 24px;
  border: none;
  border-radius: 8px;
  background: #011a4f;
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
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
.settings-groups {
  display: flex;
  flex-direction: column;
  gap: 32px;
  max-width: 700px;
}
.settings-group {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}
.settings-group h2 {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 4px;
}
.group-description {
  font-size: 13px;
  color: #94a3b8;
  margin: 0 0 20px;
}
.settings-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.setting-toggle {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}
.setting-toggle:hover {
  background: #f8fafc;
}
.toggle-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.toggle-label {
  font-size: 14px;
  color: #1e293b;
  font-weight: 500;
}
.toggle-key {
  font-size: 12px;
  color: #94a3b8;
  font-family: monospace;
}
.toggle-switch {
  position: relative;
  width: 44px;
  height: 24px;
  flex-shrink: 0;
}
.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}
.toggle-slider {
  position: absolute;
  inset: 0;
  background: #e2e8f0;
  border-radius: 24px;
  transition: background 0.2s;
  cursor: pointer;
}
.toggle-slider::before {
  content: '';
  position: absolute;
  width: 18px;
  height: 18px;
  left: 3px;
  bottom: 3px;
  background: white;
  border-radius: 50%;
  transition: transform 0.2s;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.15);
}
.toggle-switch input:checked + .toggle-slider {
  background: #011a4f;
}
.toggle-switch input:checked + .toggle-slider::before {
  transform: translateX(20px);
}
.toast-success {
  position: fixed;
  bottom: 24px;
  right: 24px;
  padding: 12px 20px;
  background: #166534;
  color: white;
  border-radius: 8px;
  font-size: 14px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 100;
}
.toast-error {
  position: fixed;
  bottom: 24px;
  right: 24px;
  padding: 12px 20px;
  background: #dc2626;
  color: white;
  border-radius: 8px;
  font-size: 14px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 100;
}
</style>
