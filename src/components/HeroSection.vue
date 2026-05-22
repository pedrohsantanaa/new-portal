<template>
  <section class="hero">

    <div class="container">

      <!-- TABS -->
      <div class="hero-tabs">

        <button
          v-for="item in heroItems"
          :key="item.id"
          class="hero-tab"
          :class="{
            active:
              selectedHero.id === item.id
          }"
          @click="selectedHero = item"
        >
          {{ item.tab }}
        </button>

      </div>

      <!-- CONTENT -->
      <Transition
        name="hero"
        mode="out-in"
      >
        <div
          :key="selectedHero.id"
          class="hero-content"
          :class="selectedHero.layout"
        >

          <!-- SPLIT -->
          <template
            v-if="
              selectedHero.layout ===
              'split'
            "
          >
            <div class="hero-text">

              <span
                v-if="
                  selectedHero.badge
                "
                class="badge"
              >
                {{ selectedHero.badge }}
              </span>

              <h1>
                {{ selectedHero.title }}
              </h1>

              <p>
                {{
                  selectedHero.description
                }}
              </p>

              <div class="buttons">

                <a
                  v-for="button in selectedHero.buttons"
                  :key="
                    button.label
                  "
                  :href="
                    button.link
                  "
                  class="hero-btn"
                  :class="
                    button.type
                  "
                >
                  {{ button.label }}
                </a>

              </div>

            </div>

            <div
              class="hero-image"
            >
              <img
                :src="
                  selectedHero.image
                "
                :alt="
                  selectedHero.title
                "
              />
            </div>
          </template>

          <!-- FULL -->
          <template
            v-else-if="
              selectedHero.layout ===
              'full'
            "
          >
            <div
              class="
                hero-full
              "
            >
              <img
                :src="
                  selectedHero.image
                "
                class="
                  full-image
                "
              />

              <div
                class="
                  hero-overlay
                "
              />

              <div
                class="
                  hero-full-content
                "
              >
                <span
                  class="
                    badge
                  "
                >
                  {{
                    selectedHero.badge
                  }}
                </span>

                <h1>
                  {{
                    selectedHero.title
                  }}
                </h1>

                <p>
                  {{
                    selectedHero.description
                  }}
                </p>

                <a
                  :href="
                    selectedHero.buttons[0].link
                  "
                  class="
                    hero-btn
                    primary
                  "
                >
                  {{
                    selectedHero.buttons[0].label
                  }}
                </a>
              </div>
            </div>
          </template>

        </div>
      </Transition>

    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const heroItems = [
  {
    id: 1,
    tab: 'Empresarial',
    layout: 'split',

    badge:
      'Crédito Empresarial',

    title:
      'Impulsione o seu negócio com crédito inteligente',

    description:
      'Soluções financeiras acessíveis para pequenos empreendedores.',

    image:
      'https://images.unsplash.com/photo-1556157382-97eda2d62296?w=1200',

    buttons: [
      {
        label:
          'Solicitar Crédito',

        type: 'primary',
        link: '#'
      },

      {
        label:
          'Simular Agora',

        type: 'secondary',
        link: '#'
      }
    ]
  },

  {
    id: 2,
    tab: 'Mulher',
    layout: 'full',

    badge:
      'Mulher Empreendedora',

    title:
      'Transforme sonhos em oportunidades',

    description:
      'Linha especial de crédito para mulheres empreendedoras.',

    image:
      'https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=1200',

    buttons: [
      {
        label:
          'Saiba Mais',

        type: 'primary',
        link: '#'
      }
    ]
  },

  {
    id: 3,
    tab: 'Rural',
    layout: 'split',

    badge:
      'Produtor Rural',

    title:
      'Invista no crescimento do campo',

    description:
      'Linhas especiais para agricultura e produção rural.',

    image:
      'https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=1200',

    buttons: [
      {
        label:
          'Conhecer Linhas',

        type: 'primary',
        link: '#'
      }
    ]
  },

  {
    id: 4,
    tab: 'Turismo',
    layout: 'split',

    badge:
      'Turismo',

    title:
      'Fortaleça o turismo regional',

    description:
      'Crédito ideal para pousadas, hotéis e turismo.',

    image:
      'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=1200',

    buttons: [
      {
        label:
          'Saiba Mais',

        type: 'primary',
        link: '#'
      }
    ]
  }
]

const selectedHero =
  ref(heroItems[0])
</script>

<style scoped>
.hero {
  background:
    linear-gradient(
      135deg,
      #082f63,
      #0f4c81
    );

  padding: 50px 0 80px;
}

/* TABS */
.hero-tabs {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 35px;
}

.hero-tab {
  height: 48px;
  padding: 0 22px;
  border-radius: 999px;
  border: none;

  background:
    rgba(255,255,255,.12);

  color: white;
  cursor: pointer;
  transition: .3s;
}

.hero-tab.active {
  background: white;
  color: #082f63;
}

/* CONTENT */
.hero-content.split {
  display: grid;
  grid-template-columns:
    1.1fr .9fr;

  align-items: center;
  gap: 40px;
}

.hero-text h1 {
  font-size:
    clamp(2.5rem,5vw,4.5rem);

  color: white;
  line-height: 1.1;
  margin: 20px 0;
}

.hero-text p {
  color:
    rgba(255,255,255,.85);

  line-height: 1.8;
  margin-bottom: 30px;
}

.hero-image img {
  width: 100%;
  object-fit: contain;
}

/* FULL */
.hero-full {
  position: relative;
  min-height: 600px;
  border-radius: 32px;
  overflow: hidden;
}

.full-image {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background:
    rgba(0,0,0,.45);
}

.hero-full-content {
  position: relative;
  z-index: 2;

  height: 600px;

  display: flex;
  flex-direction: column;
  justify-content: center;

  color: white;
  padding: 50px;
}

/* COMMON */
.badge {
  display: inline-flex;
  background:
    rgba(255,255,255,.12);

  padding: 10px 18px;
  border-radius: 999px;
  color: white;
}

.buttons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.hero-btn {
  padding: 16px 26px;
  border-radius: 14px;
  text-decoration: none;
  font-weight: bold;
}

.primary {
  background: #ffc107;
  color: black;
}

.secondary {
  background:
    rgba(255,255,255,.12);

  color: white;
}

/* MOBILE */
@media(max-width:992px){

  .hero-content.split {
    grid-template-columns:
      1fr;

    text-align: center;
  }

  .hero-image {
    order: -1;
  }

  .buttons {
    justify-content: center;
  }
}

@media(max-width:768px){

  .buttons {
    flex-direction: column;
  }

  .hero-btn {
    width: 100%;
    text-align: center;
  }

  .hero-full {
    min-height: 480px;
  }

  .hero-full-content {
    height: 480px;
    text-align: center;
    padding: 30px;
  }
}

/* TRANSITION */
.hero-enter-active,
.hero-leave-active {
  transition:
    opacity .35s ease,
    transform .35s ease;
}

.hero-enter-from,
.hero-leave-to {
  opacity: 0;
  transform:
    translateY(10px);
}
</style>