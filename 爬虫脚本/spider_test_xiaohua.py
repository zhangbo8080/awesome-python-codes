import spider_function

import re

if __name__ == "__main__":
    # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    page = 2

    url = 'http://www.qiushibaike.com/hot/page/' + str(page)

    data_final = spider_function.getHtml(url)

#     print(data_final)
#     pattern = re.compile('<span>(.*?)</span>', re.S)
    pattern = re.compile(
        '<div.*?author.*?<h2>(.*?)</h2>.*?<span>(.*?)</span>', re.S)
    items = pattern.findall(data_final)
#     print(items)
    for item in items:
        haveimg = re.search('img', item[1])
        if not haveimg:
            print(item[0], "\n", item[1], "\n")
