from apis.aichat import AIChat
from apis.constant import ModelTypes
from apis.config import API_KEY, SECRET_KEY

chat = AIChat(_model_type=ModelTypes.ModelTypes_QIANWEN, _api_key=API_KEY, _secret_key=SECRET_KEY).get_obj()

res = chat.chat('你叫什么名字')
print(res)

res = chat.text_translate('翻译成英文：春天来了，花朵都开了。')
print(res)