<template>
  <div class="info-access-page">
    <div class="info-hero">
      <div class="container">
        <h1>Acesso à Informação</h1>
        <p>Transparência e compromisso com você.</p>
      </div>
    </div>

    <div class="container info-content">
      <!-- Busca -->
      <div class="search-section">
        <div class="search-bar">
          <Search :size="20" />
          <input v-model="searchQuery" type="text"
            placeholder="Buscar documentos por título, palavra-chave ou assunto..." @input="debouncedSearch" />
          <button class="btn-search" @click="searchDocuments">
            <Search :size="16" /> Buscar
          </button>
        </div>
      </div>

      <!-- Categorias -->
      <div class="categories-grid">
        <div v-for="cat in categories" :key="cat.id" class="category-card"
          :class="{ active: selectedCategory === cat.slug }" @click="filterByCategory(cat.slug)">
          <div class="category-icon">
            <component :is="getIcon(cat.icon)" :size="28" />
          </div>
          <div class="category-info">
            <h3>{{ cat.name }}</h3>
            <p>{{ cat.description }}</p>
          </div>
          <ChevronRight :size="18" class="category-arrow" />
        </div>
      </div>

      <!-- Documentos em destaque -->
      <div class="section-highlight" v-if="highlightDocs.length > 0">
        <div class="section-header">
          <h2>
            <Star :size="20" />
            Documentos em destaque
          </h2>
          <a href="#" class="link-all" @click.prevent="showAllHighlights = !showAllHighlights">
            {{ showAllHighlights ? 'Ver menos' : 'Ver todos' }}
          </a>
        </div>
        <div class="docs-table">
          <div v-for="doc in displayedHighlights" :key="doc.id" class="doc-row">
            <span class="doc-type-badge" :class="'badge-' + doc.file_type">
              {{ doc.file_type.toUpperCase() }}
            </span>
            <a :href="doc.file_url" target="_blank" class="doc-title">{{ doc.title }}</a>
            <span class="doc-category">{{ doc.category_name }}</span>
            <span class="doc-date">{{ formatDate(doc.created_at) }}</span>
            <span class="doc-size">{{ formatSize(doc.file_size) }}</span>
            <div class="doc-actions">
              <a :href="doc.file_url" target="_blank" class="btn-action">
                <Eye :size="14" /> Visualizar
              </a>
              <a :href="doc.file_url" download class="btn-action">
                <Download :size="14" /> Baixar
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- Lista de documentos -->
      <div class="section-documents">
        <div class="section-header">
          <h2>
            <FileText :size="20" />
            {{ documentsSectionTitle }}
          </h2>
        </div>

        <div v-if="loadingDocs" class="loading">Carregando documentos...</div>

        <div v-else-if="documents.length === 0" class="empty-state">
          <p>Nenhum documento encontrado.</p>
        </div>

        <div v-else class="docs-table">
          <div v-for="doc in documents" :key="doc.id" class="doc-row">
            <span class="doc-type-badge" :class="'badge-' + doc.file_type">
              {{ doc.file_type.toUpperCase() }}
            </span>
            <a :href="doc.file_url" target="_blank" class="doc-title">{{ doc.title }}</a>
            <span class="doc-category">{{ doc.category_name }}</span>
            <span class="doc-date">{{ formatDate(doc.created_at) }}</span>
            <span class="doc-size">{{ formatSize(doc.file_size) }}</span>
            <div class="doc-actions">
              <a :href="doc.file_url" target="_blank" class="btn-action">
                <Eye :size="14" /> Visualizar
              </a>
              <a :href="doc.file_url" download class="btn-action">
                <Download :size="14" /> Baixar
              </a>
            </div>
          </div>
        </div>

        <div v-if="totalPages > 1" class="pagination">
          <button class="page-btn" :disabled="currentPage <= 1" @click="goToPage(currentPage - 1)">← Anterior</button>
          <div class="page-numbers">
            <button v-for="page in visiblePages" :key="page" :class="['page-num', { active: page === currentPage }]"
              @click="goToPage(page)">{{ page }}</button>
          </div>
          <button class="page-btn" :disabled="currentPage >= totalPages" @click="goToPage(currentPage + 1)">Próxima
            →</button>
        </div>
      </div>

      <!-- Navegue por ano -->
      <div class="section-years" v-if="years.length > 0">
        <div class="section-header">
          <h2>
            <Calendar :size="20" />
            Navegue por ano
          </h2>
        </div>
        <div class="year-buttons">
          <button v-for="year in years" :key="year" :class="['year-btn', { active: selectedYear === year }]"
            @click="filterByYear(year)">{{ year }}</button>
        </div>
      </div>

      <!-- CTA -->
      <div class="cta-section">
        <div class="cta-icon">
          <Headphones :size="32" />
        </div>
        <div class="cta-text">
          <h3>Não encontrou o que procura?</h3>
          <p>Fale com a nossa equipe e solicite a informação desejada.</p>
        </div>
        <a href="#" class="btn-cta">
          Solicitar informação
          <ArrowRight :size="16" />
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  Search, ChevronRight, Star, Eye, Download, FileText, Calendar,
  Headphones, ArrowRight, FileBarChart, Calculator, Network,
  Megaphone, ShieldCheck, Users, Scale
} from 'lucide-vue-next'
import api from '@/services/api'

const categories = ref([])
const documents = ref([])
const highlightDocs = ref([])
const years = ref([])
const loadingDocs = ref(true)
const searchQuery = ref('')
const selectedCategory = ref('')
const selectedYear = ref('')
const currentPage = ref(1)
const totalPages = ref(1)
const showAllHighlights = ref(false)
const limit = 10

const displayedHighlights = computed(() => {
  return showAllHighlights.value ? highlightDocs.value : highlightDocs.value.slice(0, 5)
})

const selectedCategoryName = computed(() => {
  return categories.value.find((cat) => cat.slug === selectedCategory.value)?.name || ''
})

const documentsSectionTitle = computed(() => {
  if (selectedCategory.value) return selectedCategoryName.value || 'Documentos da categoria'
  if (searchQuery.value) return 'Resultado da busca'
  if (selectedYear.value) return `Documentos de ${selectedYear.value}`
  return 'Todos os documentos'
})

const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, currentPage.value - 2)
  const end = Math.min(totalPages.value, start + 4)
  for (let i = start; i <= end; i++) pages.push(i)
  return pages
})

const iconMap = {
  'file-text': FileText,
  'bar-chart-3': FileBarChart,
  'calculator': Calculator,
  'network': Network,
  'megaphone': Megaphone,
  'shield-check': ShieldCheck,
  'users': Users,
  'scale': Scale,
}

function getIcon(name) {
  return iconMap[name] || FileText
}

let searchTimeout = null
function debouncedSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    currentPage.value = 1
    searchDocuments()
  }, 400)
}

async function loadCategories() {
  try {
    const { data } = await api.get('/api/info-categories/')
    categories.value = data.items
  } catch (err) {
  }
}

async function loadHighlights() {
  try {
    const { data } = await api.get('/api/info-documents/public', {
      params: { highlight_only: true, limit: 10 }
    })
    highlightDocs.value = data.items
  } catch (err) {
  }
}

async function loadYears() {
  try {
    const { data } = await api.get('/api/info-documents/years')
    years.value = data.years
  } catch (err) {
  }
}

async function loadDocuments() {
  loadingDocs.value = true
  try {
    const params = { page: currentPage.value, limit }
    if (selectedCategory.value) params.category_slug = selectedCategory.value
    if (selectedYear.value) params.year = selectedYear.value
    if (searchQuery.value) params.search = searchQuery.value

    const { data } = await api.get('/api/info-documents/public', { params })
    documents.value = data.items
    totalPages.value = data.pages
  } catch (err) {
  } finally {
    loadingDocs.value = false
  }
}

function searchDocuments() {
  currentPage.value = 1
  selectedCategory.value = ''
  loadDocuments()
}

function filterByCategory(slug) {
  if (selectedCategory.value === slug) {
    selectedCategory.value = ''
  } else {
    selectedCategory.value = slug
  }
  searchQuery.value = ''
  selectedYear.value = ''
  currentPage.value = 1
  loadDocuments()
}

function filterByYear(year) {
  if (selectedYear.value === year) {
    selectedYear.value = ''
  } else {
    selectedYear.value = year
  }
  currentPage.value = 1
  loadDocuments()
}

function goToPage(page) {
  currentPage.value = page
  loadDocuments()
  window.scrollTo({ top: 400, behavior: 'smooth' })
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  })
}

function formatSize(bytes) {
  if (!bytes) return '—'
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

onMounted(() => {
  loadCategories()
  loadHighlights()
  loadYears()
  loadDocuments()
})
</script>

<style scoped>
.info-hero {
  background: linear-gradient(135deg, #011a4f 0%, #083ea8 100%);
  color: white;
  padding: 60px 0 40px;
  text-align: center;
}

.info-hero h1 {
  font-size: clamp(2rem, 5vw, 3rem);
  font-weight: 800;
  color: white;
  margin: 0 0 8px;
}

.info-hero p {
  font-size: clamp(1rem, 2vw, 1.2rem);
  opacity: 0.85;
  margin: 0;
}

.info-content {
  padding: 40px 20px;
  max-width: 1200px;
  margin: 0 auto;
}

/* Busca */
.search-section {
  margin-bottom: 40px;
}

.search-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  padding: 12px 20px;
  max-width: 700px;
  margin: 0 auto;
  transition: border-color 0.2s;
}

.search-bar:focus-within {
  border-color: #083ea8;
}

.search-bar input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 15px;
  color: #334155;
  background: transparent;
}

.btn-search {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 20px;
  background: #011a4f;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-search:hover {
  background: #0a2d6a;
}

/* Categorias */
.categories-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
  margin-bottom: 48px;
}

.category-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px 16px;
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.category-card:hover {
  border-color: #083ea8;
  box-shadow: 0 4px 12px rgba(8, 62, 168, 0.1);
}

.category-card.active {
  border-color: #083ea8;
  background: #f0f5ff;
}

.category-icon {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0f5ff;
  border-radius: 10px;
  color: #083ea8;
}

.category-info {
  flex: 1;
  min-width: 0;
}

.category-info h3 {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 4px;
}

.category-info p {
  font-size: 12px;
  color: #64748b;
  margin: 0;
  line-height: 1.4;
}

.category-arrow {
  flex-shrink: 0;
  color: #cbd5e1;
}

/* Sections */
.section-highlight,
.section-documents,
.section-years {
  margin-bottom: 48px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h2 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.link-all {
  font-size: 14px;
  color: #083ea8;
  text-decoration: none;
  font-weight: 500;
}

.link-all:hover {
  text-decoration: underline;
}

/* Document table */
.docs-table {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
}

.doc-row {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  border-bottom: 1px solid #f1f5f9;
}

.doc-row:last-child {
  border-bottom: none;
}

.doc-row:hover {
  background: #f8fafc;
}

.doc-type-badge {
  flex-shrink: 0;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 700;
  min-width: 48px;
  text-align: center;
}

.badge-pdf {
  background: #fef2f2;
  color: #dc2626;
}

.badge-xlsx {
  background: #dcfce7;
  color: #166534;
}

.badge-csv {
  background: #dbeafe;
  color: #1e40af;
}

.doc-title {
  flex: 1;
  font-size: 14px;
  font-weight: 500;
  color: #1e293b;
  text-decoration: none;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.doc-title:hover {
  color: #083ea8;
}

.doc-category {
  flex-shrink: 0;
  font-size: 13px;
  color: #64748b;
  min-width: 140px;
}

.doc-date {
  flex-shrink: 0;
  font-size: 13px;
  color: #64748b;
  min-width: 90px;
}

.doc-size {
  flex-shrink: 0;
  font-size: 13px;
  color: #94a3b8;
  min-width: 70px;
}

.doc-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.btn-action {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  font-size: 12px;
  font-weight: 500;
  color: #083ea8;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-action:hover {
  background: #f0f5ff;
  border-color: #083ea8;
}

/* Year buttons */
.year-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.year-btn {
  padding: 10px 24px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  background: white;
  color: #475569;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.year-btn:hover {
  border-color: #083ea8;
  color: #083ea8;
}

.year-btn.active {
  background: #011a4f;
  border-color: #011a4f;
  color: white;
}

/* Pagination */
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-top: 24px;
}

.page-btn {
  padding: 8px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: white;
  color: #475569;
  font-size: 14px;
  cursor: pointer;
}

.page-btn:hover:not(:disabled) {
  background: #f8fafc;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-numbers {
  display: flex;
  gap: 4px;
}

.page-num {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: white;
  color: #475569;
  font-size: 14px;
  cursor: pointer;
}

.page-num.active {
  background: #011a4f;
  border-color: #011a4f;
  color: white;
}

/* Empty & Loading */
.empty-state {
  text-align: center;
  padding: 40px;
  color: #64748b;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #64748b;
}

/* CTA */
.cta-section {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 28px 32px;
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  margin-top: 20px;
}

.cta-icon {
  flex-shrink: 0;
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0f5ff;
  border-radius: 50%;
  color: #083ea8;
}

.cta-text {
  flex: 1;
}

.cta-text h3 {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 4px;
}

.cta-text p {
  font-size: 14px;
  color: #64748b;
  margin: 0;
}

.btn-cta {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: #d4a017;
  color: #1e293b;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  transition: background 0.2s;
  flex-shrink: 0;
}

.btn-cta:hover {
  background: #c4940e;
}

/* Responsive */
@media (max-width: 992px) {
  .categories-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .doc-category {
    display: none;
  }
}

@media (max-width: 768px) {
  .categories-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .doc-row {
    flex-wrap: wrap;
    gap: 8px;
  }

  .doc-size {
    display: none;
  }

  .cta-section {
    flex-direction: column;
    text-align: center;
  }
}

@media (max-width: 480px) {
  .categories-grid {
    grid-template-columns: 1fr;
  }
}

/* ALTO CONTRASTE */
:global(html.high-contrast) .info-hero {
  background: var(--color-primary) !important;
}
:global(html.high-contrast) .docs-table {
  background: var(--color-bg) !important;
}
:global(html.high-contrast) .btn-search {
  background: var(--color-primary) !important;
}
:global(html.high-contrast) .year-btn.active {
  background: var(--color-primary) !important;
}
:global(html.high-contrast) .page-num.active {
  background: var(--color-primary) !important;
}
:global(html.high-contrast) .btn-cta {
  background: var(--color-secondary) !important;
}
:global(html.high-contrast) .badge-pdf {
  background: rgba(255, 0, 0, 0.1) !important;
}
:global(html.high-contrast) .badge-xlsx {
  background: rgba(0, 255, 0, 0.1) !important;
}
:global(html.high-contrast) .badge-csv {
  background: rgba(0, 0, 255, 0.1) !important;
}
</style>
