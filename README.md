# JobRadar - Sistema de Búsqueda y Scraping de Empleos

## Descripción General
JobRadar es una aplicación web moderna que combina búsqueda de empleos con web scraping automatizado. Desarrollada con Django, ofrece una API REST para recopilar y gestionar ofertas de trabajo de diferentes fuentes como CompuTrabajo y LinkedIn.

## Características Principales

1. **Web Scraping de Empleos**
   - Scraping automatizado de CompuTrabajo
   - Extracción inteligente de:
     - Salarios
     - Años de experiencia
     - Habilidades requeridas
   - Soporte para múltiples fuentes

2. **API REST Completa**
   - Endpoints para scraping bajo demanda
   - Estadísticas de ofertas de trabajo
   - Autenticación JWT
   - Documentación con Swagger

3. **Frontend Moderno**
   - Diseño responsive con Bootstrap
   - Búsqueda y filtrado avanzado
   - Perfiles de usuario personalizados

## Estructura del Proyecto

### Backend

#### API (api/)
- `models.py`: Modelos de datos
  - UserProfile: Perfiles de usuario
  - JobOffer: Ofertas de trabajo

- `views.py`: Lógica de negocio
  - Endpoints de scraping
  - Gestión de ofertas
  - Estadísticas

- `scraper.py`: Motor de web scraping
  - Scraping de CompuTrabajo
  - Análisis de texto
  - Extracción de datos

### Frontend (frontend/)
- `templates/`: Plantillas HTML
  - `base.html`: Plantilla base
  - `home.html`: Página principal
  - `job_list.html`: Lista de empleos
  - `job_detail.html`: Detalles de empleo
  - `profile.html`: Perfil de usuario
  - `login.html`: Inicio de sesión
  - `register.html`: Registro

## Endpoints de la API

1. **Scraping de Empleos**
```http
POST /api/jobs/scrape_jobs/
Body: {
    "keyword": "python",
    "location": "bogota",
    "source": "computrabajo",
    "num_pages": 1
}
```

2. **Estadísticas**
```http
GET /api/jobs/statistics/
```

## Requisitos

```
python>=3.8
django
djangorestframework
beautifulsoup4
selenium
webdriver-manager
pandas
nltk
```

## Instalación Rápida

1. **Clonar y Preparar**
```bash
git clone <repositorio>
cd jobradar
pip install -r requirements.txt
```

2. **Configurar**
```bash
python manage.py migrate
python manage.py createsuperuser
```

3. **Ejecutar**
```bash
python manage.py runserver
```

## Uso del Scraping

1. Obtener token JWT:
```http
POST /api/token/
Body: {
    "username": "tu_usuario",
    "password": "tu_contraseña"
}
```

2. Hacer scraping:
```http
POST /api/jobs/scrape_jobs/
Headers: {
    "Authorization": "Bearer <tu_token>"
}
Body: {
    "keyword": "python"
}
```

## Contribuir
1. Haz fork del repositorio
2. Crea una rama para tu feature
3. Haz commit de tus cambios
4. Envía un pull request

## Agradecimientos

### Bibliotecas y Frameworks
- Django y Django REST Framework para el backend
- BeautifulSoup4 y Selenium para web scraping
- NLTK para procesamiento de texto
- Bootstrap para el frontend

### Recursos
- Documentación oficial de Django
- Documentación de Selenium WebDriver
- CompuTrabajo para datos de prueba

## Desarrollo y Contribución

- Usar entorno virtual
- Seguir PEP 8 para estilo de código
- Documentar nuevas funcionalidades
- Realizar pruebas antes de commits

## Seguridad

- Autenticación JWT implementada
- Protección CSRF activada
- Validación de datos en formularios
- Sanitización de entradas de usuario.

## Arquitectura del Sistema

El sistema está compuesto por los siguientes componentes:

### 1. Frontend (JobRadar)
- Interfaz de usuario web responsive
- Implementado con HTML5, TailwindCSS y JavaScript
- Gestión de estado del cliente
- Sistema de autenticación JWT

### 2. Backend API (JobRadar Django)
- API REST implementada en Django
- Gestión de usuarios y autenticación
- Base de datos SQLite para almacenamiento
- Manejo de ofertas favoritas

### 3. Servicio de Scraping
- Microservicio independiente en Python
- Scraping de ofertas de trabajo de diferentes fuentes
- Cola de mensajes para procesamiento asíncrono
- Almacenamiento en caché Redis

### 4. Servicio de Notificaciones
- Sistema de notificaciones en tiempo real
- Implementado con WebSockets
- Notificaciones push para nuevas ofertas
- Alertas personalizadas

## Tecnologías Utilizadas

### Frontend
- HTML5
- TailwindCSS
- JavaScript (Vanilla)
- JWT para autenticación

### Backend
- Django 4.2
- Django REST Framework
- SQLite
- Redis (caché)

### Servicios
- Python 3.9+
- BeautifulSoup4 (scraping)
- RabbitMQ (mensajería)
- WebSocket (notificaciones)

### DevOps
- Docker
- Docker Compose
- GitHub Actions (CI/CD)
- Nginx (proxy inverso)

## Estructura del Proyecto

```
/
├── jobradar/              # Frontend y API principal
│   ├── api/              # API Django
│   │   ├── static/        # Archivos estáticos
│   │   ├── models/        # Modelos de datos
│   │   ├── views/         # Lógica de negocio
│   │   └── tests/         # Pruebas unitarias
│   └── jobradar/         # Configuración Django
├── scraper/              # Servicio de scraping
│   ├── scrapers/         # Módulos de scraping
│   ├── processors/      # Procesadores de datos
│   └── tests/           # Pruebas unitarias
├── notifications/        # Servicio de notificaciones
│   ├── websocket/        # Servidor WebSocket
│   ├── processors/      # Procesadores de eventos
│   └── tests/           # Pruebas unitarias
├── docker/               # Configuración Docker
└── docs/                 # Documentación
```

## Características Principales

1. **Búsqueda de Empleos**
   - Búsqueda en tiempo real
   - Filtros avanzados
   - Guardado de búsquedas favoritas

2. **Gestión de Usuario**
   - Registro y autenticación
   - Perfil personalizado
   - Preferencias de búsqueda

3. **Ofertas Favoritas**
   - Guardado de ofertas
   - Organización por categorías
   - Notificaciones de actualizaciones

4. **Notificaciones**
   - Alertas en tiempo real
   - Notificaciones por email
   - Configuración personalizada

## Instalación y Configuración

### Requisitos Previos
- Docker y Docker Compose
- Python 3.9+
- Node.js 14+
- Redis
- RabbitMQ

### Pasos de Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd proyecto-final
```

2. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con las configuraciones necesarias
```

3. Iniciar servicios con Docker:
```bash
docker-compose up -d
```

4. Inicializar la base de datos:
```bash
docker-compose exec api python manage.py migrate
```

5. Crear superusuario:
```bash
docker-compose exec api python manage.py createsuperuser
```

## Desarrollo

### Entorno de Desarrollo

1. Iniciar servicios de desarrollo:
```bash
docker-compose -f docker-compose.dev.yml up
```

2. Ejecutar pruebas:
```bash
# Pruebas de API
docker-compose exec api python manage.py test

# Pruebas de scraper
docker-compose exec scraper pytest

# Pruebas de notificaciones
docker-compose exec notifications pytest
```

### Flujo de Trabajo Git

1. Crear rama de feature:
```bash
git checkout -b feature/nueva-caracteristica
```

2. Commit de cambios:
```bash
git add .
git commit -m "feat: descripción del cambio"
```

3. Push y Pull Request:
```bash
git push origin feature/nueva-caracteristica
# Crear Pull Request en GitHub
```

## Despliegue

### Producción

1. Construir imágenes:
```bash
docker-compose -f docker-compose.prod.yml build
```

2. Desplegar:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Monitoreo

- Acceder a logs:
```bash
docker-compose logs -f [servicio]
```

- Monitoreo de recursos:
```bash
docker stats
```

## API Documentation

### Endpoints Principales

#### Autenticación
```
POST /api/token/
POST /api/token/refresh/
POST /api/register/
```

#### Ofertas de Trabajo
```
GET /api/jobs/
GET /api/jobs/{id}/
POST /api/jobs/favorite/
```

#### Perfil de Usuario
```
GET /api/profile/
PUT /api/profile/
GET /api/profile/favorites/
```

## Contribución

1. Fork del repositorio
2. Crear rama de feature
3. Commit de cambios
4. Push a la rama
5. Crear Pull Request

### Guías de Contribución

- Seguir guías de estilo de código
- Escribir pruebas para nuevas características
- Documentar cambios en API
- Mantener commits atómicos


## Contacto

- **Desarrollador**: Santiago Rodriguez Angel
- **Email**: ing.santiagorodriguezangel@gmail.com
- **GitHub**: EngAngel

