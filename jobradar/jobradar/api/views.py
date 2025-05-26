from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django_filters import rest_framework as django_filters
from django.db.models import Count, Avg, Q
from .models import JobOffer, SavedOffer, UserProfile
from .serializers import (JobOfferSerializer, SavedOfferSerializer,
                         UserSerializer, UserProfileSerializer)

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
        queryset = self.get_queryset()
        total_offers = queryset.count()
        
        # Salary statistics
        salary_stats = queryset.filter(salary_min__isnull=False).aggregate(
            avg_min=Avg('salary_min'),
            avg_max=Avg('salary_max')
        )
        
        # Modality distribution
        modality_stats = dict(
            queryset.values('modality')
            .annotate(count=Count('id'))
            .values_list('modality', 'count')
        )
        
        # Skills analysis
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
            'total_offers': total_offers,
            'salary_statistics': salary_stats,
            'modality_distribution': modality_stats,
            'top_skills': top_skills
        })

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def me(self, request):
        profile = self.get_queryset().first()
        if not profile:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'])
    def update_me(self, request):
        profile = self.get_queryset().first()
        if not profile:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        
        if not username or not password:
            return Response({
                'error': 'Por favor proporciona usuario y contraseña'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        if User.objects.filter(username=username).exists():
            return Response({
                'error': 'El usuario ya existe'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        user = User.objects.create_user(username=username, password=password, email=email)
        UserProfile.objects.create(user=user)
        
        return Response({
            'message': 'Usuario creado exitosamente'
        }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'error': 'Por favor proporciona usuario y contraseña'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        login(request, user)
        return Response({
            'message': 'Login exitoso',
            'username': user.username,
        })
    else:
        return Response({
            'error': 'Credenciales inválidas'
        }, status=status.HTTP_401_UNAUTHORIZED)

class SavedOfferViewSet(viewsets.ModelViewSet):
    serializer_class = SavedOfferSerializer
    permission_classes = [IsAuthenticated]  # requiere autenticación

    def get_queryset(self):
        return SavedOffer.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)