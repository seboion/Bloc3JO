#SEB : ce fichier additionnel dans l'app sert à personnaliser et étendre les fonctionnalités sécurisés de Django concernant les données Users

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    adresse = forms.CharField(max_length=255, required=True)
    telephone = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            # Enregistrer le profil avec les informations supplémentaires
            Profile.objects.create(
                user=user,
                adresse=self.cleaned_data['adresse'],
                telephone=self.cleaned_data['telephone']
            )
        return user

# Formulaire de MAJ des info perso de l'utilisateur (cele prévu par Django):
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

# Formulaire pour la MAJ des info perso "étendues" :
class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['adresse', 'telephone']

# Personnalisation de l'affichage du login de Django
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d\'utilisateur'}),
        required=True
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}),
        required=True
    )

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
