import random

random_mobile_number = random.choice(['139', '188', '185', '136', '158', '151']) + "".join(
	random.choice("0123456789") for i in range(8))

print('随机生成的手机号为：', random_mobile_number)
