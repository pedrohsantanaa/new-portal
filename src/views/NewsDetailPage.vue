<template>
  <div class="detail-page">
    <!-- Loading -->
    <div v-if="loading" class="loading">Carregando notícia...</div>

    <!-- Erro -->
    <div v-else-if="error" class="error-container">
      <h2>Notícia não encontrada</h2>
      <p>{{ error }}</p>
      <router-link to="/noticias" class="btn-back">← Voltar para Notícias</router-link>
    </div>

    <!-- Conteúdo -->
    <template v-else-if="news">
      <div class="detail-hero">
        <img
          :src="news.image_url || defaultImage"
          :alt="news.title"
          class="hero-image"
          @error="$event.target.src = defaultImage"
        />
      </div>

      <div class="container detail-content">
        <div class="detail-header">
          <span class="tag">{{ news.category }}</span>
          <h1>{{ news.title }}</h1>
          <div class="meta">
            <span>{{ formatDate(news.published_at || news.created_at) }}</span>
          </div>
        </div>

        <div class="detail-body">
          <p class="summary">{{ news.summary }}</p>
          <div class="content-text" v-html="formattedContent"></div>
        </div>

        <div class="detail-footer">
          <router-link to="/noticias" class="btn-back">
            ← Voltar para Notícias
          </router-link>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/services/api'

const route = useRoute()

const news = ref(null)
const loading = ref(true)
const error = ref('')

const defaultImage = 'https://images.unsplash.com/photo-1504711434969-e33886168d6c?w=1200'

const formattedContent = computed(() => {
  if (!news.value?.content) return ''
  return news.value.content.replace(/\n/g, '<br>')
})

async function fetchNews() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.get(`/api/news/${route.params.slug}`)
    news.value = data
  } catch (e) {
    error.value = e.response?.data?.detail || 'Erro ao carregar notícia.'
  } finally {
    loading.value = false
  }
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
  })
}

onMounted(fetchNews)
</script>

<style scoped>
.detail-page {
  min-height: 100vh;
}

.detail-hero {
  width: 100%;
  max-height: 480px;
  overflow: hidden;
}

.hero-image {
  width: 100%;
  height: 480px;
  object-fit: cover;
}

.detail-content {
  max-width: 800px;
  padding: 48px 20px 80px;
}

.detail-header {
  margin-bottom: 40px;
}

.tag {
  display: inline-block;
  background: #083ea8;
  color: white;
  padding: 6px 16px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 16px;
}

.detail-header h1 {
  font-size: clamp(1.8rem, 4vw, 2.8rem);
  color: #011a4f;
  line-height: 1.3;
  margin-bottom: 16px;
}

.meta {
  color: #64748b;
  font-size: 15px;
}

.detail-body {
  margin-bottom: 48px;
}

.summary {
  font-size: 1.2rem;
  color: #334155;
  line-height: 1.7;
  margin-bottom: 32px;
  padding-bottom: 32px;
  border-bottom: 1px solid #e2e8f0;
  font-weight: 500;
}

.content-text {
  font-size: 1.05rem;
  color: #475569;
  line-height: 1.8;
}

.detail-footer {
  padding-top: 32px;
  border-top: 1px solid #e2e8f0;
}

.btn-back {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #083ea8;
  text-decoration: none;
  font-weight: 600;
  font-size: 15px;
  padding: 12px 24px;
  border: 2px solid #083ea8;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.btn-back:hover {
  background: #083ea8;
  color: white;
}

/* LOADING / ERROR */
.loading {
  text-align: center;
  padding: 120px 20px;
  font-size: 16px;
  color: #64748b;
}

.error-container {
  text-align: center;
  padding: 120px 20px;
}

.error-container h2 {
  color: #011a4f;
  margin-bottom: 12px;
}

.error-container p {
  color: #64748b;
  margin-bottom: 24px;
}

/* RESPONSIVO */
@media (max-width: 768px) {
  .hero-image {
    height: 280px;
  }

  .detail-content {
    padding: 32px 16px 60px;
  }
}
</style>
