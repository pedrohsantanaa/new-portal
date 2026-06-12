<template>
  <section class="services-section">
    <div class="container">

      <!-- Header -->
      <div class="section-header">
        <h2>
          Serviços rápidos
        </h2>

        <p>
          Acesse os principais serviços
          com rapidez e praticidade.
        </p>
      </div>

      <!-- Grid -->
      <div class="services-grid">

        <a
          v-for="service in services"
          :key="service.id"
          :href="service.link"
          class="service-card"
        >
          <div class="icon-wrapper">
            {{ service.icon }}
          </div>

          <h3>
            {{ service.title }}
          </h3>
        </a>

      </div>

    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const services = ref([
  {
    id: 1,
    title: 'Consultar Protocolo',
    icon: '📄',
    link: '#'
  },

  {
    id: 2,
    title: 'Emitir Boleto',
    icon: '💳',
    link: '#'
  },

  {
    id: 3,
    title: 'Segunda Via',
    icon: '📑',
    link: '#'
  },

  {
    id: 4,
    title: 'Simulador',
    icon: '🧮',
    link: '#'
  },

  {
    id: 5,
    title: 'Perguntas Frequentes',
    icon: '❓',
    link: '#'
  },

  {
    id: 6,
    title: 'Ouvidoria',
    icon: '🗣️',
    link: '#'
  },

  {
    id: 7,
    title: 'Fale Conosco',
    icon: '📞',
    link: '#'
  },

  {
    id: 8,
    title: 'Transparência',
    icon: '📊',
    link: '#'
  }
])
</script>

<style scoped>
.services-section {
  padding: 80px 0;
  background: var(--color-bg);
}

/* HEADER */
.section-header {
  text-align: center;
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

/* GRID */
.services-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

/* CARD */
.service-card {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 35px 20px;
  text-decoration: none;
  text-align: center;
  transition: var(--transition);
}

.service-card:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-hover);
  border-color: var(--color-accent);
}

.icon-wrapper {
  width: 72px;
  height: 72px;
  margin: 0 auto 20px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--color-bg-alt), var(--color-border));
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 34px;
}

.service-card h3 {
  color: var(--color-text);
  font-size: 18px;
  line-height: 1.5;
  font-weight: 700;
}

/* TABLET */
@media(max-width:1100px){
  .services-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* MOBILE */
@media(max-width:768px){
  .services-section {
    padding: 60px 0;
  }

  .services-grid {
    grid-template-columns: 1fr;
  }

  .service-card {
    padding: 28px;
  }
}
</style>