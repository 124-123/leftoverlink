from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth import get_user_model
import json
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_naive, make_aware
from decimal import Decimal, InvalidOperation
from .models import FoodPost, Donation,Notification, CustomUser,UserProfile,Category,Profile, NGOVerificationRequest,NGOProfile
from django.utils import timezone
from django.contrib.auth.forms import PasswordChangeForm
from datetime import datetime
from django.contrib.auth import update_session_auth_hash
User = get_user_model()


def landingpage(request):
     return render(request,'landingpage.html')

def Navbar(request):
     return render(request,'navbar.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '').strip()
        password2 = request.POST.get('password2', '').strip()
        user_type = request.POST.get('user_type', '').strip()

        if not username or not email or not password1 or not password2 or not user_type:
            messages.error(request, "All fields are required.")
            return redirect('signup')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('signup')

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password1,
            user_type=user_type,
        )
        messages.success(request, "Account created successfully. Please sign in.")
        return redirect('signin')

    return render(request, 'signup.html')

def signin_view(request):
 if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect_user_dashboard(user)
    else:
        error_message = "Invalid username or password"
        return render(request, 'signin.html', {'error': error_message})
 else:
     return render(request, 'signin.html')

def signout_view(request):
    logout(request)
    return redirect('landingpage')

def redirect_user_dashboard(user):
    if user.user_type == 'donor':
        return redirect('donor')
    elif user.user_type == 'ngo':
        return redirect('ngo_verification')
    elif user.user_type == 'receiver':
        return redirect('receiver_dashboard')
    else:
        return redirect('/')


def aboutus(request):
       return render(request,'aboutus.html')

@login_required
def ngo_verification_request(request):
  
    verification_record = NGOVerificationRequest.objects.filter(user=request.user).first()
    if verification_record and verification_record.is_verified:
        return redirect('ngo') 

    if request.method == 'POST':
        ngo_name = request.POST.get('ngo_name', '').strip()
        registration_number = request.POST.get('registration_number', '').strip()
        date_of_registration = request.POST.get('date_of_registration', '').strip()
        address = request.POST.get('address', '').strip()
        contact_person = request.POST.get('contact_person', '').strip()
        contact_email = request.POST.get('contact_email', '').strip()
        contact_phone = request.POST.get('contact_phone', '').strip()

     
        registration_certificate = request.FILES.get('registration_certificate') or (verification_record.registration_certificate if verification_record else None)
        certificate_80g = request.FILES.get('certificate_80g') or (verification_record.certificate_80g if verification_record else None)
        certificate_12a = request.FILES.get('certificate_12a') or (verification_record.certificate_12a if verification_record else None)
        pan_card = request.FILES.get('pan_card') or (verification_record.pan_card if verification_record else None)
        aadhaar_card = request.FILES.get('aadhaar_card') or (verification_record.aadhaar_card if verification_record else None)
        annual_report = request.FILES.get('annual_report') or (verification_record.annual_report if verification_record else None)
        bank_statement = request.FILES.get('bank_statement') or (verification_record.bank_statement if verification_record else None)

     
        if not all([ngo_name, registration_number, date_of_registration, contact_email, contact_phone]):
            messages.error(request, "Please fill all required fields.")
            return render(request, 'ngo_verification_form.html', {
                'data': request.POST,
                'existing': verification_record
            })

        try:
            parsed_date = datetime.strptime(date_of_registration, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format. Use YYYY-MM-DD.")
            return render(request, 'ngo_verification_form.html', {
                'data': request.POST,
                'existing': verification_record
            })

       
        verification = verification_record or NGOVerificationRequest(user=request.user)
        verification.ngo_name = ngo_name
        verification.registration_number = registration_number
        verification.date_of_registration = parsed_date
        verification.address = address
        verification.contact_person = contact_person
        verification.contact_email = contact_email
        verification.contact_phone = contact_phone
        verification.registration_certificate = registration_certificate
        verification.certificate_80g = certificate_80g
        verification.certificate_12a = certificate_12a
        verification.pan_card = pan_card
        verification.aadhaar_card = aadhaar_card
        verification.annual_report = annual_report
        verification.bank_statement = bank_statement
        verification.is_verified = False
        verification.save()

        messages.success(request, "NGO verification request submitted. We'll review and contact you.")
        return redirect('verification_success')

    return render(request, 'ngo_verification_form.html', {
        'existing': verification_record,
        'data': None
    })

@login_required
def verification_success(request):
    return render(request, 'verification_success.html')

@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user) 

    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name')
        request.user.email = request.POST.get('email')
        profile.phone_number = request.POST.get('phone_number')
        profile.address = request.POST.get('address')

        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']

        request.user.save()
        profile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')

    return render(request, 'profile.html', {'profile': profile})

def dashboard_view(request):
    listings_chart = {
        "labels": ["Jan", "Feb", "Mar"], 
        "data": [5, 10, 8]
    }
    donations_chart = {
        "labels": ["Mon", "Tue", "Wed"],
        "data": [3, 4, 2]
    }

    return render(request, "admin/dashboard.html", {
        "listings_chart_json": json.dumps(listings_chart),
        "donations_chart_json": json.dumps(donations_chart),
    })

def food_post(request):
    if request.method == 'POST':
        food_title = request.POST.get('food_title')
        quantity = request.POST.get('quantity')
        category_id = request.POST.get('category')
        contact = request.POST.get('contact')
        expiry = request.POST.get('expiry')
        food_image = request.FILES.get('food_image')
        latitude = request.POST.get('latitude', None)
        longitude = request.POST.get('longitude', None)
        location = request.POST.get('location', '')

        try:
            quantity = Decimal(quantity)
        except (InvalidOperation, TypeError):
            messages.error(request, "Please enter a valid quantity.")
            return redirect('food_post')

        try:
            latitude = float(latitude) if latitude else None
            longitude = float(longitude) if longitude else None
        except ValueError:
            latitude = None
            longitude = None

        expiry = parse_datetime(expiry)
        if expiry and is_naive(expiry):
            expiry = make_aware(expiry)

        if not all([food_title, quantity, category_id, contact, expiry, food_image]):
            messages.error(request, "All fields are required.")
            return redirect('food_post')

        category = Category.objects.filter(id=category_id).first()
        if not category:
            messages.error(request, "Invalid category selected.")
            return redirect('food_post')

        FoodPost.objects.create(
            food_title=food_title,
            quantity=quantity,
            category=category,
            contact=contact,
            expiry=expiry,
            food_image=food_image,
            latitude=latitude,
            longitude=longitude,
            location=location,
            donor=request.user,
        )


        messages.success(request, "Food post created successfully!")
        return redirect('donor')

    categories = Category.objects.all()
    return render(request, 'food_post.html', {'categories': categories})


def food_list(request):

    posts = FoodPost.objects.filter(status="available")

    categories = request.GET.getlist("category")
    if categories:
        posts = posts.filter(category__id__in=categories)

    status = request.GET.getlist("status")
    if status:
        posts = posts.filter(status__in=status)

    sort = request.GET.get("sort")
    if sort == "newest":
        posts = posts.order_by("-id")
    elif sort == "popular":
        posts = posts.order_by("?")

    for post in posts:
        if post.is_expired():
            post.status = "expired"
            post.save()

    posts = posts.filter(status="available")

    food_posts_json = json.dumps([
        {
            "id": post.id,
            "food_title": post.food_title,
            "quantity": float(post.quantity),
            "category": post.category.name if post.category else "",
            "status": post.status,
            "expiry": post.expiry.strftime("%Y-%m-%d %H:%M") if post.expiry else "",
            "latitude": post.latitude,
            "longitude": post.longitude,
            "location": post.location,
            "food_image_url": post.food_image.url if post.food_image else "",
        }
        for post in posts
    ])
    print(food_posts_json)
    return render(request, "food_list.html", {
        "posts": posts,
        "food_posts_json": food_posts_json,
    })

@login_required
def realtimedash(request):

    food_posted_data = [5, 15, 30, 60, 100, 150, 250]

    meals_saved_data = [20, 150, 180, 250, 350, 500, 650, 750, 900, 1050]
   
    contribution_data = {
        'labels': ['Contributions', 'Donations', 'Other'],
        'values': [45, 35, 20],
        'colors': ['#2c6ef7', '#3cb043', '#80deea'],
    }

    impact_percentage = 25.4

    context = {
        'food_posted_data': food_posted_data,
        'meals_saved_data': meals_saved_data,
        'contribution_data': contribution_data,
        'impact_percentage': impact_percentage,
    }
    return render(request, "realtimedash.html", context)

@login_required
def settings_view(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        password_form = PasswordChangeForm(user, request.POST)
        if 'change_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  
                messages.success(request, "Password updated successfully.")
                return redirect('settings')
            else:
                messages.error(request, "Please correct the errors in the password form.")
    else:
        password_form = PasswordChangeForm(user)

    context = {
        'password_form': password_form,
    }
    return render(request, 'settings.html', context)

@login_required
def donor(request):
    user = request.user

    active_listings = FoodPost.objects.filter(
        donor=user,
        status='available',
        expiry__gt=timezone.now()
    ).order_by('-expiry')

    donation_history = Donation.objects.filter(
        donor=user
    ).order_by('-date_donated')

    context = {
        'active_listings': active_listings,
        'donation_history': donation_history,
    }
    return render(request, 'donor.html', context)

@login_required
def claim_food_post(request, post_id):
    food_post = get_object_or_404(FoodPost, id=post_id)
    if food_post.status != 'available':
        messages.error(request, "This food post is no longer available.")
        return redirect('food_list')

    food_post.status = 'claimed'
    food_post.save()

    Donation.objects.create(
        food_post=food_post,
        donor=food_post.donor,
        recipient_name=request.user.username,
        status='pending',
    )
    messages.success(request, "You have claimed this food post successfully.")
    user_type = request.user.user_type
    if user_type == 'ngo':
        return redirect('ngo')
    elif user_type == 'receiver':
        return redirect('receiver_dashboard')
    else:
        return redirect('food_list')

@login_required
def receiver_dashboard(request):
    available_foods = FoodPost.objects.filter(status='available').order_by('-expiry')

    request_history = Donation.objects.filter(recipient_name=request.user.username).order_by('-date_donated')

    context = {
        'available_foods': available_foods,
        'request_history': request_history,
    }
    return render(request, 'receiver_dashboard.html', context)

@login_required
def mark_donation_completed(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)

    if request.user != donation.donor and request.user.username != donation.recipient_name:
        messages.error(request, "You don't have permission to update this donation.")
        return redirect('donor') 

    donation.status = 'completed'
    donation.save()

    food_post = donation.food_post
    food_post.status = 'expired'  
    food_post.save()

    messages.success(request, f"Donation '{donation.food_post.food_title}' marked as completed.")

    user_type = request.user.user_type
    if user_type == 'donor':
        return redirect('donor')
    elif user_type == 'ngo':
        return redirect('ngo')
    elif user_type == 'receiver':
        return redirect('receiver_dashboard')
    else:
        return redirect('food_list')

@login_required
def notifications_page(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': notifications})

@login_required
def mark_as_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications')

def send_notification(user, message):
    Notification.objects.create(user=user, message=message)

from django.shortcuts import get_object_or_404, redirect
from .models import NGOProfile, CustomUser

def verify_ngo(request, ngo_id):
    ngo_user = get_object_or_404(CustomUser, id=ngo_id) 
    ngo_profile, created = NGOProfile.objects.get_or_create(user=ngo_user)
    ngo_profile.is_verified = True
    ngo_profile.save()
    return redirect('ngo') 

@login_required
def ngo(request):
    if request.user.user_type != 'ngo':
        return render(request, "403.html", status=403)

    total_donations_received = Donation.objects.filter(
        recipient_name=request.user.username
    ).count()

    active_food_posts = FoodPost.objects.filter(
        status='available'
    ).count()

    donors_connected = Donation.objects.filter(
        recipient_name=request.user.username
    ).values('donor').distinct().count()

    recent_activity = Donation.objects.filter(
        recipient_name=request.user.username
    ).order_by('-date_donated')[:10]

    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]
    ngo_profile, created = NGOProfile.objects.get_or_create(user=request.user)
    ngo_profile.is_verified = True
    ngo_profile.save()

    ngo_profile = NGOVerificationRequest.objects.filter(user=request.user).first()
    context = {
        'total_donations_received': total_donations_received,
        'active_food_posts': active_food_posts,
        'donors_connected': donors_connected,
        'recent_activity': recent_activity,
        'notifications': notifications,
        'ngo_profile': ngo_profile
    }
    return render(request, "ngo.html", context)



