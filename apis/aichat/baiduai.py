import requests
import json
import logging
from .baseai import BaseAI

logger = logging.getLogger(__file__)


class BaiduAI(BaseAI):
    def __init__(self, _api_key=None, _secret_key=None):
        super(BaiduAI, self).__init__(_api_key, _secret_key)
        self._chat_chat_session = [{"role": "system", "content": "你是一个能干的助手."}]

    def getAccessToken(self):
        url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}".format(self._api_key, self._secret_key)

        payload = json.dumps("")
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json().get("access_token")

    def chat(self, text, model="gpt-3.5-turbo"):
        model = model or "gpt-3.5-turbo"
        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/chatBaidu?access_token=" + self.getAccessToken()
        self._chat_chat_session.append({
                    "role": "user",
                    "content": text
                })
        payload = json.dumps({
            "messages": self._chat_chat_session
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        code, text = response.status_code, response.text
        self._chat_chat_session.append({
                    "role": "assistant",
                    "content": text
                })
        return code, text






