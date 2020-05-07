import xml.etree.cElementTree as et
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def crawl_xml(xml_path):
    tree = et.parse(xml_path)  # 打开xml文件

    root = tree.getroot()

    content_list = []
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
    table = 'hahah http://www.sohu.com <table border="1" width="100%" >\n<thead><tr>{0}</tr></thead>\n<tbody>\n{1}'.format(
        theader,
        '\n'.join(
            trs_list))
    # print(table)
    return table
    # html_str = "".join(content_list)
    # return html_str


def SendMail(sender='autotestsns@sohu-inc.com', receiver='bozhang213817@sohu-inc.com', content=None):
    sender = sender
    subject = u'test'
    smtpserver = 'mail.mtpc.sohu.com'
    message = MIMEText(content, 'html', 'utf-8')
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


if '__main__' == __name__:
    table = crawl_xml("D:/testReport.xml")
    SendMail(content=table)
