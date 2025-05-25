from rest_framework import serializers
from .models import JobOffer, SavedOffer

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
        fields = ['id', 'offer', 'user', 'saved_at']
        read_only_fields = ['user', 'saved_at']  # El usuario se asigna automáticamente
