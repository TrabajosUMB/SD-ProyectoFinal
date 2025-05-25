from django.db import models
from django.contrib.auth.models import User

class JobOffer(models.Model):
    # Campos básicos
    title = models.CharField(max_length=200, db_index=True)
    company = models.CharField(max_length=150, db_index=True)
    location = models.CharField(max_length=100, db_index=True)
    modality = models.CharField(max_length=50, db_index=True)  # Remoto, Presencial, Híbrido
    description = models.TextField()
    category = models.CharField(max_length=100, db_index=True)
    url = models.URLField(max_length=500, unique=True)
    date_posted = models.DateTimeField(auto_now_add=True, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    
    # Campos para búsqueda avanzada
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_index=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_index=True)
    contract_type = models.CharField(max_length=50, null=True, blank=True, db_index=True)  # Tiempo completo, Medio tiempo, Por proyecto
    experience_years = models.IntegerField(null=True, blank=True, db_index=True)
    skills_required = models.JSONField(default=list, blank=True)  # Lista de habilidades/tecnologías
    education_level = models.CharField(max_length=50, null=True, blank=True, db_index=True)  # Bachiller, Técnico, Profesional, etc.
    
    class Meta:
        ordering = ['-date_posted']
        indexes = [
            models.Index(fields=['salary_min', 'salary_max']),
            models.Index(fields=['experience_years', 'education_level']),
            models.Index(fields=['contract_type', 'modality']),
            models.Index(fields=['title', 'company']),
            models.Index(fields=['location', 'category'])
        ]

    def __str__(self):
        return f"{self.title} - {self.company}"

class SavedOffer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_offers')
    offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'offer')

    def __str__(self):
        return f"{self.user.username} - {self.offer.title}"
