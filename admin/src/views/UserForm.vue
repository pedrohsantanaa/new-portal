<template>
  <div class="user-form-page">
    <div class="form-top-actions">
      <button type="button" class="btn-cancel" @click="router.push('/users')">Cancelar</button>
      <button type="button" class="btn-save" :disabled="saving" @click="handleSave">
        {{ saving ? 'Salvando...' : (isEdit ? 'Salvar alteracoes' : 'Criar usuario') }}
      </button>
    </div>

    <div v-if="loading" class="loading">Carregando usuario...</div>

    <div v-else class="form-layout">
      <!-- Dados do usuario -->
      <div class="form-main">
        <div class="sidebar-card">
          <h3>Dados do usuario</h3>

          <div class="field">
            <label>Nome completo</label>
            <input v-model="form.name" type="text" placeholder="Nome do usuario" />
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
              Usuario ativo
            </label>
          </div>
        </div>

        <!-- 2FA Section -->
        <div v-if="isEdit && savedUserId" class="sidebar-card twofa-card">
          <h3>
            <ShieldCheck :size="20" />
            Autenticacao em Dois Fatores
          </h3>

          <!-- Ja tem 2FA ativo -->
          <div v-if="userTwoFactorEnabled" class="twofa-active">
            <div class="twofa-status">
              <CheckCircle :size="20" class="icon-success" />
              <span>2FA esta ativo para este usuario</span>
            </div>
            <p class="twofa-hint">O usuario precisara digitar um codigo do Google Authenticator a cada login.</p>
            <button type="button" class="btn-disable-2fa" @click="handleDisable2FA" :disabled="loading2fa">
              {{ loading2fa ? 'Desativando...' : 'Desativar 2FA' }}
            </button>
          </div>

          <!-- Setup 2FA -->
          <div v-else>
            <div v-if="!setupSecret" class="twofa-setup-start">
              <p>Ative a autenticacao de dois fatores para aumentar a seguranca da conta deste usuario.</p>
              <button type="button" class="btn-setup-2fa" @click="handleSetup2FA" :disabled="loading2fa">
                {{ loading2fa ? 'Gerando...' : 'Gerar QR Code' }}
              </button>
            </div>

            <!-- QR Code -->
            <div v-else class="twofa-qr-section">
              <div class="twofa-steps">
                <p><strong>Como configurar:</strong></p>
                <ol>
                  <li>Abra o <strong>Google Authenticator</strong> no celular</li>
                  <li>Toque em <strong>"Adicionar conta"</strong> (+)</li>
                  <li>Toque em <strong>"Escanear codigo QR"</strong></li>
                  <li>Escaneie o QR Code ao lado</li>
                  <li>Digite o codigo de 6 digitos abaixo</li>
                </ol>
              </div>

              <div class="twofa-qr-and-code">
                <div class="qr-container">
                  <canvas ref="qrCanvas"></canvas>
                  <p class="qr-secret">Manual: <code>{{ setupSecret }}</code></p>
                </div>

                <div class="twofa-verify">
                  <div class="field">
                    <label>Codigo de 6 digitos</label>
                    <input
                      v-model="verifyCode"
                      type="text"
                      inputmode="numeric"
                      pattern="[0-9]*"
                      maxlength="6"
                      placeholder="000000"
                      class="totp-input"
                    />
                  </div>
                  <button
                    type="button"
                    class="btn-verify-2fa"
                    @click="handleVerify2FA"
                    :disabled="loading2fa || verifyCode.length !== 6"
                  >
                    {{ loading2fa ? 'Verificando...' : 'Confirmar e Ativar' }}
                  </button>
                  <button type="button" class="btn-cancel-2fa" @click="cancelSetup" :disabled="loading2fa">
                    Cancelar
                  </button>
                </div>
              </div>

              <div v-if="twofaSuccess" class="twofa-success">
                <CheckCircle :size="20" />
                2FA ativado com sucesso!
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Permissoes -->
      <div class="form-sidebar">
        <div class="sidebar-card">
          <h3>Permissoes de acesso</h3>
          <p class="perms-description">Selecione quais telas este usuario pode acessar:</p>

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
            <span>Nenhuma permissao = usuario nao acessa o painel</span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="error" class="error-message">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ShieldCheck, CheckCircle } from 'lucide-vue-next'
import QRCode from 'qrcode'
import api from '@/services/api'

const router = useRouter()
const route = useRoute()

const isEdit = computed(() => !!route.params.id)
const loading = ref(false)
const saving = ref(false)
const error = ref('')
const availablePermissions = ref([])

const savedUserId = ref(null)
const userTwoFactorEnabled = ref(false)

const setupSecret = ref('')
const verifyCode = ref('')
const loading2fa = ref(false)
const twofaSuccess = ref(false)
const qrCanvas = ref(null)

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
      savedUserId.value = data.id
      userTwoFactorEnabled.value = data.two_factor_enabled
    } catch (err) {
      error.value = 'Erro ao carregar usuario'
    } finally {
      loading.value = false
    }
  }
})

async function handleSave() {
  if (!form.value.email.trim()) {
    error.value = 'E-mail e obrigatorio'
    return
  }
  if (!isEdit.value && !form.value.password) {
    error.value = 'Senha e obrigatoria'
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
      const { data } = await api.post('/api/users/', payload)
      savedUserId.value = data.id
    }
    if (!isEdit.value) {
      router.push(`/users/${savedUserId.value}/edit`)
    }
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erro ao salvar usuario'
  } finally {
    saving.value = false
  }
}

async function handleSetup2FA() {
  loading2fa.value = true
  error.value = ''
  twofaSuccess.value = false
  try {
    const { data } = await api.post(`/api/users/${savedUserId.value}/setup-2fa`)
    setupSecret.value = data.secret
    await nextTick()
    if (qrCanvas.value) {
      QRCode.toCanvas(qrCanvas.value, data.otpauth_url, {
        width: 180,
        margin: 2,
        color: { dark: '#1e293b', light: '#ffffff' },
      })
    }
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erro ao gerar QR Code'
  } finally {
    loading2fa.value = false
  }
}

async function handleVerify2FA() {
  loading2fa.value = true
  error.value = ''
  try {
    await api.post(`/api/users/${savedUserId.value}/verify-2fa`, {
      code: verifyCode.value,
    })
    userTwoFactorEnabled.value = true
    twofaSuccess.value = true
    setupSecret.value = ''
    verifyCode.value = ''
  } catch (err) {
    error.value = err.response?.data?.detail || 'Codigo invalido'
  } finally {
    loading2fa.value = false
  }
}

async function handleDisable2FA() {
  if (!confirm('Tem certeza que deseja desativar o 2FA deste usuario?')) return
  loading2fa.value = true
  error.value = ''
  try {
    await api.post(`/api/users/${savedUserId.value}/disable-2fa`)
    userTwoFactorEnabled.value = false
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erro ao desativar 2FA'
  } finally {
    loading2fa.value = false
  }
}

function cancelSetup() {
  setupSecret.value = ''
  verifyCode.value = ''
  twofaSuccess.value = false
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
  display: flex;
  align-items: center;
  gap: 8px;
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

/* 2FA Styles */
.twofa-card {
  margin-top: 24px;
  border: 2px solid #e2e8f0;
}
.twofa-active {
  text-align: center;
}
.twofa-status {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  background: #f0fdf4;
  border-radius: 8px;
  margin-bottom: 12px;
}
.icon-success {
  color: #16a34a;
}
.twofa-hint {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 16px;
}
.btn-disable-2fa {
  padding: 8px 16px;
  border: 1px solid #fecaca;
  border-radius: 8px;
  background: #fef2f2;
  color: #dc2626;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-disable-2fa:hover {
  background: #fee2e2;
}
.twofa-setup-start {
  text-align: center;
}
.twofa-setup-start p {
  font-size: 14px;
  color: #64748b;
  margin-bottom: 16px;
}
.btn-setup-2fa {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  background: #011a4f;
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
}
.btn-setup-2fa:hover {
  background: #0a2d6a;
}
.twofa-qr-section {
  text-align: center;
}
.twofa-steps {
  text-align: left;
  margin-bottom: 20px;
  font-size: 14px;
  color: #475569;
}
.twofa-steps ol {
  margin: 8px 0 0 20px;
  padding: 0;
}
.twofa-steps li {
  margin-bottom: 6px;
}
.twofa-qr-and-code {
  display: flex;
  gap: 24px;
  align-items: flex-start;
  margin-bottom: 20px;
}
@media (max-width: 600px) {
  .twofa-qr-and-code {
    flex-direction: column;
    align-items: center;
  }
}
.qr-container {
  flex-shrink: 0;
}
.qr-container canvas {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
}
.qr-secret {
  font-size: 11px;
  color: #94a3b8;
  margin-top: 8px;
  word-break: break-all;
}
.qr-secret code {
  font-size: 10px;
  background: #f1f5f9;
  padding: 2px 4px;
  border-radius: 3px;
}
.twofa-verify {
  flex: 1;
  text-align: left;
}
.totp-input {
  text-align: center;
  font-size: 22px !important;
  letter-spacing: 6px;
  font-weight: 700;
}
.btn-verify-2fa {
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 8px;
  background: #16a34a;
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  margin-top: 8px;
}
.btn-verify-2fa:hover {
  background: #15803d;
}
.btn-verify-2fa:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.btn-cancel-2fa {
  width: 100%;
  padding: 8px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: white;
  color: #64748b;
  font-size: 13px;
  cursor: pointer;
  margin-top: 8px;
}
.twofa-success {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  background: #f0fdf4;
  color: #16a34a;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  margin-top: 16px;
}
</style>
