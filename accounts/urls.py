from django.urls import path
from . import views

urlpatterns = [
    # User Registration
    path('register/', views.register, name='register'),
    
    # Email Verification
    path('activate/<uidb64>/<token>/', views.email_verification, name='email_verification'),  # Updated path
    path('email_verification/<uidb64>/<token>/', views.email_verification, name='email_verification'),
    path('email_verification_sent/', views.email_verification_sent, name='email_verification_sent'),
    path('email_verification_success/', views.email_verification_success, name='email_verification_success'),
    path('email_verification_failed/', views.email_verification_failed, name='email_verification_failed'),
    path('email_verification_expired/', views.email_verification_expired, name='email_verification_expired'),
    path('resend_verification_link/', views.resend_verification_link, name='resend_verification_link'),
    
    # Login & Logout
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    
    # Password Reset
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('accounts/reset_password_complete/', views.password_reset_complete, name='password_reset_complete'),

    
    # Profile Management & Account Deletion
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile_management/', views.edit_profile, name='edit_profile'),
    path('delete_account/', views.delete_account, name='delete_account'),
]
