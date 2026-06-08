<template>
    <section class="hero-banner">

        <!-- BACKGROUND -->
        <Transition name="fade" mode="out-in">
            <div :key="activeBanner.id" class="hero-slide">

                <!-- IMAGE -->
                <img :src="activeBanner.image" :alt="activeBanner.title" class="hero-image" />

                <!-- OVERLAY -->
                <div class="overlay" :class="{
                    light:
                        activeBanner
                            .overlay ===
                        'light'
                }" />

                <!-- CONTENT -->
                <div class="container hero-content">

                    <div class="content-wrapper" :class="activeBanner.align ||
                        'left'
                        ">

                        <!-- Badge -->
                        <span v-if="
                            activeBanner.badge
                        " class="badge">
                            {{
                                activeBanner.badge
                            }}
                        </span>

                        <!-- Title -->
                        <h1 v-if="
                            activeBanner.title
                        ">
                            {{
                                activeBanner.title
                            }}
                        </h1>

                        <!-- Description -->
                        <p v-if="
                            activeBanner.description
                        ">
                            {{
                                activeBanner.description
                            }}
                        </p>

                        <!-- Buttons -->
                        <div v-if="
                            activeBanner.buttons
                                ?.length
                        " class="buttons">
                            <a v-for="button in activeBanner.buttons" :key="button.label" :href="button.link"
                                class="hero-btn" :class="button.type
                                    ">
                                {{ button.label }}
                            </a>
                        </div>

                    </div>

                </div>

            </div>
        </Transition>

        <!-- DOTS -->
        <div class="dots">
            <button v-for="(_, index) in banners" :key="index" class="dot" :class="{
                active:
                    currentIndex ===
                    index
            }" @click="
                changeSlide(index)
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

const currentIndex = ref(0)

let interval = null

const banners = ref([
    {
        id: 1,
        type: 'location',

        badge:
            '',

        title:
            // 'Crédito para fortalecer o Tocantins',
           '',
        description:
            // 'Linhas especiais para produção rural e desenvolvimento agrícola.',
            '',
        image:
            '/carroussel/b7.png',

        overlay: 'dark',
        align: 'center',

        buttons: [
            {
                label:
                    'Conheça nossas linhas de crédito',

                type: 'primary',
                link: '#'
            },


        ]
    },
    {
        id: 2,
        type: 'location',

        badge:
            'ATENDIMENTO PRESENCIAL',

        title:
            'Estamos mais perto de você',

        description:
            'Conheça nossa agência em Palmas e receba atendimento especializado.',

        image:
            '/carroussel/b3.png',

        overlay: 'dark',
        align: 'left',

        buttons: [
            {
                label:
                    'Ver localização',

                type: 'primary',
                link: '#'
            }
        ]
    },

    // {
    //     id: 2,
    //     type:
    //         'commemorative',

    //     badge:
    //         'DIA DAS MÃES',

    //     title:
    //         'Homenagem a quem transforma sonhos em realidade',

    //     description:
    //         'Nosso carinho e reconhecimento a todas as mães empreendedoras.',

    //     image:
    //         'https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?w=1800',

    //     overlay: 'light',
    //     align: 'center',

    //     buttons: []
    // },


])

const activeBanner =
    computed(() =>
        banners.value[
        currentIndex.value
        ]
    )

const changeSlide =
    (index) => {
        currentIndex.value =
            index
    }

const nextSlide = () => {
    currentIndex.value =
        (
            currentIndex.value + 1
        ) %
        banners.value.length
}

onMounted(() => {
    interval =
        setInterval(
            nextSlide,
            6000
        )
})

onUnmounted(() => {
    clearInterval(interval)
})
</script>

<style scoped>
.hero-banner {
    position: relative;
    overflow: hidden;
}

/* SLIDE */
.hero-slide {
    position: relative;
    min-height: 680px;
}

/* IMAGE */
.hero-image {
    position: absolute;
    inset: 0;

    width: 100%;
    height: 100%;

    object-fit: cover;
    object-position: center top;
}

/* OVERLAY */
.overlay {
    position: absolute;
    inset: 0;

    background:
        linear-gradient(90deg,
            rgba(3, 23, 52, .88) 15%,

            rgba(3, 23, 52, .58) 50%,

            rgba(3, 23, 52, .18) 100%);
}

.overlay.light {
    background:
        linear-gradient(rgba(0, 0, 0, .38),
            rgba(0, 0, 0, .38));
}

/* CONTENT */
.hero-content {
    position: relative;
    z-index: 2;

    min-height: 680px;

    display: flex;
    align-items: center;
}

.content-wrapper {
    max-width: 720px;
    color: var(--color-white);

    height: 100%;

    display: flex;
    flex-direction: column;
    justify-content: center;
}

.content-wrapper.center {
    text-align: center;
    margin: auto;
}

.badge {
    display: inline-flex;
    padding: 12px 20px;
    border-radius: 999px;

    background:
        rgba(255, 255, 255, .12);

    backdrop-filter:
        blur(10px);

    color: var(--color-secondary);
    font-weight: 700;
    margin-bottom: 22px;
}

h1 {
    font-size:
        clamp(2.8rem,
            5vw,
            5rem);

    line-height: 1.05;
    margin-bottom: 24px;
    color: var(--color-white);
}

p {
    font-size: 1.15rem;
    line-height: 1.8;
    color:
        rgba(255,
            255,
            255,
            .92);

    max-width: 620px;
}

.center p {
    margin-inline: auto;
}

/* BUTTONS */
.buttons {
    display: flex;
    gap: 14px;
    margin-top: 32px;
    flex-wrap: wrap;
}

.hero-btn {
    padding: 18px 30px;
    border-radius: 16px;
    text-decoration: none;
    font-weight: 700;
    transition: var(--transition);
}

.primary {
    background: var(--color-secondary);
    color: var(--color-primary);
}

.primary:hover {
    transform:
        translateY(-3px);
}

.secondary {
    background:
        rgba(255,
            255,
            255,
            .12);

    color: white;

    border:
        1px solid rgba(255,
            255,
            255,
            .2);
}

/* DOTS */
.dots {
    position: absolute;
    bottom: 28px;
    left: 50%;

    transform:
        translateX(-50%);

    display: flex;
    gap: 10px;

    z-index: 10;
}

.dot {
    width: 12px;
    height: 12px;

    border-radius: 999px;
    border: none;

    cursor: pointer;

    background:
        rgba(255,
            255,
            255,
            .35);

    transition: .3s;
}

.dot.active {
    width: 38px;
    background: white;
}

/* RESPONSIVO */
@media(max-width:992px) {

    .hero-slide,
    .hero-content {
        min-height: 600px;
    }

    .content-wrapper {
        text-align: center;
        margin: auto;
    }

    p {
        margin-inline: auto;
    }

    .buttons {
        justify-content: center;
    }
}

@media(max-width:768px) {

    .hero-slide,
    .hero-content {
        min-height: 520px;
    }

    h1 {
        font-size: 2.3rem;
    }

    p {
        font-size: 1rem;
    }

    .buttons {
        flex-direction: column;
    }

    .hero-btn {
        width: 100%;
        text-align: center;
    }
}

/* TRANSITION */
.fade-enter-active,
.fade-leave-active {
    transition:
        opacity .45s ease,
        transform .45s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
    transform:
        scale(1.02);
}
</style>