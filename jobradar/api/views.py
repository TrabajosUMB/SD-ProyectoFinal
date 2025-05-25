from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as django_filters
from django.db.models import Count, Avg, Q
from .models import JobOffer, SavedOffer
from .serializers import JobOfferSerializer, SavedOfferSerializer

class JobOfferFilter(django_filters.FilterSet):
    salary_min = django_filters.NumberFilter(field_name='salary_min', lookup_expr='gte')
    salary_max = django_filters.NumberFilter(field_name='salary_max', lookup_expr='lte')
    experience_years = django_filters.NumberFilter()
    skills = django_filters.CharFilter(method='filter_skills')
    location = django_filters.CharFilter(lookup_expr='icontains')
    modality = django_filters.CharFilter(lookup_expr='iexact')
    contract_type = django_filters.CharFilter(lookup_expr='iexact')
    education_level = django_filters.CharFilter(lookup_expr='iexact')
    search = django_filters.CharFilter(method='filter_search')
    
    def filter_skills(self, queryset, name, value):
        if not value:
            return queryset
        skills = [skill.strip().lower() for skill in value.split(',')]
        return queryset.filter(skills_required__contains=skills)
    
    def filter_search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value) |
            Q(company__icontains=value)
        )
    
    class Meta:
        model = JobOffer
        fields = ['salary_min', 'salary_max', 'experience_years', 'skills',
                'location', 'modality', 'contract_type', 'education_level']

class JobOfferViewSet(viewsets.ModelViewSet):
    queryset = JobOffer.objects.all().order_by('-date_posted')
    serializer_class = JobOfferSerializer
    permission_classes = [AllowAny]
    filterset_class = JobOfferFilter
    
    def get_queryset(self):
        return JobOffer.objects.filter(is_active=True).order_by('-date_posted')
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Obtener estadísticas sobre las ofertas de trabajo"""
        queryset = self.get_queryset()
        total_jobs = queryset.count()
        
        modality_stats = dict(
            queryset.values('modality')
            .annotate(count=Count('id'))
            .values_list('modality', 'count')
        )
        
        salary_stats = queryset.filter(salary_min__isnull=False).aggregate(
            avg_min=Avg('salary_min'),
            avg_max=Avg('salary_max')
        )
        
        # Procesar skills para obtener las más comunes
        skills_list = queryset.values_list('skills_required', flat=True)
        all_skills = []
        for skills in skills_list:
            if skills:
                all_skills.extend(skills)
        
        skill_counts = {}
        for skill in all_skills:
            skill_counts[skill] = skill_counts.get(skill, 0) + 1
        
        top_skills = dict(sorted(
            skill_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10])
        
        return Response({
            'total_jobs': total_jobs,
            'modality_distribution': modality_stats,
            'salary_statistics': salary_stats,
            'top_skills': top_skills
        })
        top_skills = self.get_queryset().values_list('skills_required', flat=True)
        
        # Procesar skills para obtener las más comunes
        all_skills = []
        for skills in top_skills:
            if skills:
                all_skills.extend(skills)
        skill_counts = {}
        for skill in all_skills:
            skill_counts[skill] = skill_counts.get(skill, 0) + 1
        top_skills = dict(sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:10])
        
        return Response({
            'total_jobs': total_jobs,
            'modality_distribution': modality_stats,
            'average_salary_min': avg_salary_min,
            'top_skills': top_skills
        })

class SavedOfferViewSet(viewsets.ModelViewSet):
    serializer_class = SavedOfferSerializer
    permission_classes = [IsAuthenticated]  # requiere autenticación

    def get_queryset(self):
        return SavedOffer.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)