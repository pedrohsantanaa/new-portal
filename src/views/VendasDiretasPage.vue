<template>
  <div class="vendas-page">
    <!-- Hero -->
    <section class="vendas-hero">
      <div class="container">
        <h1>Vendas Diretas</h1>
        <p>Imóveis e veículos disponíveis em todo o Tocantins</p>
        <div class="hero-stats">
          <div class="stat-card">
            <div class="stat-icon"><Home :size="28" /></div>
            <div class="stat-info">
              <span class="stat-number">{{ stats.imoveis }}</span>
              <span class="stat-label">Imóveis disponíveis</span>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon"><Car :size="28" /></div>
            <div class="stat-info">
              <span class="stat-number">{{ stats.veiculos }}</span>
              <span class="stat-label">Veículos disponíveis</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Filtros -->
    <section class="filters-section">
      <div class="container">
        <div class="filters-bar">
          <div class="filter-tabs">
            <button :class="{ active: activeTab === '' }" @click="activeTab = ''; loadFeatured()">
              <Home :size="16" /> Todos
            </button>
            <button :class="{ active: activeTab === 'imovel' }" @click="activeTab = 'imovel'; loadFeatured()">
              <Home :size="16" /> Imóveis
            </button>
            <button :class="{ active: activeTab === 'veiculo' }" @click="activeTab = 'veiculo'; loadFeatured()">
              <Car :size="16" /> Veículos
            </button>
          </div>
          <div class="filter-selects">
            <select v-model="filterCity" @change="loadFeatured()">
              <option value="">Todas as cidades</option>
              <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
            </select>
          </div>
          <div class="filter-search">
            <Search :size="18" />
            <input v-model="searchText" type="text" placeholder="Buscar cidade, região ou referência..." @input="debouncedSearch" />
          </div>
        </div>
      </div>
    </section>

    <!-- Imóveis em destaque -->
    <section v-if="imoveis.length" class="featured-section">
      <div class="container">
        <div class="section-header">
          <h2>Imóveis em destaque</h2>
        </div>
        <div class="cards-carousel">
          <div class="cards-track" ref="imoveisTrack">
            <div v-for="item in imoveis" :key="item.id" class="sale-card" @click="openModal(item)">
              <div class="card-image">
                <img v-if="item.image_url" :src="item.image_url" :alt="item.title" />
                <div v-else class="card-placeholder"><Home :size="40" /></div>
                <span class="card-badge" :class="item.property_type === 'Rural' ? 'badge-rural' : 'badge-urbano'">
                  {{ item.property_type || 'Imóvel' }}
                </span>
              </div>
              <div class="card-body">
                <h3>{{ item.title }}</h3>
                <p class="card-city">{{ item.city }}</p>
                <p class="card-type">{{ item.property_type }} · {{ item.purpose }}</p>
                <p class="card-price-label">Valor à vista</p>
                <p class="card-price">R$ {{ formatPrice(item.price) }}</p>
                <p v-if="item.area_m2" class="card-area"><Ruler :size="14" /> {{ item.area_m2 }} m²</p>
                <div class="card-actions">
                  <a v-if="item.phone" :href="`tel:${item.phone}`" class="btn-phone" @click.stop><Phone :size="16" /></a>
                  <button class="btn-details" @click.stop="openModal(item)">Ver detalhes</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Veículos em destaque -->
    <section v-if="veiculos.length" class="featured-section">
      <div class="container">
        <div class="section-header">
          <h2>Veículos em destaque</h2>
        </div>
        <div class="cards-carousel">
          <div class="cards-track" ref="veiculosTrack">
            <div v-for="item in veiculos" :key="item.id" class="sale-card" @click="openModal(item)">
              <div class="card-image">
                <img v-if="item.image_url" :src="item.image_url" :alt="item.title" />
                <div v-else class="card-placeholder"><Car :size="40" /></div>
              </div>
              <div class="card-body">
                <h3>{{ item.title }}</h3>
                <p class="card-info">{{ item.year }} · {{ item.fuel }} · {{ item.transmission }}</p>
                <p class="card-price-label">Valor à vista</p>
                <p class="card-price">R$ {{ formatPrice(item.price) }}</p>
                <div class="card-actions">
                  <a v-if="item.phone" :href="`tel:${item.phone}`" class="btn-phone" @click.stop><Phone :size="16" /></a>
                  <button class="btn-details" @click.stop="openModal(item)">Ver detalhes</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Badges de confiança -->
    <section class="trust-section">
      <div class="container">
        <div class="trust-grid">
          <div class="trust-item">
            <FileCheck :size="24" />
            <span>Imóveis com documentação regularizada</span>
          </div>
          <div class="trust-item">
            <Handshake :size="24" />
            <span>Negociação direta com a Agência</span>
          </div>
          <div class="trust-item">
            <ShieldCheck :size="24" />
            <span>Processo transparente e seguro</span>
          </div>
          <div class="trust-item">
            <MapPin :size="24" />
            <span>Oportunidades em diversas regiões do Tocantins</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Modal de detalhes -->
    <SaleItemModal :is-open="isModalOpen" :item="selectedItem" @close="isModalOpen = false" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Home, Car, Search, Phone, Ruler, FileCheck, Handshake, ShieldCheck, MapPin } from 'lucide-vue-next'
import api from '@/services/api'
import SaleItemModal from '../components/SaleItemModal.vue'

const stats = ref({ imoveis: 0, veiculos: 0 })
const imoveis = ref([])
const veiculos = ref([])
const cities = ref([])
const activeTab = ref('')
const filterCity = ref('')
const searchText = ref('')
const isModalOpen = ref(false)
const selectedItem = ref(null)

let searchTimeout = null

function debouncedSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(loadFeatured, 300)
}

function formatPrice(value) {
  return new Intl.NumberFormat('pt-BR', { minimumFractionDigits: 2 }).format(value)
}

function openModal(item) {
  selectedItem.value = item
  isModalOpen.value = true
}

async function loadStats() {
  try {
    const { data } = await api.get('/api/sale-items/public/stats')
    stats.value = data
  } catch { /* ignore */ }
}

async function loadFeatured() {
  try {
    const params = {}
    if (activeTab.value) params.item_type = activeTab.value
    if (filterCity.value) params.city = filterCity.value
    if (searchText.value) params.search = searchText.value

    const [imoveisRes, veiculosRes] = await Promise.all([
      api.get('/api/sale-items/public/featured', { params: { ...params, item_type: activeTab.value || 'imovel', limit: 8 } }),
      api.get('/api/sale-items/public/featured', { params: { ...params, item_type: activeTab.value || 'veiculo', limit: 8 } }),
    ])

    if (!activeTab.value || activeTab.value === 'imovel') {
      imoveis.value = imoveisRes.data
    } else {
      imoveis.value = []
    }

    if (!activeTab.value || activeTab.value === 'veiculo') {
      veiculos.value = veiculosRes.data
    } else {
      veiculos.value = []
    }
  } catch { /* ignore */ }
}

async function loadCities() {
  try {
    const { data } = await api.get('/api/sale-items/public', { params: { limit: 200 } })
    const uniqueCities = [...new Set(data.items.map(i => i.city).filter(Boolean))].sort()
    cities.value = uniqueCities
  } catch { /* ignore */ }
}

onMounted(() => {
  loadStats()
  loadFeatured()
  loadCities()
})
</script>

<style scoped>
.vendas-hero {
  background: linear-gradient(135deg, #011a4f 0%, #0a2d6a 100%);
  color: white;
  padding: 60px 0 50px;
}
.vendas-hero h1 {
  font-size: clamp(2rem, 4vw, 3rem);
  font-weight: 800;
  margin: 0 0 8px;
}
.vendas-hero p {
  font-size: 1.1rem;
  opacity: 0.9;
  margin: 0 0 30px;
}
.hero-stats {
  display: flex;
  gap: 20px;
}
.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 16px 24px;
  border: 1px solid rgba(255, 255, 255, 0.15);
}
.stat-icon {
  width: 52px;
  height: 52px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.stat-number {
  display: block;
  font-size: 1.8rem;
  font-weight: 800;
  line-height: 1;
}
.stat-label {
  font-size: 0.85rem;
  opacity: 0.85;
}

.filters-section {
  background: white;
  border-bottom: 1px solid #e2e8f0;
  padding: 16px 0;
  position: sticky;
  top: 85px;
  z-index: 50;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}
.filters-bar {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}
.filter-tabs {
  display: flex;
  gap: 4px;
  background: #f1f5f9;
  border-radius: 8px;
  padding: 4px;
}
.filter-tabs button {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  background: transparent;
  font-size: 14px;
  font-weight: 500;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}
.filter-tabs button.active {
  background: #011a4f;
  color: white;
}
.filter-selects select {
  padding: 10px 14px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  color: #334155;
  background: white;
  outline: none;
  min-width: 180px;
}
.filter-search {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  flex: 1;
  min-width: 200px;
}
.filter-search input {
  border: none;
  outline: none;
  font-size: 14px;
  width: 100%;
  background: transparent;
}

.featured-section {
  padding: 40px 0;
}
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}
.section-header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}
.cards-carousel {
  overflow-x: auto;
  scrollbar-width: thin;
  margin: 0 -8px;
  padding: 0 8px;
}
.cards-track {
  display: flex;
  gap: 20px;
  padding-bottom: 8px;
}
.sale-card {
  flex: 0 0 280px;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}
.sale-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}
.card-image {
  position: relative;
  height: 180px;
  background: #f1f5f9;
  overflow: hidden;
}
.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.card-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
}
.card-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  color: white;
}
.badge-urbano { background: #011a4f; }
.badge-rural { background: #16a34a; }
.card-body {
  padding: 16px;
}
.card-body h3 {
  font-size: 1rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 4px;
}
.card-city, .card-info {
  font-size: 13px;
  color: #64748b;
  margin: 0 0 2px;
}
.card-type {
  font-size: 12px;
  color: #94a3b8;
  margin: 0 0 12px;
}
.card-price-label {
  font-size: 12px;
  color: #64748b;
  margin: 0 0 2px;
}
.card-price {
  font-size: 1.15rem;
  font-weight: 800;
  color: #011a4f;
  margin: 0 0 8px;
}
.card-area {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #64748b;
  margin: 0 0 12px;
}
.card-actions {
  display: flex;
  gap: 8px;
  margin-top: 12px;
}
.btn-phone {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: white;
  color: #011a4f;
  text-decoration: none;
  transition: all 0.2s;
}
.btn-phone:hover {
  background: #eff6ff;
  border-color: #011a4f;
}
.btn-details {
  flex: 1;
  padding: 10px 16px;
  border: 2px solid #011a4f;
  border-radius: 8px;
  background: white;
  color: #011a4f;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-details:hover {
  background: #011a4f;
  color: white;
}

.trust-section {
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
  padding: 32px 0;
}
.trust-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}
.trust-item {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  color: #475569;
  font-weight: 500;
}
.trust-item svg {
  color: #011a4f;
  flex-shrink: 0;
}

@media (max-width: 992px) {
  .hero-stats { flex-direction: column; }
  .trust-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 768px) {
  .filters-bar { flex-direction: column; align-items: stretch; }
  .filter-tabs { justify-content: center; }
  .filter-selects select { width: 100%; }
  .trust-grid { grid-template-columns: 1fr; }
  .sale-card { flex: 0 0 260px; }
}
</style>
