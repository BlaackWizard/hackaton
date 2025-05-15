from dishka import Provider, Scope, provide_all
from backend.src.access_service.application.history import History
from backend.src.access_service.application.new_chat import NewChat
from backend.src.access_service.application.send_message import SendMessage
from backend.src.access_service.application.frequent_requests import FrequentRequests
from backend.src.access_service.application.graphic_request import GraphicRequest
from backend.src.access_service.application.problem_type import ProblemType

class InteractorProvider(Provider):
    scope = Scope.REQUEST

    provides = provide_all(
        History,
        NewChat,
        SendMessage,
        FrequentRequests,
        GraphicRequest,
        ProblemType
    )
