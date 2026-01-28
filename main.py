from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
import models, database, secrets
from datetime import datetime

# 1. Configurazione Iniziale del Database
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
security = HTTPBasic()

# 2. Funzione per ottenere la connessione al Database
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 3. Funzione di Sicurezza (Il "Guardiano")
def controlla_credenziali(credentials: HTTPBasicCredentials = Depends(security)):
    # QUI PUOI CAMBIARE UTENTE E PASSWORD
    username_corretto = secrets.compare_digest(credentials.username, "admin")
    password_corretta = secrets.compare_digest(credentials.password, "password123")
    
    if not (username_corretto and password_corretta):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenziali errate",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# --- LE PAGINE WEB (FRONTEND) ---

# Pagina Pubblica (Per i clienti)
@app.get("/")
def home():
    return FileResponse("index.html")

# Pagina Privata (Per il titolare) - PROTETTA DA PASSWORD
@app.get("/admin")
def pannello_admin(username: str = Depends(controlla_credenziali)):
    return FileResponse("admin.html")

# --- LE API (IL CERVELLO) ---

# Salva una prenotazione (Pubblico)
@app.post("/prenota")
def prenota(nome: str, servizio: str, data: str, ora: str, db: Session = Depends(get_db)):
    # Controllo doppioni
    esiste = db.query(models.Appointment).filter(
        models.Appointment.data == data,
        models.Appointment.ora == ora
    ).first()

    if esiste:
        raise HTTPException(status_code=400, detail="Spiacente, orario già occupato!")
    
    # Salvataggio
    nuova_prenotazione = models.Appointment(cliente=nome, servizio=servizio, data=data, ora=ora)
    db.add(nuova_prenotazione)
    db.commit()
    
    return {"status": "successo", "messaggio": f"Prenotata sessione per {nome} il {data} alle {ora}"}

# Leggi la lista appuntamenti (Usato dalla pagina Admin)
@app.get("/lista_appuntamenti")
def lista(db: Session = Depends(get_db)):
    return db.query(models.Appointment).all()

# Cancella una prenotazione (Usato dalla pagina Admin)
@app.delete("/cancella/{appointment_id}")
def cancella_prenotazione(appointment_id: int, db: Session = Depends(get_db)):
    appuntamento = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    
    if not appuntamento:
        raise HTTPException(status_code=404, detail="Appuntamento non trovato")
    
    db.delete(appuntamento)
    db.commit()
    
    return {"status": "successo", "messaggio": "Appuntamento rimosso correttamente"}