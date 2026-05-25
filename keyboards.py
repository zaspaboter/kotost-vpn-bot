from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import CHANNEL_LINK_1, CHANNEL_LINK_2


menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔑 Получить VPN")],
        [KeyboardButton(text="👤 Профиль"), KeyboardButton(text="👥 Рефералы")],
        [KeyboardButton(text="🐱 Котики"), KeyboardButton(text="🛒 Магазин")],
        [KeyboardButton(text="🏆 Топ")],
        [KeyboardButton(text="📖 Инструкция"), KeyboardButton(text="💬 Поддержка")]
    ],
    resize_keyboard=True
)


subscribe_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📢 Канал 1", url=CHANNEL_LINK_1)],
        [InlineKeyboardButton(text="📢 Канал 2", url=CHANNEL_LINK_2)],
        [InlineKeyboardButton(text="✅ Проверить подписку", callback_data="check_sub")]
    ]
)


shop_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📦 ZIP — 1 🐱", callback_data="buy_zip")],
        [InlineKeyboardButton(text="🖼 Аватарка — 2 🐱", callback_data="buy_avatar")],
        [InlineKeyboardButton(text="🔥 ВД — 3 🐱", callback_data="buy_vd")]
    ]
)


vpn_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📋 ПОЛУЧИТЬ КОНФИГ", callback_data="get_vpn")]
    ]
)
