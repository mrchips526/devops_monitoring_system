from log_parser import SessionLocal, LogEntry

db = SessionLocal()

try:
    entries = db.query(LogEntry).all()

    print(f"---Всего записей в базе данных: {len(entries)} ---")

    for entry in entries:
        print(f"[{entry.id}] Время: {entry.timestamp} | Уровень: {entry.level} | Текст: {entry.message}")

except Exception as e:
    print(f"Ошибка при чтении базы: {e}")
finally:
    db.close()