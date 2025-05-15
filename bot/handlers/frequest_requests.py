# solid_bot/handlers.py
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile

from bot.services.frequent_requests_service import FrequentRequestService
from bot.services.graphic_request_service import GraphicRequestService
from bot.services.history_service import HistoryService
from bot.services.message_send_service import MessageSendService
from bot.services.problem_type_service import ProblemTypeService

router = Router()

@router.message(F.text == 'Частые запросы')
async def frequent_request_handler(message: Message):
    service = FrequentRequestService()
    await service.handle(message)

@router.message(F.text == 'История запросов')
async def history_handler(message: Message):
    service = HistoryService()
    await service.handle(message)

@router.message(F.text == 'Перечислить типы проблемов')
async def problem_type_handler(message: Message):
    service = ProblemTypeService()
    await service.handle(message)

@router.message(F.text == 'Графический анализ')
async def graphic_requests(message: Message):
    service = GraphicRequestService()
    await service.handle(message)

@router.message(F.text)
async def send_message_handler(message: Message):
    service = MessageSendService()
    await service.handle(message)
