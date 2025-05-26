from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from api.models import JobOffer, UserProfile

def home(request):
    recent_jobs = JobOffer.objects.filter(is_active=True).order_by('-created_at')[:6]
    return render(request, 'frontend/home.html', {'recent_jobs': recent_jobs})

def job_list(request):
    jobs = JobOffer.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'frontend/job_list.html', {'jobs': jobs})

def job_detail(request, pk):
    job = JobOffer.objects.get(pk=pk)
    return render(request, 'frontend/job_detail.html', {'job': job})

@login_required
def profile(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        # Actualizar perfil
        profile.professional_title = request.POST.get('professional_title')
        profile.experience_years = request.POST.get('experience_years')
        profile.skills = request.POST.get('skills')
        profile.save()
        messages.success(request, 'Perfil actualizado correctamente')
        return redirect('profile')
    
    return render(request, 'frontend/profile.html', {'profile': profile})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            messages.success(request, '¡Cuenta creada exitosamente!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'frontend/register.html', {'form': form})
