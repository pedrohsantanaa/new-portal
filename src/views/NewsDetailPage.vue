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
          :src="(news.image_url || defaultImage) + cacheBust"
          :alt="news.title"
          class="hero-image"
          @error="handleImageError($event)"
        />
      </div>

      <div class="container detail-content">
        <div class="detail-header">
          <span class="tag">{{ news.category }}</span>
          <h1>{{ news.title }}</h1>
          <div class="meta">
            <span v-if="news.author">Por {{ news.author }}</span>
            <span v-if="news.author">·</span>
            <span>{{ formatDate(news.published_at || news.created_at) }}</span>
          </div>
        </div>

        <div class="detail-body">
          <p class="summary" v-if="news.summary">{{ news.summary }}</p>
          <div class="content-text" v-html="formattedContent"></div>
        </div>

        <!-- Notícias relacionadas -->
        <div v-if="relatedNews.length" class="related-section">
          <h2>Notícias relacionadas</h2>
          <div class="related-grid">
            <article
              v-for="item in relatedNews"
              :key="item.id"
              class="related-card"
              @click="goToRelated(item.slug)"
            >
              <div class="related-image">
                <img
                  :src="(item.image_url || defaultImage) + cacheBust"
                  :alt="item.title"
@error="handleImageError($event)"
                />
              </div>
              <div class="related-content">
                <span class="related-tag">{{ item.category }}</span>
                <h3>{{ item.title }}</h3>
                <span class="related-date">{{ formatDate(item.published_at || item.created_at) }}</span>
              </div>
            </article>
          </div>
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
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'
import { sanitize } from '@/utils/sanitize'

const route = useRoute()
const router = useRouter()

const news = ref(null)
const relatedNews = ref([])
const loading = ref(true)
const error = ref('')

const defaultImage = 'https://placehold.co/1200x800/e2e8f0/64748b?text=Sem+Imagem'
const cacheBust = '?v=' + Date.now()

const formattedContent = computed(() => {
  if (!news.value?.content) return ''
  return sanitize(news.value.content)
})

async function fetchNews(slug) {
  loading.value = true
  error.value = ''
  news.value = null
  relatedNews.value = []
  try {
    const { data } = await api.get(`/api/news/${slug}`)
    news.value = data
    fetchRelated(slug)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Erro ao carregar notícia.'
  } finally {
    loading.value = false
  }
}

async function fetchRelated(slug) {
  try {
    const { data } = await api.get(`/api/news/${slug}/related`)
    relatedNews.value = data
  } catch {
    relatedNews.value = []
  }
}

function goToRelated(slug) {
  router.push(`/noticias/${slug}`)
}

function handleImageError(e) {
  if (e.target.src !== defaultImage) {
    e.target.src = defaultImage
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

onMounted(() => fetchNews(route.params.slug))

watch(() => route.params.slug, (newSlug) => {
  if (newSlug) fetchNews(newSlug)
})
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
  display: flex;
  gap: 8px;
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

.content-text :deep(h2) {
  font-size: 1.6rem;
  color: #011a4f;
  margin: 2em 0 0.8em;
  font-weight: 700;
  line-height: 1.3;
}

.content-text :deep(h3) {
  font-size: 1.35rem;
  color: #011a4f;
  margin: 1.8em 0 0.6em;
  font-weight: 600;
  line-height: 1.4;
}

.content-text :deep(h4) {
  font-size: 1.15rem;
  color: #011a4f;
  margin: 1.5em 0 0.5em;
  font-weight: 600;
}

.content-text :deep(p) {
  margin-bottom: 1.2em;
}

.content-text :deep(ul),
.content-text :deep(ol) {
  margin: 1em 0;
  padding-left: 1.8em;
}

.content-text :deep(li) {
  margin-bottom: 0.5em;
}

.content-text :deep(blockquote) {
  border-left: 4px solid #083ea8;
  padding: 16px 24px;
  margin: 1.5em 0;
  background: #f8fafc;
  border-radius: 0 8px 8px 0;
  font-style: italic;
  color: #334155;
}

.content-text :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin: 1.5em 0;
}

.content-text :deep(code) {
  background: #f1f5f9;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.9em;
}

.content-text :deep(pre) {
  background: #1e293b;
  color: #e2e8f0;
  padding: 16px 20px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 1.5em 0;
}

.content-text :deep(pre code) {
  background: none;
  padding: 0;
  color: inherit;
}

/* RELATED */
.related-section {
  margin-top: 60px;
  padding-top: 40px;
  border-top: 1px solid #e2e8f0;
}

.related-section h2 {
  font-size: 1.5rem;
  color: #011a4f;
  margin-bottom: 24px;
}

.related-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.related-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  cursor: pointer;
  transition: all 0.3s;
}

.related-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.related-image {
  height: 140px;
  overflow: hidden;
}

.related-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.related-content {
  padding: 16px;
}

.related-tag {
  display: inline-block;
  background: #eff6ff;
  color: #083ea8;
  padding: 3px 10px;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 600;
  margin-bottom: 8px;
}

.related-content h3 {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  line-height: 1.4;
  margin-bottom: 8px;
}

.related-date {
  font-size: 12px;
  color: #94a3b8;
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

@media (max-width: 768px) {
  .hero-image {
    height: 280px;
  }

  .detail-content {
    padding: 32px 16px 60px;
  }

  .related-grid {
    grid-template-columns: 1fr;
  }
}

/* ALTO CONTRASTE */
:global(html.high-contrast) .related-card {
  background: var(--color-bg) !important;
}
:global(html.high-contrast) .tag {
  background: var(--color-accent) !important;
}
:global(html.high-contrast) .related-tag {
  background: var(--color-bg-alt) !important;
}
:global(html.high-contrast) .btn-back:hover {
  background: var(--color-accent) !important;
}
:global(html.high-contrast) .content-text :deep(blockquote) {
  background: var(--color-bg-alt) !important;
}
:global(html.high-contrast) .content-text :deep(code) {
  background: var(--color-bg-alt) !important;
}
:global(html.high-contrast) .content-text :deep(pre) {
  background: #000000 !important;
}
</style>
