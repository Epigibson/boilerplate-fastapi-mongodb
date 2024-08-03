from fastapi import HTTPException, APIRouter
from schemas.notifications_schema import NotificationCreate
from services.send_notification_services import SendNotificationService

notification_router = APIRouter()


@notification_router.post('/send_notification_email', summary="Send notification", tags=["Notification"])
async def send_notification_email(dynamic_recipient: str,
                                  dynamic_action: str,
                                  dynamic_amount: str,
                                  dynamic_date: str,
                                  dynamic_greeting: str):
    # Send email notification
    result = SendNotificationService.send_email_notification(
        ["hackminor@live.com.mx"],
        "Notificacion",
        dynamic_recipient,
        dynamic_action,
        dynamic_amount,
        dynamic_date,
        dynamic_greeting
    )
    if not result:
        raise HTTPException(status_code=500, detail="Failed to send email notification")

    return {"message": "Notification sent successfully"}


@notification_router.post('/send_notification_email/test', summary="Send notification test", tags=["Notification"])
async def send_notification_email_test(recipients: list[str], subject: str):
    result = SendNotificationService.send_email_notification_test(recipients, subject)
    return result


@notification_router.post('/send_notification_whatsapp', summary="Send notification", tags=["Notification"])
async def send_notification_whats(notification: NotificationCreate):
    recipients = notification.recipients
    body = notification.message

    # Send email notification
    result = SendNotificationService.send_whatsapp_notification(recipients, body)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to send email notification")

    return {"message": "Notification sent successfully"}
