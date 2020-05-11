# -*- coding: utf-8 -*-
# __Author__='Zhangbo'
# __Time__='2020/5/11 10:15'

import requests
import wget


class FileDownload:

    def __init__(self, path=None, url=None):
        self.path = path
        self.url = url

    # 使用requests库
    def download_file_by_requests(self):
        # 如果需要重定向，需要allow_redirects为True
        # 如果需要分块下载，需要加上stream为True
        myfile = requests.get(self.url)

        open(self.path, "wb").write(myfile.content)

    # 使用wget库
    def download_file_by_wget(self):
        wget.download(self.url, self.path)


if __name__ == "__main__":
    path = "D:/test.png"
    url = "https://img02.sogoucdn.com/app/a/100520020/9619bdf2c73e8cf0e970c586b9dd5ab6"
    file_download = FileDownload(path=path, url=url)
    file_download.download_file_by_wget()
