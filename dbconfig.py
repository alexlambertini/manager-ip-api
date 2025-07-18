from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.event import listens_for

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# Configuração do engine com foreign_keys ativado
engine = create_engine(
    sqlite_url,
    echo=True,
    connect_args={"check_same_thread": False}
)

# Ativação de foreign keys para SQLite (CRUCIAL)
@listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)