<template>
  <Transition name="fade">
    <div v-if="isOpen" class="sitemap-overlay" @click.self="$emit('close')" @keydown.escape="$emit('close')" role="dialog" aria-modal="true" aria-label="Mapa do Site">
      <div class="sitemap-modal">
        <header class="modal-header">
          <h2>Mapa do Site</h2>
          <button class="close-btn" @click="$emit('close')" aria-label="Fechar mapa do site">✕</button>
        </header>
        
        <div class="modal-body">
          <div class="sitemap-grid">
            <div class="sitemap-column">
              <h3>Principal</h3>
              <ul>
                <li><a href="#inicio" @click.prevent="navigate('inicio')">Início</a></li>
                <li><a href="#creditos" @click.prevent="navigate('creditos')">Linhas de Crédito</a></li>
                <li><a href="/noticias" @click.prevent="navigateTo('/noticias')">Notícias</a></li>
                <li><a href="#" class="disabled-link" aria-disabled="true">Acesso a Informação</a></li>
              </ul>
            </div>
            
            <div class="sitemap-column">
              <h3>Linhas de Crédito</h3>
              <ul>
                <li><a href="#creditos" @click.prevent="navigate('creditos')">Microcrédito</a></li>
                <li><a href="#creditos" @click.prevent="navigate('creditos')">Crédito Online</a></li>
                <li><a href="#creditos" @click.prevent="navigate('creditos')">Agronegócio</a></li>
                <li><a href="#creditos" @click.prevent="navigate('creditos')">Turismo</a></li>
                <li><a href="#creditos" @click.prevent="navigate('creditos')">Mulher Empreendedora</a></li>
              </ul>
            </div>
            
            <div class="sitemap-column">
              <h3>Institucional</h3>
              <ul>
                <li><a href="#" class="disabled-link" aria-disabled="true">Quem Somos</a></li>
                <li><a href="#" class="disabled-link" aria-disabled="true">Transparência</a></li>
                <li><a href="#" class="disabled-link" aria-disabled="true">Ouvidoria</a></li>
                <li><a href="#" class="disabled-link" aria-disabled="true">Contato</a></li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

defineProps({
  isOpen: Boolean
})
const emit = defineEmits(['close', 'navigate'])

const navigate = (sectionId) => {
  emit('navigate', sectionId)
  emit('close')
}

const navigateTo = (path) => {
  router.push(path)
  emit('close')
}
</script>

<style scoped>
.sitemap-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(5px);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.sitemap-modal {
  background: var(--color-bg);
  width: 100%;
  max-width: 800px;
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

.modal-header {
  padding: 24px 32px;
  border-bottom: 1px solid var(--color-bg-alt);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--color-primary);
  color: var(--color-white);
}

.close-btn {
  background: transparent;
  border: none;
  color: inherit;
  font-size: 24px;
  cursor: pointer;
}

.modal-body {
  padding: 40px;
  max-height: 70vh;
  overflow-y: auto;
}

.sitemap-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 40px;
}

.sitemap-column h3 {
  color: var(--color-primary);
  margin-bottom: 20px;
  font-size: 1.2rem;
  border-left: 4px solid var(--color-secondary);
  padding-left: 12px;
}

.sitemap-column ul {
  list-style: none;
}

.sitemap-column li {
  margin-bottom: 12px;
}

.sitemap-column a {
  text-decoration: none;
  color: var(--color-text);
  transition: var(--transition);
}

.sitemap-column a:hover:not(.disabled-link) {
  color: var(--color-accent);
  padding-left: 8px;
}

.sitemap-column a.disabled-link {
  color: var(--color-text-muted);
  cursor: not-allowed;
  opacity: 0.6;
}

/* Transitions */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .modal-body {
    padding: 24px;
  }
  .sitemap-grid {
    grid-template-columns: 1fr;
    gap: 30px;
  }
}
</style>
