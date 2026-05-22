<template>
  <section class="hero">

    <!-- SPLIT LAYOUT -->
    <Transition name="fade" mode="out-in">
      <div :key="activeSlide.id">

        <!-- ===================================== -->
        <!-- SPLIT -->
        <!-- ===================================== -->
        <div v-if="activeSlide.type === 'split'" class="hero-split container">

          <div class="hero-text">

            <span v-if="activeSlide.badge" class="badge">
              {{ activeSlide.badge }}
            </span>

            <h1>
              {{ activeSlide.title }}
            </h1>

            <p v-if="
              activeSlide.description
            ">
              {{ activeSlide.description }}
            </p>

            <div v-if="
              activeSlide.buttons
                ?.length
            " class="buttons">
              <a v-for="button in activeSlide.buttons" :key="button.label" :href="button.link" class="hero-btn"
                :class="button.type">
                {{ button.label }}
              </a>
            </div>

          </div>

          <div v-if="activeSlide.image" class="hero-image">
            <img :src="activeSlide.image" :alt="activeSlide.title
              " />
          </div>

        </div>

        <!-- ===================================== -->
        <!-- FULL BANNER -->
        <!-- ===================================== -->
        <div v-else-if="
          activeSlide.type ===
          'full-banner'
        " class="hero-full">

          <img :src="activeSlide.image
            " class="banner-image" />

          <div class="overlay"></div>

          <div class="
              hero-full-content
              container
            ">
            <span v-if="
              activeSlide.badge
            " class="badge">
              {{ activeSlide.badge }}
            </span>

            <h1>
              {{ activeSlide.title }}
            </h1>

            <p v-if="
              activeSlide.description
            ">
              {{ activeSlide.description }}
            </p>

            <div v-if="
              activeSlide.buttons
                ?.length
            " class="buttons btn-full">
              <a v-for="button in activeSlide.buttons" :key="button.label" :href="button.link" class="hero-btn"
                :class="button.type">
                {{ button.label }}
              </a>
            </div>

          </div>

        </div>

        <!-- ===================================== -->
        <!-- SIMPLE -->
        <!-- ===================================== -->
        <div v-else class="
            hero-simple
            container
          ">

          <span v-if="
            activeSlide.badge
          " class="badge">
            {{ activeSlide.badge }}
          </span>

          <h1>
            {{ activeSlide.title }}
          </h1>

          <p v-if="
            activeSlide.description
          ">
            {{ activeSlide.description }}
          </p>

          <div v-if="
            activeSlide.buttons
              ?.length
          " class="buttons">
            <a v-for="button in activeSlide.buttons" :key="button.label" :href="button.link" class="hero-btn"
              :class="button.type">
              {{ button.label }}
            </a>
          </div>

        </div>

      </div>
    </Transition>

    <!-- DOTS -->
    <div class="dots">
      <button v-for="(_, index) in slides" :key="index" class="dot" :class="{
        active:
          currentSlide ===
          index
      }" @click="
        currentSlide = index
        " />
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
  // {
  //   id: 1,
  //   type: 'full-banner',

  //   badge:
  //     '',

  //   title:
  //     '',

  //   description:
  //     '',

  //   image:
  //     'b1.png',

  //   buttons: [
  //     {
  //       label:
  //         'Acesse o Dashboard',

  //       type: 'primary',
  //       link: '#'
  //     }
  //   ]
  // },
  // {
  //   id: 2,
  //   type: 'full-banner',

  //   badge:
  //     '',

  //   title:
  //     '',

  //   description:
  //     '',

  //   image:
  //     'b3.png',

  //   buttons: [
  //     {
  //       label:
  //         'Nossa localização',

  //       type: 'primary',
  //       link: '#'
  //     }
  //   ]
  // },
  {
    id: 1,
    type: 'split',

    badge:
      'Crédito Empresarial',

    title:
      'Impulsione o seu negócio com crédito inteligente',

    description:
      'Soluções financeiras acessíveis para pequenos empreendedores.',

    image:
      'b1.png',

    buttons: [
      {
        label:
          'Solicitar Crédito',

        type: 'primary',
        link: '#'
      },

      // {
      //   label:
      //     'Simular Agora',

      //   type: 'secondary',
      //   link: '#'
      // }
    ]
  },
    {
    id: 2,
    type: 'split',

    badge:
      'Localização',

    title:
      'Onde estamos',

    description:
      '',

    image:
      'b3.png',

    buttons: [
      {
        label:
          'Solicitar Crédito',

        type: 'primary',
        link: '#'
      },

      // {
      //   label:
      //     'Simular Agora',

      //   type: 'secondary',
      //   link: '#'
      // }
    ]
  },


  // {
  //   id: 4,
  //   type: 'simple',

  //   badge:
  //     'Turismo',

  //   title:
  //     'Linhas especiais para turismo',

  //   description:
  //     'Invista no crescimento do turismo regional.',

  //   buttons: [
  //     {
  //       label:
  //         'Conhecer Linhas',

  //       type: 'primary',
  //       link: '#'
  //     }
  //   ]
  // }
])

const activeSlide =
  computed(() =>
    slides.value[
    currentSlide.value
    ]
  )

onMounted(() => {
  interval = setInterval(() => {

    currentSlide.value =
      (
        currentSlide.value + 1
      ) %
      slides.value.length

  }, 5000)
})

onUnmounted(() => {
  clearInterval(interval)
})
</script>

<style scoped>
.hero {
  background:
    linear-gradient(135deg,
      #082f63,
      #0f4c81);

  position: relative;
  overflow: hidden;
}

/* SPLIT */
.hero-split {
  min-height: 650px;

  display: grid;
  grid-template-columns:
    1.1fr .9fr;

  align-items: center;
  gap: 40px;
}

/* FULL */
.hero-full {
  min-height: auto;
  position: relative;
}

.banner-image {
  width: 100%;
  height: 700px;
  object-fit: cover;
}

.overlay {
  position: absolute;
  inset: 0;

  background:
    linear-gradient(rgba(0, 0, 0, .5),
      rgba(0, 0, 0, .5));
}

.hero-full-content {
  position: absolute;
  inset: 0;

  display: flex;
  flex-direction: column;
  justify-content: center;

  color: white;
}

/* SIMPLE */
.hero-simple {
  min-height: 650px;

  display: flex;
  flex-direction: column;
  justify-content: center;

  max-width: 700px;
}

/* COMMON */
.hero-text h1,
.hero-simple h1,
.hero-full h1 {
  font-size: clamp(2.5rem,
      5vw,
      4.5rem);

  color: white;
  line-height: 1.1;
}

.hero-text p,
.hero-simple p,
.hero-full p {
  color:
    rgba(255, 255, 255, .85);

  margin: 24px 0;
  line-height: 1.8;
}

.badge {
  display: inline-flex;
  background:
    rgba(255, 255, 255, .12);

  padding: 12px 20px;
  border-radius: 999px;
  color: white;
  margin-bottom: 20px;
}

.buttons {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
}

.hero-btn {
  padding: 16px 28px;
  border-radius: 14px;
  text-decoration: none;
  font-weight: 700;

}

.primary {
  background: #ffc107;
  color: black;
}

.secondary {
  background:
    rgba(255, 255, 255, .12);

  color: white;
}

.hero-image img {
  width: 100%;
  object-fit: contain;
}

/* DOTS */
.dots {
  position: absolute;
  bottom: 30px;
  left: 50%;
  transform:
    translateX(-50%);

  display: flex;
  gap: 10px;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 999px;
  border: none;
  cursor: pointer;

  background:
    rgba(255, 255, 255, .4);
}

.dot.active {
  width: 40px;
  background: white;
}

.btn-full {
  justify-content: center;
}

/* RESPONSIVO */
@media(max-width:992px) {

  .hero-split {
    grid-template-columns: 1fr;
    text-align: center;
    padding: 70px 0;
    min-height: auto;
  }

  .hero-image {
    order: -1;
  }

  .hero-image img {
    max-width: 450px;
    margin: 0 auto;
  }

  .buttons {
    justify-content: center;
  }

  .hero-full {
    min-height: auto;
  }

  .hero-full-content {
    min-height: 520px;
    text-align: center;
    align-items: center;
  }

  .hero-simple {
    min-height: auto;
    text-align: center;
    padding: 90px 0;
  }
}

@media(max-width:768px) {

  .hero {
    overflow: hidden;
  }

  /* FULL */
  .hero-full {
    min-height: auto;
  }

  .hero-full-content {
    min-height: 460px;
    padding: 80px 0;
  }

  .hero-full h1 {
    font-size: 2.2rem;
  }

  /* SPLIT */
  .hero-split {
    padding: 50px 0;
  }

  .hero-image img {
    max-width: 100%;
  }

  /* BUTTONS */
  .buttons {
    flex-direction: column;
    width: 100%;
  }

  .hero-btn {
    width: 100%;
    text-align: center;
  }

  /* TEXT */
  .hero-text h1,
  .hero-simple h1,
  .hero-full h1 {
    font-size: 2.2rem;
    line-height: 1.2;
  }

  .hero-text p,
  .hero-simple p,
  .hero-full p {
    font-size: 1rem;
  }
}

/* TRANSITION */
.fade-enter-active,
.fade-leave-active {
  transition:
    opacity .5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>