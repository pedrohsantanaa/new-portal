<template>
  <Transition name="fade">
    <div v-if="isOpen" class="bio-overlay" @click.self="$emit('close')" @keydown.escape="$emit('close')" role="dialog" aria-modal="true" :aria-label="`Biografia de ${director?.name}`">
      <div class="bio-modal">
        <header class="bio-header">
          <h2>Biografia</h2>
          <button class="bio-close-btn" @click="$emit('close')" aria-label="Fechar biografia">✕</button>
        </header>

        <div class="bio-body">
          <div class="bio-profile">
            <img :src="director.photo" :alt="`Foto de ${director.name}`" class="bio-photo" />
            <div class="bio-info">
              <h3>{{ director.name }}</h3>
              <p class="bio-role">{{ director.role }}</p>
            </div>
          </div>
          <div class="bio-text">
            <p v-for="(paragraph, index) in director.biography" :key="index">{{ paragraph }}</p>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
defineProps({
  isOpen: Boolean,
  director: {
    type: Object,
    required: true,
    default: () => ({ name: '', role: '', photo: '', biography: [] })
  }
})

defineEmits(['close'])
</script>

<style scoped>
.bio-overlay {
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

.bio-modal {
  background: var(--color-bg);
  width: 100%;
  max-width: 640px;
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

.bio-header {
  padding: 24px 32px;
  border-bottom: 1px solid var(--color-bg-alt);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--color-primary);
  color: var(--color-white);
}

.bio-close-btn {
  background: transparent;
  border: none;
  color: inherit;
  font-size: 24px;
  cursor: pointer;
}

.bio-body {
  padding: 32px;
  max-height: 70vh;
  overflow-y: auto;
}

.bio-profile {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 24px;
}

.bio-photo {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid var(--color-accent);
  flex-shrink: 0;
}

.bio-info h3 {
  margin: 0 0 4px;
  font-size: 1.3rem;
  color: var(--color-primary);
}

.bio-role {
  margin: 0;
  font-size: 14px;
  color: var(--color-text-muted);
  font-weight: 600;
}

.bio-text p {
  color: var(--color-text);
  line-height: 1.7;
  margin-bottom: 16px;
}

.bio-text p:last-child {
  margin-bottom: 0;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .bio-body {
    padding: 20px;
  }
  .bio-photo {
    width: 90px;
    height: 90px;
  }
  .bio-info h3 {
    font-size: 1.1rem;
  }
}

@media (max-width: 480px) {
  .bio-profile {
    flex-direction: column;
    text-align: center;
  }
}
</style>
