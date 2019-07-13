from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=224, required=True, help_text='Professional email address.')
    first_name = forms.CharField(max_length=50, required=True, help_text='Enter your first name')
    last_name = forms.CharField(max_length=50, required=True, help_text='Enter your last name')
    mobile = forms.CharField(max_length=10, min_length=10, required=True, help_text='Enter your valid mobile number')
    domain = forms.CharField(max_length=50, required=True, help_text='Enter your domain linked with email address')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'mobile', 'domain', 'password1', 'password2')
    
    def clean_domain(self):
        domain = self.cleaned_data['domain']
        domain = domain.replace("http://", "").replace("https://", "").replace("www.", "")
        return domain