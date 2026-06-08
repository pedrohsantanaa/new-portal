<template>
  <section class="credit-section">
    <div class="container">

      <!-- HEADER -->
      <div class="section-header">

        <div>
          <span class="badge">
            Soluções financeiras
          </span>

          <h2>
            Encontre a linha de crédito ideal
          </h2>

          <p>
            Escolha a melhor solução para
            impulsionar seu negócio.
          </p>
        </div>

        <a href="/linhas-de-credito" class="view-all desktop-link">
          Ver todas →
        </a>

      </div>

      <!-- TABS -->
      <div class="tabs">
        <button v-for="category in categories" :key="category" class="tab" :class="{
          active:
            selectedCategory === category
        }" @click="selectedCategory = category">
          {{ category }}
        </button>
      </div>

      <!-- TOP ACTIONS -->
      <div class="carousel-top">

        <div class="navigation-buttons">

          <button class="arrow-btn" @click="swiper?.slidePrev()">
            ←
          </button>

          <button class="arrow-btn" @click="swiper?.slideNext()">
            →
          </button>

        </div>

      </div>

      <!-- CAROUSEL -->
      <!-- <Swiper
        @swiper="onSwiper"
        :modules="modules"
        :slides-per-view="1"
        :space-between="22"
        :grab-cursor="true"
        :pagination="{
          clickable: true
        }"
        :breakpoints="{
          640: {
            slidesPerView: 2
          },

          992: {
            slidesPerView: 3
          },

          1200: {
            slidesPerView: 4
          }
        }"
        class="credit-swiper"
      > -->
      <Swiper @swiper="onSwiper" :modules="modules" :slides-per-view="'auto'" :space-between="22" :grab-cursor="true"
        :pagination="{
          clickable: true
        }" :breakpoints="{
          640: {
            slidesPerView: 2
          },

          992: {
            slidesPerView: 3
          },

          1200: {
            slidesPerView: 4
          }
        }" class="credit-swiper">
        <SwiperSlide v-for="credit in filteredCredits" :key="credit.id">
          <div class="credit-card">

            <div class="icon-box" :style="{
              background:
                credit.color
            }">
              <img :src="credit.icon" :alt="credit.title" class="icon-image" />
            </div>

            <span class="category">
              {{ credit.category }}
            </span>

            <h3>
              {{ credit.title }}
            </h3>

            <p>
              {{ credit.description }}
            </p>

            <button class="credit-btn">
              Saiba mais →
            </button>

          </div>
        </SwiperSlide>
      </Swiper>

      <!-- MOBILE BUTTON -->
      <div class="mobile-button">
        <a href="/linhas-de-credito" class="view-all">
          Ver todas as linhas →
        </a>
      </div>

    </div>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue'

import {
  Swiper,
  SwiperSlide
} from 'swiper/vue'

import {
  Pagination
} from 'swiper/modules'

import 'swiper/css'
import 'swiper/css/pagination'

const modules = [Pagination]

const swiper = ref(null)

const onSwiper = (instance) => {
  swiper.value = instance
}

const selectedCategory =
  ref('Todas')

const categories = [
  'Todas',
  'Empresas',
  'Agro',
  'Turismo',
  'Especiais'
]

const credits = ref([
  {
    id: 1,
    title: 'Microcrédito Online',
    category: 'Empresas',
    description:
      ' Até R$20 mil. Crédito ideal para microempreendedores expandirem seus negócios.',

    icon: '/icons/microcredito2.png',
    color: '#EEF4FF'
  },

  {
    id: 2,
    title: 'Crédito Online',
    category: 'Empresas',
    description:
      'Até R$50 mil. Financiamento para expansão e crescimento sustentável.',

    icon: '/icons/credito-online.png',
    color: '#ECFDF3'
  },

  {
    id: 3,
    title: 'Mãos que Criam',
    category: 'Especiais',
    description:
      'Até R$15 mil para artesãos e pequenos produtores culturais.',

    icon: '/icons/maos.svg',
    color: '#F0FDF4'
  },

  {
    id: 4,
    title: 'Agricultura Familiar',
    category: 'Agro',
    description:
      'Crédito para impulsionar pequenos produtores rurais.',

    icon: '/icons/agricultura-familiar.svg',
    color: '#FEFCE8'
  },

  {
    id: 5,
    title: 'Fungetur - MEI',
    category: 'Turismo',
    description:
      'Até R$20 mil. Invista no crescimento do seu negócio turístico.',

    icon: '/icons/fungetur.svg',
    color: '#FFF7ED'
  },
  {
    id: 6,
    title: 'Fungetur - ME',
    category: 'Turismo',
    description:
      'Até R$50 mil. Invista no crescimento do seu negócio turístico.',

    icon: '/icons/fungetur2.svg',
    color: '#FFF7ED'
  },
  {
    id: 6,
    title: 'Fungetur - Média e Grande porte',
    category: 'Turismo',
    description:
      'De R$50 mil a R$300 mil. Invista no crescimento do seu negócio turístico.',

    icon: '/icons/fungetur2.svg',
    color: '#FFF7ED'
  },
  {
    id: 7,
    title: 'Crédito BNDES',
    category: 'Especiais',
    description:
      'De R$50 mil a R$300 mil. Financiamento para projetos de investimento e capital de giro.',
    icon: '/icons/bndes.svg',
    color: '#FAF5FF'
  },
  {
    id: 8,
    title: 'Crédito Pronaf B',
    category: 'Agro',
    description:
      'Mulher: Até R$15 mil Homem: Até R$12 mil',
    icon: '/icons/pronaf.svg',
    color: '#FAF5FF'
  },
  {
    id: 9,
    title: 'Crédito Popular',
    category: 'Especiais',
    description:
      '',
    icon: '/icons/crédito-online.svg',
    color: '#FAF5FF'
  }
])

const filteredCredits =
  computed(() => {

    if (
      selectedCategory.value ===
      'Todas'
    ) {
      return credits.value
    }

    return credits.value.filter(
      credit =>
        credit.category ===
        selectedCategory.value
    )
  })
</script>

<style scoped>
.credit-section {
  padding: 90px 0;
  background: var(--color-bg-alt);
}

/* HEADER */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: 20px;
  margin-bottom: 35px;
}

.badge {
  display: inline-flex;
  padding: 10px 18px;
  border-radius: 999px;
  background: var(--color-accent);
  color: var(--color-white);
  font-weight: 600;
  margin-bottom: 18px;
}

.section-header h2 {
  font-size: 42px;
  color: var(--color-primary);
}

.section-header p {
  color: var(--color-text-muted);
  margin-top: 10px;
}

.view-all {
  color: var(--color-accent);
  text-decoration: none;
  font-weight: bold;
}

/* TABS */
.tabs {
  display: flex;
  gap: 14px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.tab {
  border: none;
  background: var(--color-bg);
  height: 48px;
  padding: 0 22px;
  border-radius: 999px;
  cursor: pointer;
  transition: var(--transition);
  font-weight: 600;
  color: var(--color-text);
}

.tab:hover {
  background: var(--color-bg-alt);
}

.tab.active {
  background: var(--color-accent);
  color: var(--color-white);
}

/* TOP */
.carousel-top {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 24px;
}

.navigation-buttons {
  display: flex;
  gap: 12px;
}

/* BUTTON */
.arrow-btn {
  width: 54px;
  height: 54px;
  border-radius: 50%;
  border: none;

  background: var(--color-bg);
  color: var(--color-accent);

  font-size: 22px;
  cursor: pointer;
  transition: var(--transition);

  box-shadow:
    0 10px 30px rgba(0, 0, 0, .08);
}

.arrow-btn:hover {
  transform: translateY(-3px);

  background: var(--color-accent);
  color: var(--color-white);
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

:deep(.swiper-pagination-bullet-active) {
  background: var(--color-accent);
}

/* CARD */
.credit-card {
  width: 100%;
  min-height: 360px;
  height: 100%;

  background: var(--color-bg);
  border-radius: 28px;
  padding: 30px;
  border: 1px solid var(--color-bg-alt);

  display: flex;
  flex-direction: column;

  transition: var(--transition);
}

.credit-card:hover {
  transform: translateY(-8px);

  box-shadow:
    0 20px 40px rgba(0, 0, 0, .08);
}

.icon-box {
  width: 75px;
  height: 75px;
  border-radius: 22px;

  display: flex;
  align-items: center;
  justify-content: center;

  margin-bottom: 20px;
  overflow: hidden;
}

.icon-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.category {
  color: var(--color-accent);
  font-size: 14px;
  font-weight: 600;
}

.credit-card h3 {
  font-size: 24px;
  color: var(--color-text);
  margin: 12px 0;
  min-height: 62px;
}

.credit-card p {
  color: var(--color-text-muted);
  line-height: 1.7;

  flex: 1;
  min-height: 72px;
}

.credit-btn {
  border: none;
  background: transparent;
  color: var(--color-accent);
  font-weight: bold;
  cursor: pointer;
  margin-top: auto;
  transition: var(--transition);
}

.credit-btn:hover {
  transform: translateX(4px);
}

/* MOBILE */
.mobile-button {
  display: none;
}

@media(max-width:768px) {

  .credit-section {
    padding: 60px 0;
  }

  .section-header {
    flex-direction: column;
    align-items: start;
  }

  .section-header h2 {
    font-size: 30px;
  }

  .desktop-link {
    display: none;
  }

  .mobile-button {
    display: flex;
    justify-content: center;
    margin-top: 24px;
  }

  .carousel-top {
    justify-content: center;
  }

  .arrow-btn {
    width: 46px;
    height: 46px;
  }

  .credit-card {
    min-height: 330px;
    padding: 28px;
  }
}
</style>