from .models import JobOffer

class JobScraper:
    def __init__(self):
        # Importar dependencias solo cuando se instancia la clase
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.chrome.options import Options
            from webdriver_manager.chrome import ChromeDriverManager
            import nltk
            
            # Descargar recursos NLTK solo si no están descargados
            try:
                nltk.data.find('tokenizers/punkt')
            except LookupError:
                nltk.download('punkt')
            try:
                nltk.data.find('corpora/stopwords')
            except LookupError:
                nltk.download('stopwords')
            
            # Configurar Selenium
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            
        except Exception as e:
            raise Exception(f'Error al inicializar el scraper: {str(e)}')


class JobScraper:
    def __init__(self):
        # Configurar Selenium
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ejecutar en modo headless
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
    
    def extract_salary(self, text):
        """Extrae el rango salarial del texto usando expresiones regulares"""
        salary_pattern = r'\$\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:-|a)\s*\$\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
        match = re.search(salary_pattern, text)
        if match:
            min_salary = float(match.group(1).replace(',', ''))
            max_salary = float(match.group(2).replace(',', ''))
            return min_salary, max_salary
        return None, None

    def extract_experience(self, text):
        """Extrae los años de experiencia requeridos del texto"""
        exp_pattern = r'(\d+)\s*(?:años?|year)'
        match = re.search(exp_pattern, text.lower())
        return int(match.group(1)) if match else 0

    def extract_skills(self, text):
        """Extrae habilidades del texto usando NLTK"""
        from nltk.tokenize import word_tokenize
        
        # Lista de habilidades comunes en tecnología
        common_skills = {'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node', 'django', 
                        'flask', 'sql', 'mongodb', 'aws', 'docker', 'kubernetes', 'git', 'agile', 'scrum'}
        
        # Tokenizar el texto
        tokens = word_tokenize(text.lower())
        
        # Encontrar habilidades
        found_skills = [token for token in tokens if token in common_skills]
        return list(set(found_skills))  # Eliminar duplicados

    def scrape_computrabajo(self, keyword, location=None, num_pages=1):
        """Scrape jobs from CompuTrabajo"""
        from bs4 import BeautifulSoup
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        jobs = []
        base_url = "https://co.computrabajo.com/trabajo-de-{}"
        
        for page in range(1, num_pages + 1):
            url = base_url.format(keyword)
            if page > 1:
                url += f"-pagina-{page}"
            
            self.driver.get(url)
            
            # Esperar a que los elementos de trabajo se carguen
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "box_offer"))
            )
            
            # Obtener el HTML y crear el objeto BeautifulSoup
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            job_listings = soup.find_all('div', class_='box_offer')
            
            for job in job_listings:
                title = job.find('h2').text.strip()
                company = job.find('a', class_='fc_base').text.strip()
                description = job.find('p', class_='text-word-break').text.strip()
                location = job.find('p', class_='fs13').text.strip()
                url = "https://co.computrabajo.com" + job.find('a')['href']
                
                # Extraer información adicional
                salary_min, salary_max = self.extract_salary(description)
                experience_years = self.extract_experience(description)
                skills = self.extract_skills(description)
                
                # Crear objeto JobOffer
                job_offer = JobOffer(
                    title=title,
                    company=company,
                    location=location,
                    salary_min=salary_min if salary_min else 0,
                    salary_max=salary_max if salary_max else 0,
                    description=description,
                    skills_required=", ".join(skills),
                    url=url,
                    modality='presencial',  # Por defecto
                    contract_type='tiempo_completo',  # Por defecto
                    education_level='universitario',  # Por defecto
                    experience_years=experience_years
                )
                jobs.append(job_offer)
        
        return jobs

    def scrape_linkedin(self, keyword, location=None, num_pages=1):
        """Scrape jobs from LinkedIn"""
        # Implementación similar a CompuTrabajo
        pass

    def close(self):
        """Cerrar el driver de Selenium"""
        self.driver.quit()

    def get_job_statistics(self, jobs):
        """Genera estadísticas de las ofertas de trabajo"""
        stats = {
            'total_jobs': len(jobs),
            'avg_salary_min': sum(job.salary_min for job in jobs) / len(jobs) if jobs else 0,
            'avg_salary_max': sum(job.salary_max for job in jobs) / len(jobs) if jobs else 0,
            'companies': {},
            'skills': {},
            'locations': {}
        }
        
        for job in jobs:
            # Contar empresas
            stats['companies'][job.company] = stats['companies'].get(job.company, 0) + 1
            
            # Contar habilidades
            for skill in job.skills_required.split(', '):
                stats['skills'][skill] = stats['skills'].get(skill, 0) + 1
            
            # Contar ubicaciones
            stats['locations'][job.location] = stats['locations'].get(job.location, 0) + 1
        
        return stats
