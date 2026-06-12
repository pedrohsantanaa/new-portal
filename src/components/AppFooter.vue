<script setup>
import { Instagram, Facebook } from 'lucide-vue-next'
</script>

<template>
  <footer class="footer">

    <!-- TOP -->
    <div class="container footer-grid">

      <!-- Marca -->
      <div class="footer-brand">

        <img
          src="../assets/image/logo_branco.png"
          alt="Logo"
          class="footer-logo"
        />

        <p>
          Impulsionando sonhos e fortalecendo
          empreendedores por meio de soluções
          financeiras acessíveis.
        </p>

        <div class="socials">
          <a href="#" title="Facebook">
            <Facebook class="social-icon" />
          </a>
          <a href="#" title="Instagram">
            <Instagram class="social-icon" />
          </a>
        </div>

      </div>

      <!-- Institucional -->
      <div class="footer-column">
        <h3>Institucional</h3>

        <ul>
          <li><a href="#">Transparência</a></li>
          <li><a href="#">Notícias</a></li>
          <li><a href="#">Ouvidoria</a></li>
        </ul>
      </div>

      <!-- Serviços -->
      <div class="footer-column">
        <h3>Serviços</h3>

        <ul>
          <li><a href="#">Simulador</a></li>
          <li><a href="#">Emitir Boleto</a></li>
          <li><a href="#">Consultar Protocolo</a></li>
        </ul>
      </div>

      <!-- Contato -->
      <div class="footer-column">
        <h3>Atendimento Presencial</h3>

        <ul class="contact-list">
          <li>
            <strong>SEDE PALMAS</strong><br>
            ACSE 80 – Av. Siqueira Campos, 802 – Plano Diretor Sul
          </li>
          <li style="margin-top: 15px;">
            <strong>PRONTOS</strong><br>
            • Gurupi • Araguaína • Porto Nacional
          </li>
        </ul>
      </div>

    </div>

    <!-- BOTTOM -->
    <div class="footer-bottom">
      <div class="container bottom-content">

        <p>
          © 2026 Fomento Tocantins.
          Todos os direitos reservados.
        </p>

        <div class="bottom-links">
          <a href="#">
            Política de Privacidade
          </a>

          <a href="#">
            Termos de Uso
          </a>
        </div>

      </div>
    </div>

  </footer>
</template>

<style scoped>
/* FOOTER */
.footer {
  background: linear-gradient(180deg, #011A4F 0%, #0a2d6a 100%);
  color: var(--color-white);
  overflow: hidden;
  width: 100%;
}

/* GRID */
.footer-grid {
  padding: 60px 0 50px;
  display: grid;
  grid-template-columns: 1.5fr 1fr 1fr 1fr;
  gap: 32px;
}

/* BRAND */
.footer-brand {
  min-width: 0;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: var(--radius-md);
  padding: 28px;
}

.footer-logo {
  height: 56px;
  width: auto;
  display: block;
  margin-bottom: 20px;
}

.footer-brand p {
  color: rgba(255, 255, 255, 0.70);
  line-height: 1.7;
  margin-bottom: 24px;
  max-width: 320px;
  font-size: 15px;
}

/* REDES */
.socials {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.socials a {
  width: 46px;
  height: 46px;
  border-radius: var(--radius-full);
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.10);
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  transition: var(--transition);
}

.socials a:hover {
  background: var(--color-secondary);
  border-color: var(--color-secondary);
  transform: translateY(-3px);
}

.socials a:hover .social-icon {
  color: var(--color-primary);
}

.social-icon {
  width: 20px;
  height: 20px;
  color: var(--color-white);
  transition: var(--transition);
}

/* COLUNAS */
.footer-column {
  min-width: 0;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: var(--radius-md);
  padding: 28px;
}

.footer-column h3 {
  margin-bottom: 22px;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: var(--color-secondary);
}

.footer-column ul {
  list-style: none;
}

.footer-column li {
  margin-bottom: 14px;
}

.footer-column a {
  text-decoration: none;
  color: rgba(255, 255, 255, 0.70);
  transition: var(--transition);
  word-break: break-word;
  font-size: 14px;
}

.footer-column a:hover {
  color: var(--color-secondary);
}

.contact-list li {
  color: rgba(255, 255, 255, 0.70);
  line-height: 1.6;
  word-break: break-word;
  font-size: 14px;
}

.contact-list li strong {
  color: var(--color-white);
  font-size: 13px;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

/* BOTTOM */
.footer-bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(0, 0, 0, 0.15);
  padding: 22px 0;
}

.bottom-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
}

.bottom-content p {
  color: rgba(255, 255, 255, 0.60);
  font-size: 13px;
}

.bottom-links {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  justify-content: center;
}

.bottom-links a {
  color: rgba(255, 255, 255, 0.60);
  text-decoration: none;
  transition: var(--transition);
  text-align: center;
  font-size: 13px;
}

.bottom-links a:hover {
  color: var(--color-secondary);
}

/* TABLET */
@media(max-width:1024px){
  .footer-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 28px;
  }
}

/* MOBILE */
@media(max-width:768px){
  .footer-grid {
    grid-template-columns: 1fr;
    text-align: center;
    padding: 50px 0 40px;
    gap: 24px;
  }

  .footer-brand,
  .footer-column {
    padding: 24px;
  }

  .footer-logo {
    margin: 0 auto 20px;
  }

  .footer-brand p {
    margin-inline: auto;
  }

  .socials {
    justify-content: center;
  }

  .footer-column ul {
    padding: 0;
  }

  .contact-list {
    padding: 0;
  }

  .bottom-content {
    flex-direction: column;
    text-align: center;
    gap: 14px;
  }

  .bottom-links {
    flex-direction: column;
    align-items: center;
    gap: 10px;
  }
}
</style>