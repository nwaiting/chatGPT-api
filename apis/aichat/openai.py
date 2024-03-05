import openai
from openai import OpenAI
import logging
from .baseai import BaseAI

logger = logging.getLogger(__file__)


class OpenAIChat(BaseAI):
    def __init__(self, _api_key=None, _secret_key=None):
        super(OpenAIChat, self).__init__(_api_key, _secret_key)
        self.client = OpenAI(api_key=_api_key)
        self._chat_chat_session = [{"role": "system", "content": "你是一个能干的助手."}]

    def chat(self, text, model="gpt-3.5-turbo"):
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



