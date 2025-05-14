from typing import Annotated

from fastapi import APIRouter
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute

from backend.src.application.dto import UserIdRequest, NewChatUserIdRequest, NewMessageSendRequest
from backend.src.application.frequent_requests import FrequentRequests
from backend.src.application.graphic_request import GraphicRequest
from backend.src.application.history import History
from backend.src.application.new_chat import NewChat
from backend.src.application.problem_type import ProblemType
from backend.src.application.send_message import SendMessage
from fastapi import Query, Depends
from fastapi.responses import JSONResponse

router = APIRouter(prefix='/energy-insight', route_class=DishkaRoute)

def get_user_id_request(user_id: int = Query(...)) -> UserIdRequest:
    return UserIdRequest(user_id=user_id)

@router.get("/frequent-requests")
async def get_frequent_requests(
    interactor: FromDishka[FrequentRequests],
    data: Annotated[UserIdRequest, Depends(get_user_id_request)],
) -> JSONResponse:
    return JSONResponse(await interactor.execute(data))

@router.get("/history")
async def get_history(
    interactor: FromDishka[History],
    data: Annotated[UserIdRequest, Depends(get_user_id_request)],
) -> list[dict]:
    return await interactor.execute(data)

@router.post('/new-chat')
async def create_new_chat(
    interactor: FromDishka[NewChat],
    data: Annotated[UserIdRequest, Depends(get_user_id_request)]
) -> None:
    return await interactor.execute(data)

@router.get('/problem-type')
async def get_problem_type(
    interactor: FromDishka[ProblemType],
    data: Annotated[UserIdRequest, Depends(get_user_id_request)],
) -> dict:
    return await interactor.execute(data)

@router.post('/send-message')
async def send_message(
    interactor: FromDishka[SendMessage],
    data: NewMessageSendRequest
) -> str:
    return await interactor.execute(data)

@router.get('/graphic-requests')
async def get_graphic_requests(
    interactor: FromDishka[GraphicRequest],
    data: Annotated[UserIdRequest, Depends(get_user_id_request)]
) -> str:
    return await interactor.execute(data)
