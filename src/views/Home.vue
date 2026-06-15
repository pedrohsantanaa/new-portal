<template>
  <div>
    <HeroEditorial/>
    <div id="creditos">
      <CreditSection />
    </div>
    <div id="noticias">
      <NewsSection />
    </div>
    <PartnerSection />
  </div>
</template>

<script setup>
import HeroEditorial from '@/components/HeroEditorial.vue'
import CreditSection from '@/components/CreditSection.vue'
import NewsSection from '@/components/NewsSection.vue'
import PartnerSection from '@/components/PartnerSection.vue'
</script>
