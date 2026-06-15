<script setup>
import AppHeader from './components/AppHeader.vue'
import AppFooter from './components/AppFooter.vue'
import CreditSection from './components/CreditSection.vue'
import NewsSection from './components/NewsSection.vue'
import PartnerSection from './components/PartnerSection.vue'
import HeroEditorial from './components/HeroEditorial.vue'
</script>
<template>
  <div>
    <AppHeader />
    <div id="inicio">
      <HeroEditorial/>
    </div>
    <div id="creditos">
      <CreditSection />
    </div>
    <div id="noticias">
      <NewsSection />
    </div>
    <PartnerSection />
    <AppFooter />
  </div>
</template>
