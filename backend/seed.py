import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.category import Category
from app.models.permission import Permission
from app.models.info_category import InfoCategory
from app.utils.auth import hash_password

PERMISSIONS = [
    ("dashboard", "Dashboard"),
    ("news", "Notícias"),
    ("credit_lines", "Linhas de Crédito"),
    ("categories", "Categorias"),
    ("users", "Usuários"),
    ("settings", "Configurações"),
    ("reports", "Relatórios"),
    ("info_access", "Acesso à Informação"),
]

CATEGORIES = [
    ("Crédito", "credito", 1),
    ("Programa", "programa", 2),
    ("Evento", "evento", 3),
    ("Empreendedorismo", "empreendedorismo", 4),
]

INFO_CATEGORIES = [
    ("Políticas, Manuais e Resoluções", "politicas-manuais-e-resolucoes", "Aceça políticas, manuais e resoluções institucionais.", "file-text", 1),
    ("Relatórios", "relatorios", "Relatórios administrativos, de gestão e de atividades.", "bar-chart-3", 2),
    ("Financeiro e Contábil", "financeiro-e-contabil", "Despesas, execuções, balanços e demonstrações financeiras.", "calculator", 3),
    ("Organograma", "organograma", "Estrutura organizacional da Agência de Fomento.", "network", 4),
    ("Editais", "editais", "Editais de chamamento, contratações e avisos.", "megaphone", 5),
    ("Gestão de Riscos", "gestao-de-riscos", "Políticas e relatórios de gestão de riscos.", "shield-check", 6),
    ("Concursos", "concursos", "Editais, resultados e informações de concursos.", "users", 7),
    ("Legislação", "legislacao", "Leis, decretos, portarias e normas aplicáveis.", "scale", 8),
]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Criar permissões
        for codename, name in PERMISSIONS:
            existing = db.query(Permission).filter(Permission.codename == codename).first()
            if not existing:
                db.add(Permission(codename=codename, name=name))
        db.commit()

        # Criar categorias de notícias
        now = datetime.now(timezone.utc)
        for name, slug, order in CATEGORIES:
            existing = db.query(Category).filter(Category.slug == slug).first()
            if not existing:
                db.add(Category(name=name, slug=slug, order=order, active=True, created_at=now, updated_at=now))
        db.commit()

        # Criar categorias de acesso à informação
        for name, slug, description, icon, sort_order in INFO_CATEGORIES:
            existing = db.query(InfoCategory).filter(InfoCategory.slug == slug).first()
            if not existing:
                db.add(InfoCategory(name=name, slug=slug, description=description, icon=icon, sort_order=sort_order, created_at=now))
        db.commit()

        # Criar admin com todas as permissões
        admin = db.query(User).filter(User.email == "admin@fomento.to.gov.br").first()
        if admin:
            print("Admin já existe.")
            return

        all_permissions = db.query(Permission).all()
        admin = User(
            email="admin@fomento.to.gov.br",
            name="Administrador",
            hashed_password=hash_password("admin123"),
            is_active=True,
            permissions=all_permissions,
        )
        db.add(admin)
        db.commit()
        print("Admin criado com sucesso!")
        print("  Email: admin@fomento.to.gov.br")
        print("  Senha: admin123")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
