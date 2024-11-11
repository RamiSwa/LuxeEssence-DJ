# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser, UserProfile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['skin_type', 'skin_concerns', 'favorite_products', 'bio', 'profile_picture', 'address_line_1', 'address_line_2', 'city', 'state', 'country', 'preferred_appointment_times']
        
        

# LoginForm for user authentication
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))