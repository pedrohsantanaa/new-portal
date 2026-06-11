# AGENTS.md

## Project overview

Vue 3 + Vite single-page portal (no router, no SSR, no tests). All content is in Portuguese (Brazilian). This is a financial services / credit portal for Tocantins, Brazil.

## Commands

- `npm run dev` — Vite dev server (default port 5173)
- `npm run build` — production build to `dist/`
- `npm run preview` — preview production build

No linter, formatter, typecheck, or test framework is configured. No pre-commit hooks or CI workflows exist.

## Tech stack

- Vue 3 with `<script setup>` (Composition API)
- Pinia for state (single store: `src/store/useSettingsStore.js`)
- Swiper (`swiper/vue`) for carousels — requires importing CSS: `import 'swiper/css'` and `import 'swiper/css/pagination'`
- Lucide Vue Next for icons (e.g. `import { Phone } from 'lucide-vue-next'`)
- Vite 8 with `@vitejs/plugin-vue`

## Key architecture facts

- **No router.** `App.vue` assembles all sections directly as components.
- **Entry point:** `src/main.js` → creates app, installs Pinia, mounts to `#app`.
- **Global styles:** `src/assets/styles/global.css` — defines CSS custom properties (design tokens). Imported in `main.js`, not in `style.css`.
- **`src/style.css` is unused boilerplate** from the Vite template. It is not imported anywhere. Do not edit it expecting visual changes.
- **Design tokens** live in `global.css` as CSS custom properties: `--color-primary`, `--color-secondary`, `--color-accent`, `--color-bg`, `--color-bg-alt`, `--color-text`, `--color-text-muted`, `--color-white`, `--transition`.
- **Theme system:** Three modes toggled via `data-theme` attribute and `.high-contrast` class on `<html>`: default (blue), alternative (green), high-contrast. Managed by `useSettingsStore`.
- **Static assets** served from `public/` (carousel images in `public/carroussel/`, icons in `public/icons/`, partner logos in `public/partners/`).
- **Content data is hardcoded** inside component `<script setup>` blocks, not fetched from an API.

## Component layout in App.vue

Active components: `AppHeader`, `HeroEditorial`, `CreditSection`, `StoriesSection`, `NewsSection`, `QuickServices`, `PartnersSection`, `AppFooter`.

Commented out: `HeroCarousel`, `HeroSection`, `Carousel`, `FinanceSection`. These are alternative hero/section implementations kept in the codebase.

## Coding conventions

- All components use `<script setup>` (no Options API).
- Scoped `<style scoped>` in all components.
- Responsive breakpoints: 992px (tablet), 768px (mobile), 480px (small mobile).
- Container class: `.container` (max-width 1280px, centered, responsive padding).
- Component data (credit lines, banners, stories, news) is defined as `ref()` arrays in each component's script block.
