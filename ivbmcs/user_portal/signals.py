from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string

# Signal handler for post_save on user_service_details
@receiver(post_save, sender=user_service_details)
def update_notifications(sender, instance, created, **kwargs):
    print("-------------------entered")
    if created:  # Only consider new instances
        # Assuming you have a logic to determine when to create a notification
        if instance.taken_by and instance.status:
            # Create a new notification for the user
            user_notification.objects.create(
                recepient=instance.user_id,
                service=instance.service,
                message=f"Service status changed to '{instance.status}' and taken by '{instance.taken_by}'.",
            )
        # You can add additional conditions or logic as needed
    else:
        # Assuming you want to update the notification when existing instances are updated
        notification = user_notification.objects.filter(recepient=instance.user_id).first()
        if notification:
            notification.message = f"Service status changed to '{instance.status}' and taken by '{instance.taken_by}'."
            notification.save()


@receiver(post_save, sender=user_notification)
def send_notification(sender, instance ,created,**kwargs):
    print("Signal is  working:",instance.recepient.first_name)
    if created:
        subject = 'Your Sevice has started'
        html_content = render_to_string('admin/super_user/user_email_template.html', {'username': instance})
        text_content = strip_tags(html_content)  # Strip HTML tags for the plain text version
        sender_email = 'your@email.com'  # Replace with your email
        recipient_email = [instance.recepient.email]
        print("ready to send----",recipient_email)
        send_mail(subject, '', "testnft400@gmail.com", recipient_email, html_message=html_content)
        print("sucess send user")
        print("instance id ",instance.sender)
        #a = user_service_details.objects.filter(user=instance.recepient,service)
        
        if instance.sender != '':
            print("sending staff")
            subject = 'Your Task Was Assigned'
            html_content = render_to_string('admin/super_user/staff_email_template.html', {'username': instance})
            text_content = strip_tags(html_content)  # Strip HTML tags for the plain text version
            sender_email = 'your@email.com'  # Replace with your email
            recipient_email = [instance.sender]
            print("ready to send----",recipient_email)
            send_mail(subject, '', "testnft400@gmail.com", recipient_email, html_message=html_content)
            print("sucess send staff")
        # msg = EmailMultiAlternatives(subject, text_content, sender_email, [recipient_email])
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()