# AGENTS.md

## Visão geral do projeto

Portal single-page em Vue 3 + Vite (sem router, sem SSR, sem testes). Todo o conteúdo está em português do Brasil. Portal de serviços financeiros / crédito para Tocantins.

## Comandos

- `npm run dev` — servidor de desenvolvimento Vite (porta padrão 5173)
- `npm run build` — build de produção em `dist/`
- `npm run preview` — visualiza o build de produção

Nenhum linter, formatter, typecheck ou framework de testes está configurado. Não há pre-commit hooks nem workflows de CI.

## Stack técnica

- Vue 3 com `<script setup>` (Composition API)
- Pinia para estado (store única: `src/store/useSettingsStore.js`)
- Swiper (`swiper/vue`) para carousels — requer importação de CSS: `import 'swiper/css'` e `import 'swiper/css/pagination'`
- Lucide Vue Next para ícones (ex: `import { Phone } from 'lucide-vue-next'`)
- Vite 8 com `@vitejs/plugin-vue`

## Fatos arquitetônicos importantes

- **Sem router.** `App.vue` monta todas as seções diretamente como componentes.
- **Ponto de entrada:** `src/main.js` → cria o app, instala Pinia, monta em `#app`.
- **Estilos globais:** `src/assets/styles/global.css` — define custom properties CSS (design tokens). Importado em `main.js`, não em `style.css`.
- **`src/style.css` é boilerplate não utilizado** do template Vite. Não é importado em lugar algum. Não edite esperando mudanças visuais.
- **Design tokens** ficam em `global.css` como custom properties CSS: `--color-primary`, `--color-secondary`, `--color-accent`, `--color-bg`, `--color-bg-alt`, `--color-text`, `--color-text-muted`, `--color-white`, `--transition`.
- **Sistema de temas:** Três modos alternados via atributo `data-theme` e classe `.high-contrast` no `<html>`: padrão (azul), alternativo (verde), alto contraste. Gerenciado por `useSettingsStore`.
- **Assets estáticos** servidos de `public/` (imagens de carousel em `public/carroussel/`, ícones em `public/icons/`, logos de parceiros em `public/partners/`).
- **Dados do conteúdo são hardcoded** dentro dos blocos `<script setup>` dos componentes, não buscados de API.

## Layout de componentes em App.vue

Componentes ativos: `AppHeader`, `HeroEditorial`, `CreditSection`, `StoriesSection`, `NewsSection`, `QuickServices`, `PartnersSection`, `AppFooter`.

Comentados: `HeroFeatures`, `Carousel`, `FinanceSection`. São implementações alternativas de hero/seção mantidas no código. `HeroCarousel` e `HeroSection` **não existem** neste repositório — não os crie.

Componente órfão: `SiteMapModal.vue` existe em `components/` mas nunca é importado em lugar algum. Pode ser ignorado ou removido.

## Convenções de código

- Todos os componentes usam `<script setup>` (sem Options API).
- `<style scoped>` em todos os componentes.
- Breakpoints responsivos: 992px (tablet), 768px (mobile), 480px (mobile pequeno).
- Classe container: `.container` (max-width 1280px, centralizado, padding responsivo).
- Dados dos componentes (linhas de crédito, banners, stories, notícias) são definidos como arrays `ref()` no bloco script de cada componente.
- **Atenção ao alias de importação:** `PartnerSection.vue` (sem 's') é importado como `PartnersSection` (com 's') em `App.vue`. O nome do arquivo e o nome da variável de importação divergem.
