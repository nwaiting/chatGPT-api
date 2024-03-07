# -*- coding: utf-8 -*-
from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
import logging
import dashscope
from dashscope import MultiModalEmbedding
from .baseai import BaseAI

logger = logging.getLogger(__file__)


class QianwenAI(BaseAI):
    def __init__(self, _api_key=None, _secret_key=None):
        super(QianwenAI, self).__init__(_api_key, _secret_key)
        dashscope.api_key = _api_key

    def chat(self, text, model='qwen-turbo'):
        """
        问答
        :param text:
        :param model:
        :return:
        """
        model = model or 'qwen-turbo'
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
        """
        文字生成图片
        :param text:
        :param model:
        :return:
        """
        model = model or "stable-diffusion-xl"
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
                logger.info("{}:{}".format(rsp.output, rsp.usage))
            else:
                logger.error('Failed, status_code: {}, code: {}, message: {}'.format(rsp.status_code, rsp.code, rsp.message))
            status = dashscope.ImageSynthesis.fetch(rsp)
            if status.status_code == HTTPStatus.OK:
                logger.info(status.output.task_status)
            else:
                logger.error('Failed, status_code:{}, code:{}, message:{}'.format(status.status_code, status.code, status.message))

            rsp = dashscope.ImageSynthesis.wait(rsp)
            if rsp.status_code == HTTPStatus.OK:
                logger.info(rsp.output)
            else:
                logger.error('Failed, status_code:{}, code:{}, message:{}'.format(rsp.status_code, rsp.code, rsp.message))

        return sample_block_call()
    
    def text2image2(self, text, prompt, result_path='./', model='wordart-semantic', font="dongfangdakai"):
        """
        文字变形，生成艺术字
        :param text:
        :param result_path:
        :return:
        """
        model = model or 'wordart-semantic'
        url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/wordart/semantic'
        headers = {
            'X-DashScope-Async': 'enable',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer  {}'.format(self._api_key)
        }
        json_data = {
            "model": model,
            "input": {
                "text": text,
                "prompt": prompt
            },
            "parameters": {
                "steps": 80,
                "n": 1,
                "output_image_ratio": "1024x1024",
                "font_name": font
            }
        }
        res = requests.post(url, headers=headers, json=json_data)
        return res.status_code, res.json()

    def get_images(self, task_id):
        """
        根据任务id获取结果
        :param task_id:
        :return:
        """
        headers = {
            'Authorization': 'Bearer  {}'.format(self._api_key)
        }
        url = 'https://dashscope.aliyuncs.com/api/v1/tasks/{}'.format(task_id)
        res = requests.get(url, headers=headers)
        return res.status_code, res.text

    def image_detect(self, image_path: list):
        """
        对用户上传的人物图像进行检测，判断其中所包含的人脸是否符合facechain微调所需的标准，检测维度包括人脸数量、大小、角度、光照、清晰度等多维度，支持图像组输入，并返回每张图像对应的检测结果。
        :param image_path:  输入的图像 URL，分辨率不小于256*256，不超过4096*4096，文件大小不超过5MB, 支持格式包括JPEG, PNG, JPG, WEBP
        :return:
        """
        for it in image_path:
            if not it.startswith('http'):
                return -1, '图片地址有误,请使用图片链接'

        url = 'https://dashscope.aliyuncs.com/api/v1/services/vision/facedetection/detect'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer  {}'.format(self._api_key)
        }
        json_data = {
          "model": "facechain-facedetect",
          "input": {
            "images": image_path
          },
          "parameters": {
          }
        }
        res = requests.post(url, headers=headers, json=json_data)
        return res.status_code, res.json()

    def image_fine_train(self, file_zip_path):
        """
        本接口为模型定制类服务，需要相对较长的算法调用时间，所以在接口层面采用了异步调用的方式进行任务提交，在通过任务接口提交作业之后，系统会返回对应的作业ID，随后可以通过对模型定制类任务的查询/管理接口进行相应操作
        :param file_zip_path:
        :return:
        """
        url = 'https://dashscope.aliyuncs.com/api/v1/files'
        headers = {
            'Authorization': 'Bearer  {}'.format(self._api_key)
        }
        files = {
            'files': open(file_zip_path, 'rb'),
            "descriptions": "a sample fine-tune data file for facechain"
        }
        res = requests.post(url, headers=headers, files=files)
        return res.status_code, res.text

    def image_fine_task(self, file_id, model="facechain-finetune"):
        """
        完成训练数据的上传之后，就可以使用在上传之后得到的 file_id 发起facechain模型定制任务了
        :param file_id:
        :return:
        """
        model = model or "facechain-finetune"
        url = 'https://dashscope.aliyuncs.com/api/v1/fine-tunes'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer  {}'.format(self._api_key)
        }
        json_data = {
            "model": model,
            "training_file_ids": [file_id],
        }
        res = requests.post(url, headers=headers, json=json_data)
        return res.status_code, res.text

    def image_fine_task_result(self, job_id):
        """
        查询模型定制任务的状态，并在任务完成之后获取对应的任务结果。当训练任务成功之后，就可以使用对应的 finetuned_output 内容做推理调用
        :param job_id:
        :return:
        """
        url = 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/{}'.format(job_id)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer  {}'.format(self._api_key)
        }
        res = requests.get(url, headers=headers)
        return res.status_code, res.text

    def image_aigc_generator(self, model="facechain-generation", resource_id="women_model", resource_type="facelora"):
        """
        基于人物形象训练已经得到的形象，可以继续通过人物生成写真模型完成该形象的写真生成，支持多种预设风格，包括证件照、商务写真等
        :param model:
        :param resource_id:
        :param resource_type:
        :return:
        """
        model = model or "facechain-generation"
        url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/album/gen_potrait'
        headers = {
            'X-DashScope-Async': 'enable',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer  {}'.format(self._api_key)
        }
        json_data = {
            "model": model,
            "parameters": {
                "style": "f_idcard_female",
                "size": "512*512",
                "n": 4
            },
            "resources": [
                {
                    "resource_id": resource_id,
                    "resource_type": resource_type
                }
            ]
        }
        res = requests.post(url, headers=headers, json=json_data)
        return res.status_code, res.text

    def get_text_embedding(self, text, model=dashscope.TextEmbedding.Models.text_embedding_v1):
        """
        通用文本向量，是通义实验室基于LLM底座的多语言文本统一向量模型，面向全球多个主流语种，提供高水准的向量服务，帮助开发者将文本数据快速转换为高质量的向量数据。
        :param text:
        :return:
        """
        res = dashscope.TextEmbedding.call(
            model=model,
            input=text)
        return res.status_code, res

    def get_image_embedding(self, image:list, model=MultiModalEmbedding.Models.multimodal_embedding_one_peace_v1):
        """
        生成图片embedding
        :param image:
        :param model:
        :return:
        """
        input = []
        for it in image:
            input.append({
                'image': it
            })
        res = MultiModalEmbedding.call(model=model, input=input, auto_truncation=True)
        return 0, res

    def get_image_embedding_with_voice(self, image, voice, model=MultiModalEmbedding.Models.multimodal_embedding_one_peace_v1):
        """
        结合图片和语音，生成Embedding
        :param image:
        :param voice:
        :param model:
        :return:
        """

        input = [{'audio': voice},
                 {'image': image}]
        res = MultiModalEmbedding.call(model=model, input=input, auto_truncation=True)
        return 0, res

    def get_multimodal_embedding(self, image, voice, text, model=MultiModalEmbedding.Models.multimodal_embedding_one_peace_v1):
        """
        生成图片embedding
        :param image:
        :param model:
        :return:
        """
        input = [{'factor': 1, 'text': text},
                 {'factor': 2, 'audio': voice},
                 {'factor': 3, 'image': image}]
        res = MultiModalEmbedding.call(model=model, input=input, auto_truncation=True)
        return 0, res
