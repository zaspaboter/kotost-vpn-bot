import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from config import *
from database import *
from keyboards import *

bot = Bot(TOKEN)
dp = Dispatcher()


# =========================
# 🔥 ПРОВЕРКА ПОДПИСКИ (ИСПРАВЛЕНА)
# =========================
async def check_sub(user_id: int):

    try:
        member1 = await bot.get_chat_member(CHANNEL_1, user_id)
        member2 = await bot.get_chat_member(CHANNEL_2, user_id)

        allowed = ["member", "administrator", "creator"]

        if member1.status in allowed and member2.status in allowed:
            return True

        return False

    except Exception as e:
        print("SUB CHECK ERROR:", e)
        return False


# =========================
# 🐾 START
# =========================
@dp.message(CommandStart())
async def start(message: Message):

    ref_by = None
    args = message.text.split()

    if len(args) > 1:
        try:
            ref_by = int(args[1])
        except:
            pass

    add_user(message.from_user.id, message.from_user.username, ref_by)

    text = """
🐾 ДОБРО ПОЖАЛОВАТЬ В КОТОСТЬ VPN

😼 Самый уютный VPN бот в Telegram

━━━━━━━━━━━━━━━━━━

🌍 Быстрые сервера по миру
🔐 Полная защита соединения
⚡ Стабильная скорость без лагов
🐱 Котики за приглашения друзей
🛒 Магазин наград от Zaspa

━━━━━━━━━━━━━━━━━━

🔥 Начните пользоваться прямо сейчас через кнопки ниже
"""

    await message.answer(text, reply_markup=menu)


# =========================
# 🔑 VPN
# =========================
@dp.message(F.text == "🔑 Получить VPN")
async def vpn(message: Message):

    if not await check_sub(message.from_user.id):
        await message.answer(
            "❌ ДЛЯ ДОСТУПА К VPN НУЖНО ПОДПИСАТЬСЯ НА ДВА КАНАЛА",
            reply_markup=subscribe_kb
        )
        return

    await message.answer(
        """
🐾 ВАШ VPN ГОТОВ К ИСПОЛЬЗОВАНИЮ

━━━━━━━━━━━━━━━━━━

⚠️ ВАЖНО:
Нажмите кнопку ниже чтобы получить конфиг

━━━━━━━━━━━━━━━━━━

😼 После получения вы сможете подключиться через приложение Happ
""",
        reply_markup=vpn_kb
    )


# =========================
# 📋 ВЫДАЧА VPN (ИСПРАВЛЕНИЕ КОПИРОВАНИЯ)
# =========================
@dp.callback_query(F.data == "get_vpn")
async def get_vpn(callback: CallbackQuery):

    await callback.message.answer(
        f"""
📋 ВАШ VPN КОНФИГ:

━━━━━━━━━━━━━━━━━━

<code>{VPN_CONFIG}</code>

━━━━━━━━━━━━━━━━━━

📌 КАК КОПИРОВАТЬ:
- нажмите и удержите текст
- выберите "копировать"

━━━━━━━━━━━━━━━━━━

📱 ПОДКЛЮЧЕНИЕ ЧЕРЕЗ HAPP:

1. Установите Happ
2. Откройте приложение
3. Нажмите "Добавить VPN"
4. Вставьте скопированный конфиг
5. Нажмите подключить

━━━━━━━━━━━━━━━━━━

🔥 ГОТОВО — ВАШ VPN АКТИВЕН
""",
        parse_mode="HTML"
    )

    await callback.answer()


# =========================
# 📢 ПРОВЕРКА ПОДПИСКИ
# =========================
@dp.callback_query(F.data == "check_sub")
async def check(callback: CallbackQuery):

    if await check_sub(callback.from_user.id):
        await callback.message.answer("✅ ПОДПИСКА ПОДТВЕРЖДЕНА")
    else:
        await callback.message.answer("❌ ВЫ НЕ ПОДПИСАНЫ НА ВСЕ КАНАЛЫ")

    await callback.answer()


# =========================
# 👤 ПРОФИЛЬ
# =========================
@dp.message(F.text == "👤 Профиль")
async def profile(message: Message):

    user = get_user(message.from_user.id)

    await message.answer(f"""
🐾 ВАШ ПРОФИЛЬ

━━━━━━━━━━━━━━━━━━

👤 Ник: @{user[1]}
🆔 ID: {message.from_user.id}

🐱 Котики: {user[2]}
👥 Рефералы: {user[3]}

━━━━━━━━━━━━━━━━━━

🎁 За каждого друга вы получаете 1 котика
""")


# =========================
# 👥 РЕФЕРАЛЫ
# =========================
@dp.message(F.text == "👥 Рефералы")
async def refs(message: Message):

    link = f"https://t.me/{(await bot.get_me()).username}?start={message.from_user.id}"

    await message.answer(f"""
👥 РЕФЕРАЛЬНАЯ СИСТЕМА

━━━━━━━━━━━━━━━━━━

🐱 1 ДРУГ = 1 КОТИК

🎁 Приглашайте друзей и получайте награды

━━━━━━━━━━━━━━━━━━

🔗 ВАША ССЫЛКА:

{link}

━━━━━━━━━━━━━━━━━━

🔥 ЧЕМ БОЛЬШЕ ДРУЗЕЙ — ТЕМ БОЛЬШЕ КОТИКОВ
""")


# =========================
# 🐱 КОТИКИ
# =========================
@dp.message(F.text == "🐱 Котики")
async def cats(message: Message):

    user = get_user(message.from_user.id)

    await message.answer(f"""
🐱 ВАШ БАЛАНС КОТИКОВ

━━━━━━━━━━━━━━━━━━

💰 Котиков: {user[2]}

━━━━━━━━━━━━━━━━━━

🛒 Используйте котиков в магазине
""")


# =========================
# 🛒 МАГАЗИН
# =========================
@dp.message(F.text == "🛒 Магазин")
async def shop(message: Message):

    await message.answer("""
🛒 МАГАЗИН НАГРАД

━━━━━━━━━━━━━━━━━━

📦 ZIP — 1 🐱
🖼 Аватарка — 2 🐱
🔥 ВД — 3 🐱

━━━━━━━━━━━━━━━━━━

😼 Покупки обрабатываются автоматически админом
""", reply_markup=shop_kb)


# =========================
# 🛒 ПОКУПКИ
# =========================
@dp.callback_query(F.data.startswith("buy_"))
async def buy(callback: CallbackQuery):

    user = get_user(callback.from_user.id)

    items = {
        "buy_zip": ("ZIP от Zaspa", 1),
        "buy_avatar": ("Аватарка от Zaspa", 2),
        "buy_vd": ("ВД от Zaspa", 3)
    }

    item, price = items[callback.data]

    if user[2] < price:
        await callback.message.answer("❌ НЕДОСТАТОЧНО КОТИКОВ")
        return

    buy_item(callback.from_user.id, item, price)

    await bot.send_message(
        ADMIN_ID,
        f"""
🛒 НОВАЯ ПОКУПКА

👤 @{callback.from_user.username}
🆔 {callback.from_user.id}

🎁 {item}
🐱 {price} котиков
"""
    )

    await callback.message.answer(f"✅ ВЫ КУПИЛИ: {item}")

    await callback.answer()


# =========================
# 🏆 ТОП
# =========================
@dp.message(F.text == "🏆 Топ")
async def top(message: Message):

    users = top_users()

    text = "🏆 ТОП ПОЛЬЗОВАТЕЛЕЙ\n\n"

    i = 1
    for u in users:
        text += f"{i}. @{u[0]} — {u[1]} друзей\n"
        i += 1

    await message.answer(text)


# =========================
# 📖 ИНСТРУКЦИЯ
# =========================
@dp.message(F.text == "📖 Инструкция")
async def instruction(message: Message):

    await message.answer("""
📖 ПОЛНАЯ ИНСТРУКЦИЯ КОТОСТЬ VPN

━━━━━━━━━━━━━━━━━━

🔑 КАК ПОЛУЧИТЬ VPN:
- подпишитесь на каналы
- нажмите кнопку
- получите конфиг
- вставьте в Happ

━━━━━━━━━━━━━━━━━━

👥 КАК ПОЛУЧАТЬ КОТИКИ:
- отправляйте реферальную ссылку друзьям
- за каждого друга +1 котик

━━━━━━━━━━━━━━━━━━

🛒 КАК ПОКУПАТЬ:
- заходите в магазин
- выбираете товар
- нажимаете купить
- админ получает уведомление

━━━━━━━━━━━━━━━━━━

😼 УДАЧНОГО ИСПОЛЬЗОВАНИЯ
""")


# =========================
# 💬 ПОДДЕРЖКА
# =========================
@dp.message(F.text == "💬 Поддержка")
async def support(message: Message):

    await message.answer(f"💬 ПОДДЕРЖКА: @{SUPPORT_USERNAME}")


# =========================
# START BOT
# =========================
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
