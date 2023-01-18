import os
from twilio.rest import Client
from google_sheets import GoogleSheets

account_sid = YOUR_ACCCOUNT_SID
auth_token = YOUR_AUTH_TOKEN

data_manager = GoogleSheets(url=os.getenv("SHEETS_URL"))


class Sms:
    def __init__(self):
        self.data = data_manager.get_data()

    def send_sms(self, message):
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=message,
            from_=YOUR_TWILIO_NUMBER
            to=YOUR_NUMBER
        )

        print(message.sid)
