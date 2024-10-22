from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2', 'first_name', 'last_name']
        extra_kwargs = {
            'username': {'required': True},
            'first_name': {'required': False},
            'last_name': {'required': False}
        }

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas"})
        return attrs

    def create(self, validated_data):
        # Supprimer password2 des données validées
        validated_data.pop('password2', None)
        
        # Récupérer le mot de passe
        password = validated_data.pop('password')
        
        # Créer l'utilisateur sans le mot de passe
        user = User.objects.create(**validated_data)
        
        # Définir le mot de passe correctement
        user.set_password(password)
        user.save()
        
        return user

    def update(self, instance, validated_data):
        # Si le mot de passe est dans les données à mettre à jour
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        
        # Mettre à jour les autres champs
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        instance.save()
        return instance
    
    
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'profile_photo']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        # Ici, tu peux ajouter des validations supplémentaires pour le nouveau mot de passe
        if len(value) < 8:
            raise serializers.ValidationError("Le nouveau mot de passe doit contenir au moins 8 caractères.")
        return value