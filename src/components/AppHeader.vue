<template>
    <header class="header">
        <!-- Top Bar -->
        <div class="top-bar">
            <div class="container top-content">
                <div class="contact-info">
                    <Phone class="phone-icon-highlight" />
                    <span class="contact-label">Atendimento:</span>
                    <span class="phone-number">(63) 3220-9800</span>
                </div>


                <div class="top-links">
                    <div class="accessibility-wrapper" ref="accessWrapperRef">
                        <button class="top-btn" @click="toggleAccessPanel" :aria-expanded="isAccessMenuOpen"
                            aria-haspopup="true" aria-label="Menu de acessibilidade">
                            Acessibilidade
                        </button>

                        <!-- Painel de Acessibilidade -->
                        <div v-if="isAccessMenuOpen" class="access-panel" role="menu"
                            aria-label="Opções de acessibilidade">
                            <div class="panel-section">
                                <span id="font-size-label">Fonte</span>
                                <div class="btn-group" role="group" aria-labelledby="font-size-label">
                                    <button @click="settings.decreaseFontSize" aria-label="Diminuir fonte">A-</button>
                                    <button @click="settings.increaseFontSize" aria-label="Aumentar fonte">A+</button>
                                </div>
                            </div>
                            <div class="panel-section">
                                <span id="theme-label">Tema</span>
                                <div class="btn-group theme-btns" role="group" aria-labelledby="theme-label">
                                    <button :class="{ active: settings.theme === 'default' }"
                                        @click="settings.setTheme('default')" title="Tema Padrão"
                                        :aria-pressed="settings.theme === 'default'">Azul</button>
                                    <button :class="{ active: settings.theme === 'alternative' }"
                                        @click="settings.setTheme('alternative')" title="Tema Verde"
                                        :aria-pressed="settings.theme === 'alternative'">Verde</button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <button class="top-btn" @click="settings.toggleHighContrast" :aria-pressed="settings.isHighContrast"
                        :aria-label="settings.isHighContrast ? 'Desativar alto contraste' : 'Ativar alto contraste'">
                        {{ settings.isHighContrast ? 'Contraste Normal' : 'Alto Contraste' }}
                    </button>

                    <button class="top-btn" @click="isSiteMapOpen = true" aria-label="Abrir mapa do site">
                        Mapa do Site
                    </button>
                </div>
            </div>
        </div>

        <!-- Navbar -->
        <div class="navbar">
            <div class="container nav-content">

                <!-- Logo -->
                <div class="logo">
                    <a href="/">
                        <img src="../assets/image/logo.png" alt="Logo">
                    </a>

                </div>

                <!-- Menu Desktop -->
                <nav class="nav-menu" :class="{ active: isMenuOpen }" aria-label="Menu principal">
                    <ul class="menu">
                        <li><router-link to="/" @click="closeMenu">Início</router-link></li>
                        <li><a href="/#creditos" @click.prevent="navigateToHome('creditos')">Linhas de Crédito</a></li>
                        <li><a href="/#noticias" @click.prevent="navigateToHome('noticias')">Notícias</a></li>
                        <li><router-link to="/acesso-a-informacao" @click="closeMenu">Acesso a Informação</router-link></li>
                        <li><router-link to="/institucional" @click="closeMenu">Institucional</router-link></li>

                        <!-- Botão Mobile -->
                        <li class="mobile-btn">
                            <a href="https://intranet.fomento.to.gov.br/" target="_blank" rel="noopener">
                                <button class="btn-primary">
                                    Intranet
                                </button>
                            </a>

                        </li>
                    </ul>
                </nav>

                <!-- CTA Desktop -->
                <a href="https://intranet.fomento.to.gov.br/" target="_blank" rel="noopener">
                    <button class="btn-primary">
                        Intranet
                    </button>
                </a>

                <!-- Hamburguer -->
                <button class="hamburger" @click="toggleMenu" :aria-expanded="isMenuOpen"
                    aria-label="Abrir menu de navegação" aria-controls="nav-menu">
                    <span :class="{ open: isMenuOpen }"></span>
                    <span :class="{ open: isMenuOpen }"></span>
                    <span :class="{ open: isMenuOpen }"></span>
                </button>

            </div>
        </div>
    </header>

    <SiteMapModal :isOpen="isSiteMapOpen" @close="isSiteMapOpen = false" @navigate="scrollTo" />
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { Phone } from 'lucide-vue-next'
import { useSettingsStore } from '../store/useSettingsStore'
import SiteMapModal from './SiteMapModal.vue'

const router = useRouter()
const settings = useSettingsStore()
const isMenuOpen = ref(false)
const isAccessMenuOpen = ref(false)
const isSiteMapOpen = ref(false)
const accessWrapperRef = ref(null)

const toggleMenu = () => {
    isMenuOpen.value = !isMenuOpen.value
}

const toggleAccessPanel = () => {
    isAccessMenuOpen.value = !isAccessMenuOpen.value
}

const closeMenu = () => {
    isMenuOpen.value = false
}

const scrollTo = (sectionId) => {
    const element = document.getElementById(sectionId)
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' })
    }
    isMenuOpen.value = false
    isSiteMapOpen.value = false
}

const navigateToHome = (sectionId) => {
    isMenuOpen.value = false
    isSiteMapOpen.value = false
    if (window.location.pathname === '/') {
        scrollTo(sectionId)
    } else {
        router.push({ path: '/', hash: `#${sectionId}` })
    }
}

const handleKeydown = (e) => {
    if (e.key === 'Escape') {
        if (isAccessMenuOpen.value) {
            isAccessMenuOpen.value = false
        }
        if (isSiteMapOpen.value) {
            isSiteMapOpen.value = false
        }
    }
}

const handleClickOutside = (e) => {
    if (accessWrapperRef.value && !accessWrapperRef.value.contains(e.target)) {
        isAccessMenuOpen.value = false
    }
}

onMounted(() => {
    document.addEventListener('keydown', handleKeydown)
    document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
    document.removeEventListener('keydown', handleKeydown)
    document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
/* HEADER */
.header {
    width: 100%;
    position: sticky;
    top: 0;
    z-index: 999;
}

/* TOP BAR */
.top-bar {
    background: var(--color-primary);
    color: var(--color-white);
    font-size: 14px;
}

.top-content {
    min-height: 45px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.contact-info {
    display: flex;
    align-items: center;
    gap: 8px;
}

.phone-icon-highlight {
    width: 18px;
    height: 18px;
    color: var(--color-secondary);
    stroke-width: 2.5;
}

.contact-label {
    opacity: 0.85;
    font-size: 13px;
}

.phone-number {
    font-weight: 700;
    letter-spacing: 0.3px;
}

.top-links {
    display: flex;
    gap: 20px;
}

.top-btn {
    background: transparent;
    border: none;
    color: rgba(255, 255, 255, 0.85);
    cursor: pointer;
    font-size: 14px;
    transition: var(--transition);
}

.top-btn:hover {
    color: var(--color-white);
}

/* Painel de Acessibilidade */
.accessibility-wrapper {
    position: relative;
}

.access-panel {
    position: absolute;
    top: 100%;
    right: 0;
    background: var(--color-bg);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: 16px;
    box-shadow: var(--shadow-md);
    min-width: 180px;
    z-index: 1000;
    margin-top: 10px;
    color: var(--color-text);
}

.panel-section {
    margin-bottom: 12px;
}

.panel-section:last-child {
    margin-bottom: 0;
}

.panel-section span {
    display: block;
    font-size: 12px;
    font-weight: bold;
    margin-bottom: 8px;
    text-transform: uppercase;
}

.btn-group {
    display: flex;
    gap: 8px;
}

.btn-group button {
    flex: 1;
    padding: 6px;
    border: 1px solid var(--color-border);
    background: var(--color-bg-alt);
    cursor: pointer;
    border-radius: var(--radius-sm);
    font-weight: 600;
    color: var(--color-text);
}

.btn-group button:hover {
    background: var(--color-accent);
    color: var(--color-white);
}

.theme-btns button.active {
    background: var(--color-primary);
    color: var(--color-white);
}

/* NAVBAR */
.navbar {
    /* background: rgba(255, 255, 255, 0.521); */ 
    background: #faf8f3;
     
    /* background-image: url('/icons/appbar.png'); */
    /* backdrop-filter: blur(10px); */
    position: relative;
    /* height: 30vh;   */
    box-shadow: var(--shadow-sm);
}

.navbar::before {
    content: "";
    position: absolute;
    inset: 0;
    background-image: url("/carroussel/appbar.svg");
    background-repeat: no-repeat;
    background-position: center;
    background-size: cover;
    

    /* filter: contrast(1.4) saturate(1.2); */

    opacity: 0.70;      /* Ajuste entre 0.03 e 0.10 */

    pointer-events: none;
    z-index: 0;
}

.navbar > * {
    position: relative;
    z-index: 1;
}

/* Quando em alto contraste, tirar a transparência */
:global(html.high-contrast) .navbar {
    background: var(--color-bg);
}

.nav-content {
    min-height: 85px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo img {
    height: 65px;
    width: auto;
    object-fit: contain;
}

/* MENU */
.menu {
    display: flex;
    list-style: none;
    gap: 30px;
    align-items: center;
}

.menu a {
    text-decoration: none;
    color: var(--color-text);
    font-weight: 500;
    transition: var(--transition);
    font-size: 20px;
}

.menu a:hover:not(.disabled-link) {
    color: var(--color-accent);
    background-color: var(--color-secondary);
    padding: 15px;
}

.menu a.disabled-link {
    color: var(--color-text-muted);
    cursor: not-allowed;
    opacity: 0.6;
}

/* BUTTON */
.btn-primary {
    background: linear-gradient(135deg, var(--color-secondary), color-mix(in srgb, var(--color-secondary), black 15%));
    border: none;
    padding: 14px 24px;
    border-radius: var(--radius-sm);
    font-weight: 700;
    cursor: pointer;
    transition: var(--transition);
    color: var(--color-primary);
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-sm);
}

/* HAMBURGER */
.hamburger {
    display: none;
    flex-direction: column;
    gap: 6px;
    background: transparent;
    border: none;
    cursor: pointer;
}

.hamburger span {
    width: 28px;
    height: 3px;
    background: var(--color-primary);
    border-radius: var(--radius-sm);
    transition: var(--transition);
}

/* Animation */
.hamburger span.open:nth-child(1) {
    transform: rotate(45deg) translate(6px, 6px);
}

.hamburger span.open:nth-child(2) {
    opacity: 0;
}

.hamburger span.open:nth-child(3) {
    transform: rotate(-45deg) translate(7px, -7px);
}

.phone-icon {
    width: 18px;
    height: 18px;
    stroke-width: 2.3;
    color: var(--color-white);
    vertical-align: middle;
    margin-right: 5px;
}

.mobile-btn {
    display: none;
}

/* RESPONSIVO */
@media (max-width: 992px) {
    .desktop-btn {
        display: none;
    }

    .hamburger {
        display: flex;
    }

    .nav-menu {
        position: absolute;
        top: 130px;
        left: -100%;
        width: 100%;
        background: var(--color-bg);
        transition: var(--transition);
        box-shadow: var(--shadow-md);
        padding: 30px;
    }

    .nav-menu.active {
        left: 0;
    }

    .menu {
        flex-direction: column;
        align-items: center;
        gap: 25px;
    }

    .mobile-btn {
        display: block;
    }

    .top-content {
        flex-direction: column;
        padding: 12px 0;
        text-align: center;
        gap: 12px;
    }
}

@media (max-width: 768px) {
    .nav-content {
        min-height: 75px;
    }

    .top-links {
        flex-wrap: wrap;
        justify-content: center;
        gap: 10px;
    }
}
</style>