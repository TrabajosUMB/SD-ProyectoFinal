from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from .models import UserProfile, JobOffer
from .serializers import UserSerializer, UserProfileSerializer, JobOfferSerializer
from .scraper import JobScraper

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=self.request.user)

class JobOfferViewSet(viewsets.ModelViewSet):
    queryset = JobOffer.objects.all()
    serializer_class = JobOfferSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['modality', 'contract_type', 'education_level', 'experience_years', 'is_active']
    search_fields = ['title', 'company', 'location', 'description', 'skills_required']
    ordering_fields = ['created_at', 'salary_min', 'salary_max']
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            # Permitir crear ofertas (via scraping) y ver ofertas a usuarios autenticados
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def scrape_jobs(self, request):
        """Endpoint para iniciar el scraping de trabajos"""
        keyword = request.data.get('keyword')
        location = request.data.get('location')
        source = request.data.get('source', 'computrabajo')
        num_pages = int(request.data.get('num_pages', 1))

        if not keyword:
            return Response(
                {'error': 'Se requiere una palabra clave para la búsqueda'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            scraper = JobScraper()
            if source == 'computrabajo':
                jobs = scraper.scrape_computrabajo(keyword, location, num_pages)
            elif source == 'linkedin':
                jobs = scraper.scrape_linkedin(keyword, location, num_pages)
            else:
                return Response(
                    {'error': 'Fuente no soportada'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Guardar trabajos en la base de datos
            JobOffer.objects.bulk_create(jobs)

            return Response({
                'message': f'Se encontraron {len(jobs)} ofertas de trabajo',
                'jobs': JobOfferSerializer(jobs, many=True).data
            })

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        finally:
            scraper.close()

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Endpoint para obtener estadísticas de las ofertas de trabajo"""
        try:
            # Estadísticas generales
            stats = {
                'total_jobs': JobOffer.objects.count(),
                'avg_salary': {
                    'min': JobOffer.objects.aggregate(avg=Avg('salary_min'))['avg'],
                    'max': JobOffer.objects.aggregate(avg=Avg('salary_max'))['avg'],
                },
                'top_companies': JobOffer.objects.values('company')
                    .annotate(total=Count('company'))
                    .order_by('-total')[:10],
                'top_locations': JobOffer.objects.values('location')
                    .annotate(total=Count('location'))
                    .order_by('-total')[:10],
                'modality_distribution': JobOffer.objects.values('modality')
                    .annotate(total=Count('modality')),
                'contract_types': JobOffer.objects.values('contract_type')
                    .annotate(total=Count('contract_type')),
                'education_levels': JobOffer.objects.values('education_level')
                    .annotate(total=Count('education_level')),
            }

            return Response(stats)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
