<template>
  <Transition name="fade">
    <div v-if="isOpen" class="modal-overlay" @click.self="$emit('close')" @keydown.escape="$emit('close')" role="dialog" aria-modal="true" :aria-label="`Detalhes de ${item?.title}`">
      <div class="modal-content">
        <button class="modal-close" @click="$emit('close')" aria-label="Fechar">✕</button>

        <div v-if="item" class="modal-body">
          <div class="modal-image">
            <img v-if="selectedImage" :src="selectedImage" :alt="item.title" />
            <div v-else class="modal-placeholder">
              <component :is="item.item_type === 'veiculo' ? Car : Home" :size="60" />
            </div>
          </div>

          <div v-if="parsedGallery.length" class="modal-gallery">
            <div
              v-for="(img, idx) in parsedGallery"
              :key="idx"
              class="gallery-thumb"
              :class="{ active: selectedImage === img }"
              @click="selectedImage = img"
            >
              <img :src="img" :alt="`Imagem ${idx + 1}`" />
            </div>
          </div>

          <div class="modal-details">
            <div class="modal-header-info">
              <h2>{{ item.title }}</h2>
              <p class="modal-location"><MapPin :size="16" /> {{ item.city }}</p>
            </div>

            <div class="modal-specs">
              <template v-if="item.item_type === 'imovel'">
                <div v-if="item.property_type" class="spec-item">
                  <span class="spec-label">Tipo</span>
                  <span class="spec-value">{{ item.property_type }}</span>
                </div>
                <div v-if="item.purpose" class="spec-item">
                  <span class="spec-label">Finalidade</span>
                  <span class="spec-value">{{ item.purpose }}</span>
                </div>
                <div v-if="item.area_m2" class="spec-item">
                  <span class="spec-label">Área</span>
                  <span class="spec-value">{{ item.area_m2 }} m²</span>
                </div>
              </template>
              <template v-if="item.item_type === 'veiculo'">
                <div v-if="item.year" class="spec-item">
                  <span class="spec-label">Ano</span>
                  <span class="spec-value">{{ item.year }}</span>
                </div>
                <div v-if="item.fuel" class="spec-item">
                  <span class="spec-label">Combustível</span>
                  <span class="spec-value">{{ item.fuel }}</span>
                </div>
                <div v-if="item.transmission" class="spec-item">
                  <span class="spec-label">Câmbio</span>
                  <span class="spec-value">{{ item.transmission }}</span>
                </div>
              </template>
            </div>

            <div v-if="item.description" class="modal-description">
              <p>{{ item.description }}</p>
            </div>

            <div v-if="item.details" class="modal-rich-content" v-html="item.details"></div>

            <div class="modal-price">
              <span class="price-label">Valor à vista</span>
              <span class="price-value">R$ {{ formatPrice(item.price) }}</span>
            </div>

            <div class="modal-actions">
              <a v-if="item.phone" :href="`tel:${item.phone}`" class="btn-call">
                <Phone :size="18" /> Ligar
              </a>
              <button class="btn-close-modal" @click="$emit('close')">Fechar</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Home, Car, MapPin, Phone } from 'lucide-vue-next'

const props = defineProps({
  isOpen: Boolean,
  item: Object,
})

defineEmits(['close'])

const selectedImage = ref('')

const parsedGallery = computed(() => {
  if (!props.item?.gallery) return []
  try {
    const parsed = typeof props.item.gallery === 'string'
      ? JSON.parse(props.item.gallery)
      : props.item.gallery
    return Array.isArray(parsed) ? parsed : []
  } catch {
    return []
  }
})

watch(() => props.item, (val) => {
  selectedImage.value = val?.image_url || ''
}, { immediate: true })

function formatPrice(value) {
  if (!value) return '0,00'
  return new Intl.NumberFormat('pt-BR', { minimumFractionDigits: 2 }).format(value)
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}
.modal-content {
  background: white;
  width: 100%;
  max-width: 700px;
  max-height: 90vh;
  border-radius: 16px;
  overflow: hidden;
  position: relative;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.3);
}
.modal-close {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  font-size: 18px;
  cursor: pointer;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}
.modal-close:hover {
  background: rgba(0, 0, 0, 0.7);
}
.modal-body {
  overflow-y: auto;
  max-height: 90vh;
}
.modal-image {
  width: 100%;
  height: 300px;
  background: #f1f5f9;
  overflow: hidden;
}
.modal-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.modal-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
}
.modal-gallery {
  display: flex;
  gap: 8px;
  padding: 12px 24px;
  overflow-x: auto;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}
.modal-gallery::-webkit-scrollbar {
  height: 4px;
}
.modal-gallery::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}
.gallery-thumb {
  flex: 0 0 64px;
  height: 64px;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  border: 2px solid transparent;
  opacity: 0.7;
  transition: all 0.2s;
}
.gallery-thumb:hover {
  opacity: 1;
}
.gallery-thumb.active {
  border-color: #011a4f;
  opacity: 1;
}
.gallery-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.modal-details {
  padding: 24px;
}
.modal-header-info h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 4px;
}
.modal-location {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: #64748b;
  margin: 0 0 20px;
}
.modal-specs {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 20px;
}
.spec-item {
  background: #f8fafc;
  border-radius: 8px;
  padding: 10px 16px;
}
.spec-label {
  display: block;
  font-size: 11px;
  font-weight: 600;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 2px;
}
.spec-value {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}
.modal-description {
  margin-bottom: 20px;
}
.modal-description p {
  font-size: 14px;
  color: #475569;
  line-height: 1.6;
  margin: 0;
}
.modal-rich-content {
  margin-bottom: 20px;
  font-size: 14px;
  color: #475569;
  line-height: 1.6;
}
.modal-price {
  background: #eff6ff;
  border-radius: 12px;
  padding: 16px 20px;
  margin-bottom: 24px;
}
.price-label {
  display: block;
  font-size: 12px;
  color: #64748b;
  margin-bottom: 2px;
}
.price-value {
  font-size: 1.5rem;
  font-weight: 800;
  color: #011a4f;
}
.modal-actions {
  display: flex;
  gap: 12px;
}
.btn-call {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: #16a34a;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-call:hover {
  background: #15803d;
}
.btn-close-modal {
  flex: 1;
  padding: 12px 24px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  background: white;
  color: #475569;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-close-modal:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .modal-content {
    max-height: 95vh;
    border-radius: 12px;
  }
  .modal-image {
    height: 200px;
  }
  .modal-details {
    padding: 16px;
  }
  .modal-actions {
    flex-direction: column;
  }
}
</style>
