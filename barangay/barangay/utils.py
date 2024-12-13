from twilio.rest import Client
from django.conf import settings

def send_sms(to, message):
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        # Send SMS
        message = client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to  # Must be in international format
        )

        print(f"SMS sent successfully. SID: {message.sid}")
        return True

    except Exception as e:
        print(f"Failed to send SMS: {e}")
        return False
