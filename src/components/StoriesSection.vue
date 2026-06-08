<template>
  <section class="stories-section">
    <div class="container">

      <!-- Header -->
      <div class="section-header">
        <h2>
          Histórias que inspiram
        </h2>

        <p>
          Conheça empreendedores que
          transformaram seus sonhos
          em realidade.
        </p>
      </div>

      <!-- Carousel -->
      <div class="carousel-wrapper">

        <button
          class="nav prev"
          @click="prevSlide"
        >
          ‹
        </button>

        <div class="carousel">
          <div
            class="track"
            :style="{
              transform:
                `translateX(-${currentSlide * slideWidth}%)`
            }"
          >
            <div
              v-for="story in stories"
              :key="story.id"
              class="story-card"
            >
              <img
                :src="story.image"
                :alt="story.name"
              />

              <div class="story-content">

                <div class="quote">
                  "
                </div>

                <p>
                  {{ story.text }}
                </p>

                <h3>
                  {{ story.name }}
                </h3>

                <span>
                  {{ story.city }}
                </span>
<!-- 
                <div class="funding">
                  Financiamento:
                  <strong>
                    {{ story.value }}
                  </strong>
                </div> -->

              </div>
            </div>
          </div>
        </div>

        <button
          class="nav next"
          @click="nextSlide"
        >
          ›
        </button>

      </div>

      <!-- Dots -->
      <div class="dots">
        <span
          v-for="(_, index) in totalDots"
          :key="index"
          :class="[
            'dot',
            {
              active:
                currentSlide === index
            }
          ]"
          @click="goTo(index)"
        />
      </div>

    </div>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue'

const currentSlide = ref(0)

const stories = ref([
  {
    id: 1,
    name: 'Ivãyres Rodrigues Sousa',
    city: 'São Miguel do Tocantins',
    value: '',
    text:
      'Venho por meio dessa nota agradecer primeiramente a Deus e a agência do FOMENTO ao governo do estado TO por essa ação para os micro empreendedores que assim como eu precisam de recursos para o investimento no empreendimento, graças a essa ação consegui o recurso necessário que irá me ajudar a impulsionar ainda mais as vendas eu irei usa-lo em compras de mercadorias . Irei investir esse crédito de forma consciente e sou muito grata pela a credibilidade!',

    image:
      'public/stories/ivayres.jpg'
  },

  {
    id: 2,
    name: 'Marialber',
    city: 'Araguaína - TO',
    value: '0',
    text:
      'Sou imensamente grata pelo apoio que recebi da Agência de Fomento. Através da linha Crédito Popular, consegui recurso para alavancar o meu pequeno negócio. Aumentei a minha produção com os maquinários adquiridos e consequentemente o a renda familiar.',

    image:
      'public/stories/marialber.jpeg'
  },
  {
    id: 3,
    name: 'Leticia França',
    city: 'Palmas – Tocantins',
    value: '0',
    text:
      'Padaria e Confeitaria.\n Linha de crédito: Capital de Giro - Recurso próprio.',
    image:
      'public/stories/leticia.jpg'
  },

])

const cardsPerView = 3
const slideWidth = 100 / cardsPerView

const totalDots = computed(() =>
  Math.ceil(
    stories.value.length / cardsPerView
  )
)

const nextSlide = () => {
  if (
    currentSlide.value <
    totalDots.value - 1
  ) {
    currentSlide.value++
  } else {
    currentSlide.value = 0
  }
}

const prevSlide = () => {
  if (currentSlide.value > 0) {
    currentSlide.value--
  } else {
    currentSlide.value =
      totalDots.value - 1
  }
}

const goTo = (index) => {
  currentSlide.value = index
}
</script>

<style scoped>
.stories-section {
  padding: 90px 0;
  background: white;
}

.section-header {
  text-align: center;
  margin-bottom: 50px;
}

.section-header h2 {
  font-size: 42px;
  color: #0f2f63;
}

.section-header p {
  color: #64748b;
  margin-top: 12px;

}

.carousel-wrapper {
  position: relative;
}

.carousel {
  overflow: hidden;
}

.track {
  display: flex;
  transition: .5s ease;
  gap: 24px;
}

.story-card {
  min-width: calc(33.333% - 16px);
  background: #fff;
  border-radius: 28px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
  transition: .3s;
}

.story-card:hover {
  transform: translateY(-6px);
  box-shadow:
    0 20px 40px rgba(0,0,0,.08);
}

.story-card img {
  width: 100%;
  height: 350px;
  object-fit: cover;
}

.story-content {
  padding: 28px;
}

.quote {
  font-size: 50px;
  color: #16a34a;
}

.story-content p {
  color: #475569;
  line-height: 1.8;
  margin-bottom: 20px;
  text-align: justify;
}

.story-content h3 {
  color: #0f172a;
}

.story-content span {
  color: #64748b;
}

.funding {
  margin-top: 20px;
  color: #334155;
}

.nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 52px;
  height: 52px;
  border: none;
  border-radius: 50%;
  background: white;
  box-shadow:
    0 10px 30px rgba(0,0,0,.12);

  cursor: pointer;
  z-index: 10;
}

.prev {
  left: -20px;
}

.next {
  right: -20px;
}

.dots {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 30px;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #cbd5e1;
  cursor: pointer;
}

.dot.active {
  background: #16a34a;
}

/* RESPONSIVO */
@media(max-width:992px){

  .story-card {
    min-width: calc(50% - 12px);
  }
}

@media(max-width:768px){

  .story-card {
    min-width: 100%;
  }

  .section-header h2 {
    font-size: 30px;
  }

  .nav {
    display: none;
  }
}
</style>