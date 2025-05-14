from dishka import Provider, Scope, provide_all
from backend.src.application.history import History
from backend.src.application.new_chat import NewChat
from backend.src.application.send_message import SendMessage
from backend.src.application.frequent_requests import FrequentRequests
from backend.src.application.graphic_request import GraphicRequest
from backend.src.application.problem_type import ProblemType

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
