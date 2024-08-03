from typing import List, Union, Optional

from fastapi import HTTPException, status
from sendgrid import SendGridAPIClient, Mail, Personalization, Email, Content
from twilio.rest import Client

from core.config import settings


class SendNotificationService:

    @staticmethod
    def send_email_notification(recipients: List[str], subject: str,
                                dynamic_recipient: Optional[str], dynamic_action: Optional[str],
                                dynamic_amount: Optional[str], dynamic_date: Optional[str],
                                dynamic_greeting: Optional[str]) -> Union[dict[str, str], str]:
        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            message = Mail(from_email="noreply@beplus.com.mx", subject=subject)

            for recipient in recipients:
                # Personalización del destinatario
                personalization = Personalization()
                personalization.add_to(Email(recipient))
                message.add_personalization(personalization)

                # Plantilla de correo electrónico
                message.template_id = "d-329dbd69971b4dcdbd0f00cd46787bbb"

                # Variables de sustitución
                message.dynamic_template_data = {
                    "dynamic_recipient": dynamic_recipient,
                    "dynamic_action": dynamic_action,
                    "dynamic_amount": dynamic_amount,
                    "dynamic_date": dynamic_date,
                    "dynamic_greeting": dynamic_greeting
                }

                sg.send(message)
            return {"status": "success", "message": "Email sent successfully"}
        except Exception as e:
            return str(e)

    @staticmethod
    def send_email_notification_test(recipients: list[str], subject: str):
        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            message = Mail(from_email="noreply@beplus.com.mx", subject=subject)

            personalization = Personalization()
            for recipient in recipients:
                personalization.add_to(Email(recipient))

            message.add_personalization(personalization)
            # Añadir contenido de texto plano
            message.add_content(Content("text/plain", subject))
            # Añadir contenido HTML
            message.add_content(Content("text/html", subject))
            sg.send(message)
            return {"status": "success", "message": "Email sent successfully"}
        except Exception as e:
            return e

    @staticmethod
    def send_whatsapp_notification(recipients: List[str], message: str) -> Union[bool, str]:
        try:
            account_sid = settings.TWILIO_ACCOUNT_SID
            auth_token = settings.TWILIO_AUTH_TOKEN
            client = Client(account_sid, auth_token)
            for recipient in recipients:
                message = client.messages.create(
                    body=message,
                    from_='whatsapp:+14155238886',
                    to=f'whatsapp:{recipient}'
                )
            return True
        except Exception as e:
            return str(e)
