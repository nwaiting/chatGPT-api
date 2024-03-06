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

    CHATGPT_CHAT_MODEL  配置聊天的模型名字

    CHATGPT_IMAGE_MODEL 配置生成图片的模型名字


#### *openai*

在apis/config.py中配置key，在 [官网](https://platform.openai.com/account/api-keys) 申请api的key

支持接口：

chat            [聊天]()

getEmbeddings   [获取文本的embeddings]()

text2image      [文本生成图片]()

editImage       [编辑图片]()

changeImage     [修改图片]()

text2voice      [文本生成语音]()

voice2text      [语音生成文本]()


#### *googleai*

在apis/config.py中配置key，在 [官网](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini?hl=zh-cn) 申请api的key

#### *千问*

在apis/config.py中配置key，在 [官网](https://help.aliyun.com/zh/dashscope/developer-reference/tongyi-qianwen-vl-api) 申请api的key


#### *文心一言*

在apis/config.py中配置key，在 [官网](https://yiyan.baidu.com/welcome) 申请api的key


#### *智谱AI*

在apis/config.py中配置key，在 [官网](https://maas.aminer.cn/) 申请api的key



## 交流沟通
<img src="./images/wx.jpg" width="249"/>
