<template>
  <div class="login-page">
    <div class="login-card">
      <h1>Portal de Credito</h1>
      <p>Painel Administrativo</p>

      <!-- Passo 1: Email + Senha -->
      <form v-if="!auth.requires2fa" @submit.prevent="handleLogin">
        <div v-if="error" class="error">{{ error }}</div>
        <div class="field">
          <label>Email</label>
          <input v-model="email" type="email" required placeholder="admin@fomento.to.gov.br" />
        </div>
        <div class="field">
          <label>Senha</label>
          <input v-model="password" type="password" required placeholder="Sua senha" />
        </div>
        <button type="submit" :disabled="loading">
          {{ loading ? 'Entrando...' : 'Entrar' }}
        </button>
      </form>

      <!-- Passo 2: Codigo TOTP -->
      <form v-else @submit.prevent="handleVerify2FA">
        <div v-if="error" class="error">{{ error }}</div>
        <div class="twofa-info">
          <ShieldCheck :size="48" class="twofa-icon" />
          <h2>Verificacao em Dois Fatores</h2>
          <p>Abra o Google Authenticator no seu celular e digite o codigo de 6 digitos:</p>
        </div>
        <div class="field">
          <label>Codigo de Autenticacao</label>
          <input
            v-model="totpCode"
            type="text"
            inputmode="numeric"
            pattern="[0-9]*"
            maxlength="6"
            placeholder="000000"
            autocomplete="one-time-code"
            required
            class="totp-input"
          />
        </div>
        <button type="submit" :disabled="loading || totpCode.length !== 6">
          {{ loading ? 'Verificando...' : 'Verificar' }}
        </button>
        <button type="button" class="btn-back" @click="handleCancel" :disabled="loading">
          Voltar
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ShieldCheck } from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const email = ref('')
const password = ref('')
const totpCode = ref('')
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    const result = await auth.login(email.value, password.value)
    if (!result.requires_2fa) {
      router.push('/')
    }
  } catch (e) {
    error.value = e.response?.data?.detail || 'Erro ao fazer login'
  } finally {
    loading.value = false
  }
}

async function handleVerify2FA() {
  error.value = ''
  loading.value = true
  try {
    await auth.verifyTOTP(totpCode.value)
    router.push('/')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Codigo invalido'
  } finally {
    loading.value = false
  }
}

function handleCancel() {
  auth.cancel2FA()
  totpCode.value = ''
  error.value = ''
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-card {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.login-card h1 {
  font-size: 24px;
  color: #011a4f;
  margin-bottom: 4px;
}

.login-card > p {
  color: #64748b;
  margin-bottom: 24px;
}

.field {
  margin-bottom: 16px;
}

.field label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 6px;
  color: #334155;
}

.field input {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 15px;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.field input:focus {
  outline: none;
  border-color: #083ea8;
}

.totp-input {
  text-align: center;
  font-size: 24px !important;
  letter-spacing: 8px;
  font-weight: 700;
}

button {
  width: 100%;
  padding: 12px;
  background: #011a4f;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

button:hover {
  background: #083ea8;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-back {
  margin-top: 8px;
  background: transparent;
  color: #64748b;
  border: 1px solid #e2e8f0;
}

.btn-back:hover {
  background: #f8fafc;
  color: #334155;
}

.error {
  background: #fef2f2;
  color: #dc2626;
  padding: 10px 14px;
  border-radius: 8px;
  margin-bottom: 16px;
  font-size: 14px;
}

.twofa-info {
  text-align: center;
  margin-bottom: 24px;
}

.twofa-icon {
  color: #011a4f;
  margin-bottom: 12px;
}

.twofa-info h2 {
  font-size: 18px;
  color: #1e293b;
  margin: 0 0 8px;
}

.twofa-info p {
  font-size: 14px;
  color: #64748b;
  margin: 0;
  line-height: 1.5;
}
</style>
