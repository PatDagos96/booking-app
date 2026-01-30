from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Sostituisci la stringa qui sotto con quella che hai copiato da Neon.tech
# Deve iniziare con postgres:// e finire con .neon.tech/neondb... (o simile)
# IMPORTANTE: Se la stringa inizia con "postgres://", cambiala in "postgresql://" (aggiungi la 'ql')
DATABASE_URL = "npx neonctl@latest init"

# Correzione automatica per un piccolo bug di compatibilità (se serve)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Creazione del motore di connessione
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()