#SEB : ce fichier additionnel dans l'app sert à personnaliser et étendre les fonctionnalités sécurisés de Django concernant les données Users

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile
import re #pour valider les données saisies par l'utilisateur dans kes classes "clean_..."
from django.contrib.auth.forms import PasswordChangeForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    adresse = forms.CharField(max_length=255, required=True)
    telephone = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if not re.match(r'^\+?\d{10,15}$', telephone):
            raise forms.ValidationError("Veuillez entrer un numéro de téléphone valide (10 à 15 chiffres).")
        return telephone

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match(r"^[a-zA-Zéèêëàâôï\s\-'']+$", first_name): #autorise aussi les - et ' en plus de toutes les lettres et les espaces (\s)
            raise forms.ValidationError("Le prénom ne doit contenir que des lettres.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match(r"^[a-zA-Zéèêëàâôï\s\-'']+$", last_name):
            raise forms.ValidationError("Le nom ne doit contenir que des lettres.")
        return last_name

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

# Formulaire de MAJ des infos perso de l'utilisateur (celle prévue par Django):
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match(r"^[a-zA-Zéèêëàâôï\s\-'']+$", first_name): #autorise aussi les - et ' en plus de toutes les lettres
            raise forms.ValidationError("Le prénom ne doit contenir que des lettres.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match(r"^[a-zA-Zéèêëàâôï\s\-'']+$", last_name):
            raise forms.ValidationError("Le nom ne doit contenir que des lettres.")
        return last_name

# Formulaire pour la MAJ des infos perso "étendues" :
class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['adresse', 'telephone']
    
    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if not re.match(r'^\+?\d{10,15}$', telephone):
            raise forms.ValidationError("Veuillez entrer un numéro de téléphone valide (10 à 15 chiffres).")
        return telephone

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

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Pour définir un nouveau mot de passe, saisissez ici votre ancien mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ancien mot de passe'}),
    )
    new_password1 = forms.CharField(
        label="Saisissez ensuite ici votre nouveau mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nouveau mot de passe'}),
    )
    new_password2 = forms.CharField(
        label="Enfin, confirmer ici votre nouveau mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmer le nouveau mot de passe'}),
    )


