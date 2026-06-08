<template>
    <header class="header">
        <!-- Top Bar -->
        <div class="top-bar">
            <div class="container top-content">
                <div class="contact-info">
                    <Phone class="phone-icon-highlight" />
                    <span class="contact-label">Atendimento:</span>
                    <span class="phone-number">(63) 3218-1548</span>
                </div>


                <div class="top-links">
                    <div class="accessibility-wrapper">
                        <button class="top-btn" @click="isAccessMenuOpen = !isAccessMenuOpen">
                            Acessibilidade
                        </button>
                        
                        <!-- Painel de Acessibilidade -->
                        <div v-if="isAccessMenuOpen" class="access-panel">
                            <div class="panel-section">
                                <span>Fonte</span>
                                <div class="btn-group">
                                    <button @click="settings.decreaseFontSize">A-</button>
                                    <button @click="settings.increaseFontSize">A+</button>
                                </div>
                            </div>
                            <div class="panel-section">
                                <span>Tema</span>
                                <div class="btn-group theme-btns">
                                    <button 
                                        :class="{ active: settings.theme === 'default' }"
                                        @click="settings.setTheme('default')"
                                        title="Tema Padrão"
                                    >Azul</button>
                                    <button 
                                        :class="{ active: settings.theme === 'alternative' }"
                                        @click="settings.setTheme('alternative')"
                                        title="Tema Verde"
                                    >Verde</button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <button class="top-btn" @click="settings.toggleHighContrast">
                        {{ settings.isHighContrast ? 'Contraste Normal' : 'Alto Contraste' }}
                    </button>
                    
                    <button class="top-btn" @click="isSiteMapOpen = true">
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
                    <img src="../assets/image/logo.png" alt="Logo">
                </div>

                <!-- Menu Desktop -->
                <nav class="nav-menu" :class="{ active: isMenuOpen }">
                    <ul class="menu">
                        <li><a href="#">Início</a></li>
                        <li><a href="#">Linhas de Crédito</a></li>
                        <li><a href="#">Institucional</a></li>
                        <li><a href="#">Notícias</a></li>
                        <li><a href="#">Acesso a Informação</a></li>

                        <!-- Botão Mobile -->
                        <li class="mobile-btn">
                            <button class="btn-primary">
                                Intranet
                            </button>
                        </li>
                    </ul>
                </nav>

                <!-- CTA Desktop -->
                <button class="btn-primary desktop-btn">
                    Intranet
                </button>

                <!-- Hamburguer -->
                <button class="hamburger" @click="toggleMenu">
                    <span :class="{ open: isMenuOpen }"></span>
                    <span :class="{ open: isMenuOpen }"></span>
                    <span :class="{ open: isMenuOpen }"></span>
                </button>

            </div>
        </div>
    </header>

    <SiteMapModal :isOpen="isSiteMapOpen" @close="isSiteMapOpen = false" />
</template>

<script setup>
import { ref } from 'vue'
import { Phone } from 'lucide-vue-next'
import { useSettingsStore } from '../store/useSettingsStore'
import SiteMapModal from './SiteMapModal.vue'

const settings = useSettingsStore()
const isMenuOpen = ref(false)
const isAccessMenuOpen = ref(false)
const isSiteMapOpen = ref(false)

const toggleMenu = () => {
    isMenuOpen.value = !isMenuOpen.value
}
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
    border: 1px solid var(--color-bg-alt);
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
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
    border: 1px solid var(--color-bg-alt);
    background: var(--color-bg-alt);
    cursor: pointer;
    border-radius: 6px;
    font-weight: bold;
    color: var(--color-text);
}

.btn-group button:hover {
    background: var(--color-accent);
    color: white;
}

.theme-btns button.active {
    background: var(--color-primary);
    color: white;
}

/* NAVBAR */
.navbar {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    box-shadow: 0 2px 12px rgba(0, 0, 0, .08);
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
}

.menu a:hover {
    color: var(--color-accent);
}

/* BUTTON */
.btn-primary {
    background: linear-gradient(135deg, var(--color-secondary), #f59e0b);
    border: none;
    padding: 14px 24px;
    border-radius: 12px;
    font-weight: bold;
    cursor: pointer;
    transition: var(--transition);
    color: var(--color-primary);
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
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
    border-radius: 10px;
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
    color: white;
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
        transition: .4s ease;
        box-shadow: 0 10px 30px rgba(0, 0, 0, .1);
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