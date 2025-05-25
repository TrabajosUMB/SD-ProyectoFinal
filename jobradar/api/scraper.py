import requests
from bs4 import BeautifulSoup
from .models import JobOffer
import logging
from django.utils import timezone
from datetime import datetime
import re

logger = logging.getLogger(__name__)

def extract_salary(text):
    """Extraer rango salarial del texto"""
    text = text.lower()
    # Patrones comunes de salario
    patterns = [
        r'\$\s*(\d+[.,]?\d*)\s*-\s*\$?\s*(\d+[.,]?\d*)',  # $1000 - $2000
        r'entre\s*\$?\s*(\d+[.,]?\d*)\s*y\s*\$?\s*(\d+[.,]?\d*)',  # entre 1000 y 2000
        r'(\d+[.,]?\d*)\s*a\s*(\d+[.,]?\d*)\s*(?:millones|mil)',  # 1000 a 2000 mil
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            min_salary = float(match.group(1).replace(',', ''))
            max_salary = float(match.group(2).replace(',', ''))
            # Ajustar si son millones
            if 'millones' in text:
                min_salary *= 1_000_000
                max_salary *= 1_000_000
            elif 'mil' in text:
                min_salary *= 1_000
                max_salary *= 1_000
            return min_salary, max_salary
    return None, None

def extract_experience(text):
    """Extraer años de experiencia requeridos"""
    text = text.lower()
    patterns = [
        r'(\d+)\s*(?:años?|years?) de experiencia',
        r'experiencia(?:[^\n.]*?)\s(\d+)\s*(?:años?|years?)',
        r'experiencia mínima (?:de )?\s*(\d+)\s*(?:años?|years?)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return int(match.group(1))
    return None

def extract_education(text):
    """Extraer nivel educativo requerido"""
    text = text.lower()
    education_levels = {
        'bachiller': ['bachiller', 'bachillerato'],
        'técnico': ['técnico', 'tecnico', 'tecnologo'],
        'profesional': ['profesional', 'universitario', 'pregrado'],
        'postgrado': ['postgrado', 'maestría', 'doctorado']
    }
    
    for level, keywords in education_levels.items():
        if any(keyword in text for keyword in keywords):
            return level
    return None

def extract_contract_type(text):
    """Extraer tipo de contrato"""
    text = text.lower()
    if 'tiempo completo' in text or 'full time' in text:
        return 'Tiempo completo'
    elif 'medio tiempo' in text or 'part time' in text:
        return 'Medio tiempo'
    elif 'por proyecto' in text or 'freelance' in text:
        return 'Por proyecto'
    return None

def extract_skills(text):
    """Extraer habilidades/tecnologías requeridas"""
    common_skills = [
        'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node', 'django',
        'flask', 'sql', 'mongodb', 'aws', 'docker', 'kubernetes', 'git', 'agile',
        'scrum', 'php', 'laravel', 'spring', 'typescript', '.net', 'c#', 'ruby',
        'rails', 'html', 'css', 'sass', 'less', 'bootstrap', 'tailwind'
    ]
    
    found_skills = set()
    text = text.lower()
    
    for skill in common_skills:
        if skill in text:
            found_skills.add(skill)
    
    return list(found_skills)

def get_job_details(url, headers):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        description = soup.find('div', class_='box_detail')
        if description:
            text = description.text.strip()
            return {
                'description': text,
                'salary_min': extract_salary(text)[0],
                'salary_max': extract_salary(text)[1],
                'experience_years': extract_experience(text),
                'education_level': extract_education(text),
                'contract_type': extract_contract_type(text),
                'skills_required': extract_skills(text)
            }
        return None
    except Exception as e:
        logger.error(f'Error getting job details: {str(e)}')
        return None

def detect_modality(description):
    description = description.lower()
    if 'remoto' in description or 'teletrabajo' in description or 'home office' in description:
        return 'Remoto'
    elif 'híbrido' in description or 'hibrido' in description:
        return 'Híbrido'
    return 'Presencial'

def scrape_computrabajo(keyword="desarrollador", location="bogota"):
    url = f"https://co.computrabajo.com/ofertas-de-trabajo/?q={keyword}&l={location}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        offers = soup.find_all("article", class_="box_offer")
        jobs_created = 0

        for offer in offers:
            try:
                # Extraer datos básicos
                title = offer.find("a", class_="js-o-link").text.strip()
                company = offer.find("a", class_="text-primary font-size1 font-weight-bold")
                company = company.text.strip() if company else "Empresa Confidencial"
                location = offer.find("p", class_="fs13")
                location = location.text.strip() if location else "Colombia"
                url_job = "https://co.computrabajo.com" + offer.find("a", class_="js-o-link")["href"]
                
                # Obtener detalles adicionales
                details = get_job_details(url_job, headers)
                if not details:
                    continue

                # Detectar modalidad
                modality = detect_modality(details['description'])
                
                # Crear o actualizar la oferta
                job, created = JobOffer.objects.update_or_create(
                    url=url_job,
                    defaults={
                        'title': title,
                        'company': company,
                        'location': location,
                        'modality': modality,
                        'description': details['description'],
                        'category': keyword,
                        'is_active': True,
                        'date_posted': timezone.now(),
                        'salary_min': details['salary_min'],
                        'salary_max': details['salary_max'],
                        'experience_years': details['experience_years'],
                        'education_level': details['education_level'],
                        'contract_type': details['contract_type'],
                        'skills_required': details['skills_required']
                    }
                )
                
                if created:
                    jobs_created += 1
                    logger.info(f'Created new job: {title} at {company}')
                    logger.info(f'Skills required: {details["skills_required"]}')
                
            except Exception as e:
                logger.error(f'Error processing job offer: {str(e)}')
                continue

        return jobs_created

    except requests.RequestException as e:
        logger.error(f'Error fetching jobs: {str(e)}')
        raise
    except Exception as e:
        logger.error(f'Unexpected error: {str(e)}')
        raise

