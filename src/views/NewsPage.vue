<template>
  <div class="news-page">
    <div class="news-hero">
      <div class="container">
        <h1>Notícias</h1>
        <p>Fique por dentro das novidades e ações da instituição.</p>
      </div>
    </div>

    <div class="container news-content">
      <!-- Filtros -->
      <div class="filters">
        <button
          v-for="cat in categories"
          :key="cat"
          :class="['filter-btn', { active: selectedCategory === cat }]"
          @click="filterByCategory(cat)"
        >
          {{ cat }}
        </button>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading">Carregando notícias...</div>

      <!-- Erro -->
      <div v-else-if="error" class="error">{{ error }}</div>

      <!-- Grid de Notícias -->
      <div v-else class="news-grid">
        <article
          v-for="item in newsList"
          :key="item.id"
          class="news-card"
          @click="goToDetail(item.slug)"
        >
          <div class="image-wrapper">
            <img
              :src="(item.image_url || defaultImage) + cacheBust"
              :alt="item.title"
              @error="handleImageError"
            />
            <span class="tag">{{ item.category }}</span>
          </div>

          <div class="news-content-card">
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

      <!-- Sem resultados -->
      <div v-if="!loading && !error && newsList.length === 0" class="empty">
        Nenhuma notícia encontrada.
      </div>

      <!-- Paginação -->
      <div v-if="totalPages > 1" class="pagination">
        <button
          class="page-btn"
          :disabled="currentPage <= 1"
          @click="goToPage(currentPage - 1)"
        >
          ← Anterior
        </button>

        <div class="page-numbers">
          <button
            v-for="page in visiblePages"
            :key="page"
            :class="['page-num', { active: page === currentPage }]"
            @click="goToPage(page)"
          >
            {{ page }}
          </button>
        </div>

        <button
          class="page-btn"
          :disabled="currentPage >= totalPages"
          @click="goToPage(currentPage + 1)"
        >
          Próxima →
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '@/services/api'

const router = useRouter()
const route = useRoute()

const newsList = ref([])
const loading = ref(true)
const error = ref('')
const currentPage = ref(1)
const totalPages = ref(1)
const selectedCategory = ref('')
const limit = 12

const defaultImage = 'https://placehold.co/800x600/e2e8f0/64748b?text=Sem+Imagem'
const cacheBust = '?v=' + Date.now()

const categories = ['Todos', 'Crédito', 'Programa', 'Evento', 'Empreendedorismo']

const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, currentPage.value - 2)
  const end = Math.min(totalPages.value, start + 4)
  for (let i = start; i <= end; i++) pages.push(i)
  return pages
})

async function fetchNews() {
  loading.value = true
  error.value = ''
  try {
    const params = {
      page: currentPage.value,
      limit,
      published_only: true,
    }
    if (selectedCategory.value && selectedCategory.value !== 'Todos') {
      params.category = selectedCategory.value
    }
    const { data } = await api.get('/api/news/', { params })
    newsList.value = data.items
    totalPages.value = data.pages
  } catch (e) {
    error.value = 'Erro ao carregar notícias. Tente novamente.'
    console.error(e)
  } finally {
    loading.value = false
  }
}

function filterByCategory(cat) {
  selectedCategory.value = cat
  currentPage.value = 1
  fetchNews()
}

function goToPage(page) {
  currentPage.value = page
  fetchNews()
  window.scrollTo({ top: 0, behavior: 'smooth' })
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

onMounted(() => {
  if (route.query.page) {
    currentPage.value = parseInt(route.query.page) || 1
  }
  fetchNews()
})
</script>

<style scoped>
.news-page {
  min-height: 100vh;
}

.news-hero {
  background: linear-gradient(135deg, #011a4f 0%, #083ea8 100%);
  color: white;
  padding: 80px 0 60px;
}

.news-hero h1 {
  font-size: clamp(2rem, 5vw, 3.5rem);
  margin-bottom: 12px;
}

.news-hero p {
  font-size: 1.1rem;
  opacity: 0.85;
}

.news-content {
  padding: 40px 20px 80px;
}

/* FILTROS */
.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 40px;
}

.filter-btn {
  padding: 10px 20px;
  border: 2px solid #e2e8f0;
  background: white;
  border-radius: 999px;
  font-size: 14px;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-btn:hover {
  border-color: #083ea8;
  color: #083ea8;
}

.filter-btn.active {
  background: #011a4f;
  border-color: #011a4f;
  color: white;
}

/* GRID */
.news-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 28px;
}

/* CARD */
.news-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  cursor: pointer;
  transition: all 0.3s ease;
}

.news-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12);
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

.tag {
  position: absolute;
  top: 14px;
  left: 14px;
  background: #083ea8;
  color: white;
  padding: 6px 14px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
}

.news-content-card {
  padding: 22px;
}

.news-content-card h3 {
  font-size: 17px;
  font-weight: 700;
  color: #1e293b;
  line-height: 1.5;
  margin-bottom: 8px;
}

.news-content-card p {
  font-size: 14px;
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 16px;
}

.news-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 14px;
  border-top: 1px solid #e2e8f0;
  font-size: 13px;
  color: #64748b;
}

.footer-left {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.author {
  font-weight: 600;
  color: #334155;
}

.read-more {
  color: #083ea8;
  font-weight: 600;
}

/* LOADING / ERROR / EMPTY */
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

/* PAGINAÇÃO */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  margin-top: 50px;
}

.page-btn {
  padding: 10px 20px;
  border: 2px solid #e2e8f0;
  background: white;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #334155;
  cursor: pointer;
  transition: all 0.2s ease;
}

.page-btn:hover:not(:disabled) {
  border-color: #083ea8;
  color: #083ea8;
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-numbers {
  display: flex;
  gap: 6px;
}

.page-num {
  width: 40px;
  height: 40px;
  border: none;
  background: white;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
}

.page-num:hover {
  background: #f1f5f9;
  color: #011a4f;
}

.page-num.active {
  background: #011a4f;
  color: white;
}

/* RESPONSIVO */
@media (max-width: 992px) {
  .news-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .news-hero {
    padding: 60px 0 40px;
  }

  .news-grid {
    grid-template-columns: 1fr;
  }

  .filters {
    justify-content: center;
  }

  .pagination {
    flex-direction: column;
    gap: 16px;
  }

  .page-numbers {
    order: -1;
  }
}
</style>
