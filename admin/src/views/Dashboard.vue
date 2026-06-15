<template>
  <div class="dashboard">
    <h1>Dashboard</h1>
    <div class="stats-grid">
      <div class="stat-card">
        <span class="stat-icon">📰</span>
        <div class="stat-info">
          <span class="stat-value">{{ stats.news }}</span>
          <span class="stat-label">Notícias</span>
        </div>
      </div>
      <div class="stat-card">
        <span class="stat-icon">💰</span>
        <div class="stat-info">
          <span class="stat-value">{{ stats.creditLines }}</span>
          <span class="stat-label">Linhas de Crédito</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const stats = ref({ news: 0, creditLines: 0 })

onMounted(async () => {
  try {
    const [newsRes, creditRes] = await Promise.all([
      api.get('/api/news/?limit=1'),
      api.get('/api/credit-lines/?limit=1'),
    ])
    stats.value.news = newsRes.data.total
    stats.value.creditLines = creditRes.data.total
  } catch (e) {
    console.error('Erro ao carregar stats', e)
  }
})
</script>

<style scoped>
.dashboard h1 {
  margin-bottom: 24px;
  color: #011a4f;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
}

.stat-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.stat-icon {
  font-size: 36px;
}

.stat-value {
  display: block;
  font-size: 32px;
  font-weight: 700;
  color: #011a4f;
}

.stat-label {
  color: #64748b;
  font-size: 14px;
}
</style>
