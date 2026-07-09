<template>
    <section class="hero-carousel-section">
        <div class="carousel-container">
            <div class="carousel-track" :style="{ transform: `translateX(-${currentSlide * slideWidth}%)` }">
                <!-- SLIDES -->
                <div v-for="(card, index) in carouselCards" :key="index" class="carousel-slide" :style="{ backgroundImage: `url(${card.image})` }">
                    <div class="slide-overlay"></div>
                    <div class="slide-content">
                        <h2>{{ card.title }}</h2>
                        <p v-if="card.description">{{ card.description }}</p>
                        <a :href="card.link" class="slide-btn" :class="card.btnClass">{{ card.btnLabel }}</a>
                    </div>
                </div>
            </div>
        </div>

        <!-- Carousel Dots -->
        <div class="dots-container" v-if="totalPages > 1">
            <button v-for="page in totalPages" :key="page" class="dot" :class="{ active: currentPage === page - 1 }" @click="goToPage(page - 1)" aria-label="Ver slide"></button>
        </div>
    </section>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import api from '@/services/api'

const carouselCards = ref([])

const currentSlide = ref(0)
const itemsPerPage = ref(3)

const totalPages = computed(() => {
    const pages = Math.ceil(carouselCards.value.length / itemsPerPage.value)
    return pages > 0 ? pages : 1
})

const currentPage = computed(() => {
    return Math.floor(currentSlide.value / itemsPerPage.value)
})

const slideWidth = computed(() => {
    return 100 / itemsPerPage.value
})

const updateItemsPerPage = () => {
    if (window.innerWidth <= 768) {
        itemsPerPage.value = 1
    } else if (window.innerWidth <= 1024) {
        itemsPerPage.value = 2
    } else {
        itemsPerPage.value = 3
    }
    currentSlide.value = 0
}

const goToPage = (pageIndex) => {
    currentSlide.value = pageIndex * itemsPerPage.value
}

let autoplayInterval = null
const startAutoplay = () => {
    autoplayInterval = setInterval(() => {
        let nextPage = currentPage.value + 1
        if (nextPage >= totalPages.value) nextPage = 0
        goToPage(nextPage)
    }, 6000)
}

async function loadSlides() {
    try {
        const { data } = await api.get('/api/carousel-slides/public')
        carouselCards.value = data.map(s => ({
            image: s.image_url,
            title: s.title,
            description: s.description,
            link: s.link || '#',
            btnLabel: s.btn_label,
            btnClass: s.btn_class,
        }))
    } catch {
        carouselCards.value = []
    }
}

onMounted(() => {
    loadSlides()
    updateItemsPerPage()
    window.addEventListener('resize', updateItemsPerPage)
    startAutoplay()
})

onUnmounted(() => {
    window.removeEventListener('resize', updateItemsPerPage)
    if (autoplayInterval) clearInterval(autoplayInterval)
})
</script>

<style scoped>
.hero-carousel-section {
    position: relative;
    width: 100%;
    overflow: hidden;
    background: var(--color-primary);
}

.carousel-container {
    width: 100%;
}

.carousel-track {
    display: flex;
    transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.carousel-slide {
    flex: 0 0 calc(100% / 3);
    min-height: 90vh;
    background-size: cover;
    background-position: top center;
    position: relative;
    display: flex;
    align-items: flex-end;
}

.slide-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(to top, rgba(0, 0, 0, 0.9) 0%, rgba(0, 0, 0, 0.3) 50%, rgba(0, 0, 0, 0.1) 100%);
}

.slide-content {
    position: relative;
    z-index: 2;
    padding: 60px 40px;
    color: var(--color-white);
}

.slide-content h2 {
    font-size: clamp(1.8rem, 3vw, 2.8rem);
    font-weight: 800;
    margin-bottom: 12px;
    line-height: 1.1;
    color: var(--color-white);
}

.slide-content p {
    font-size: 1.1rem;
    margin-bottom: 24px;
    color: rgba(255, 255, 255, 0.9);
    max-width: 400px;
}

.slide-btn {
    display: inline-flex;
    align-items: center;
    padding: 12px 24px;
    font-weight: 700;
    border-radius: var(--radius-sm);
    text-decoration: none;
    transition: var(--transition);
    font-size: 1rem;
}

.btn-orange {
    background: var(--color-secondary);
    color: var(--color-black);
}

.btn-orange:hover {
    background: color-mix(in srgb, var(--color-secondary), black 15%);
    transform: translateY(-2px);
}

.btn-light {
    background: var(--color-white);
    color: var(--color-primary);
}

.btn-light:hover {
    background: var(--color-bg-alt);
    transform: translateY(-2px);
}

/* Dots */
.dots-container {
    position: absolute;
    bottom: 20px;
    left: 0;
    width: 100%;
    display: flex;
    justify-content: center;
    gap: 10px;
    z-index: 10;
}

.dot {
    width: 12px;
    height: 12px;
    border-radius: var(--radius-full);
    background: rgba(255, 255, 255, 0.3);
    border: none;
    cursor: pointer;
    transition: var(--transition);
    padding: 0;
}

.dot.active {
    background: var(--color-white);
    transform: scale(1.2);
}

/* Responsive fixes */
@media (max-width: 1024px) {
    .carousel-slide {
        flex: 0 0 50%;
    }
}

@media (max-width: 768px) {
    .carousel-slide {
        flex: 0 0 100%;
        min-height: 480px;
    }
    .slide-content {
        padding: 40px 20px;
    }
    .slide-content h2 {
        font-size: 2rem;
    }
}
</style>



