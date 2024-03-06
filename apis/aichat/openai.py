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
        """
        聊天助手
        :param text:
        :param model:
        :return:
        """
        self._chat_chat_session.append({"role": "user", "content": text})
        response = self.client.chat.completions.create(
            model=model,
            messages=self._chat_chat_session
        )
        res = response["choices"][0]["message"]
        self._chat_chat_session.append({"role": "assistant", "content": res})
        return res

    def text2image(self, text, model=None, size="1024x1024"):
        """
        文字生成图片
        :param text:
        :param model:
        :param size:
        :return:
        """
        model = model or 'dall-e-3'
        response = self.client.images.generate(
            model=model,
            prompt=text,
            size=size,
            quality="standard",
            n=1,
        )
        return response.data[0].url

    def editImage(self, text, source_img, mask_img, model=None):
        """
        编辑图片
        :param text:
        :param source_img:
        :param mask_img:
        :param model:
        :return:
        """
        model = model or "dall-e-2"
        response = self.client.images.edit(
            model=model,
            image=open(source_img, "rb"),
            mask=open(mask_img, "rb"),
            prompt=text,
            n=1,
            size="1024x1024"
        )
        return response.data[0].url

    def changeImage(self, source_img, size="1024x1024"):
        """
        修改图片
        :param source_img:
        :param size:
        :return:
        """
        response = self.client.images.create_variation(
            image=open(source_img, "rb"),
            n=2,
            size=size
        )

        return response.data[0].url

    def getEmbeddings(self, text, model=None):
        """
        获取文本的embedding
        :param text:
        :param model:
        :return:
        """
        model = "text-embedding-3-small" or model
        response = self.client.embeddings.create(
            input=text,
            model=model
        )
        return response.data[0].embedding

    def text2voice(self, text, model=None, speech_file_path=None):
        """
        文本生成语音
        :param text:
        :param model:
        :param speech_file_path:
        :return:
        """
        model = model or "tts-1"
        response = self.client.audio.speech.create(
            model=model,
            voice="alloy",
            input=text
        )

        return response.stream_to_file(speech_file_path)

    def voice2text(self, audio_file, model="whisper-1"):
        """
        语音生成文本
        :param audio_file:
        :param model:
        :return:
        """
        model = model or "whisper-1"
        with open(audio_file, "rb") as audio_file:
            transcription = self.client.audio.transcriptions.create(
                model=model,
                file=audio_file,
                response_format="text"
            )
            return transcription.text

