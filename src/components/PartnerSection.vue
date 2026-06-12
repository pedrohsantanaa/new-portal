<template>
  <section class="partners-section">
    <div class="container">

      <!-- Header -->
      <div class="section-header">
        <span class="badge">
          Quem está conosco
        </span>

        <h2>
          Nossos parceiros
        </h2>
      </div>

      <!-- Carousel -->
      <div class="partners-slider">

        <div class="partners-track">

          <!-- lista duplicada para loop infinito -->
          <div v-for="partner in duplicatedPartners" :key="partner.id + Math.random()" class="partner-item">
            <img :src="partner.logo" :alt="partner.name" />
          </div>

        </div>

      </div>

    </div>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue'

const partners = ref([
  {
    id: 1,
    name: 'FACIET',
    logo: '/partners/logo_faciet.png'
  },

  {
    id: 2,
    name: 'FUNGETUR',
    logo: '/partners/fungetur_new.png'
  },

  {
    id: 3,
    name: 'SICS',
    logo: '/partners/sics-to.png'
  },

  {
    id: 4,
    name: 'Brasil',
    logo: '/partners/mtur.png'
  },

  {
    id: 5,
    name: 'SEBRAE',
    logo: '/partners/logo-sebrae.png'
  },
  {
    id: 6,
    name: 'FAET',
    logo: '/partners/logo-faet.jpg'
  },
  {
    id: 7,
    name: 'ABDE',
    logo: '/partners/logo-abde.png'
  },
  {
    id: 8,
    name: 'FCDL',
    logo: '/partners/logo-fcdl.png'
  },
  {
    id: 9,
    name: 'FECOMERCIO',
    logo: '/partners/logo-fecomercio.png'
  },
  {
    id: 10,
    name: 'SICON',
    logo: '/partners/logo-sicon.jpg'
  },
  {
    id: 11,
    name: 'SINDUSCON',
    logo: '/partners/logo-sinduscon.jpg'
  },
  {
    id: 12,
    name: 'GOVERNO DO TOCANTINS',
    logo: '/partners/new_logo_governo.png'
  }
])

/* duplicamos para loop infinito */
const duplicatedPartners =
  computed(() => [
    ...partners.value,
    ...partners.value
  ])
</script>

<style scoped>
.partners-section {
  padding: 80px 0;
  background: var(--color-bg);
  overflow: hidden;
}

/* HEADER */
.section-header {
  margin-bottom: 40px;
}

.badge {
  display: inline-flex;
  padding: 10px 18px;
  border-radius: var(--radius-full);
  background: var(--color-bg-alt);
  color: var(--color-accent);
  font-weight: 600;
  margin-bottom: 18px;
}

.section-header h2 {
  font-size: clamp(1.8rem, 4vw, 3rem);
  color: var(--color-primary);
}

/* SLIDER */
.partners-slider {
  position: relative;
  overflow: hidden;
}

/* fade laterais */
.partners-slider::before,
.partners-slider::after {
  content: '';
  position: absolute;
  top: 0;
  width: 120px;
  height: 100%;
  z-index: 2;
}

.partners-slider::before {
  left: 0;
  background: linear-gradient(to right, var(--color-bg), transparent);
}

.partners-slider::after {
  right: 0;
  background: linear-gradient(to left, var(--color-bg), transparent);
}

/* TRACK */
.partners-track {
  display: flex;
  align-items: center;
  gap: 80px;
  width: max-content;
  animation: scroll 25s linear infinite;
}

.partner-item {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.partner-item img {
  height: 80px;
  width: auto;
  object-fit: contain;
  opacity: 0.75;
  transition: var(--transition);
  filter: grayscale(100%);
}

.partner-item:hover img {
  opacity: 1;
  filter: grayscale(0%);
  transform: scale(1.05);
}

/* LOOP */
@keyframes scroll {
  from { transform: translateX(0); }
  to { transform: translateX(-50%); }
}

/* TABLET */
@media(max-width:992px) {
  .partners-track {
    gap: 50px;
  }

  .partner-item img {
    height: 65px;
  }
}

/* MOBILE */
@media(max-width:768px) {
  .partners-section {
    padding: 60px 0;
  }

  .section-header {
    text-align: center;
  }

  .partners-track {
    gap: 40px;
  }

  .partner-item img {
    height: 50px;
  }

  .partners-slider::before,
  .partners-slider::after {
    width: 50px;
  }
}
</style>