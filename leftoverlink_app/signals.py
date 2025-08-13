from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FoodPost, Donation,CustomUser, Notification

@receiver(post_save, sender=FoodPost)
def create_donation_on_claim(sender, instance, created, **kwargs):
    if not created and instance.status == 'claimed':
        # Check if Donation already exists for this FoodPost to avoid duplicates
        if not Donation.objects.filter(food_post=instance).exists():
            Donation.objects.create(
                food_post=instance,
                donor=instance.donor,
                recipient_name='Recipient not set',  
                status='pending'
            )

@receiver(post_save, sender=FoodPost)
def notify_ngos_on_new_food(sender, instance, created, **kwargs):
    if created:
        ngos = CustomUser.objects.filter(user_type='ngo')
        for ngo in ngos:
            Notification.objects.create(
                user=ngo,
                message=f"New food post: {instance.food_title} by {instance.donor.username}"
            )
