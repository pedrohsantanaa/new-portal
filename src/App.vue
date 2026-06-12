<script setup>
import AppHeader from './components/AppHeader.vue'
import AppFooter from './components/AppFooter.vue'
import CreditSection from './components/CreditSection.vue'
import FinanceSection from './components/FinanceSection.vue'
import StoriesSection from './components/StoriesSection.vue'
import NewsSection from './components/NewsSection.vue'
import QuickServices from './components/QuickServices.vue'
import PartnersSection from './components/PartnerSection.vue'
import Carousel from './components/Carousel.vue'
import HeroEditorial from './components/HeroEditorial.vue'
import HeroFeatures from './components/HeroFeatures.vue'

</script>
<template>
  <div>
    <AppHeader />
    <HeroEditorial/>
    <!-- <HeroFeatures/> -->
    <!-- <Carousel/> -->
    <CreditSection />
    <!-- <FinanceSection /> -->
    <!-- <StoriesSection /> -->
    <NewsSection />
    <QuickServices />
    <PartnersSection />
    <AppFooter />

  </div>
</template>
