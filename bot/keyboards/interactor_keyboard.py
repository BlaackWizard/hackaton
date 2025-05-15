from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

actions_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Частые запросы')],
    [KeyboardButton(text='Графический анализ')],
    [KeyboardButton(text='История запросов')],
    [KeyboardButton(text='Перечислить типы проблемов')],
], resize_keyboard=True, input_field_placeholder="Выберите одну из опций")
