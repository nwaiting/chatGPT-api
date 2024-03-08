# <p align="center">chatGPT-api</p>

<br>
<p align="center">
    <a href="#"><img src="https://img.shields.io/badge/python-3.9-green.svg"></a>
</p>
<br />

## Documentation

<p> 集成各大模型的api接口截集合 </p>


## Install

#### 配置

修改需要使用的模型，在apis/config.py的配置中

    API_KEY  配置api key

    SECRET_KEY 配置secret key


#### *openai*

在apis/config.py中配置key，在 [官网](https://platform.openai.com/account/api-keys) 申请api的key

支持接口：

[问答](https://github.com/nwaiting/chatGPT-api/blob/master/apis/aichat/openai.py)

[获取文本的embeddings](https://github.com/nwaiting/chatGPT-api/blob/master/apis/aichat/openai.py)

[文本生成图片](https://github.com/nwaiting/chatGPT-api/blob/master/apis/aichat/openai.py)

[编辑图片](https://github.com/nwaiting/chatGPT-api/blob/master/apis/aichat/openai.py)

[修改图片](https://github.com/nwaiting/chatGPT-api/blob/master/apis/aichat/openai.py)

[文本生成语音](https://github.com/nwaiting/chatGPT-api/blob/master/apis/aichat/openai.py)

[语音生成文本](https://github.com/nwaiting/chatGPT-api/blob/master/apis/aichat/openai.py)


#### *googleai*

在apis/config.py中配置key，在 [官网](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini?hl=zh-cn) 申请api的key

[问答](https://github.com/nwaiting/chatGPT-api/blob/master/apis/aichat/googleai.py)

[图片生成文字](https://github.com/nwaiting/chatGPT-api/blob/master/apis/aichat/googleai.py)

[文字生成图片](https://github.com/nwaiting/chatGPT-api/blob/master/apis/aichat/googleai.py)

[根据图片回答问题](https://github.com/nwaiting/chatGPT-api/blob/master/apis/aichat/googleai.py)

[多模态生成embedding](https://github.com/nwaiting/chatGPT-api/blob/master/apis/aichat/googleai.py)


#### *千问*

在apis/config.py中配置key，在 [官网](https://help.aliyun.com/zh/dashscope/developer-reference/tongyi-qianwen-vl-api) 申请api的key

支持接口：

[问答](https://github.com/nwaiting/chatGPT-api/blob/master/apis/aichat/qianwenai.py)

[文字生成图片](https://github.com/nwaiting/chatGPT-api/blob/master/apis/aichat/qianwenai.py)

[文字变形，生成艺术字](https://github.com/nwaiting/chatGPT-api/blob/master/apis/aichat/qianwenai.py)

[根据任务id获取结果](https://github.com/nwaiting/chatGPT-api/blob/master/apis/aichat/qianwenai.py)

[人物图像进行检测](https://github.com/nwaiting/chatGPT-api/blob/master/apis/aichat/qianwenai.py)

[训练模型](https://github.com/nwaiting/chatGPT-api/blob/master/apis/aichat/qianwenai.py)

[应用训练的模型](https://github.com/nwaiting/chatGPT-api/blob/master/apis/aichat/qianwenai.py)

[训练模型推理结果](https://github.com/nwaiting/chatGPT-api/blob/master/apis/aichat/qianwenai.py)

[证件照、商务写真等](https://github.com/nwaiting/chatGPT-api/blob/master/apis/aichat/qianwenai.py)

[生成通用文本向量](https://github.com/nwaiting/chatGPT-api/blob/master/apis/aichat/qianwenai.py)

[生成图片embedding](https://github.com/nwaiting/chatGPT-api/blob/master/apis/aichat/qianwenai.py)

[结合图片和语音，生成Embedding](https://github.com/nwaiting/chatGPT-api/blob/master/apis/aichat/qianwenai.py)

[多模态生成embedding](https://github.com/nwaiting/chatGPT-api/blob/master/apis/aichat/qianwenai.py)

[文本理解任务](https://github.com/nwaiting/chatGPT-api/blob/master/apis/aichat/qianwenai.py)

[实时语音合成](https://github.com/nwaiting/chatGPT-api/blob/master/apis/aichat/qianwenai.py)

[翻译](https://github.com/nwaiting/chatGPT-api/blob/master/apis/aichat/qianwenai.py)


#### *文心一言*

在apis/config.py中配置key，在 [官网](https://yiyan.baidu.com/welcome) 申请api的key


#### *智谱AI*

在apis/config.py中配置key，在 [官网](https://maas.aminer.cn/) 申请api的key



## 交流沟通
<img src="./images/wx.jpg" width="249"/>
