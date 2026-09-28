import os
from datetime import datetime
from sqlite3.dbapi2 import Timestamp
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///monitoring.db"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class LogEntry(Base):
    __tablename__ = "log_entries"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)
    level = Column(String, nullable=False)
    message = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

def parse_log_file(log_filename: str):
    """Функция читает текстовый лог и сохраняет новые записи в БД"""
    if not os.path.exists(log_filename):
        print(f"Файл логов {log_filename} пока не создан.")
        return

    db = SessionLocal()

    try:
        with open(log_filename, "r") as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()
            if not line:
                continue

            parts = line.split(" - ", 2)
            if len(parts) < 3:
                continue

            time_str, level, message = parts

            log_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

            new_entry = LogEntry(timestamp=log_time, level=level, message=message)
            db.add(new_entry)

        db.commit()
        print("Логи успешно отсканированы и сохранены в базу данных!")

    except Exception as e:
        print(f"Ошибка при парсинге логов: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    LOG_FILE = "system_activity.log"
    print("Запуск парсера логов...")
    parse_log_file(LOG_FILE)