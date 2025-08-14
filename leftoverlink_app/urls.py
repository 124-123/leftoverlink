from django.urls import path
from leftoverlink_app import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

    path('',views.landingpage,name='landingpage'),
    path('navbar/',views.Navbar,name='navbar'),
    path('aboutus/',views.aboutus,name='aboutus'),
    path('food_post/',views.food_post,name='food_post'),
    path('donor/',views.donor,name='donor'),
    path('ngo/',views.ngo,name='ngo'),
    path('receiver/dashboard/', views.receiver_dashboard, name='receiver_dashboard'),
    path('realtimedashboard/',views.realtimedash,name='realtimedash'),
    path('food_list/', views.food_list, name='food_list'),
    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.signin_view, name='signin'),
    path('logout/', views.signout_view, name='logout'),
    path('dashboard/', views.redirect_user_dashboard, name='dashboard_redirect'),
    path('ngo-verification/', views.ngo_verification_request, name='ngo_verification'),
    path('verification-success/', views.verification_success, name='verification_success'),
    path('profile/', views.profile_view, name='profile'),
    path('food/claim/<int:post_id>/', views.claim_food_post, name='claim_food'),
    path('settings/',views.settings_view, name='settings'),
    path('donation/<int:donation_id>/complete/', views.mark_donation_completed, name='mark_donation_completed'),
    path('notifications/', views.notifications_page, name='notifications'),
    path('notifications/read/<int:pk>/', views.mark_as_read, name='mark_as_read'),

 ]
if settings.DEBUG:
 urlpatterns+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

