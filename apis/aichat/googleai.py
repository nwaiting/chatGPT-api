import openai
from vertexai.language_models import ChatModel
import logging
from .baseai import BaseAI

logger = logging.getLogger(__file__)


class GoogleAIChat(BaseAI):
    def __init__(self, _api_key=None, _secret_key=None):
        super(GoogleAIChat, self).__init__(_api_key, _secret_key)
        self.client = None
        self._chat_chat_session = [{"role": "system", "content": "你是一个能干的助手."}]

    def chat(self, text, model=""):
        model = model or 'chat-bison@002'
        self.client = ChatModel.from_pretrained(model)

        chat = self.client.start_chat(
            context="My name is Ned. You are my personal assistant. My favorite movies are Lord of the Rings and Hobbit.",
            examples=[
                InputOutputTextPair(
                    input_text="Who do you work for?",
                    output_text="I work for Ned.",
                ),
                InputOutputTextPair(
                    input_text="What do I like?",
                    output_text="Ned likes watching movies.",
                ),
            ],
            temperature=0.3,
        )

        chat.send_message("Do you know any cool events this weekend?")

        self._chat_chat_session.append({"role": "user", "content": text})
        response = openai.ChatCompletion.create(
            model=model,
            messages=self._chat_chat_session
        )
        res = response["choices"][0]["message"]
        self._chat_chat_session.append({"role": "assistant", "content": res})
        return res

    def text2image(self, text, model=None):
        response = openai.Image.create(
            prompt=text,
            n=1,
            size="1024x1024"
        )
        return response['data'][0]['url']

    def editImage(self, text, source_img, mask_img):
        response = openai.Image.create_edit(
            image=open(source_img, "rb"),
            mask=open(mask_img, "rb"),
            prompt=text,
            n=1,
            size="1024x1024"
        )
        return response['data'][0]['url']

    def changeImage(self, source_img):
        response = openai.Image.create_variation(
            image=open(source_img, "rb"),
            n=1,
            size="1024x1024"
        )
        return response['data'][0]['url']



