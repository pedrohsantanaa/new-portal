<template>
  <div>
    <HeroEditorial v-if="isVisible('home_hero')" />
    <div id="creditos" v-if="isVisible('home_creditos')">
      <CreditSection />
    </div>
    <div id="noticias" v-if="isVisible('home_noticias')">
      <NewsSection />
    </div>
    <PartnerSection v-if="isVisible('home_parceiros')" />
  </div>
</template>

<script setup>
import HeroEditorial from '@/components/HeroEditorial.vue'
import CreditSection from '@/components/CreditSection.vue'
import NewsSection from '@/components/NewsSection.vue'
import PartnerSection from '@/components/PartnerSection.vue'
import { useSiteSettings } from '@/composables/useSiteSettings'

const { isVisible } = useSiteSettings()
</script>
