#!/bin/bash
set -e

echo "=== Portal de Credito - Backend ==="
echo "Aguardando banco de dados..."

until python -c "
import psycopg2
from app.config import settings
url = settings.DATABASE_URL
conn = psycopg2.connect(url)
conn.close()
print('Banco de dados conectado!')
" 2>/dev/null; do
  echo "Banco indisponivel, tentando novamente em 2s..."
  sleep 2
done

echo "Rodando migrations..."
alembic upgrade head

echo "Verificando seed..."
python -c "
import sys
from pathlib import Path
sys.path.insert(0, str(Path('.').resolve()))
from app.database import SessionLocal
from app.models.user import User
db = SessionLocal()
admin = db.query(User).filter(User.email == 'admin@fomento.to.gov.br').first()
db.close()
if not admin:
    print('Admin nao encontrado, executando seed...')
    from seed import seed
    seed()
else:
    print('Seed ja executado.')
"

echo "Iniciando servidor..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
