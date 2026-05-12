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

        <a
          href="/linhas-de-credito"
          class="view-all desktop-link"
        >
          Ver todas →
        </a>

      </div>

      <!-- TABS -->
      <div class="tabs">
        <button
          v-for="category in categories"
          :key="category"
          class="tab"
          :class="{
            active:
              selectedCategory === category
          }"
          @click="selectedCategory = category"
        >
          {{ category }}
        </button>
      </div>

      <!-- TOP ACTIONS -->
      <div class="carousel-top">

        <div class="navigation-buttons">

          <button
            class="arrow-btn"
            @click="swiper?.slidePrev()"
          >
            ←
          </button>

          <button
            class="arrow-btn"
            @click="swiper?.slideNext()"
          >
            →
          </button>

        </div>

      </div>

      <!-- CAROUSEL -->
      <Swiper
        @swiper="onSwiper"
        :modules="modules"
        :slides-per-view="1.1"
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
      >
        <SwiperSlide
          v-for="credit in filteredCredits"
          :key="credit.id"
        >
          <div class="credit-card">

            <div
              class="icon-box"
              :style="{
                background:
                  credit.color
              }"
            >
              {{ credit.icon }}
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
        <a
          href="/linhas-de-credito"
          class="view-all"
        >
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
    title: 'MEI',
    category: 'Empresas',
    description:
      'Crédito ideal para microempreendedores expandirem seus negócios.',

    icon: '👤',
    color: '#EEF4FF'
  },

  {
    id: 2,
    title: 'Pequena Empresa',
    category: 'Empresas',
    description:
      'Financiamento para expansão e crescimento sustentável.',

    icon: '🏢',
    color: '#ECFDF3'
  },

  {
    id: 3,
    title: 'Produtor Rural',
    category: 'Agro',
    description:
      'Linhas especiais para fortalecer o agronegócio.',

    icon: '🌱',
    color: '#F0FDF4'
  },

  {
    id: 4,
    title: 'Agricultura Familiar',
    category: 'Agro',
    description:
      'Crédito para impulsionar pequenos produtores rurais.',

    icon: '🚜',
    color: '#FEFCE8'
  },

  {
    id: 5,
    title: 'Turismo',
    category: 'Turismo',
    description:
      'Invista no crescimento do seu negócio turístico.',

    icon: '🧳',
    color: '#FFF7ED'
  },

  {
    id: 6,
    title: 'Mulher Empreendedora',
    category: 'Especiais',
    description:
      'Soluções financeiras exclusivas para mulheres.',

    icon: '👩',
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
  background: #f8fafc;
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
  background: #dbeafe;
  color: #083ea8;
  font-weight: 600;
  margin-bottom: 18px;
}

.section-header h2 {
  font-size: 42px;
  color: #0f2f63;
}

.section-header p {
  color: #64748b;
  margin-top: 10px;
}

.view-all {
  color: #083ea8;
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
  background: white;
  height: 48px;
  padding: 0 22px;
  border-radius: 999px;
  cursor: pointer;
  transition: .3s;
  font-weight: 600;
}

.tab:hover {
  background: #eff6ff;
}

.tab.active {
  background: #083ea8;
  color: white;
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

  background: white;
  color: #083ea8;

  font-size: 22px;
  cursor: pointer;
  transition: .3s;

  box-shadow:
    0 10px 30px rgba(0,0,0,.08);
}

.arrow-btn:hover {
  transform: translateY(-3px);

  background: #083ea8;
  color: white;
}

/* SWIPER */
.credit-swiper {
  overflow: visible;
  padding-bottom: 50px;
}

:deep(.swiper-slide) {
  display: flex;
  height: auto;
}

:deep(.swiper-pagination-bullet-active) {
  background: #083ea8;
}

/* CARD */
.credit-card {
  width: 100%;
  min-height: 360px;
  height: 100%;

  background: white;
  border-radius: 28px;
  padding: 30px;
  border: 1px solid #e2e8f0;

  display: flex;
  flex-direction: column;

  transition: .35s;
}

.credit-card:hover {
  transform: translateY(-8px);

  box-shadow:
    0 20px 40px rgba(0,0,0,.08);
}

.icon-box {
  width: 75px;
  height: 75px;
  border-radius: 22px;

  display: flex;
  align-items: center;
  justify-content: center;

  font-size: 34px;
  margin-bottom: 20px;
}

.category {
  color: #083ea8;
  font-size: 14px;
  font-weight: 600;
}

.credit-card h3 {
  font-size: 24px;
  color: #0f172a;
  margin: 12px 0;
  min-height: 62px;
}

.credit-card p {
  color: #64748b;
  line-height: 1.7;

  flex: 1;
  min-height: 72px;
}

.credit-btn {
  border: none;
  background: transparent;
  color: #083ea8;
  font-weight: bold;
  cursor: pointer;
  margin-top: auto;
  transition: .3s;
}

.credit-btn:hover {
  transform: translateX(4px);
}

/* MOBILE */
.mobile-button {
  display: none;
}

@media(max-width:768px){

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