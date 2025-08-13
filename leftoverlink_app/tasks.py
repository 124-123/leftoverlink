from celery import shared_task
from django.utils import timezone
from .models import FoodPost

@shared_task
def mark_expired_posts():
    now = timezone.now()
    expired = FoodPost.objects.filter(expiry_time__lt=now, status='active')
    expired_count = expired.update(status='expired')
    return f"{expired_count} posts marked as expired"
