


from backend.src.access_service.adapters.config_loader import AIModelConfig
from backend.src.access_service.models.message import Message
from backend.src.access_service.application.common.ai_model import AiModel
from openai import OpenAI


class ChatGPTAiModel(AiModel):
    def __init__(self, config: AIModelConfig):
        self.config = config

    async def generate_text(self, message: Message) -> str:

        client = OpenAI(
            api_key=self.config.get_config['api_key'],
            base_url=self.config.get_config['base_url']
        )
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message.content}
            ]
        )

        return response.choices[0].message.content
