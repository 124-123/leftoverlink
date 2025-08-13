from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib import admin
from django.utils import timezone
from django.utils.timezone import make_aware
from django.conf import settings
# Create your models here.


class FoodPost(models.Model):
    CATEGORY_CHOICES = [
        ('fruits', 'Fruits'),
        ('vegetables', 'Vegetables'),
        ('canned', 'Canned Goods'),
        ('snacks', 'Snacks'),
    ]
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('claimed', 'Claimed'),
        ('expired', 'Expired'),
    ]

    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    food_title = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    contact = models.CharField(max_length=15, default='N/A')
    expiry = models.DateTimeField(null=True, blank=True)
    food_image = models.ImageField(upload_to="food_images/")
    location = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    def is_expired(self):
        if self.expiry is None:
            return False  
        return timezone.now() > self.expiry

    def save(self, *args, **kwargs):
       
        if self.latitude == '':
            self.latitude = None
        if self.longitude == '':
            self.longitude = None

        if isinstance(self.expiry, str):
            from django.utils.dateparse import parse_datetime
            self.expiry = parse_datetime(self.expiry)
        if self.expiry and timezone.is_naive(self.expiry):
            self.expiry = make_aware(self.expiry)

        if self.is_expired() and self.status != 'expired':
            self.status = 'expired'

        super().save(*args, **kwargs)


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('donor', 'Donor'),
        ('ngo', 'NGO'),
        ('receiver', 'Receiver'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return self.username

class NGOVerificationRequest(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ngo_name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=100)
    date_of_registration = models.DateField()
    address = models.TextField()
    contact_person = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)

    registration_certificate = models.FileField(upload_to='ngo_docs/registration/')
    certificate_80g = models.FileField(upload_to='ngo_docs/80g/', blank=True, null=True)
    certificate_12a = models.FileField(upload_to='ngo_docs/12a/', blank=True, null=True)
    pan_card = models.FileField(upload_to='ngo_docs/pan/')
    aadhaar_card = models.FileField(upload_to='ngo_docs/aadhaar/')
    annual_report = models.FileField(upload_to='ngo_docs/annual_report/', blank=True, null=True)
    bank_statement = models.FileField(upload_to='ngo_docs/bank_statement/')

    submitted_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.ngo_name} ({self.user.username})"

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="my_profile")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username

    def __str__(self):
        return self.site_name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    receive_notifications = models.BooleanField(default=True)
    preferred_language = models.CharField(max_length=20, default='en')
    dark_mode = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.username}'s profile"


class Donation(models.Model):
    food_post = models.ForeignKey(FoodPost, on_delete=models.CASCADE)
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    recipient_name = models.CharField(max_length=100)
    date_donated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')

    def __str__(self):
        return f"Donation of {self.food_post.food_title} to {self.recipient_name}"
    

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message[:20]}"

class NGOProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)  

    def __str__(self):
        return self.user.username
