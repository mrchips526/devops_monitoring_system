import os
import shutil
from datetime import datetime
import logging
from turtle import back

logging.basicConfig(
    filename='system_activity.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def create_backup(source_dir: str, dest_dir: str) -> bool:
    if not os.path.exists(source_dir):
        logging.error(f"Ошибка бэкапа: Исходная папка не найдена: {source_dir}")
        return False

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        logging.info(f"Создана директория для бэкапов: {dest_dir}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"backup_{timestamp}"
    full_dest_path = os.path.join(dest_dir, backup_filename)

    try:
        logging.info(f"Старт копирования папки {source_dir}...")
        shutil.make_archive(full_dest_path, 'gztar', source_dir)
        logging.info(f"Успех. Бэкап создан: {full_dest_path}.tar.gz")
        return True
    except Exception as e:
        logging.error(f"Критическая ошибка при создании бэкапа: {str(e)}")

if __name__ == "__main__":
    SOURCE = "./test_source"
    DESTINATION = "./test_backups"

    if not os.path.exists(SOURCE):
        os.makedirs(SOURCE)
        with open(f"{SOURCE}/sample.txt", "w") as f:
            f.write("Hello! This is a test file for our first portfolio project.")

    print("Запуск скрипта бэкапа...")
    create_backup(SOURCE, DESTINATION)
    print("Готово! Проверьте появившийся файл system_activity.log")