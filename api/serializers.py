from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, JobOffer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'professional_title', 'experience_years', 'skills')
        read_only_fields = ('id',)

class JobOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOffer
        fields = '__all__'
        read_only_fields = ('id', 'created_at')
