import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.category import Category
from app.models.permission import Permission
from app.models.info_category import InfoCategory
from app.models.site_setting import SiteSetting
from app.models.carousel_slide import CarouselSlide
from app.models.sale_item import SaleItem
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

SITE_SETTINGS = [
    ("home_hero", True, "Banner Principal (Hero)", "home", 1),
    ("home_creditos", True, "Seção de Créditos", "home", 2),
    ("home_noticias", True, "Seção de Notícias", "home", 3),
    ("home_parceiros", True, "Seção de Parceiros", "home", 4),
    ("page_noticias", True, "Página de Notícias", "pages", 1),
    ("page_creditos", True, "Página de Linhas de Crédito", "pages", 2),
    ("page_acesso", True, "Página de Acesso à Informação", "pages", 3),
    ("page_institucional", True, "Página Institucional", "pages", 4),
    ("nav_creditos", True, "Link \"Linhas de Crédito\" no Menu", "nav", 1),
    ("nav_noticias", True, "Link \"Notícias\" no Menu", "nav", 2),
    ("nav_acesso", True, "Link \"Acesso à Informação\" no Menu", "nav", 3),
    ("nav_institucional", True, "Link \"Institucional\" no Menu", "nav", 4),
]

CAROUSEL_SLIDES = [
    ("/carroussel/b1.png", None, None, "#", "Conheça Nossos Programas", "btn-orange", 1, True),
    ("/carroussel/b2.png", None, None, "#", "Ver Dashboard", "btn-orange", 2, True),
    ("/carroussel/b3.png", None, None, "#", "Localização", "btn-orange", 3, True),
    ("/carroussel/b8.png", None, None, "#", "Renegociação de Dívidas", "btn-orange", 4, True),
    ("/carroussel/b5.png", None, None, "#", "Compras Diretas", "btn-orange", 5, True),
    ("/carroussel/b6.png", None, None, "#", "Saiba Mais", "btn-orange", 6, True),
]

SALE_ITEMS = [
    ("imovel", "Palmas", "Imóvel residencial urbano em Palmas", None, "Palmas", None, "Urbano", "Residencial", None, None, None, 243000.00, 360, None, "(63) 99999-0001", True, True, 1),
    ("imovel", "Porto Nacional", "Imóvel residencial urbano em Porto Nacional", None, "Porto Nacional", None, "Urbano", "Residencial", None, None, None, 225000.00, 300, None, "(63) 99999-0002", True, True, 2),
    ("imovel", "Pedro Afonso", "Imóvel residencial urbano em Pedro Afonso", None, "Pedro Afonso", None, "Urbano", "Residencial", None, None, None, 252047.67, 450, None, "(63) 99999-0003", True, True, 3),
    ("imovel", "Caseara", "Imóvel residencial urbano em Caseara", None, "Caseara", None, "Rural", "Residencial", None, None, None, 75000.00, 250, None, "(63) 99999-0004", True, True, 4),
    ("veiculo", "Toyota Hilux SRX", "Pick-up Toyota Hilux SRX 4x4", None, "Palmas", None, None, None, 2019, "Diesel", "Automática", 145000.00, None, None, "(63) 99999-0005", True, True, 5),
    ("veiculo", "Chevrolet Onix LT", "Hatch Chevrolet Onix LT", None, "Porto Nacional", None, None, None, 2018, "Flex", "Manual", 42500.00, None, None, "(63) 99999-0006", True, True, 6),
    ("veiculo", "Jeep Renegade Sport", "SUV Jeep Renegade Sport 4x4", None, "Palmas", None, None, None, 2016, "Flex", "Automática", 56000.00, None, None, "(63) 99999-0007", True, True, 7),
    ("veiculo", "Honda CG 160 Titan", "Motocicleta Honda CG 160 Titan", None, "Araguaína", None, None, None, 2020, "Flex", "Manual", 12000.00, None, None, "(63) 99999-0008", True, True, 8),
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

        # Criar configurações do site
        for key, value, label, group, order in SITE_SETTINGS:
            existing = db.query(SiteSetting).filter(SiteSetting.key == key).first()
            if not existing:
                db.add(SiteSetting(key=key, value=value, label=label, group=group, order=order))
        db.commit()

        # Criar slides do carrossel
        for image_url, title, description, link, btn_label, btn_class, order, active in CAROUSEL_SLIDES:
            existing = db.query(CarouselSlide).filter(CarouselSlide.image_url == image_url).first()
            if not existing:
                db.add(CarouselSlide(
                    image_url=image_url, title=title, description=description,
                    link=link, btn_label=btn_label, btn_class=btn_class,
                    order=order, active=active,
                ))
        db.commit()

        # Criar itens de vendas diretas
        for item_type, title, description, details, city, region, property_type, purpose, year, fuel, transmission, price, area_m2, image_url, phone, featured, active, order in SALE_ITEMS:
            existing = db.query(SaleItem).filter(SaleItem.title == title, SaleItem.item_type == item_type).first()
            if not existing:
                db.add(SaleItem(
                    item_type=item_type, title=title, description=description, details=details,
                    city=city, region=region, property_type=property_type, purpose=purpose,
                    year=year, fuel=fuel, transmission=transmission, price=price,
                    area_m2=area_m2, image_url=image_url, phone=phone,
                    featured=featured, active=active, order=order,
                ))
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
