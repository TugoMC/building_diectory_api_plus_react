# authapp/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import UserProfile
import re

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_photo', 'last_name', 'first_name', 'phone_number', 'profession', 'city', 'commune']
        labels = {
            'profile_photo': 'Photo de profil',
            'last_name': 'Nom',
            'first_name': 'Prénom',
            'phone_number': 'Numéro de téléphone',
            'profession': 'Profession',
            'city': 'Ville',
            'commune': 'Commune',
        }
        widgets = {
            'profile_photo': forms.FileInput(attrs={'class': 'form-control-file'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '+225', 'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'commune': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        
        # Supprimer tous les espaces dans le numéro de téléphone
        phone_number = phone_number.replace(' ', '')
        
        # Vérifier le format du numéro de téléphone
        if not re.match(r'^\+?\d+$', phone_number):
            raise forms.ValidationError("Le numéro de téléphone ne doit contenir que des chiffres")
        
        # Vérifier et ajouter l'indicatif +225 si nécessaire
        if not phone_number.startswith('+'):
            phone_number = '+225' + phone_number
        elif not phone_number.startswith('+225'):
            phone_number = '+225' + phone_number[1:]
        
        # Vérifier la longueur du numéro de téléphone
        if len(phone_number) < 10:
            raise forms.ValidationError("Le numéro de téléphone doit contenir au moins 10 caractères, incluant l'indicatif '+225'.")
        
        return phone_number
    

    def clean_profile_photo(self):
        profile_photo = self.cleaned_data.get('profile_photo')
        if profile_photo:
            if profile_photo.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("L'image est trop grande. La taille maximale est de 5MB.")
        return profile_photo
    
    
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Mot de passe actuel'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nouveau mot de passe'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmer le nouveau mot de passe'})

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']