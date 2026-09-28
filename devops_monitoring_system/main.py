from unittest import result

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from log_parser import SessionLocal, LogEntry

app = FastAPI(title="DevOps Monitoring System API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    """Главная страница API"""
    return {"status": "working", "message": "Welcome to DevOps Monitoring API"}

@app.get("/api/logs")
def get_all_logs(db: Session = Depends(get_db)):
    """Эндпоинт, который возвращает все логи из базы данных"""
    logs = db.query(LogEntry).all()

    result = []
    for log in logs:
        result.append({
            "id": log.id,
            "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "level": log.level,
            "message": log.message
        })

    return {"total_count": len(result), "logs": result}