from django.core.management.base import BaseCommand
from jobradar.api.models import JobOffer

class Command(BaseCommand):
    help = 'Carga datos de prueba para las ofertas de trabajo'

    def handle(self, *args, **kwargs):
        test_jobs = [
            {
                'title': 'Desarrollador Full Stack',
                'company': 'TechCorp',
                'location': 'Bogotá, Colombia',
                'salary_min': 4000000,
                'salary_max': 6000000,
                'description': 'Buscamos desarrollador full stack con experiencia en React y Django',
                'skills_required': ['React', 'Django', 'Python', 'JavaScript'],
                'url': 'https://example.com/job1',
                'modality': 'remote',
                'contract_type': 'full_time',
                'education_level': 'professional',
                'experience_years': 3,
                'is_active': True
            },
            {
                'title': 'Frontend Developer',
                'company': 'WebSolutions',
                'location': 'Medellín, Colombia',
                'salary_min': 3500000,
                'salary_max': 5000000,
                'description': 'Se busca desarrollador frontend con experiencia en React y diseño UI/UX',
                'skills_required': ['React', 'HTML', 'CSS', 'JavaScript'],
                'url': 'https://example.com/job2',
                'modality': 'hybrid',
                'contract_type': 'full_time',
                'education_level': 'professional',
                'experience_years': 2,
                'is_active': True
            },
            {
                'title': 'Backend Developer',
                'company': 'DataSystems',
                'location': 'Cali, Colombia',
                'salary_min': 4500000,
                'salary_max': 7000000,
                'description': 'Desarrollador backend con experiencia en Python y bases de datos',
                'skills_required': ['Python', 'Django', 'PostgreSQL', 'API REST'],
                'url': 'https://example.com/job3',
                'modality': 'on_site',
                'contract_type': 'full_time',
                'education_level': 'professional',
                'experience_years': 4,
                'is_active': True
            }
        ]

        for job_data in test_jobs:
            JobOffer.objects.create(**job_data)

        self.stdout.write(self.style.SUCCESS('Datos de prueba cargados exitosamente'))
