

class BaseAI(object):
    def __init__(self, _api_key=None, _secret_key=None):
        self._api_key = _api_key
        self._secret_key = _secret_key
        self._chat_chat_session = []

    def chat(self, text, model=None):
        return ''

    def text2image(self, text, model=None):
        return ''

    def text2audio(self, text, model=None):
        return ''

    def text2video(self, text, model=None):
        return ''




