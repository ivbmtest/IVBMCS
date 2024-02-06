import pyotp
from datetime import datetime,timedelta
import re
from twilio.rest import Client
from django.core.mail import send_mail




def check_phone_number(data):
    phone_pattern = re.compile(r'^\+\d+$')
    match = phone_pattern.fullmatch(data)
    return bool(match)

def send_otp_number(request,data):
    totp = pyotp.TOTP(pyotp.random_base32(),interval = 60)
    otp = totp.now()
    print(data)
    account_sid = 'ACea07b1ac009276f9122f2b841e54145d'
    auth_token = '1350b9e7e96c56e0e1ec3de66f834c1f'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    from_='+12564745625',
    body=str(otp),
    to=data
    )
    print(message.sid)
    request.session['otp_secret_key'] = totp.secret
    validate_otp = datetime.now() + timedelta(minutes=1)
    request.session['validate_otp'] = str(validate_otp)
    print("your otp is here : ",otp)


def check_email(data):
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    match = email_pattern.search(data)
    print(match)
    return bool(match)

def send_otp_email(request,data):
    totp = pyotp.TOTP(pyotp.random_base32(),interval = 60)
    otp = totp.now()
    subject = 'Ivbmcs otp'
    message = f' OTP : {str(otp)}'
    from_email = 'testnft400@gmail.com'  # Replace with your Gmail email
    recipient_list = [data]  # Replace with the recipient's email

    send_mail(subject, message, from_email, recipient_list)

    
    request.session['otp_secret_key'] = totp.secret
    validate_otp = datetime.now() + timedelta(minutes=1)
    request.session['validate_otp'] = str(validate_otp)
    print("your otp is here : ",otp)