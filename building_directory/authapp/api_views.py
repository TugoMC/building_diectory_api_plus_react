from rest_framework import serializers
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer, LoginSerializer, ChangePasswordSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.permissions import AllowAny
import logging

logger = logging.getLogger(__name__)


from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Assurez-vous que c'est une liste et non un tuple
    authentication_classes = []  # Ajoutez ceci pour désactiver l'authentification

    def create(self, request, *args, **kwargs):
        print("Received request data:", request.data)  # Pour voir les données reçues
        print("Request headers:", request.headers)
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            # Créer le token
            token, created = Token.objects.get_or_create(user=user)
            
            # Définir l'utilisateur comme inactif jusqu'à la confirmation par email
            user.is_active = False
            user.save()

            # Générer le lien d'activation
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            activation_token = default_token_generator.make_token(user)
            activation_link = f"{settings.FRONTEND_URL}/activate/{uidb64}/{activation_token}"

            # Préparer et envoyer l'e-mail
            subject = 'Activez votre compte'
            message = f"""
            Bonjour {user.username},

            Merci de vous être inscrit. Pour activer votre compte, veuillez cliquer sur le lien suivant :

            {activation_link}

            Ce lien expirera dans 24 heures.

            L'équipe de support
            """

            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                # Log l'erreur et supprimer l'utilisateur si l'email ne peut pas être envoyé
                user.delete()
                return Response(
                    {"error": "Erreur lors de l'envoi de l'email d'activation"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            return Response(
                {
                    "user": serializer.data,
                    "token": token.key,
                    "message": "Inscription réussie. Veuillez vérifier vos emails pour activer votre compte."
                },
                status=status.HTTP_201_CREATED,
                headers=headers
            )

        except serializers.ValidationError as e:
            return Response(
                {"error": "Erreur de validation", "details": e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": "Une erreur est survenue lors de l'inscription"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def perform_create(self, serializer):
        return serializer.save()
      
      


class ActivateAccountView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []  # Pas besoin d'authentification pour l'activation

    def get(self, request, uidb64, token):
        try:
            # Décoder l'ID utilisateur
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            logger.debug(f"Attempting to activate user: {user.username}")

        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            logger.error(f"Error decoding user ID or finding user: {e}")
            return Response(
                {"error": "Lien d'activation invalide."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Vérifier si le token est valide
        if default_token_generator.check_token(user, token):
            # Vérifier si le compte n'est pas déjà activé
            if user.is_active:
                logger.info(f"User {user.username} is already active")
                return Response(
                    {"message": "Ce compte est déjà activé."},
                    status=status.HTTP_200_OK
                )

            # Activer le compte
            user.is_active = True
            user.save()
            logger.info(f"Successfully activated user: {user.username}")

            # Générer un nouveau token d'authentification
            from rest_framework.authtoken.models import Token
            token, _ = Token.objects.get_or_create(user=user)

            return Response({
                "message": "Votre compte a été activé avec succès.",
                "token": token.key,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name
                }
            }, status=status.HTTP_200_OK)
        else:
            logger.warning(f"Invalid activation token for user: {user.username}")
            return Response(
                {"error": "Le lien d'activation est invalide ou a expiré."},
                status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request, uidb64, token):
        # Permettre aussi l'activation via POST pour plus de flexibilité
        return self.get(request, uidb64, token)


class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        # Log les données reçues
        logger.debug(f"Received login request data: {request.data}")
        
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            logger.warning(f"Invalid serializer data: {serializer.errors}")
            return Response(
                {"error": "Données de connexion invalides", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        # Log avant authentification
        logger.debug(f"Attempting authentication for user: {username}")
        
        # Vérifier si l'utilisateur existe
        try:
            user_exists = User.objects.filter(username=username).exists()
            logger.debug(f"User exists in database: {user_exists}")
        except Exception as e:
            logger.error(f"Error checking user existence: {e}")

        # Tentative d'authentification
        user = authenticate(request, username=username, password=password)
        logger.debug(f"Authentication result for {username}: {'Success' if user else 'Failed'}")

        if not user:
            return Response(
                {"error": "Nom d'utilisateur ou mot de passe incorrect"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            logger.warning(f"Inactive user attempted to log in: {username}")
            return Response(
                {"error": "Ce compte n'est pas activé. Veuillez vérifier vos emails."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Login successful
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        logger.info(f"User {username} successfully logged in")
        
        return Response({
            "user": UserSerializer(user).data,
            "token": token.key,
            "message": "Connexion réussie"
        })
               
        
class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        logout(request)
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user.userprofile

class ChangePasswordView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get("old_password")):
                user.set_password(serializer.data.get("new_password"))
                user.save()
                update_session_auth_hash(request, user)  # To update session after password change
                return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
            return Response({"error": "Incorrect old password."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"message": "If a user with this email exists, a password reset link has been sent."}, status=status.HTTP_200_OK)

        current_site = get_current_site(request)
        subject = "Password Reset Requested"
        message = f"""
        Hello {user.username},
        Please click on the link below to reset your password:
        http://{current_site.domain}/api/auth/password-reset-confirm/{urlsafe_base64_encode(force_bytes(user.pk))}/{default_token_generator.make_token(user)}/
        """
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        return Response({"message": "If a user with this email exists, a password reset link has been sent."}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            new_password = request.data.get("new_password")
            if new_password:
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "New password is required."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Password reset link is invalid or has expired."}, status=status.HTTP_400_BAD_REQUEST)
        
        


