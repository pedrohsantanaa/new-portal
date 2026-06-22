# AGENTS.md

## Visão geral

Monorepo: frontend Vue 3, backend FastAPI, admin Vue 3.
Portal de crédito/serviços para Tocantins, conteúdo em pt-BR.

## Comandos

- `npm run dev` — frontend (porta 5173)
- `npm run dev:backend` — backend FastAPI (porta 8000)
- `npm run dev:admin` — admin (porta 5174)
- `npm run build` — build frontend em `dist/`
- `npm run build:admin` — build admin
- `npm run preview` — visualizar build de produção
- `npm run db:migrate` — rodar migrações Alembic
- `npm run db:seed` — popular banco com dados iniciais

Nenhum linter, formatter, typecheck ou framework de testes está configurado. Sem pre-commit hooks nem workflows de CI.

## Arquitetura

### Frontend (`src/`)
- Vue 3 com `<script setup>`, vue-router, Pinia, Swiper, Lucide icons
- **App.vue**: shell com `AppHeader` + `<router-view />` + `AppFooter`
- **3 rotas**: `/` (Home), `/noticias` (listagem), `/noticias/:slug` (detalhe)
- **Home.vue** compõe: `HeroEditorial`, `CreditSection`, `NewsSection`, `PartnerSection`
- **Design tokens** em `src/assets/styles/global.css` (custom properties CSS)
- **Temas**: padrão (azul), alternativo (verde), alto contraste — via `data-theme` + `.high-contrast`
- **Proxy Vite**: `/api` e `/uploads` → `localhost:8000`

### Backend (`backend/`)
- FastAPI + SQLAlchemy + Alembic + PostgreSQL
- Rotas: `/api/auth`, `/api/news`, `/api/credit-lines`, `/api/upload`
- JWT auth com refresh tokens

### Admin (`admin/`)
- Vue 3 + TinyMCE para edição de conteúdo
- Rotas autenticadas com guards

## Fatos para agents

- `src/style.css` é boilerplate do Vite, não utilizado
- `src/icons/` é cópia não referenciada de `public/icons/`
- `NewsSection` é o único componente frontend que busca dados da API
- `CreditSection` e `PartnerSection` usam dados hardcoded
- `StoriesSection` e `QuickServices` existem mas **não são renderizados** em nenhuma view
- `HeroFeatures`, `Carousel`, `FinanceSection` existem mas **não são importados** em lugar algum
- `SiteMapModal` é usado por `AppHeader.vue` (não é componente órfão)
- `v-html` em `NewsDetailPage` pode ter risco de XSS se conteúdo não for sanitizado
- `useSettingsStore` **não persiste** no `localStorage` — tema/fonte resetam ao recarregar

## Convenções

- `<script setup>` em todos os componentes (sem Options API)
- `<style scoped>` em todos os componentes
- Breakpoints responsivos: 992px (tablet), 768px (mobile), 480px (mobile pequeno)
- Classe `.container`: max-width 1280px, centralizado, padding responsivo
- Ícones: `lucide-vue-next` (ex: `import { Phone } from 'lucide-vue-next'`)
- Swiper requer: `import 'swiper/css'` e `import 'swiper/css/pagination'`
