from rest_framework import serializers
from django.contrib.auth.models import User
from .models import JobOffer, SavedOffer, UserProfile

class JobOfferSerializer(serializers.ModelSerializer):
    skills_required = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = JobOffer
        fields = '__all__'
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Formatear salarios si existen
        if data['salary_min'] and data['salary_max']:
            data['salary_range'] = f"${data['salary_min']:,.2f} - ${data['salary_max']:,.2f}"
        # Asegurar que skills_required sea una lista
        if not data['skills_required']:
            data['skills_required'] = []
        return data

class SavedOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedOffer
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    email = serializers.EmailField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ('user',)

    def update(self, instance, validated_data):
        user_data = {}
        for field in ['email', 'username', 'password', 'first_name', 'last_name']:
            if field in validated_data:
                user_data[field] = validated_data.pop(field)

        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                if attr == 'password':
                    user.set_password(value)
                else:
                    setattr(user, attr, value)
            user.save()

        return super().update(instance, validated_data)
    class Meta:
        model = SavedOffer
        fields = ['id', 'offer', 'user', 'saved_at']
        read_only_fields = ['user', 'saved_at']  # El usuario se asigna automáticamente
