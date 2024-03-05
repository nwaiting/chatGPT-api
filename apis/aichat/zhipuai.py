from .baseai import BaseAI
from zhipuai import ZhipuAI


class ZhipuAIChat(BaseAI):
    def __init__(self, _api_key=None, _secret_key=None):
        super(ZhipuAIChat, self).__init__(_api_key, _secret_key)
        self._chat_chat_session = [{"role": "system", "content": "你是一个能干的助手."}]
        self.client = ZhipuAI(api_key=_api_key)

    def chat(self, text, model="glm-4"):
        self._chat_chat_session.append({
                    "role": "user",
                    "content": text
                })
        response = self.client.chat.completions.create(
            model=model,
            messages=self._chat_chat_session,
        )
        code, text = response.status_code, response.text
        self._chat_chat_session.append({
                    "role": "assistant",
                    "content": text
                })
        return code, text



