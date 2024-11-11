from django.contrib import messages, auth
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from accounts.models import CustomUser, UserProfile
from accounts.forms import CustomUserCreationForm, UserProfileForm, LoginForm
from .token import user_tokenizer_generate  # Custom token generator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


# User Registration View
def register(request):
    form = CustomUserCreationForm()
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Inactive until email verification
            user.save()

            # Email verification
            current_site = get_current_site(request)
            subject = 'Activate Your Luxe Essence Account'
            timestamp = timezone.now().timestamp()
            message = render_to_string('accounts/registration/email_verification.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user),
                'timestamp': timestamp,
                 'verification_url': reverse('email_verification', args=[urlsafe_base64_encode(force_bytes(user.pk)), user_tokenizer_generate.make_token(user)]),
            })

            email = EmailMessage(subject, message, to=[user.email])
            email.content_subtype = "html"  # Send as HTML
            email.send()

            return redirect('email_verification_sent')
    
    context = {'form': form}
    return render(request, 'accounts/registration/register.html', context)

# Email Verification Views
def email_verification(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    timestamp = request.GET.get('timestamp', timezone.now().timestamp())
    if user and user_tokenizer_generate.check_token(user, token):
        if not user_tokenizer_generate.is_token_expired(float(timestamp)):
            user.is_active = True
            user.save()
            return redirect('email_verification_success')
        else:
            return redirect('email_verification_expired')
    else:
        return redirect('email_verification_failed')

def email_verification_sent(request):
    return render(request, 'accounts/registration/email_verification_sent.html')

def email_verification_success(request):
    return render(request, 'accounts/registration/email_verification_success.html')

def email_verification_failed(request):
    return render(request, 'accounts/registration/email_verification_failed.html')

def email_verification_expired(request):
    return render(request, 'accounts/registration/email_verification_expired.html')

def resend_verification_link(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            if not user.is_active:
                current_site = get_current_site(request)
                subject = 'Resend Account Verification Email'
                timestamp = timezone.now().timestamp()
                message = render_to_string('accounts/registration/email_verification.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': user_tokenizer_generate.make_token(user),
                    'timestamp': timestamp,
                })

                email_message = EmailMessage(subject, message, to=[user.email])
                email_message.content_subtype = "html"
                email_message.send()

                return redirect('email_verification_sent')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Email not registered.')
            return redirect('resend_verification_link')
    return render(request, 'accounts/registration/resend_verification_link.html')

# Login View
def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user and user.is_active:
                auth_login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Account inactive. Please verify your email.')
                return redirect('resend_verification_link')
    return render(request, 'accounts/login.html', {'form': form})

# Logout View
@login_required(login_url='login')
def logout(request):
    auth_logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('blog:blog_list')

# Password Reset Views
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            current_site = get_current_site(request)
            
            # Load email subject from template
            mail_subject = render_to_string('accounts/password/password_reset_subject.txt').strip()
            
            message = render_to_string('accounts/password/password_reset_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            
            email_message = EmailMessage(mail_subject, message, to=[email])
            email_message.content_subtype = "html"  # Send as HTML
            email_message.send()
            
            messages.success(request, 'Password reset email sent!')
            return redirect('login')
        else:
            messages.error(request, 'No account found with that email.')
    return render(request, 'accounts/password/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Reset your password.')
        return redirect('reset_password')
    else:
        messages.error(request, 'Invalid link. Please try again.')
        return redirect('login')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            uid = request.session.get('uid')
            user = CustomUser.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful!')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
    return render(request, 'accounts/password/password_reset_confirm.html')




# Password Reset Complete View
def password_reset_complete(request):
    messages.success(request, 'Your password has been reset successfully!')
    return render(request, 'accounts/password/password_reset_complete.html')



@login_required(login_url='login')
def delete_account(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        messages.error(request, "Account deleted.")
        return redirect('blog')
    return render(request, 'accounts/delete_account.html')



# Profile Management and Account Deletion
@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

@login_required(login_url='login')
def edit_profile(request):
    user_form = UserProfileForm(instance=request.user)
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Profile updated.")
            return redirect('dashboard')
    return render(request, 'accounts/edit_profile.html', {'user_form': user_form})
