<template>
  <section class="credit-section">
    <div class="container">

      <!-- HEADER -->
      <div class="section-header">
        <h2>Nossas <span>Linhas de Crédito</span></h2>
      </div>

      <!-- NAVIGATION -->
      <div class="carousel-nav">
        <button class="arrow-btn" @click="swiper?.slidePrev()">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg>
        </button>
        <button class="arrow-btn" @click="swiper?.slideNext()">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18l6-6-6-6"/></svg>
        </button>
      </div>

      <!-- CAROUSEL -->
      <Swiper
        @swiper="onSwiper"
        :modules="modules"
        :slides-per-view="'auto'"
        :space-between="22"
        :grab-cursor="true"
        :pagination="{ clickable: true }"
        :breakpoints="{
          640: { slidesPerView: 2 },
          992: { slidesPerView: 3 },
          1200: { slidesPerView: 4 }
        }"
        class="credit-swiper"
      >
        <SwiperSlide v-for="credit in creditLines" :key="credit.id">
          <div class="credit-card">
            <div class="icon-box" :style="{ background: credit.color }">
              <img :src="credit.icon_url" :alt="credit.title" class="icon-image" />
            </div>
            <div class="card-text">
              <h3>{{ credit.title }}</h3>
              <p>{{ credit.description }}</p>
            </div>
            <router-link :to="'/linhas-de-credito/' + credit.slug" class="saiba-mais">Saiba Mais ›</router-link>
          </div>
        </SwiperSlide>
      </Swiper>

      <!-- LINK "VER TODAS" -->
      <div class="view-all-container">
        <router-link to="/linhas-de-credito" class="view-all-link">Ver todas as linhas de crédito ›</router-link>
      </div>

    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'

import { Swiper, SwiperSlide } from 'swiper/vue'
import { Pagination } from 'swiper/modules'

import 'swiper/css'
import 'swiper/css/pagination'

import api from '@/services/api'

const modules = [Pagination]

const swiper = ref(null)
const creditLines = ref([])

const onSwiper = (instance) => {
  swiper.value = instance
}

async function loadCreditLines() {
  try {
    const { data } = await api.get('/api/credit-lines/?active_only=true&limit=50')
    creditLines.value = data.items
  } catch (e) {
  }
}

onMounted(loadCreditLines)
</script>

<style scoped>
.credit-section {
  padding: 80px 0;
  background: linear-gradient(180deg, #011A4F 0%, #0a2d6a 40%, #1a3f7f 70%, #2a5298 100%);
}

/* HEADER */
.section-header {
  text-align: center;
  margin-bottom: 40px;
}

.section-header h2 {
  font-size: clamp(1.8rem, 4vw, 3rem);
  color: var(--color-white);
  font-weight: 700;
}

.section-header h2 span {
  color: var(--color-secondary);
  position: relative;
}

.section-header h2 span::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 100%;
  height: 3px;
  border-radius: var(--radius-sm);
  background: linear-gradient(90deg, var(--color-secondary), var(--color-accent));
}

/* NAVIGATION */
.carousel-nav {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-bottom: 24px;
}

.arrow-btn {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-full);
  border: none;
  background: var(--color-white);
  color: var(--color-primary);
  cursor: pointer;
  transition: var(--transition);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-sm);
}

.arrow-btn:hover {
  background: var(--color-secondary);
  color: var(--color-primary);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

/* SWIPER */
.credit-swiper {
  width: 100%;
  padding-bottom: 50px;
  overflow: hidden;
}

:deep(.swiper-slide) {
  display: flex;
  height: auto;
}

:deep(.swiper-pagination-bullet) {
  width: 10px;
  height: 10px;
  background: rgba(255, 255, 255, 0.4);
  opacity: 1;
  transition: var(--transition);
}

:deep(.swiper-pagination-bullet-active) {
  background: var(--color-secondary);
  opacity: 1;
  transform: scale(1.2);
}

/* CARD */
.credit-card {
  width: 100%;
  height: 100%;
  min-height: 500px;
  background: var(--color-bg-card);
  border-radius: var(--radius-md);
  padding: 28px;
  border: none;
  display: flex;
  flex-direction: column;
  transition: var(--transition);
  box-shadow: var(--shadow-md);
}

.credit-card:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-hover);
}

.icon-box {
  width: 100%;
  height: 50%;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
  overflow: hidden;
  /* flex-shrink: 0; */
}

.icon-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-text {
  flex: 1;
}

.card-text h3 {
  font-size: 26px;
  color: var(--color-black);
  margin-bottom: 6px;
  font-weight: 700;
  text-align: center;
}

.card-text p {
  font-size:20px;
  color: var(--color-text);
  /* line-height: 1.6; */
  /* margin-bottom: 18px; */
  text-align: center;
}

.saiba-mais {
  display: block;
  align-items: center;
  gap: 4px;
  background: var(--color-secondary);
  color: var(--color-black);
  padding: 12px 24px;
  border-radius: var(--radius-sm);
  font-weight: 600;
  font-size: 15px;
  text-decoration: none;
  transition: var(--transition);
  margin-top: auto;
  align-self: center;
}

.saiba-mais:hover {
  background: color-mix(in srgb, var(--color-secondary), black 15%);
  transform: translateY(-2px);
}

/* LINK VER TODAS */
.view-all-container {
  text-align: center;
  margin-top: 40px;
}

.view-all-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: transparent;
  color: var(--color-white);
  padding: 14px 32px;
  border-radius: var(--radius-sm);
  border: 2px solid rgba(255, 255, 255, 0.3);
  font-weight: 600;
  font-size: 16px;
  text-decoration: none;
  transition: var(--transition);
}

.view-all-link:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: var(--color-secondary);
  color: var(--color-secondary);
  transform: translateY(-2px);
}

/* RESPONSIVE */
@media (max-width: 992px) {
  .credit-card {
    padding: 26px;
    min-height: 300px;
  }

  .icon-box {
    width: 60px;
    height: 60px;
  }
}

@media (max-width: 768px) {
  .credit-section {
    padding: 60px 0;
  }

  .carousel-nav {
    justify-content: center;
  }

  .view-all-link {
    padding: 12px 24px;
    font-size: 15px;
  }
}

@media (max-width: 576px) {
  .credit-card {
    padding: 24px;
    min-height: 280px;
  }

  .icon-box {
    width: 56px;
    height: 56px;
  }

  .arrow-btn {
    width: 42px;
    height: 42px;
  }
}

/* ALTO CONTRASTE */
:global(html.high-contrast) .credit-section {
  background: var(--color-bg) !important;
}
</style>
