# _*_ coding : utf-8 _*_
# @Time : 2024/11/2 22:31
# @Author : 哥几个佛
# @File : send_email
# @Project : CrawlerJDComment
import smtplib
from email.header import Header
from email.mime.text import MIMEText

from utils.custom_logger import logger


class EmailSender:
    def __init__(self, sender_email, sender_password, receiver_email):
        """
        初始化EmailSender类

        :param sender_email: 发件人邮箱地址
        :param sender_password: 发件人邮箱授权码
        :param receiver_email: 收件人邮箱地址
        """
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.receiver_email = receiver_email

    def send_email(self, subject, body):
        """
        发送邮件的方法

        :param subject: 邮件主题
        :param body: 邮件正文内容
        :return: 无
        """
        try:
            # 创建一个MIMEText对象，设置邮件内容、格式（这里是纯文本格式）以及编码
            msg = MIMEText(body, 'plain', 'utf-8')
            msg['Subject'] = Header(subject, 'utf-8')
            msg['From'] = self.sender_email
            msg['To'] = self.receiver_email

            # 创建SMTP对象，连接到SMTP服务器（以QQ邮箱为例，SMTP服务器地址为smtp.qq.com，端口为465，使用SSL加密）
            server = smtplib.SMTP_SSL("smtp.qq.com", 465)
            # 登录发件人邮箱
            server.login(self.sender_email, self.sender_password)
            # 发送邮件
            server.sendmail(self.sender_email, self.receiver_email, msg.as_string())
            logger.info("邮件发送成功！")
            # 关闭连接
            server.close()
        except Exception as e:
            logger.error(f"邮件发送失败：{e}")
