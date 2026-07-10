<template>
  <section class="news-section">
    <div class="container">

      <!-- Header -->
      <div class="section-header">
        <div>
          <h2>Notícias em destaque</h2>
          <p>Fique por dentro das novidades e ações da instituição.</p>
        </div>
        <router-link to="/noticias" class="view-all">
          Ver todas →
        </router-link>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading">Carregando notícias...</div>

      <!-- Grid -->
      <div v-else class="news-grid">
        <article
          v-for="item in newsList"
          :key="item.id"
          class="news-card"
          @click="goToDetail(item.slug)"
        >
          <!-- Image -->
          <div class="image-wrapper">
            <img
              :src="(item.image_url || defaultImage) + cacheBust"
              :alt="item.title"
              @error="handleImageError"
            />
            <span class="tag">{{ item.category }}</span>
          </div>

          <!-- Content -->
          <div class="news-content">
            <h3>{{ item.title }}</h3>
            <p>{{ item.summary }}</p>
            <div class="news-footer">
              <div class="footer-left">
                <span v-if="item.author" class="author">Por {{ item.author }}</span>
                <span>{{ formatDate(item.published_at || item.created_at) }}</span>
              </div>
              <span class="read-more">Ler mais →</span>
            </div>
          </div>
        </article>
      </div>

    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const router = useRouter()

const newsList = ref([])
const loading = ref(true)
const defaultImage = 'https://placehold.co/1200x800/e2e8f0/64748b?text=Sem+Imagem'
const cacheBust = '?v=' + Date.now()

async function fetchNews() {
  loading.value = true
  try {
    const { data } = await api.get('/api/news/', {
      params: { published_only: true, limit: 4 }
    })
    newsList.value = data.items
  } catch (e) {
  } finally {
    loading.value = false
  }
}

function goToDetail(slug) {
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

onMounted(fetchNews)
</script>

<style scoped>
.news-section {
  padding: 80px 0;
  background: linear-gradient(180deg, #e8eef8 0%, #f8fafc 100%);
}

/* HEADER */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: end;
  margin-bottom: 40px;
}

.section-header h2 {
  font-size: clamp(1.8rem, 4vw, 3rem);
  color: var(--color-primary);
}

.section-header p {
  color: var(--color-text-muted);
  margin-top: 10px;
}

.view-all {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 600;
  font-size: 15px;
  padding: 10px 20px;
  border: 2px solid var(--color-primary);
  border-radius: var(--radius-sm);
  transition: var(--transition);
}

.view-all:hover {
  background: var(--color-primary);
  color: var(--color-white);
  transform: translateY(-2px);
}

/* GRID */
.news-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

/* CARD */
.news-card {
  background: var(--color-bg-card);
  border-radius: var(--radius-md);
  overflow: hidden;
  border: none;
  transition: var(--transition);
  cursor: pointer;
  box-shadow: var(--shadow-sm);
}

.news-card:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-md);
}

.image-wrapper {
  position: relative;
  overflow: hidden;
}

.image-wrapper img {
  width: 100%;
  height: 220px;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.news-card:hover .image-wrapper img {
  transform: scale(1.05);
}

/* TAG */
.tag {
  position: absolute;
  top: 16px;
  left: 16px;
  background: var(--color-accent);
  color: var(--color-white);
  padding: 8px 14px;
  border-radius: var(--radius-full);
  font-size: 13px;
  font-weight: 600;
}

/* CONTENT */
.news-content {
  padding: 24px;
}

.news-content h3 {
  color: var(--color-text);
  font-size: 18px;
  line-height: 1.5;
  margin-bottom: 10px;
  font-weight: 700;
}

.news-content p {
  color: var(--color-text-muted);
  line-height: 1.6;
  margin-bottom: 16px;
  font-size: 14px;
}

.news-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: var(--color-text-muted);
  font-size: 13px;
  padding-top: 14px;
  border-top: 1px solid var(--color-border);
}

.footer-left {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.author {
  font-weight: 600;
  color: var(--color-text);
}

.read-more {
  color: var(--color-accent);
  font-weight: 600;
}

/* LOADING */
.loading {
  text-align: center;
  padding: 60px 20px;
  color: var(--color-text-muted);
  font-size: 16px;
}

/* TABLET */
@media(max-width:1100px){
  .news-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* MOBILE */
@media(max-width:768px){
  .news-section {
    padding: 60px 0;
  }

  .section-header {
    flex-direction: column;
    align-items: start;
    gap: 20px;
  }

  .news-grid {
    grid-template-columns: 1fr;
  }

  .view-all {
    padding: 8px 16px;
    font-size: 14px;
  }
}
</style>
