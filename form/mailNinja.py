import hmac
import requests
from form import app

def send_email(subject, sender, recipients, text_body, reply_to, message_id):
    """
    Send email using the Mailgun APIv3
    :param recipients - [list]
    :param message_id - to keep track of db/webhooks
    """
    return requests.post(
        "https://api.mailgun.net/v3/miteshshah.com/messages",
        auth=("api", app.config['MAILGUN_API_KEY']),
        data={"from": sender + " <mailgun@miteshshah.com>",
              "to": recipients,
              "subject": subject,
              "text": text_body,
              "h:Reply-to": reply_to,
              "v:my-custom-data": {"message_id": message_id}})
