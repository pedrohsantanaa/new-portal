<template>
  <Transition name="fade">
    <div v-if="isOpen" class="sitemap-overlay" @click.self="$emit('close')">
      <div class="sitemap-modal">
        <header class="modal-header">
          <h2>Mapa do Site</h2>
          <button class="close-btn" @click="$emit('close')">✕</button>
        </header>
        
        <div class="modal-body">
          <div class="sitemap-grid">
            <div class="sitemap-column">
              <h3>Principal</h3>
              <ul>
                <li><a href="#">Início</a></li>
                <li><a href="#">Linhas de Crédito</a></li>
                <li><a href="#">Institucional</a></li>
                <li><a href="#">Notícias</a></li>
                <li><a href="#">Acesso a Informação</a></li>
              </ul>
            </div>
            
            <div class="sitemap-column">
              <h3>Linhas de Crédito</h3>
              <ul>
                <li><a href="#">Microcrédito</a></li>
                <li><a href="#">Crédito Online</a></li>
                <li><a href="#">Agronegócio</a></li>
                <li><a href="#">Turismo</a></li>
                <li><a href="#">Mulher Empreendedora</a></li>
              </ul>
            </div>
            
            <div class="sitemap-column">
              <h3>Institucional</h3>
              <ul>
                <li><a href="#">Quem Somos</a></li>
                <li><a href="#">Transparência</a></li>
                <li><a href="#">Ouvidoria</a></li>
                <li><a href="#">Contato</a></li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
defineProps({
  isOpen: Boolean
})
defineEmits(['close'])
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

.sitemap-column a:hover {
  color: var(--color-accent);
  padding-left: 8px;
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
