# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/mailer.ipynb (unless otherwise specified).

__all__ = ['set_default_mail_api', 'send', 'send_test_email', 'logger', 'DEFAULT_MAIL_API', 'FROM_DEFAULT']

# Cell
import os
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from sewing import is_main, start_log

logger = logging.getLogger()

DEFAULT_MAIL_API = None
def set_default_mail_api(mail_api=None):
    global DEFAULT_MAIL_API
    if mail_api is None:
        SENDGRID_API_KEY = os.environ.get("SENDGRID_KEY")
        mail_api = SendGridAPIClient(SENDGRID_API_KEY)
        mail_api.api_name='sendgrid'

    DEFAULT_MAIL_API=mail_api
    return mail_api

FROM_DEFAULT = 'will@endao.network'

def send(to_emails, subject, html_content, from_email=FROM_DEFAULT, mail_api=DEFAULT_MAIL_API):
    logger.debug('Email request received {}'.format(
                        {'to': to_emails,
                         'subject': subject,
                         'body': html_content,
                         'from': from_email
                        }))

    if mail_api is None:
        mail_api = set_default_mail_api()

    message = Mail(from_email = from_email,
                    to_emails = to_emails,
                    subject = subject,
                    html_content = html_content)
    email_resp = mail_api.send(message)
    er = email_resp

    logger.debug('Email sent with response {}'.format({
            'status_code': er.status_code,
            'headers': dict(er.headers),
            'body': er.body}))

    return email_resp


def send_test_email(to_emails=None, from_email=FROM_DEFAULT, subject='Test email', content_file=None):
    if not content_file:
        html_content='This was an automated email.'
    else:
        with open(content_file, 'r') as f:
            html_content = f.read()

    return send(to_emails=to_emails, from_email=from_email, subject=subject, html_content=html_content)

if is_main(globals()):
    start_log()

    import argparse

    parser = argparse.ArgumentParser("Send test email")
    parser.add_argument('--to', type=str, help="Send email to")
    parser.add_argument('--sender', type=str, help='From email address', default=FROM_DEFAULT)
    parser.add_argument('--content', type=str, help="Filename of email body", default=None)
    parser.add_argument('--subject', type=str, help="Email subject", default='Test email')

    args = parser.parse_args()

    send_test_email(to_emails=[args.to], from_email=args.sender, subject=args.subject, content_file=args.content)