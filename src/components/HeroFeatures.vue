<template>
    <section class="hero-features">
        <div class="container">
            <div class="features-grid">
                <a v-for="feature in features" :key="feature.title" :href="feature.link" class="feature-card">
                    <div class="feature-icon" :style="{ background: feature.bg }">
                        <img :src="feature.icon" :alt="feature.title" />
                    </div>
                    <span class="feature-title">{{ feature.title }}</span>
                </a>
            </div>
        </div>
    </section>
</template>

<script setup>
const features = [
    {
        title: 'Microcrédito',
        icon: '/icons/microcredito.svg',
        bg: '#EEF4FF',
        link: '#'
    },
    {
        title: 'Pronaf',
        icon: '/icons/pronaf.svg',
        bg: '#ECFDF3',
        link: '#'
    },
    {
        title: 'Fungetur',
        icon: '/icons/fungetur.svg',
        bg: '#FFF7ED',
        link: '#'
    },
    {
        title: 'Crédito Online',
        icon: '/icons/crédito-online.svg',
        bg: '#FAF5FF',
        link: '#'
    }
]
</script>

<style scoped>
.hero-features {
    margin-top: -60px;
    position: relative;
    z-index: 10;
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 24px;
}

.feature-card {
    background: white;
    border-radius: 20px;
    padding: 32px 24px;
    text-align: center;
    text-decoration: none;
    color: var(--color-primary);
    box-shadow: 0 10px 30px rgba(1, 26, 79, 0.08);
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
    border: 1px solid rgba(1, 26, 79, 0.03);
}

.feature-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 40px rgba(1, 26, 79, 0.12);
}

.feature-icon {
    width: 64px;
    height: 64px;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 14px;
}

.feature-icon img {
    width: 100%;
    height: 100%;
    object-fit: contain;
}

.feature-title {
    font-weight: 700;
    font-size: 1.1rem;
    color: #011A4F;
}

/* TABLET */
@media (max-width: 992px) {
    .features-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

/* MOBILE */
@media (max-width: 768px) {
    .hero-features {
        margin-top: -40px;
    }

    .features-grid {
        grid-template-columns: 1fr;
        gap: 16px;
    }

    .feature-card {
        flex-direction: row;
        padding: 20px 24px;
        gap: 20px;
    }

    .feature-icon {
        width: 52px;
        height: 52px;
        flex-shrink: 0;
    }

    .feature-title {
        font-size: 1.05rem;
    }
}

/* ALTO CONTRASTE */
:global(html.high-contrast) .feature-card {
  background: var(--color-bg) !important;
}
</style>

