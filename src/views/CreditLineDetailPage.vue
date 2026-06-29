<template>
  <div class="credit-detail-page">
    <div v-if="loading" class="loading">Carregando linha de crédito...</div>

    <div v-else-if="error" class="error-container">
      <h2>Linha de crédito não encontrada</h2>
      <p>{{ error }}</p>
      <router-link to="/" class="btn-back">← Voltar para o Início</router-link>
    </div>

    <template v-else-if="creditLine">
      <div class="detail-hero" :style="{ backgroundColor: creditLine.color }">
        <div class="container hero-inner">
          <img
            v-if="creditLine.icon_url"
            :src="creditLine.icon_url"
            :alt="creditLine.title"
            class="hero-icon"
          />
          <h1>{{ creditLine.title }}</h1>
          <p class="hero-description">{{ creditLine.description }}</p>
        </div>
      </div>

      <div class="container detail-content">
        <div v-if="creditLine.details" class="detail-section">
          <div class="content-text" v-html="creditLine.details"></div>
        </div>

        <div v-if="creditLine.documents && creditLine.documents.length" class="detail-section documents-section">
          <h2>Documentos Necessários</h2>
          <div class="documents-list">
            <a
              v-for="(doc, index) in creditLine.documents"
              :key="index"
              :href="doc.file_url"
              target="_blank"
              rel="noopener noreferrer"
              class="document-btn"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
                <polyline points="10 9 9 9 8 9"/>
              </svg>
              {{ doc.label }}
            </a>
          </div>
        </div>

        <div v-if="creditLine.external_html" class="detail-section external-section">
          <h2>Solicitar Crédito</h2>
          <div class="external-container" v-html="creditLine.external_html"></div>
        </div>

        <div class="detail-footer">
          <router-link to="/" class="btn-back">
            ← Voltar para o Início
          </router-link>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/services/api'

const route = useRoute()

const creditLine = ref(null)
const loading = ref(true)
const error = ref('')

async function fetchCreditLine(slug) {
  loading.value = true
  error.value = ''
  creditLine.value = null
  try {
    const { data } = await api.get(`/api/credit-lines/${slug}`)
    creditLine.value = data
  } catch (e) {
    error.value = e.response?.data?.detail || 'Erro ao carregar linha de crédito.'
  } finally {
    loading.value = false
  }
}

onMounted(() => fetchCreditLine(route.params.slug))

watch(() => route.params.slug, (newSlug) => {
  if (newSlug) fetchCreditLine(newSlug)
})
</script>

<style scoped>
.credit-detail-page {
  min-height: 100vh;
}

.detail-hero {
  padding: 60px 0;
}

.hero-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 16px;
}

.hero-icon {
  width: 120px;
  height: 120px;
  object-fit: contain;
  border-radius: var(--radius-md);
}

.detail-hero h1 {
  font-size: clamp(2rem, 5vw, 3rem);
  color: var(--color-primary);
  font-weight: 700;
}

.hero-description {
  font-size: 1.2rem;
  color: var(--color-text);
  max-width: 600px;
}

.detail-content {
  max-width: 800px;
  padding: 48px 20px 80px;
}

.detail-section {
  margin-bottom: 48px;
}

.detail-section h2 {
  font-size: 1.5rem;
  color: var(--color-primary);
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid var(--color-border);
}

.content-text {
  font-size: 1.05rem;
  color: var(--color-text);
  line-height: 1.8;
}

.content-text :deep(h2) {
  font-size: 1.5rem;
  color: var(--color-primary);
  margin: 1.5em 0 0.8em;
  font-weight: 700;
}

.content-text :deep(h3) {
  font-size: 1.3rem;
  color: var(--color-primary);
  margin: 1.3em 0 0.6em;
  font-weight: 600;
}

.content-text :deep(p) {
  margin-bottom: 1em;
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
  border-left: 4px solid var(--color-accent);
  padding: 16px 24px;
  margin: 1.5em 0;
  background: var(--color-bg-alt);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  font-style: italic;
  color: var(--color-text);
}

.documents-list {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.document-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--color-bg-alt);
  color: var(--color-primary);
  padding: 12px 20px;
  border-radius: var(--radius-sm);
  font-weight: 600;
  font-size: 15px;
  text-decoration: none;
  border: 1px solid var(--color-border);
  transition: var(--transition);
}

.document-btn:hover {
  background: var(--color-primary);
  color: var(--color-white);
  border-color: var(--color-primary);
  transform: translateY(-2px);
}

.external-section {
  background: var(--color-bg-alt);
  padding: 32px;
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
}

.external-container {
  min-height: 200px;
}

.detail-footer {
  padding-top: 32px;
  border-top: 1px solid var(--color-border);
  margin-top: 48px;
}

.btn-back {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--color-accent);
  text-decoration: none;
  font-weight: 600;
  font-size: 15px;
  padding: 12px 24px;
  border: 2px solid var(--color-accent);
  border-radius: var(--radius-sm);
  transition: var(--transition);
}

.btn-back:hover {
  background: var(--color-accent);
  color: var(--color-white);
}

.loading {
  text-align: center;
  padding: 120px 20px;
  font-size: 16px;
  color: var(--color-text-muted);
}

.error-container {
  text-align: center;
  padding: 120px 20px;
}

.error-container h2 {
  color: var(--color-primary);
  margin-bottom: 12px;
}

.error-container p {
  color: var(--color-text-muted);
  margin-bottom: 24px;
}

@media (max-width: 768px) {
  .detail-hero {
    padding: 40px 0;
  }

  .hero-icon {
    width: 80px;
    height: 80px;
  }

  .detail-content {
    padding: 32px 16px 60px;
  }

  .external-section {
    padding: 20px;
  }

  .documents-list {
    flex-direction: column;
  }

  .document-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
