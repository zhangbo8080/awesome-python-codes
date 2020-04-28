import spider_function

import re

if __name__ == "__main__":
    # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    url_profix = 'http://car.autohome.com.cn/shuyu/list'
    url = 'http://car.autohome.com.cn/shuyu/index.html'

    data_final = spider_function.getHtml(url)

#     print(data_final)
#     pattern = re.compile('<span>(.*?)</span>', re.S)
    pattern_items = re.compile(
        'shuyu/list.*?html" >(.*?)</a>', re.S)
    items = pattern_items.findall(data_final)
    print(items)

    items_url_list=[]
    for x in range(len(items)):
        if x ==0:
            pattern_url = re.compile('shuyu/list(.*?)" >{}'.format(items[x]), re.S)
        else:
            pattern_url = re.compile('{}.*?shuyu/list(.*?)" >{}'.format(items[x-1],items[x]), re.S)
        items_url = pattern_url.findall(data_final)
        items_url_list.append(url_profix+items_url[0])

    print(items_url_list)

    for y in range(len(items_url_list)):

        data_url = spider_function.getHtml(items_url_list[y])

        pattern_url = re.compile(
        'shuyu/list.*?html">(.*?)</a>.*?shuyu/detail.*?html" >(.*?)</a>', re.S)
        items_url = pattern_url.findall(data_url)
        # items_url.pop()
        pattern_url2 = re.compile(
            'shuyu/detail.*?html" >(.*?)</a>', re.S)
        items_url2 = pattern_url2.findall(data_url)

        print("---",items[y])
        print(items_url)
        print(items_url2)
        print(' ')

