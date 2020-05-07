import jenkins
import requests
import qrcode
import os
from vulpo.scs.connection import SCSConnection

JENKINS_URL = 'http://10.2.11.50:8070/jenkins/view/hy_android/'
JOB_NAME = "hy_android_dev"


# 从jenkins上获取最新的apk地址
def get_apks():
    server = jenkins.Jenkins(JENKINS_URL)
    job_info = server.get_job_info(JOB_NAME)

    build_info = server.get_build_info(JOB_NAME, job_info["lastStableBuild"]["number"])

    artifacts = build_info["artifacts"]
    url = build_info["url"]
    for x in artifacts:
        if "Test_debug" in x["fileName"] and ".apk" in x["fileName"]:
            return url + "artifact/" + x["fileName"]


# 下载apk文件到本地
def download_apks(url):
    r = requests.get(url)
    with open("D:/123.apk", "wb") as code:
        code.write(r.content)


# 根据url生成二维码
def generate_qrcode(url):
    img = qrcode.make(url)
    qrcode_temp = url.split("CID")[-1]

    qrcode_build_version = qrcode_temp.split(".")[0]
    img.save('D:/{}qrcode.png'.format(qrcode_build_version))


# 将文件上传到搜狐云台
def upload_to_sohucs(local_file_name):
    conn = SCSConnection('a3vQAcgPYOXZuh+ToJWbmQ==', 'fxJR4FeSQY9W60WWbmcdYw==')
    my_bucket = conn.get_bucket('sns-hytest')
    my_key = my_bucket.new_key("/zhangbo/" + local_file_name)
    fp = open("D:/迅雷下载/" + local_file_name, 'rb')
    my_key.set_contents_from_file(fp)
    fp.close()
    # profix = "http://sns-hytest.bjcnc.scs.sohucs.com/"
    # return profix + local_file_name


# 获取文件夹下的文件名
def get_filename(filePath):
    filename_list = os.listdir(filePath)
    return filename_list


if __name__ == '__main__':
    filename = None
    count = 0
    file_path = "D:/迅雷下载/"
    filename_list = get_filename(file_path)
    print("{}文件夹下面的文件如下所示：".format(file_path))
    for y in filename_list:
        print(y)
    for x in filename_list:
        if ".apk" in x and "hy_" in x:
            filename = x
            count = count + 1
    print()
    print("选中的apk文件为：")
    print(filename)
    if filename and count == 1:
        upload_to_sohucs(filename)

        url = "http://sns-hytest.bjcnc.scs.sohucs.com/zhangbo/{}".format(filename)

        generate_qrcode(url)

        os.remove("D:/迅雷下载/" + filename)
