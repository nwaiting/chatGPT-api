import openai
from vertexai.preview.language_models import ChatModel, InputOutputTextPair
from vertexai.preview.vision_models import ImageGenerationModel
from google.generativeai import GenerativeModel, configure
import logging
from .baseai import BaseAI
import PIL.Image

logger = logging.getLogger(__file__)


class GoogleAIChat(BaseAI):
    def __init__(self, _api_key=None, _secret_key=None):
        super(GoogleAIChat, self).__init__(_api_key, _secret_key)
        configure(api_key=_api_key)
        self.client = None
        self.client_vision = None
        self._chat_chat_session = [{"role": "system", "content": "你是一个能干的助手."}]

    def chat(self, text, model=""):
        model = model or 'gemini-pro'
        self.client = GenerativeModel(model_name=model)

        res = self.client.generate_content(text)
        return res.text

    def image2text(self, text, image_path, model=None):
        model = model or 'gemini-pro-vision'
        multimodal_model = GenerativeModel(model)

        image = PIL.Image.open(image_path)

        response = multimodal_model.generate_content([text, image])
        return response.text



