<template>
  <section class="news-section">
    <div class="container">

      <!-- Header -->
      <div class="section-header">

        <div>
          <h2>
            Notícias em destaque
          </h2>

          <p>
            Fique por dentro das novidades
            e ações da instituição.
          </p>
        </div>

        <a
          href="#"
          class="view-all"
        >
          Ver todas →
        </a>
      </div>

      <!-- Grid -->
      <div class="news-grid">

        <article
          v-for="news in newsList"
          :key="news.id"
          class="news-card"
        >
          <!-- Image -->
          <div class="image-wrapper">
            <img
              :src="news.image"
              :alt="news.title"
            />

            <span class="tag">
              {{ news.category }}
            </span>
          </div>

          <!-- Content -->
          <div class="news-content">

            <h3>
              {{ news.title }}
            </h3>

            <p>
              {{ news.description }}
            </p>

            <div class="news-footer">
              <span>
                {{ news.date }}
              </span>

              <span>
                {{ news.readingTime }}
              </span>
            </div>

          </div>
        </article>

      </div>

    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const newsList = ref([
  {
    id: 1,
    category: 'Crédito',
    title:
      'Nova linha de financiamento para empreendedores',

    description:
      'Programa amplia acesso ao crédito para pequenos negócios.',

    date: '20 de maio de 2026',
    readingTime: '3 min leitura',

    image:
      'https://images.unsplash.com/photo-1556740749-887f6717d7e4?w=1200'
  },

  {
    id: 2,
    category: 'Programa',
    title:
      'Projeto fortalece pequenos negócios locais',

    description:
      'Empreendedores recebem apoio financeiro e capacitação.',

    date: '18 de maio de 2026',
    readingTime: '2 min leitura',

    image:
      'https://images.unsplash.com/photo-1521791136064-7986c2920216?w=1200'
  },

  {
    id: 3,
    category: 'Evento',
    title:
      'Instituição participa de feira de inovação',

    description:
      'Evento reuniu empresários e startups da região.',

    date: '15 de maio de 2026',
    readingTime: '4 min leitura',

    image:
      'https://images.unsplash.com/photo-1511578314322-379afb476865?w=1200'
  },

  {
    id: 4,
    category: 'Empreendedorismo',
    title:
      'Mulheres empreendedoras ganham incentivo',

    description:
      'Nova iniciativa amplia oportunidades de crescimento.',

    date: '12 de maio de 2026',
    readingTime: '3 min leitura',

    image:
      'https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=1200'
  }
])
</script>

<style scoped>
.news-section {
  padding: 80px 0;
  background: var(--color-bg-alt);
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
  color: var(--color-accent);
  text-decoration: none;
  font-weight: 700;
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
  border: 1px solid var(--color-border);
  transition: var(--transition);
  cursor: pointer;
}

.news-card:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-hover);
}

.image-wrapper {
  position: relative;
}

.image-wrapper img {
  width: 100%;
  height: 220px;
  object-fit: cover;
}

/* TAG */
.tag {
  position: absolute;
  top: 16px;
  left: 16px;
  background: var(--color-green);
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
  color: var(--color-text-muted);
  font-size: 13px;
  opacity: 0.8;
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
}
</style>