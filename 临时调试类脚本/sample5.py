import uuid
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from aliyunsdkcore.http import method_type
from prettyprinter import cpprint

# 多语言分词
wordsegment = "/nlp/api/wordsegment/general"

# 词性标注
wordpos = "/nlp/api/wordpos/general"

# 命名实体
entity = "/nlp/api/entity/ecommerce"

# 情感分析
sentiment = "/nlp/api/sentiment/ecommerce"

# 中心词提取
kwe = "/nlp/api/kwe/ecommerce"

# 智能文本分类
textstructure = "/nlp/api/textstructure/news"

# 文本信息抽取
contract_ie = "/nlp/api/ie/contract"

# 创建AcsClient实例
client = AcsClient('LTAI4FfcbPiNKinz3UdJwFmV', 'hRHvqPoSR5EvzGdEnBB3ecsfkNX798', 'cn-shanghai')
request = CommonRequest()
request.set_domain("nlp.cn-shanghai.aliyuncs.com")  # 必须设置domain

request.set_uri_pattern(entity)  # 设置所要请求的API路径

request.set_method(method_type.POST)  # 设置请求方式，目前只支持POST
request.add_header("x-acs-signature-method", "HMAC-SHA1")  # 设置签名方法
request.add_header("x-acs-signature-nonce", uuid.uuid4().hex)  # 设置请求唯一码，防止网络重放攻击, 每个请求必须不同
request.add_header("x-acs-signature-version", "1.0")  # 设置签名版本

content = '{"lang":"ZH","text":"狐友AI科技峰会"}'

request.set_content_type("application/json;chrset=utf-8")  # 设置请求格式
request.set_accept_format("application/json;chrset=utf-8") # 设置响应格式
request.set_content(bytearray(content.encode('utf-8')))  # 设置请求内容
request.set_version('2018-04-08')  # 设置版本
request.set_action_name("None")
response = client.do_action_with_exception(request)
cpprint(json.loads(response.decode()))
