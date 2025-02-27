from typing import Union, List
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, Personalization
from twilio.rest import Client

from core.config import settings


class NotificationService:
    @staticmethod
    def send_email_notification(recipients: List[str], subject: str, body: str) -> Union[bool, str]:
        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            message = Mail(from_email="hackminor@live.com.mx", subject=subject)

            for recipient in recipients:
                # Personalize destination
                personalization = Personalization()
                personalization.add_to(Email(recipient))
                message.add_personalization(personalization)

                # Email template ID
                message.template_id = "d-329dbd69971b4dcdbd0f00cd46787bbb"

                # Substitution variables
                message.dynamic_template_data = {
                    "body": body
                }

            sg.send(message)
            return True
        except Exception as e:
            return str(e)

    @staticmethod
    def send_whatsapp_notification(recipients: List[str], message: str) -> Union[bool, str]:
        try:
            account_sid = settings.TWILIO_ACCOUNT_SID
            auth_token = settings.TWILIO_AUTH_TOKEN
            client = Client(account_sid, auth_token)
            for recipient in recipients:
                message = client.messages.create(
                    body=message,
                    from_=f'whatsapp:{settings.TWILIO_NUMBER}',
                    to=f'whatsapp:{recipient}'
                )
            return True
        except Exception as e:
            return str(e)
