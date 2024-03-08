import openai
from vertexai.preview.language_models import ChatModel, InputOutputTextPair
from vertexai.preview.vision_models import ImageGenerationModel, ImageCaptioningModel, ImageQnAModel, MultiModalEmbeddingModel
from vertexai.vision_models import Image, Video
from google.generativeai import GenerativeModel, configure
import logging
from .baseai import BaseAI

logger = logging.getLogger(__file__)


class GoogleAIChat(BaseAI):
    def __init__(self, _api_key=None, _secret_key=None):
        super(GoogleAIChat, self).__init__(_api_key, _secret_key)
        configure(api_key=_api_key)
        self.client = None
        self.client_vision = None
        self._chat_chat_session = [['You are my personal assistant']]

    def chat(self, text, model=None):
        """
        问答
        :param text:
        :param model:
        :return:
        """
        model = model or "chat-bison@001"
        if not self.client:
            self.client = ChatModel.from_pretrained(model)
            examples = []
            for it in self._chat_chat_session:
                if len(it) != 2:
                    continue
                examples.append(InputOutputTextPair(
                        input_text=it[0],
                        output_text=it[1],
                    ))
            self.chat = self.client.start_chat(
                context=self._chat_chat_session[0][0],
                examples=examples,
                temperature=0.3,
            )

        res = self.chat.send_message(text)
        self._chat_chat_session.append([text, res.text])
        return res.text

    def image2text(self, image_path, model=None, language='en'):
        """
        图片生成文字
        :param image_path:
        :param model:
        :return:
        """
        model = model or "imagetext@001"
        model = ImageCaptioningModel.from_pretrained(model)
        image = Image.load_from_file(image_path)
        captions = model.get_captions(
            image=image,
            number_of_results=1,
            language=language,
        )
        return 0, captions

    def text2image(self, text, model=None, image_path=None):
        """
        文字生成图片
        :param text:
        :param image_path:
        :param model:
        :return:
        """
        model = model or "imagegeneration@002"
        model = ImageGenerationModel.from_pretrained(model)
        response = model.generate_images(
            prompt=text,
            number_of_images=1,
            seed=0,
        )
        response[0].save(image_path)
        return 0, ''

    def text2answers(self, question, model=None, image_path=None):
        """
        根据图片回答问题
        :param question:
        :param model:
        :param image_path:
        :return:
        """
        model = model or "imagetext@001"
        model = ImageQnAModel.from_pretrained(model)
        image = Image.load_from_file(image_path)
        answers = model.ask_question(
            image=image,
            question=question,
            number_of_results=1,
        )
        return 0, answers

    def get_multimodal_embedding(self, text, image=None, video=None, model=None):
        """
        多模态生成embedding
        :param text:
        :param image:
        :param video:
        :param model:
        :return:
        """
        model = model or "multimodalembedding@001"
        model = MultiModalEmbeddingModel.from_pretrained(model)
        image_obj = Image.load_from_file(image)
        video_obj = Video.load_from_file(video)

        embeddings = model.get_embeddings(
            image=image_obj,
            video=video_obj,
            contextual_text=text,
        )
        # image_embedding = embeddings.image_embedding
        # video_embeddings = embeddings.video_embeddings
        # text_embedding = embeddings.text_embedding
        return 0, embeddings


