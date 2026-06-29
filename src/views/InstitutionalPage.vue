<template>
  <div class="institutional-page">
    <!-- Hero -->
    <div class="inst-hero">
      <div class="container">
        <h1>Institucional</h1>
        <p>Conheça a Fomento TO e nossa história de desenvolvimento do estado.</p>
      </div>
    </div>

    <div class="container inst-content">
      <!-- Sobre a Agência -->
      <section class="about-section">
        <div class="about-grid">
          <div class="about-text">
            <h2>Sobre a Agência</h2>
            <p style="text-align: justify;">
              A Agência de Fomento do Estado do Tocantins S/A é uma instituição financeira não
              bancária, com sede em Palmas - TO, foi criada pela Lei Estadual n° 1298, 22 de fevereiro de 2002 e
              inaugurada em 21 de outubro de 2005.
              Tem por objeto social o financiamento de projetos de desenvolvimento, exclusivamente, no Estado do
              Tocantins e que promovam
              benefícios econômicos e/ou sociais às áreas de sua influência, em consonância com o Plano do Governo e
              levando em
              consideração as necessidades e potencialidades locais.
            </p>

            <a href="#historia" class="btn-about">
              Saiba mais sobre a nossa história
              <ArrowRight :size="16" />
            </a>
          </div>
          <div class="about-image">

            <div class="about-img-placeholder">
              <img src="/acesso_informacao/agencia.png" />
            </div>
          </div>
        </div>
      </section>

      <!-- Info Cards -->
      <section class="info-cards-section">
        <div class="info-cards-grid">
          <div class="info-card">
            <div class="info-card-icon">
              <Calendar :size="24" />
            </div>
            <div class="info-card-content">
              <span class="info-card-label">Fundação</span>
              <span class="info-card-value">2002</span>
            </div>
          </div>
          <div class="info-card">
            <div class="info-card-icon">
              <MapPin :size="24" />
            </div>
            <div class="info-card-content">
              <span class="info-card-label">Sede</span>
              <span class="info-card-value">Palmas-TO</span>
            </div>
          </div>
          <div class="info-card">
            <div class="info-card-icon">
              <Building :size="24" />
            </div>
            <div class="info-card-content">
              <span class="info-card-label">Natureza</span>
              <span class="info-card-value">Instituição Financeira não Bancária</span>
            </div>
          </div>
          <div class="info-card">
            <div class="info-card-icon">
              <Target :size="24" />
            </div>
            <div class="info-card-content">
              <span class="info-card-label">Finalidade</span>
              <span class="info-card-value">Promover o desenvolvimento econômico do Tocantins</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Nossos Números -->
      <section class="numbers-section">
        <h2>Nossos números</h2>
        <div class="numbers-grid">
          <div class="number-card">
            <span class="number-value">+20</span>
            <span class="number-label">anos</span>
          </div>
          <div class="number-card">
            <span class="number-value">139</span>
            <span class="number-label">Municípios</span>
          </div>
          <div class="number-card">
            <span class="number-value">R$ 1,2 bi+</span>
            <span class="number-label">em operações</span>
          </div>
          <div class="number-card">
            <span class="number-value">+15 mil</span>
            <span class="number-label">empresas atendidas</span>
          </div>
        </div>
      </section>

      <!-- Missão, Visão, Valores -->
      <section class="mission-section">
        <h2>Missão, Visão e Valores</h2>
        <div class="mission-grid">
          <div class="mission-card">
            <div class="mission-icon">
              <Compass :size="32" />
            </div>
            <h3>Missão</h3>
            <p>Promover o desenvolvimento econômico e social do Estado do Tocantins, por meio de soluções financeiras
              acessíveis e sustentáveis, fortalecendo o empreendedorismo e a geração de emprego e renda.</p>
          </div>
          <div class="mission-card">
            <div class="mission-icon">
              <Eye :size="32" />
            </div>
            <h3>Visão</h3>
            <p>Ser referência em agências de fomento no Brasil, reconhecida pela eficiência, transparência e impacto
              positivo na economia tocantinense.</p>
          </div>
          <div class="mission-card">
            <div class="mission-icon">
              <Heart :size="32" />
            </div>
            <h3>Valores</h3>
            <p>Ética, transparência, responsabilidade social, compromisso com o desenvolvimento sustentável e
              atendimento humanizado.</p>
          </div>
        </div>
      </section>

      <!-- Diretoria -->
      <section class="directors-section">
        <h2>Diretoria</h2>
        <div class="directors-grid">
          <div class="director-card">
            <div class="director-photo">
              <img src="/acesso_informacao/perfil_portilho.webp" />
            </div>
            <h3>Lyndon Johnson Portilho Prado</h3>
            <p class="director-role">Diretor-Presidente</p>
            <a href="#" class="btn-bio">Ver biografia</a>
          </div>
          <div class="director-card">
            <div class="director-photo">
              <img src="/acesso_informacao/perfil_jardel.webp" />
            </div>
            <h3>Jardel Crystiano Nunes Ribeiro</h3>
            <p class="director-role">Diretor Administrativo</p>
            <a href="#" class="btn-bio">Ver biografia</a>
          </div>
          <div class="director-card">
            <div class="director-photo">
              <img src="/acesso_informacao/perfil_elaine.webp" />
            </div>
            <h3>Elaine Maria de Matos</h3>
            <p class="director-role">Diretora Operacional</p>
            <a href="#" class="btn-bio">Ver biografia</a>
          </div>
        </div>
        <div class="directors-footer">
          <a href="#" class="link-all">Ver todos os perfis
            <ArrowRight :size="16" />
          </a>
        </div>
      </section>

      <!-- Conselho de Administração -->
      <section class="board-section">
        <h2>Conselho de Administração</h2>
        <div class="board-list">
          <div class="board-member">
            <div class="member-info">
              <User :size="20" />
              <div>
                <h4>Lyndon Johnson Portilho Prado</h4>
                <p>Presidente do Conselho de Administração</p>
              </div>
            </div>
          </div>
          <div class="board-member">
            <div class="member-info">
              <User :size="20" />
              <div>
                <h4>Clerson Dalvani Reis</h4>
                <p>Vice-Presidente</p>
              </div>
            </div>
          </div>
          <div class="board-member">
            <div class="member-info">
              <User :size="20" />
              <div>
                <h4>Anderson Luiz Justino Martins</h4>
                <p>Membro</p>
              </div>
            </div>
          </div>
          <div class="board-member">
            <div class="member-info">
              <User :size="20" />
              <div>
                <h4>Antonio Bandeira Costa</h4>
                <p>Membro</p>
              </div>
            </div>
          </div>
          <div class="board-member">
            <div class="member-info">
              <User :size="20" />
              <div>
                <h4>Antoniel Pontes Fernandes Filho</h4>
                <p>Membro</p>
              </div>
            </div>
          </div>
          <div class="board-member">
            <div class="member-info">
              <User :size="20" />
              <div>
                <h4>Luiz Carlos Carneiro</h4>
                <p>Membro</p>
              </div>
            </div>
          </div>
        </div>
      </section>


      <!-- Conselho Fiscal -->
      <section class="board-section">
        <h2>Conselho Fiscal</h2>
        <div class="board-list">
          <div class="board-member">
            <div class="member-info">
              <User :size="20" />
              <div>
                <h4>Sebastião Pereira Neuzin Neto</h4>
                <p>Presidente do Conselho Fiscal</p>
              </div>
            </div>
          </div>
          <div class="board-member">
            <div class="member-info">
              <User :size="20" />
              <div>
                <h4>José Pedro Dias Leite</h4>
                <p>Membro</p>
              </div>
            </div>
          </div>
          <div class="board-member">
            <div class="member-info">
              <User :size="20" />
              <div>
                <h4>Sergivan Sales</h4>
                <p>Membro</p>
              </div>
            </div>
          </div>

        </div>
      </section>

      <!-- Comitê de Auditoria -->
      <section class="board-section">
        <h2>Comitê de Auditoria</h2>
        <div class="board-list">
          <div class="board-member">
            <div class="member-info">
              <User :size="20" />
              <div>
                <h4>Claudinir de Goes Junior</h4>
                <p>Membro qualificado</p>
              </div>
            </div>
          </div>
          <div class="board-member">
            <div class="member-info">
              <User :size="20" />
              <div>
                <h4>André Luiz de Souza França</h4>
                <p>Membro</p>
              </div>
            </div>
          </div>
          <div class="board-member">
            <div class="member-info">
              <User :size="20" />
              <div>
                <h4>Larissa da Silva Fonseca</h4>
                <p>Membro</p>
              </div>
            </div>
          </div>

        </div>
      </section>

      <!-- Linha do Tempo -->
      <section class="timeline-section" id="historia">
        <h2>Linha do tempo</h2>
        <div class="timeline">
          <div class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="timeline-content">
              <span class="timeline-year">2002</span>
              <h3>Fundação</h3>
              <p>Criação da Agência de Fomento do Estado do Tocantins com o objetivo de promover o desenvolvimento
                econômico do estado.</p>
            </div>
          </div>
          <div class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="timeline-content">
              <span class="timeline-year">2005</span>
              <h3>Expansão</h3>
              <p>Ampliação da atuação para todos os municípios do estado, consolidando a presença da Fomento TO em todo
                o Tocantins.</p>
            </div>
          </div>
          <div class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="timeline-content">
              <span class="timeline-year">2010+</span>
              <h3>Consolidação</h3>
              <p>Marco na captação de recursos e na diversificação de linhas de crédito para atender diferentes
                segmentos da economia.</p>
            </div>
          </div>
          <div class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="timeline-content">
              <span class="timeline-year">2026</span>
              <h3>Hoje</h3>
              <p>Mais de 20 anos de história, com R$ 1,2 bilhão em operações e mais de 15 mil empresas atendidas em todo
                o estado.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Estrutura Organizacional -->
      <section class="org-section">
        <div class="org-banner">
          <div class="org-icon">
            <Network :size="40" />
          </div>
          <div class="org-text">
            <h2>Estrutura Organizacional</h2>
            <p>Conheça a organização interna da Fomento TO e como trabalhamos para atender você.</p>
          </div>
          <a href="#" class="btn-org">
            Visualizar organograma
            <ArrowRight :size="16" />
          </a>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import {
  ArrowRight, Building2, Calendar, MapPin, Building, Target,
  Compass, Eye, Heart, User, Network
} from 'lucide-vue-next'
</script>

<style scoped>
/* Hero */
.inst-hero {
  background: linear-gradient(135deg, #011a4f 0%, #083ea8 100%);
  color: white;
  padding: 60px 0 40px;
  text-align: center;
}

.inst-hero h1 {
  font-size: clamp(2rem, 5vw, 3rem);
  font-weight: 800;
  margin: 0 0 8px;
}

.inst-hero p {
  font-size: clamp(1rem, 2vw, 1.2rem);
  opacity: 0.85;
  margin: 0;
}

.inst-content {
  padding: 40px 20px;
  max-width: 1200px;
  margin: 0 auto;
}

/* Sobre a Agência */
.about-section {
  margin-bottom: 60px;
}

.about-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  align-items: center;
}

.about-text h2 {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 16px;
}

.about-text p {
  font-size: 15px;
  color: #475569;
  line-height: 1.7;
  margin: 0 0 16px;
}

.btn-about {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: #011a4f;
  color: white;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  transition: background 0.2s;
}

.btn-about:hover {
  background: #083ea8;
}

.about-img-placeholder {
  width: 100%;
  height: 300px;
  background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: #011a4f;
}

.about-img-placeholder span {
  font-size: 18px;
  font-weight: 700;
}

/* Info Cards */
.info-cards-section {
  margin-bottom: 60px;
}

.info-cards-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.info-card {
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: flex-start;
  gap: 16px;
  transition: all 0.2s;
}

.info-card:hover {
  border-color: #083ea8;
  box-shadow: 0 4px 12px rgba(8, 62, 168, 0.1);
}

.info-card-icon {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0f5ff;
  border-radius: 10px;
  color: #083ea8;
}

.info-card-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-card-label {
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-card-value {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
}

/* Nossos Números */
.numbers-section {
  margin-bottom: 60px;
  text-align: center;
}

.numbers-section h2 {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 32px;
}

.numbers-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.number-card {
  background: linear-gradient(135deg, #011a4f 0%, #083ea8 100%);
  color: white;
  border-radius: 16px;
  padding: 32px 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.number-value {
  font-size: 36px;
  font-weight: 800;
}

.number-label {
  font-size: 14px;
  opacity: 0.85;
}

/* Missão, Visão, Valores */
.mission-section {
  margin-bottom: 60px;
}

.mission-section h2 {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 32px;
  text-align: center;
}

.mission-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.mission-card {
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 16px;
  padding: 32px;
  text-align: center;
  transition: all 0.2s;
}

.mission-card:hover {
  border-color: #083ea8;
  box-shadow: 0 4px 12px rgba(8, 62, 168, 0.1);
}

.mission-icon {
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0f5ff;
  border-radius: 50%;
  color: #083ea8;
  margin: 0 auto 20px;
}

.mission-card h3 {
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 12px;
}

.mission-card p {
  font-size: 14px;
  color: #475569;
  line-height: 1.6;
  margin: 0;
}

/* Diretoria */
.directors-section {
  margin-bottom: 60px;
}

.directors-section h2 {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 32px;
}

.directors-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.director-card {
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 16px;
  padding: 32px;
  text-align: center;
  transition: all 0.2s;
}

.director-card:hover {
  border-color: #083ea8;
  box-shadow: 0 4px 12px rgba(8, 62, 168, 0.1);
}

.director-photo {
  width: 150px;
  height: 150px;
  background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  color: #011a4f;
}

.director-photo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: right center;
  border-radius: 50%;
}

.director-card h3 {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 4px;
}

.director-role {
  font-size: 14px;
  color: #64748b;
  margin: 0 0 16px;
}

.btn-bio {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border: 2px solid #083ea8;
  color: #083ea8;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-bio:hover {
  background: #083ea8;
  color: white;
}

.directors-footer {
  text-align: center;
  margin-top: 24px;
}

.link-all {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #083ea8;
  text-decoration: none;
  font-weight: 600;
}

.link-all:hover {
  text-decoration: underline;
}

/* Conselho de Administração */
.board-section {
  margin-bottom: 60px;
}

.board-section h2 {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 24px;
}

.board-list {
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  overflow: hidden;
}

.board-member {
  padding: 16px 24px;
  border-bottom: 1px solid #f1f5f9;
}

.board-member:last-child {
  border-bottom: none;
}

.board-member:hover {
  background: #f8fafc;
}

.member-info {
  display: flex;
  align-items: center;
  gap: 16px;
  color: #64748b;
}

.member-info h4 {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 2px;
}

.member-info p {
  font-size: 13px;
  color: #64748b;
  margin: 0;
}

/* Linha do Tempo */
.timeline-section {
  margin-bottom: 60px;
}

.timeline-section h2 {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 32px;
  text-align: center;
}

.timeline {
  position: relative;
  padding-left: 40px;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 15px;
  top: 0;
  bottom: 0;
  width: 3px;
  background: #e2e8f0;
}

.timeline-item {
  position: relative;
  padding-bottom: 40px;
}

.timeline-item:last-child {
  padding-bottom: 0;
}

.timeline-dot {
  position: absolute;
  left: -33px;
  top: 4px;
  width: 16px;
  height: 16px;
  background: #083ea8;
  border-radius: 50%;
  border: 3px solid white;
  box-shadow: 0 0 0 3px #083ea8;
}

.timeline-content {
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  padding: 20px 24px;
}

.timeline-year {
  display: inline-block;
  padding: 4px 12px;
  background: #083ea8;
  color: white;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 700;
  margin-bottom: 8px;
}

.timeline-content h3 {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 8px;
}

.timeline-content p {
  font-size: 14px;
  color: #475569;
  line-height: 1.6;
  margin: 0;
}

/* Estrutura Organizacional */
.org-section {
  margin-bottom: 40px;
}

.org-banner {
  background: linear-gradient(135deg, #011a4f 0%, #083ea8 100%);
  border-radius: 16px;
  padding: 40px;
  display: flex;
  align-items: center;
  gap: 32px;
  color: white;
}

.org-icon {
  flex-shrink: 0;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 50%;
}

.org-text {
  flex: 1;
}

.org-text h2 {
  font-size: 22px;
  font-weight: 700;
  margin: 0 0 8px;
}

.org-text p {
  font-size: 14px;
  opacity: 0.85;
  margin: 0;
}

.btn-org {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: white;
  color: #011a4f;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
  flex-shrink: 0;
}

.btn-org:hover {
  background: #f0f5ff;
}

/* Responsive */
@media (max-width: 992px) {
  .about-grid {
    grid-template-columns: 1fr;
  }

  .about-image {
    order: -1;
  }

  .info-cards-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .numbers-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .mission-grid {
    grid-template-columns: 1fr;
  }

  .directors-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .info-cards-grid {
    grid-template-columns: 1fr;
  }

  .numbers-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .directors-grid {
    grid-template-columns: 1fr;
  }

  .org-banner {
    flex-direction: column;
    text-align: center;
  }
}

@media (max-width: 480px) {
  .numbers-grid {
    grid-template-columns: 1fr;
  }
}
</style>
