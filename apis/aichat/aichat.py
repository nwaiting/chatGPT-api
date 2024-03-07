import sys
from .openai import OpenAIChat
from .qianwenai import QianwenAI
from .baiduai import BaiduAI
from .zhipuai import ZhipuAIChat
from .googleai import GoogleAIChat
from apis.constant import ModelTypes
import logging

logger = logging.getLogger(__file__)


class AIChat(object):
    def __init__(self, _model_type=None, _api_key=None, _secret_key=None):
        obj_dict = {
            ModelTypes.ModelTypes_BAIDU: BaiduAI(_api_key=_api_key, _secret_key=_secret_key),
            ModelTypes.ModelTypes_QIANWEN: QianwenAI(_api_key=_api_key, _secret_key=_secret_key),
            ModelTypes.ModelTypes_OPENAI: OpenAIChat(_api_key=_api_key, _secret_key=_secret_key),
            ModelTypes.ModelTypes_ZHIPU: ZhipuAIChat(_api_key=_api_key, _secret_key=_secret_key),
            ModelTypes.ModelTypes_GOOGLE: GoogleAIChat(_api_key=_api_key, _secret_key=_secret_key)
        }
        if _model_type not in obj_dict:
            logger.error("model type:{} error, exit".format(_model_type))
            raise Exception('不支持的模型接口')
        self._client = obj_dict.get(_model_type)

    def chat(self, text, model=None):
        return self._client.chat(text, model)

    def text2image(self, text, model=None):
        return self._client.text2image(text=text, model=model)
    
    def text2audio(self, text, model=None):
        return self._client.text2audio(text=text, model=model)

    def text2video(self, text, model=None):
        return self._client.text2video(text=text, model=model)




