# Créez un fichier nommé management/commands/create_user_profiles.py dans votre application

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from professionals.models import UserProfile

class Command(BaseCommand):
    help = 'Crée des profils utilisateurs pour les utilisateurs existants qui n\'en ont pas'

    def handle(self, *args, **kwargs):
        users_without_profile = User.objects.filter(userprofile__isnull=True)
        for user in users_without_profile:
            UserProfile.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Profil créé pour l\'utilisateur {user.username}'))