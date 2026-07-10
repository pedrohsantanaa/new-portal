<template>
  <div class="dashboard">
    <h1>Dashboard</h1>
    <p class="subtitle">Visão geral do portal</p>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon news-icon"><Newspaper :size="24" /></div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.news }}</span>
          <span class="stat-label">Notícias</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon published-icon"><CheckCircle :size="24" /></div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.published }}</span>
          <span class="stat-label">Publicadas</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon draft-icon"><FileEdit :size="24" /></div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.drafts }}</span>
          <span class="stat-label">Rascunhos</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon credit-icon"><Coins :size="24" /></div>
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
import { Newspaper, CheckCircle, FileEdit, Coins } from 'lucide-vue-next'

const stats = ref({ news: 0, published: 0, drafts: 0, creditLines: 0 })

onMounted(async () => {
  try {
    const [allRes, pubRes, draftRes, creditRes] = await Promise.all([
      api.get('/api/news/?limit=1'),
      api.get('/api/news/?limit=1&published_only=true'),
      api.get('/api/news/?limit=50'),
      api.get('/api/credit-lines/?limit=1'),
    ])
    stats.value.news = allRes.data.total
    stats.value.published = pubRes.data.total
    stats.value.drafts = allRes.data.total - pubRes.data.total
    stats.value.creditLines = creditRes.data.total
  } catch (e) {
  }
})
</script>

<style scoped>
.dashboard h1 {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
}

.subtitle {
  font-size: 14px;
  color: #64748b;
  margin-top: 4px;
  margin-bottom: 28px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
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
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.news-icon {
  background: #eff6ff;
  color: #083ea8;
}

.published-icon {
  background: #f0fdf4;
  color: #16a34a;
}

.draft-icon {
  background: #fefce8;
  color: #ca8a04;
}

.credit-icon {
  background: #faf5ff;
  color: #9333ea;
}

.stat-value {
  display: block;
  font-size: 28px;
  font-weight: 700;
  color: #1e293b;
}

.stat-label {
  color: #64748b;
  font-size: 14px;
}
</style>
