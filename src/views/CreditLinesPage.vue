<template>
  <div class="credit-lines-page">
    <div class="credit-hero">
      <div class="container">
        <h1>Linhas de Crédito</h1>
        <p>Conheça nossas opções de crédito para impulsionar seu negócio.</p>
      </div>
    </div>

    <div class="container credit-content">
      <div v-if="loading" class="loading">Carregando linhas de crédito...</div>

      <div v-else-if="error" class="error">{{ error }}</div>

      <div v-else-if="creditLines.length" class="credit-grid">
        <div
          v-for="credit in creditLines"
          :key="credit.id"
          class="credit-card"
        >
          <div class="icon-box" :style="{ background: credit.color }">
            <img
              v-if="credit.icon_url"
              :src="credit.icon_url"
              :alt="credit.title"
              class="icon-image"
            />
          </div>
          <div class="card-text">
            <h3>{{ credit.title }}</h3>
            <p>{{ credit.description }}</p>
          </div>
          <router-link :to="'/linhas-de-credito/' + credit.slug" class="saiba-mais">
            Saiba Mais ›
          </router-link>
        </div>
      </div>

      <div v-else class="empty">
        Nenhuma linha de crédito disponível no momento.
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const creditLines = ref([])
const loading = ref(true)
const error = ref('')

async function fetchCreditLines() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.get('/api/credit-lines/?active_only=true&limit=50')
    creditLines.value = data.items
  } catch (e) {
    error.value = 'Erro ao carregar linhas de crédito. Tente novamente.'
    console.error(e)
  } finally {
    loading.value = false
  }
}

onMounted(fetchCreditLines)
</script>

<style scoped>
.credit-lines-page {
  min-height: 100vh;
}

.credit-hero {
  background: linear-gradient(135deg, #011a4f 0%, #083ea8 100%);
  color: white;
  padding: 80px 0 60px;
}

.credit-hero h1 {
  font-size: clamp(2rem, 5vw, 3.5rem);
    color: white;
  margin-bottom: 12px;
}

.credit-hero p {
  font-size: 1.1rem;
  opacity: 0.85;
}

.credit-content {
  padding: 40px 20px 80px;
}

.credit-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 28px;
}

.credit-card {
  background: white;
  border-radius: 16px;
  padding: 28px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
}

.credit-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12);
}

.icon-box {
  width: 80px;
  height: 80px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
  overflow: hidden;
}

.icon-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-text {
  flex: 1;
  margin-bottom: 20px;
}

.card-text h3 {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 8px;
}

.card-text p {
  font-size: 15px;
  color: #64748b;
  line-height: 1.6;
}

.saiba-mais {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #ffc107;
  color: #000;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 15px;
  text-decoration: none;
  transition: all 0.3s ease;
}

.saiba-mais:hover {
  background: #e6ac00;
  transform: translateY(-2px);
}

.loading,
.error,
.empty {
  text-align: center;
  padding: 60px 20px;
  font-size: 16px;
}

.error {
  color: #dc2626;
}

.empty {
  color: #64748b;
}

@media (max-width: 992px) {
  .credit-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .credit-hero {
    padding: 60px 0 40px;
  }

  .credit-grid {
    grid-template-columns: 1fr;
  }
}
</style>
