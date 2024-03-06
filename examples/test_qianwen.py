from apis.aichat import AIChat
from apis.constant import ModelTypes
from apis.config import API_KEY, SECRET_KEY

chat = AIChat(_model_type=ModelTypes.ModelTypes_BAIDU, _api_key=API_KEY, _secret_key=SECRET_KEY)

chat.chat('你叫什么名字')


