
from . tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import EmailMessage

def send_mail(user,domain):
    token = account_activation_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    link = reverse('activate',kwargs={'uid':uid,'token':token})
    activate_url = f"http://{domain}{link}"


    email_subject = "Activate your account"
    email_body = f"Hi {user.username},\n\nplease verify your email by clicking this link:\n{activate_url}"
    email = EmailMessage(email_subject,email_body,to=[user.email])
    email.send()