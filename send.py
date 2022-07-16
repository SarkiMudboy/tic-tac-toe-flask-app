import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'ACa2123f89b89ef147f5cfe42f19e2012f'
auth_token = '122d72a371fdf4c4d8fb70356849ea52'
client = Client(account_sid, auth_token)

message = client.messages.create(
                              body='Hello there!',
                              from_='whatsapp:+14155238886',
                              to='whatsapp:+2348156040455'
                          )

print(message.sid)