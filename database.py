from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Questo crea un file chiamato prenotazioni.db nella tua cartella
SQLALCHEMY_DATABASE_URL = "sqlite:///./prenotazioni.db"

# Il "motore" che permette a Python di scrivere nel file .db
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# La fabbrica di connessioni (sessioni) per il database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# La base da cui creeremo le nostre tabelle
Base = declarative_base()