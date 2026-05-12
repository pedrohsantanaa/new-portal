<template>
    <header class="header">
        <!-- Top Bar -->
        <div class="top-bar">
            <div class="container top-content">
                <span>
                    <Phone class="phone-icon" />
                    Atendimento: (63) 3218-1548
                </span>


                <div class="top-links">
                    <a href="#">Acessibilidade</a>
                    <a href="#">Alto Contraste</a>
                    <a href="#">Mapa do Site</a>
                </div>
            </div>
        </div>

        <!-- Navbar -->
        <div class="navbar">
            <div class="container nav-content">

                <!-- Logo -->
                <div class="logo">
                    <img src="../assets/image/logo.png" alt="">
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
                                Solicitar Crédito
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
</template>

<script setup>
import { ref } from 'vue'

const isMenuOpen = ref(false)

const toggleMenu = () => {
    isMenuOpen.value = !isMenuOpen.value
}

import { Phone } from 'lucide-vue-next'
</script>

<style scoped>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

.logo {
    display: flex;
    align-items: center;
}

.logo img {
    height: 65px;
    width: auto;
    object-fit: contain;
}

/* Mobile */
@media (max-width: 768px) {
    .logo-image {
        height: 42px;
    }
}

.container {
    width: 90%;
    max-width: 1200px;
    margin: auto;
}

/* HEADER */
.header {
    width: 100%;
    position: sticky;
    top: 0;
    z-index: 999;
}

/* TOP BAR */
.top-bar {
    background: #0f4c81;
    color: white;
    font-size: 14px;
}

.top-content {
    min-height: 45px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.top-links {
    display: flex;
    gap: 20px;
}

.top-links a {
    color: white;
    text-decoration: none;
}

/* NAVBAR */
.navbar {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    box-shadow: 0 2px 12px rgba(0, 0, 0, .08);
}

.nav-content {
    min-height: 85px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo h2 {
    color: #0f4c81;
    font-size: 30px;
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
    color: #334155;
    font-weight: 500;
    transition: .3s;
}

.menu a:hover {
    color: #0f4c81;
}

/* BUTTON */
.btn-primary {
    background: linear-gradient(135deg, #ffc107, #f59e0b);
    border: none;
    padding: 14px 24px;
    border-radius: 12px;
    font-weight: bold;
    cursor: pointer;
    transition: .3s;
}

.btn-primary:hover {
    transform: translateY(-2px);
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
    background: #0f4c81;
    border-radius: 10px;
    transition: .3s;
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

.mobile-btn {
    display: none;
}

.phone-info {
    display: flex;
    align-items: center;
    gap: 8px;
    color: white;
    font-size: 14px;
    font-weight: 500;
}

.phone-icon {
    width: 18px;
    height: 18px;
    stroke-width: 2.3;
    color: white;
}

.phone-info a {
    color: white;
    text-decoration: none;
    transition: .3s;
}

.phone-info a:hover {
    opacity: .85;
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
        background: white;
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
        gap: 8px;
    }
}

@media (max-width: 768px) {

    .logo h2 {
        font-size: 24px;
    }

    .nav-content {
        min-height: 75px;
    }

    .top-links {
        flex-direction: column;
        gap: 8px;
    }
}
</style>