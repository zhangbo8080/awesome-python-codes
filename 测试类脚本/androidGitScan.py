import subprocess
import os
import datetime
import time
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import xml.etree.cElementTree as et


# 判断是否有新的push
def push_check(path):
    result = subprocess.Popen("cd {} && /usr/bin/git pull".format(path), shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)

    res = result.stdout.read().decode()
    # print(res)
    # with open("D:/123.txt", "w") as f:
    #     f.write(res)
    if "Already up-to-date." == res.strip():
        return False
    else:
        return True


# 创建文件夹
def mkdir(path):
    """

    :param path: 创建的文件路径
    :return: 创建成功返回True, 创建失败返回False
    """
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False


# 执行fireline命令
def exc_fireline(fireline_path, sns_path, fireline_reprot_path):
    mkdir(fireline_reprot_path)
    # chmod_shell = r"chmod -R 777 /home/zhangbo/fireline/firelineReport"

    # chmod_result = subprocess.Popen(chmod_shell, shell=True, stdout=subprocess.PIPE,
    #                           stderr=subprocess.PIPE)
    # chmod_res = chmod_result.stdout.read().decode()
    cmd_shell = r"/opt/apps_install/jdk8/bin/java -jar {0}fireline_1.7.3.jar -s={1} -r={2}".format(sns_path,
                                                                                                   fireline_path,
                                                                                                   fireline_reprot_path)
    # print(cmd_shell)
    result = subprocess.Popen(cmd_shell, shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
    res = result.stdout.read().decode('gbk')
    # zip_shell = r"zip -r -q {}.zip {}/".format(fireline_reprot_path, fireline_reprot_path)
    #
    # subprocess.Popen(zip_shell, shell=True)

    # print("扫描完成，可以访问http://localhost:8000/查看结果了")
    # print(res)
    # with open("{}.txt".format(fireline_reprot_path), "w") as f:
    #     f.write(res)


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


# def send_mail(mail_content, from_addr, mailto_list, server):
#     # print("trying to send mail by " + server)
#     msg = MIMEText(mail_content, 'html', 'utf-8')
#     msg['From'] = _format_addr(u'360火线扫描 <%s>' % from_addr)
#     msg['To'] = ",".join(mailto_list)
#     msg['Subject'] = Header(u'android代码扫描结果', 'utf-8').encode()
#     server = smtplib.SMTP(server, 25)
#     server.sendmail(from_addr, mailto_list, msg.as_string())
#     server.quit()

# print("send mail successfully")


def format_date(date):
    return date.split("T")[0]


# def crawl_xml(xml_path):
#     tree = et.parse(xml_path)  # 打开xml文件
#
#     root = tree.getroot()
#
#     content_list = []
#
#     for child in root:
#         if child.tag == "violations":
#             for x in child:
#                 for (k, v) in x.attrib.items():
#                     content_list.append(k)
#                     content_list.append(" = ")
#                     content_list.append(v)
#                     content_list.append("\n")
#                 content_list.append("\n")
#                 # print(x.key,x.value)
#                 # print(x.get("rulename"))
#                 # print(x.get("ruletype"))
#                 # print(x.get("id"))
#                 # print(x.get("priority"))
#                 # print(x.get("description"))
#     # html_str = "".join(content_list)
#     return content_list

def crawl_xml(xml_path, url):
    tree = et.parse(xml_path)  # 打开xml文件

    root = tree.getroot()

    # content_list = []
    trs_list = []
    for child in root:
        if child.tag == "violations":
            for x in child:
                # for (k, v) in x.attrib.items():
                #     content_list.append(k)
                #     content_list.append(" = ")
                #     content_list.append(v)
                #     content_list.append("\n")
                # content_list.append("\n")
                trs_list.append('<tr>')
                trs_list.append('<th align="left">{0}</th>'.format(x.get("ruletype")))
                trs_list.append('<th align="left">{0}</th>'.format(x.get("rulename")))
                trs_list.append('<th align="left">{0}</th>'.format(x.get("priority")))
                trs_list.append('<th align="left">{0}</th>'.format(x.get("id")))
                trs_list.append('<th align="left">{0}</th>'.format(x.get("description")))
                trs_list.append('</tr>')
            else:
                pass
    header_list = ['类型', '规则种类', '优先级', 'id', '描述']
    theader = '<th>{0}</th>'.format('</th><th>'.join(header_list))
    table = '报告详情可以访问：{0} <table width="100%" border="1">\n<thead><tr>{1}</tr></thead>\n<tbody>\n{2}'.format(
        url, theader,
        '\n'.join(
            trs_list))
    # print(table)
    return table


def SendMail(sender='autotestsns@sohu-inc.com', receiver='bozhang213817@sohu-inc.com', content=None):
    sender = sender
    subject = u'android代码扫描结果'
    smtpserver = 'mail.mtpc.sohu.com'
    message = MIMEText(content, 'html', 'utf-8')
    message['From'] = _format_addr(u'360火线扫描 <%s>' % sender)
    message['To'] = receiver
    # message['Cc'] = ",".join(receiver_cc)
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver, 25)
        smtp.sendmail(sender, receiver, message.as_string())
        smtp.close()
        # print('成功发送给：', receiver)
    except Exception as e:
        # print(e)
        # print('邮件发送失败')
        pass


if __name__ == '__main__':
    sns_path = "/home/zhangbo/sns"
    fireline_path = "/home/zhangbo/"
    current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    fireline_reprot_path = "/home/zhangbo/fireline/firelineReport/{}".format(current_time)
    # print(push_check(sns_path))
    if push_check(sns_path):
        # print("pull到新的代码，开始代码扫描")
        exc_fireline(sns_path, fireline_path, fireline_reprot_path)
        xml_path = fireline_reprot_path + "/testReport.xml"
        url = "http://10.16.77.182:3000/{}/testReport.html".format(current_time)
        table = crawl_xml(xml_path, url)
        SendMail(content=table)
        # mail_content_list.append("http://10.16.77.182:3000/{}/".format(current_time))
        # mail_text = "".join(mail_content_list)
        # send_mail(mail_text.strip(), "autotestsns@sohu-inc.com", ['bozhang213817@sohu-inc.com'], "mail.mtpc.sohu.com")

    #   zip -r -q pack.zip mark/
    #     else:
    #         print("没有pull到新的代码")
    # time.sleep(1800)
