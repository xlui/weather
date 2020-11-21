import smtplib
import sys
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import arrow
import requests


def get_pic(_location):
    resp = requests.get(f'http://wttr.in/{_location}.png?lang=zh')
    if resp.status_code == 200:
        print('Successfully get weather image...')
        return resp.content
    else:
        print('Failed to get weather image...')
        return None


def send_email(_receiver, content, _sender, _password):
    if not _sender:
        print('[ERROR] Sender is empty!')
        return
    if not _receiver:
        print('[ERROR] Receiver is empty!')
        return
    if not content:
        print('[ERROR] Content is empty!')
    _today = arrow.now(tz="Asia/Shanghai")
    msg = MIMEMultipart()
    ようび = {
        1: '月曜日（げつようび）',
        2: '火曜日（かようび）',
        3: '水曜日（すいようび）',
        4: '木曜日（もくようび）',
        5: '金曜日（きんようび）',
        6: '土曜日（どようび）',
        7: '日曜日（にちようび）'
    }
    msg['Subject'] = f'Weather Report - {ようび.get(_today.isoweekday())}'
    msg['From'] = _sender
    msg['To'] = _receiver
    msg.attach(MIMEText('This email contains a image of the weather.', 'plain'))
    msg.attach(MIMEText("""
    <html>
        <body>
            <img src="cid:Mailtrapimage">
        </body>
    </html>
    """, 'html'))
    image = MIMEImage(content)
    image.add_header('Content-ID', '<Mailtrapimage>')
    image.add_header('Content-Disposition', 'attachment', filename=f'weather-report-{_today.date()}')
    msg.attach(image)

    print('connecting to yandex...')
    smtp = smtplib.SMTP(host='smtp.yandex.com', port=587)
    print(f'testing noop: {smtp.noop()}')
    print(f'starting TLS...')
    smtp.starttls()
    print(f'login...')
    smtp.login(_sender, _password)
    print('sending mail...')
    res = smtp.sendmail(_sender, _receiver, msg.as_string())
    print(f'send mail result: {res}')
    smtp.quit()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python weather_report.py [Location] [Receiver] [Sender_Email] [Sender_Password]')
    location, receiver, sender, password = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    send_email(receiver, get_pic(location), sender, password)
