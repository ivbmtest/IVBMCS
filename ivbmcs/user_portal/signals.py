from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
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