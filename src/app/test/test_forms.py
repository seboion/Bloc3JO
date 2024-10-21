from django.test import TestCase
from app.forms import CustomUserCreationForm
from django.contrib.auth.models import User
from app.models import Profile

from django.test import TestCase
from app.forms import CustomUserCreationForm

class CustomUserCreationFormTest(TestCase): #Test de le formulaire de renseignement des infos personnelles

    form_data_OK = { #Ici que des données valides
        'username': 'testuser',
        'first_name': 'Sébastien',
        'last_name': 'Nom',
        'email': 'test@test.com',
        'password1': 'Mo2PasOk@!!',
        'password2': 'Mo2PasOk@!!',
        'adresse': '123 rue de Paris',
        'telephone': '0123456789'
    }

    form_data_OK2 = { #Ici aussi que des données valides mais variations (tirets espaces...)
        'username': 'testuser',
        'first_name': 'Sébastien',
        'last_name': 'De-Nom Composé',
        'email': 'test@test.com',
        'password1': 'Mo2PasOk@!!',
        'password2': 'Mo2PasOk@!!',
        'adresse': '123 rue de Paris',
        'telephone': '+33123456789'
}

    form_data_KO = { #saisies non OK
        'username': 'testuser',
        'first_name': 'Séb@stien!',
        'last_name': 'Nom%',
        'email': 'test.com',
        'password1': 'simple',
        'password2': 'simple',
        'adresse': '123 rue de Paris',
        'telephone': '789'
}
    form_data_vide = { #pas de saisie
        'username': '',
        'first_name': '',
        'last_name': '',
        'email': '',
        'password1': '',
        'password2': '',
        'adresse': '',
        'telephone': ''
}

    def test_clean_first_name_valid(self): # Cas où le prénom est valide

        form_data_OK = { #Ici que des données valides
        'username': 'testuser',
        'first_name': 'Sébastien',
        'last_name': 'Nom',
        'email': 'test@test.com',
        'password1': 'Mo2PasOk@!!',
        'password2': 'Mo2PasOk@!!',
        'adresse': '123 rue de Paris',
        'telephone': '0123456789'
    }
        
        form = CustomUserCreationForm(data=form_data_OK)
        self.assertTrue(form.is_valid())  # Le formulaire doit être valide
    
    def test_clean_first_name_invalid(self): # Cas où le prénom est invalide

        form_data_KO = { #saisies non OK
        'username': 'testuser',
        'first_name': 'Séb@stien!',
        'last_name': 'Nom%',
        'email': 'test.com',
        'password1': 'simple',
        'password2': 'simple',
        'adresse': '123 rue de Paris',
        'telephone': '789'
}

        form = CustomUserCreationForm(data=form_data_KO)
        self.assertFalse(form.is_valid())  # Le formulaire doit ne dois pas être valide
        self.assertIn('first_name', form.errors)  # Le formulaire doit renvoyer une erreur
        self.assertEqual(form.errors['first_name'], ["Le prénom ne doit contenir que des lettres."]) #vérifie que le form renvoi bien le message d'erreur

    def test_clean_first_name_tirets_espaces(self): # Cas où le prénom contient des espaces et des tirets (ce qui devrait etre valide)
        
        form_data_OK2 = { #Ici aussi que des données valides mais variations (tirets espaces...)
        'username': 'testuser',
        'first_name': "Sébastien - D'euxième",
        'last_name': 'DemComposé',
        'email': 'test@test.com',
        'password1': 'Mo2PasOk@!!',
        'password2': 'Mo2PasOk@!!',
        'adresse': '123 rue de Paris',
        'telephone': '+33123456789'
}

        form = CustomUserCreationForm(data=form_data_OK2)
        self.assertTrue(form.is_valid())  # Le formulaire doit être valide

    def test_clean_first_name_vide(self): # Cas où le prénom est vide (obligatoire)
        
        form_data_vide = { #pas de saisie
        'username': '',
        'first_name': '',
        'last_name': '',
        'email': '',
        'password1': '',
        'password2': '',
        'adresse': '',
        'telephone': ''
}

        form = CustomUserCreationForm(data=form_data_vide)
        self.assertFalse(form.is_valid())  # Le formulaire ne doit pas être valide
        self.assertIn('first_name', form.errors)  # Le champ first_name doit contenir des erreurs

#****************tests identiques pour le last_name******************

    def test_clean_last_name_valid(self): # Cas où le prénom est valide

        form_data_OK = { #Ici que des données valides
        'username': 'testuser',
        'first_name': 'Sébastien',
        'last_name': 'Nom',
        'email': 'test@test.com',
        'password1': 'Mo2PasOk@!!',
        'password2': 'Mo2PasOk@!!',
        'adresse': '123 rue de Paris',
        'telephone': '0123456789'
    }
        
        form = CustomUserCreationForm(data=form_data_OK)
        self.assertTrue(form.is_valid())  # Le formulaire doit être valide
    
    def test_clean_last_name_invalid(self): # Cas où le prénom est invalide

        form_data_KO = { #saisies non OK
        'username': 'testuser',
        'first_name': 'Séb@stien!',
        'last_name': 'Nom%',
        'email': 'test.com',
        'password1': 'simple',
        'password2': 'simple',
        'adresse': '123 rue de Paris',
        'telephone': '789'
}

        form = CustomUserCreationForm(data=form_data_KO)
        self.assertFalse(form.is_valid())  # Le formulaire doit ne dois pas être valide
        self.assertIn('last_name', form.errors)  # Le formulaire doit renvoyer une erreur
        self.assertEqual(form.errors['last_name'], ["Le nom ne doit contenir que des lettres."]) #vérifie que le form renvoi bien le message d'erreur

    def test_clean_last_name_tirets_espaces(self): # Cas où le prénom contient des espaces et des tirets (ce qui devrait etre valide)
        
        form_data_OK2 = { #Ici aussi que des données valides mais variations (tirets espaces...)
        'username': 'testuser',
        'first_name': "Sébastien - D'euxième",
        'last_name': 'DemComposé',
        'email': 'test@test.com',
        'password1': 'Mo2PasOk@!!',
        'password2': 'Mo2PasOk@!!',
        'adresse': '123 rue de Paris',
        'telephone': '+33123456789'
}

        form = CustomUserCreationForm(data=form_data_OK2)
        self.assertTrue(form.is_valid())  # Le formulaire doit être valide

    def test_clean_last_name_vide(self): # Cas où le prénom est vide (obligatoire)
        
        form_data_vide = { #pas de saisie
        'username': '',
        'first_name': '',
        'last_name': '',
        'email': '',
        'password1': '',
        'password2': '',
        'adresse': '',
        'telephone': ''
}

        form = CustomUserCreationForm(data=form_data_vide)
        self.assertFalse(form.is_valid())  # Le formulaire ne doit pas être valide
        self.assertIn('last_name', form.errors)  # Le champ first_name doit contenir des erreurs

    def test_save_profile(self):
        form = CustomUserCreationForm(data=self.form_data_OK)
        self.assertTrue(form.is_valid())  # Assure que le formulaire est valide
        user = form.save(commit=True)  # Enregistre l'utilisateur

        # Vérifie que l'utilisateur a bien été créé
        self.assertEqual(User.objects.count(), 1) # Vérifie qu'il y ait 1 user créé
        self.assertEqual(user.username, self.form_data_OK['username']) # Vérifie les données bien envoyées
        self.assertEqual(user.email, self.form_data_OK['email'])
        self.assertEqual(user.first_name, self.form_data_OK['first_name'])
        self.assertEqual(user.last_name, self.form_data_OK['last_name'])

        # Vérifie que le profil a bien été créé
        self.assertEqual(Profile.objects.count(), 1) #vérifie que le profil est bien dans la BDD
        profile = Profile.objects.first()
        self.assertEqual(profile.user, user)
        self.assertEqual(profile.adresse, self.form_data_OK['adresse'])
        self.assertEqual(profile.telephone, self.form_data_OK['telephone'])

    def test_nosave_when_commit_false(self): # Si commit false dans la fonction save : ne doit pas enregistrer l'user
        form = CustomUserCreationForm(data=self.form_data_OK)
        self.assertTrue(form.is_valid())  # Assure que le formulaire est valide
        user = form.save(commit=False)  # N'enregistre pas encore

        # Vérifie qu'aucun utilisateur n'a été créé
        self.assertEqual(User.objects.count(), 0)
        self.assertIsNone(user.id)  # Assure que l'utilisateur n'a pas d'ID assigné

        # Vérifie qu'aucun profil n'a été créé
        self.assertEqual(Profile.objects.count(), 0)