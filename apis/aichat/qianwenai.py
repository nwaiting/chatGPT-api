# -*- coding: utf-8 -*-
from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
import logging
import dashscope
from .baseai import BaseAI

logger = logging.getLogger(__file__)


class QianwenAI(BaseAI):
    def __init__(self, _api_key=None, _secret_key=None):
        super(QianwenAI, self).__init__(_api_key, _secret_key)
        dashscope.api_key = _api_key

    def chat(self, text, model='qwen-turbo'):
        response = dashscope.Generation.call(
            model=model,
            prompt=text,
            seed=1234,
            top_p=0.8,
            result_format='message',
            enable_search=False,
            max_tokens=1500,
            temperature=0.85,
            repetition_penalty=1.0
        )
        if response.status_code == HTTPStatus.OK:
            return response.status_code, response['output']['choices'][0]['message']['content']
        else:
            return response.status_code, 'Request id: {}, Status code: {}, error code: {}, error message: {}'.format(response.request_id, response.status_code, response.code, response.message)

    def text2image(self, text, model="stable-diffusion-xl"):
        prompt = text
        def sample_block_call():
            rsp = dashscope.ImageSynthesis.call(model=model,
                                      prompt=prompt,
                                      negative_prompt="garfield",
                                      n=1,
                                      size='1024*1024')
            if rsp.status_code == HTTPStatus.OK:
                logger.info("{}:{}".format(rsp.output, rsp.usage))
                r = []
                for result in rsp.output.results:
                    file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
                    with open('./%s' % file_name, 'wb+') as f:
                        f.write(requests.get(result.url).content)
                    r.append(file_name)
                return rsp.status_code, r
            else:
                return rsp.status_code, 'Failed, status_code:{}, code:{}, message:{}'.format(rsp.status_code, rsp.code, rsp.message)

        def sample_async_call():
            rsp = dashscope.ImageSynthesis.async_call(model=model,
                                            prompt=prompt,
                                            negative_prompt="garfield",
                                            n=1,
                                            size='512*512')
            if rsp.status_code == HTTPStatus.OK:
                print(rsp.output)
                print(rsp.usage)
            else:
                print('Failed, status_code: %s, code: %s, message: %s' %
                      (rsp.status_code, rsp.code, rsp.message))
            status = dashscope.ImageSynthesis.fetch(rsp)
            if status.status_code == HTTPStatus.OK:
                print(status.output.task_status)
            else:
                print('Failed, status_code: %s, code: %s, message: %s' %
                      (status.status_code, status.code, status.message))

            rsp = dashscope.ImageSynthesis.wait(rsp)
            if rsp.status_code == HTTPStatus.OK:
                print(rsp.output)
            else:
                print('Failed, status_code: %s, code: %s, message: %s' %
                      (rsp.status_code, rsp.code, rsp.message))

        return sample_block_call()
    







