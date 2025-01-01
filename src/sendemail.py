import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class sendemail:
    # 设置发送邮件的服务器及端口
    smtp_server = 'smtp.163.com'  # 163 邮箱的 SMTP 服务器
    smtp_port = 465  # 163 邮箱使用的端口（SSL）

    # 登录邮箱的用户名和密码
    sender_email = ' '  # 发送邮箱地址
    sender_password = ' '  # 163 邮箱的授权码（不是登录密码）

    # 收件人的邮箱地址列表
    receiver_emails = [' ']  # 可根据需要增加邮箱地址

    # 获取当前日期
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 纯文本内容
    text_body = f'''Hello,
    
    This is a test email sent on {current_date}.
    If you receive this email, it means the code is working!
    
    Here are some important details:
    - The email system is functioning properly.
    - This is a multi-line body text example.
    - You can add more content as needed.
    
    Best regards,
    Your Name'''

    html_body = '''<html>
        <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                }
                h1 {
                    color: #4CAF50;
                }
                p {
                    font-size: 16px;
                }
                ul {
                    list-style-type: square;
                }
                pre {
                    font-family: 'Courier New', monospace;
                    background-color: #f4f4f4;
                    padding: 10px;
                    border: 1px solid #ddd;
                }
            </style>
        </head>
        <body>
            <h1>Order Created Successfully!</h1>
            <p>Your order has been successfully created on {current_date}.</p>
            <p>Thank you for your purchase! Your order is being processed.</p>
            <p>If you have any questions, please do not hesitate to contact us.</p>
            <p>Best regards,</p>
            <p>奶龙大王</p>
            <p>
                <pre>
    ██████╗ ███████╗ █████╗  ██████╗███████╗     █████╗ ███╗   ██╗██████╗     ██╗      ██████╗ ██╗   ██╗███████╗
    ██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝    ██╔══██╗████╗  ██║██╔══██╗    ██║     ██╔═══██╗██║   ██║██╔════╝
    ██████╔╝█████╗  ███████║██║     █████╗      ███████║██╔██╗ ██║██║  ██║    ██║     ██║   ██║██║   ██║█████╗  
    ██╔═══╝ ██╔══╝  ██╔══██║██║     ██╔══╝      ██╔══██║██║╚██╗██║██║  ██║    ██║     ██║   ██║╚██╗ ██╔╝██╔══╝  
    ██║     ███████╗██║  ██║╚██████╗███████╗    ██║  ██║██║ ╚████║██████╔╝    ███████╗╚██████╔╝ ╚████╔╝ ███████╗
    ╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════╝    ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝     ╚══════╝ ╚═════╝   ╚═══╝  ╚══════╝
                </pre>
            </p>
        </body>
    </html>'''

    # 替换 HTML 内容中的当前日期
    html_body = html_body.replace('{current_date}', current_date)


    # 创建邮件对象
    msg = MIMEMultipart("alternative")
    msg['From'] = sender_email
    msg['To'] = ', '.join(receiver_emails)  # 群发多个收件人
    msg['Subject'] = 'Order Msg'

    # 添加纯文本和HTML内容
    msg.attach(MIMEText(text_body, 'plain'))  # 纯文本内容
    msg.attach(MIMEText(html_body, 'html'))  # HTML 内容

    # 连接到 SMTP 服务器并发送邮件
    try:
        # 建立连接并登录
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)  # 使用 SSL 加密
        server.login(sender_email, sender_password)

        # 发送邮件
        server.sendmail(sender_email, receiver_emails, msg.as_string())

        print("邮件发送成功!")

    except Exception as e:
        print(f"邮件发送失败: {e}")

    finally:
        server.quit()

if __name__ == '__main__':
    sendemail()
