<template>
  <section class="hero">

    <!-- BACKGROUND SHAPES -->
    <div class="hero-bg-shape shape-1"></div>
    <div class="hero-bg-shape shape-2"></div>

    <div class="container hero-wrapper">

      <!-- CONTENT -->
      <Transition name="fade" mode="out-in">

        <div
          class="hero-content"
          :key="currentSlide"
        >
          <!-- LEFT -->
          <div class="hero-text">

            <span class="badge">
              {{ activeSlide.badge }}
            </span>

            <h1>
              {{ activeSlide.title }}
            </h1>

            <p>
              {{ activeSlide.description }}
            </p>

            <div class="buttons">

              <button class="btn-primary">
                Solicitar Crédito
              </button>

              <button class="btn-secondary">
                Simular Agora
              </button>

            </div>

            <!-- Dots -->
            <div class="dots">

              <button
                v-for="(_, index) in slides"
                :key="index"
                class="dot"
                :class="{
                  active:
                    currentSlide === index
                }"
                @click="goToSlide(index)"
              />

            </div>

          </div>

          <!-- RIGHT -->
          <div class="hero-image">

            <img
              :src="activeSlide.image"
              :alt="activeSlide.title"
            />

          </div>

        </div>

      </Transition>

    </div>
  </section>
</template>

<script setup>
import {
  computed,
  onMounted,
  onUnmounted,
  ref
} from 'vue'

const currentSlide = ref(0)

let interval = null

const slides = ref([
  {
    badge: 'Crédito Empresarial',

    title:
      'Impulsione o seu negócio com crédito inteligente',

    description:
      'Soluções financeiras acessíveis para pequenos empreendedores, empresas e projetos inovadores.',

    image:
      'https://images.unsplash.com/photo-1556157382-97eda2d62296?w=1200'
  },

  {
    badge: 'Mulher Empreendedora',

    title:
      'Transforme sonhos em oportunidades',

    description:
      'Tenha acesso às melhores condições para expandir seu negócio.',

    image:
      'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=1200'
  },

  {
    badge: 'Produtor Rural',

    title:
      'Invista no crescimento do campo',

    description:
      'Linhas especiais para agricultura, produção e desenvolvimento rural.',

    image:
      'https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=1200'
  }
])

const activeSlide =
computed(() => {
  return slides.value[
    currentSlide.value
  ]
})

const goToSlide = (index) => {
  currentSlide.value = index
}

const nextSlide = () => {
  currentSlide.value =
    (
      currentSlide.value + 1
    ) %
    slides.value.length
}

onMounted(() => {
  interval = setInterval(() => {
    nextSlide()
  }, 5000)
})

onUnmounted(() => {
  clearInterval(interval)
})
</script>

<style scoped>
.hero {
  position: relative;
  overflow: hidden;

  background:
    linear-gradient(
      135deg,
      #082f63,
      #0f4c81
    );

  padding: 70px 0;
}

/* SHAPES */
.hero-bg-shape {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: .15;
}

.shape-1 {
  width: 300px;
  height: 300px;
  background: #ffffff;
  top: -100px;
  right: -100px;
}

.shape-2 {
  width: 250px;
  height: 250px;
  background: #60a5fa;
  bottom: -100px;
  left: -100px;
}

/* CONTENT */
.hero-wrapper {
  position: relative;
  z-index: 2;
}

.hero-content {
  display: grid;
  grid-template-columns:
    1.1fr .9fr;

  align-items: center;
  gap: 30px;
}

/* TEXT */
.hero-text {
  max-width: 620px;
}

.badge {
  display: inline-flex;
  padding: 12px 20px;
  border-radius: 999px;

  background:
    rgba(255,255,255,.12);

  color: white;
  font-weight: 600;
  backdrop-filter: blur(10px);
}

.hero-text h1 {
  font-size: clamp(
    2.5rem,
    5vw,
    4.4rem
  );

  line-height: 1.1;
  color: white;

  margin:
    22px 0 20px;
}

.hero-text p {
  font-size: 1.15rem;
  line-height: 1.8;

  color:
    rgba(255,255,255,.82);

  margin-bottom: 34px;
}

/* BUTTONS */
.buttons {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
}

.btn-primary,
.btn-secondary {
  height: 56px;
  padding: 0 28px;
  border-radius: 14px;
  border: none;
  cursor: pointer;
  font-weight: bold;
  transition: .3s;
}

.btn-primary {
  background:
    linear-gradient(
      135deg,
      #ffc107,
      #f59e0b
    );
}

.btn-primary:hover {
  transform:
    translateY(-3px);
}

.btn-secondary {
  background:
    rgba(255,255,255,.08);

  border:
    1px solid rgba(
      255,
      255,
      255,
      .2
    );

  color: white;
}

.btn-secondary:hover {
  background:
    rgba(255,255,255,.15);
}

/* IMAGE */
.hero-image {
  display: flex;
  justify-content: center;
}

.hero-image img {
  width: 100%;
  max-width: 540px;
  height: auto;
  object-fit: contain;

  filter:
    drop-shadow(
      0 30px 50px
      rgba(0,0,0,.22)
    );
}

/* DOTS */
.dots {
  display: flex;
  gap: 12px;
  margin-top: 45px;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;

  border: none;
  cursor: pointer;

  background:
    rgba(255,255,255,.35);

  transition: .3s;
}

.dot.active {
  width: 38px;
  border-radius: 999px;
  background: white;
}

/* TRANSITION */
.fade-enter-active,
.fade-leave-active {
  transition:
    opacity .5s ease,
    transform .5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform:
    translateY(20px);
}

/* TABLET */
@media(max-width:992px){

  .hero {
    padding: 60px 0;
  }

  .hero-content {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .hero-text {
    max-width: 100%;
  }

  .buttons,
  .dots {
    justify-content: center;
  }

  .hero-image img {
    max-width: 430px;
    margin-top: 20px;
  }
}

/* MOBILE */
@media(max-width:768px){

  .hero {
    padding: 50px 0;
  }

  .hero-text h1 {
    font-size: 2.2rem;
  }

  .hero-text p {
    font-size: 1rem;
  }

  .buttons {
    flex-direction: column;
  }

  .btn-primary,
  .btn-secondary {
    width: 100%;
  }

  .hero-image img {
    max-width: 100%;
  }

  .dots {
    margin-top: 30px;
  }
}
</style>