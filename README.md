# JobRadar - Sistema de Búsqueda de Empleos

## Descripción General
JobRadar es una aplicación web moderna para la búsqueda y gestión de ofertas de trabajo, desarrollada con Django y SQL Server.

## Estructura del Proyecto

### Backend (Django)

#### Aplicación Principal (jobradar/)
- `settings.py`: Configuración principal del proyecto
  - Gestión de la base de datos SQL Server
  - Configuración de seguridad y autenticación
  - Configuración de REST Framework

- `urls.py`: Enrutamiento principal
  - Endpoints de la API REST
  - Rutas administrativas
  - Documentación de la API

#### API (api/)
- `models.py`: Modelos de datos
  - JobOffer: Ofertas de trabajo
  - SavedOffer: Ofertas guardadas por usuarios

- `views.py`: Lógica de negocio
  - JobOfferViewSet: Gestión de ofertas de trabajo
  - SavedOfferViewSet: Gestión de ofertas guardadas

- `serializers.py`: Serialización de datos
  - Conversión de modelos a JSON y viceversa

### Frontend (templates/)
- `index.html`: Página principal
- `login.html`: Página de inicio de sesión
- `favoritos.html`: Gestión de ofertas guardadas

## Características Principales

1. **Búsqueda de Empleos**
   - Filtros avanzados por salario, experiencia, ubicación
   - Búsqueda por palabras clave
   - Ordenamiento personalizado

2. **Gestión de Usuarios**
   - Registro e inicio de sesión
   - Guardado de ofertas favoritas
   - Perfil personalizado

3. **API REST**
   - Endpoints documentados con Swagger
   - Autenticación JWT
   - Filtrado y paginación

## Requisitos Técnicos

### Base de Datos
- SQL Server 2019 o superior
- Configuración de autenticación Windows

### Python y Dependencias
```
python 3.11 o superior
django==4.2.7
djangorestframework==3.16.0
mssql-django==1.4.1
pyodbc==5.0.1
```

## Instalación y Configuración

1. **Preparar el Entorno**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configurar Base de Datos**
   - Asegurar que SQL Server esté en ejecución
   - Crear base de datos 'JobRadarDB'
   - Configurar settings.py con los datos de conexión

3. **Iniciar la Aplicación**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

## Solución de Problemas

1. **Errores de Conexión a SQL Server**
   - Verificar que el servicio esté en ejecución
   - Comprobar el nombre de la instancia
   - Asegurar que la autenticación Windows esté habilitada

2. **Errores de CSRF**
   - Verificar la configuración de MIDDLEWARE en settings.py
   - Asegurar que las cookies estén habilitadas

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

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contacto

- **Desarrollador**: [Tu Nombre]
- **Email**: [Tu Email]
- **GitHub**: [Tu perfil de GitHub]

## Agradecimientos

- Mencionar colaboradores
- Bibliotecas utilizadas
- Recursos y tutoriales
