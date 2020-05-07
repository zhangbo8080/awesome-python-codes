# -*- coding: utf-8 -*-
# __Author__='Zhangbo'
# __Time__='2019-11-12 19:06'

import nacos
import yaml

SERVER_ADDRESSES = "op-test.sns.sohuno.com:80"
NAMESPACE = "9eae126d-3501-4100-b577-baa2eaeed8ea"

client = nacos.NacosClient(SERVER_ADDRESSES, namespace=NAMESPACE)

# get config
data_id = "monitor_h5"
group = "DEFAULT_GROUP"
a=client.get_config(data_id, group)
# print(a)

b=yaml.load(a, Loader=yaml.FullLoader)

print(b)
# print(yaml.load(a,Loader=yaml.FullLoader))