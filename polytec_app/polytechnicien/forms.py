from django import forms
from .models import Resource, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'file']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError("Le message doit comporter au moins 10 caractères.")
        return message
    

from django.contrib.auth import get_user_model

User = get_user_model()
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser  # ou User si tu n’utilises pas encore CustomUser
        fields = ['username', 'password1', 'password2']


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
###############
"""class EmailUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'votre@email.com',
            'id': 'id_email'  # Ajouté pour correspondre au template
        })
    )
    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")
        return email
    """
#########7atitha tawa 

#############jebtou men views
"""class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user"""


User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    # Tu peux personnaliser le champ username si tu veux un placeholder :
    username = forms.CharField(
        label="Email",
        max_length=150,

    )

    class Meta:
        model = User
        # On ne garde plus l'email : 
        fields = ['username', 'password1', 'password2']

from .models import Course

class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['subject', 'year', 'title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }