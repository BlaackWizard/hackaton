from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

actions_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='/frequent_requests')],
    [KeyboardButton(text='/graphic_requests')],
    [KeyboardButton(text='/history')],
    [KeyboardButton(text='/new_chat')],
    [KeyboardButton(text='/type_problems')],
])
