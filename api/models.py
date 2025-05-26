from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    professional_title = models.CharField(max_length=200, null=True, blank=True)
    experience_years = models.IntegerField(default=0)
    skills = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.professional_title}'

class JobOffer(models.Model):
    MODALITY_CHOICES = [
        ('presencial', 'Presencial'),
        ('remoto', 'Remoto'),
        ('hibrido', 'Híbrido'),
    ]

    CONTRACT_TYPE_CHOICES = [
        ('tiempo_completo', 'Tiempo Completo'),
        ('medio_tiempo', 'Medio Tiempo'),
        ('por_proyecto', 'Por Proyecto'),
        ('practicas', 'Prácticas'),
    ]

    EDUCATION_LEVEL_CHOICES = [
        ('bachiller', 'Bachiller'),
        ('tecnico', 'Técnico'),
        ('universitario', 'Universitario'),
        ('postgrado', 'Postgrado'),
        ('maestria', 'Maestría'),
        ('doctorado', 'Doctorado'),
    ]

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    skills_required = models.TextField()
    url = models.URLField(max_length=500)
    modality = models.CharField(max_length=50, choices=MODALITY_CHOICES)
    contract_type = models.CharField(max_length=50, choices=CONTRACT_TYPE_CHOICES)
    education_level = models.CharField(max_length=50, choices=EDUCATION_LEVEL_CHOICES)
    experience_years = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['company']),
            models.Index(fields=['location']),
        ]

    def __str__(self):
        return f'{self.title} - {self.company}'
