from logging.config import fileConfig
from alembic import context
import sys
import os
from sqlalchemy import pool

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

config = context.config
fileConfig(config.config_file_name)

# Importação segura
try:
    from sqlmodel import SQLModel
    from dbconfig import engine
    
    # Importar depois de configurar o SQLModel
    from models import Group, Site  # noqa: F401
    
    # Forçar o registro dos modelos
    for model in [Group, Site]:
        if hasattr(model, '__table__'):
            model.__table__  # Acessa a tabela para garantir registro
    
except ImportError as e:
    raise ImportError(f"Erro ao importar módulos: {e}") from e

target_metadata = SQLModel.metadata

def run_migrations_offline():
    url = str(engine.url)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()