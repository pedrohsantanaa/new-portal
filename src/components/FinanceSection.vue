<template>
  <section class="finance-section">
    <div class="container finance-grid">

      <!-- CTA SIMULADOR -->
      <div class="simulator-card">

        <div class="simulator-content">

          <div class="left-content">
            <span class="badge">
              Simulação Online
            </span>

            <h2>
              Simule seu financiamento
            </h2>

            <p>
              Descubra as melhores condições
              para impulsionar seu negócio.
              É rápido, gratuito e 100% digital.
            </p>

            <ul class="benefits">
              <li>✔ Processo simples</li>
              <li>✔ Aprovação facilitada</li>
              <li>✔ Resultado imediato</li>
            </ul>

            <a
              href="https://seu-link-do-simulador.com"
              target="_blank"
              class="simulate-btn"
            >
              Simular Agora →
            </a>
          </div>

          <div class="right-highlight">
            <div class="result-card">
              <span>Parcelas a partir de</span>

              <h2>
                R$ 953,30
              </h2>

              <small>
                Taxas acessíveis para empreendedores
              </small>
            </div>
          </div>

        </div>
      </div>

      <!-- INDICADORES -->
      <div class="stats-card">

        <h2>
          Nossa instituição faz mais
        </h2>

        <div class="stats-grid">

          <div class="stat-item">
            <div class="icon">💰</div>

            <h3>R$ 120 milhões+</h3>

            <p>em crédito liberado</p>
          </div>

          <div class="stat-item">
            <div class="icon">👥</div>

            <h3>8 mil+</h3>

            <p>empreendedores atendidos</p>
          </div>

          <div class="stat-item">
            <div class="icon">📍</div>

            <h3>139</h3>

            <p>municípios alcançados</p>
          </div>

          <div class="stat-item">
            <div class="icon">🌱</div>

            <h3>52%</h3>

            <p>liderados por mulheres</p>
          </div>

        </div>
      </div>

    </div>
  </section>
</template>

<style scoped>
.finance-section {
  padding: 90px 0;
  background: #f8fafc;
}

.finance-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
}

/* SIMULADOR */
.simulator-card {
  background:
    linear-gradient(
      135deg,
      #eef4fb,
      #dcecff
    );

  border-radius: 28px;
  padding: 40px;
}

.simulator-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 30px;
}

.badge {
  display: inline-block;
  background: rgba(8,62,168,.1);
  color: #083ea8;
  padding: 10px 18px;
  border-radius: 999px;
  margin-bottom: 20px;
  font-weight: 600;
}

.left-content h2 {
  font-size: 40px;
  color: #0f2f63;
  margin-bottom: 16px;
}

.left-content p {
  color: #475569;
  line-height: 1.8;
  margin-bottom: 24px;
}

.benefits {
  list-style: none;
  margin-bottom: 30px;
}

.benefits li {
  margin-bottom: 10px;
  color: #334155;
}

.simulate-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 56px;
  padding: 0 32px;
  background: #083ea8;
  color: white;
  border-radius: 14px;
  text-decoration: none;
  font-weight: bold;
  transition: .3s;
}

.simulate-btn:hover {
  transform: translateY(-3px);
}

/* CARD LATERAL */
.result-card {
  background: white;
  border-radius: 24px;
  padding: 35px;
  min-width: 260px;
  text-align: center;
  box-shadow:
    0 20px 40px rgba(0,0,0,.08);
}

.result-card span {
  color: #64748b;
}

.result-card h2 {
  color: #16a34a;
  font-size: 42px;
  margin: 12px 0;
}

/* INDICADORES */
.stats-card {
  background: white;
  border-radius: 28px;
  padding: 35px;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.stat-item {
  text-align: center;
}

.icon {
  font-size: 30px;
  margin-bottom: 10px;
}

/* RESPONSIVO */
@media(max-width:1100px){
  .finance-grid {
    grid-template-columns: 1fr;
  }
}

@media(max-width:768px){

  .simulator-content {
    flex-direction: column;
  }

  .left-content h2 {
    font-size: 30px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }
}

/* ALTO CONTRASTE */
:global(html.high-contrast) .finance-section {
  background: var(--color-bg-alt) !important;
}
:global(html.high-contrast) .simulator-card {
  background: rgba(255, 255, 255, 0.1) !important;
}
:global(html.high-contrast) .tip-card {
  background: var(--color-bg) !important;
}
</style>