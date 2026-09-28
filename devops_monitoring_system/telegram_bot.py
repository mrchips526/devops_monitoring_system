import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, html
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

TOKEN = "8993908083:AAFI4C2sPp_I8GqnDvMA1ImUSzrMifgW-BU"

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_stats_from_db():
    try:
        conn = sqlite3.connect("monitoring.db")
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM log_entries")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM log_entries WHERE level = 'ERROR'")
        errors = cursor.fetchone()[0]

        cursor.execute("SELECT timestamp, level, message FROM log_entries ORDER BY id DESC LIMIT 3")
        last_logs = cursor.fetchall()

        conn.close()
        return total, errors, last_logs
    except Exception as e:
        return 0, 0, [("Ошибка", "БД", str(e))]

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Привет, {html.bold(message.from_user.full_name)}!\n\n"
        "Я - робот-сисадмин. Я слежу за базой данных системы мониторинга.\n"
        "Используйте команду /status, чтобы проверить состояние бэкапов!"
    )

@dp.message(Command("status"))
async def command_ststus_handler(message: Message) -> None:
    total, errors, last_logs = get_stats_from_db()

    response_text = f"{html.bold('ОТЧЕТ СИСТЕМЫ МОНИТОРИНГА')}\n\n"
    response_text += f"Всего событий в базе: {html.code(total)}\n"

    if errors > 0:
        response_text += f"Найдено критических ошибок: {html.bold(errors)}\n\n"
    else:
        response_text += f"Критических ошибок не обнаружено.\n\n"

    response_text += f"{html.underline('Последние 3 события в системе:')}\n"

    for timestamp, level, msg in last_logs:
        icon = "i" if level == "INFO" else "X"
        response_text += f"{icon} {timestamp} [{level}]: {msg}\n"

    await message.answer(response_text, parse_mode="HTML")

async def main() -> None:
    print("Робот-мониторинг успешно запущен и слушает команды...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())