import os
from datetime import timedelta
from pathlib import Path
import dj_database_url
import environ
from corsheaders import middleware
from dotenv import load_dotenv
load_dotenv()


"""
env = environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env()
"""

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-%2$vr3yiaj%yr!x#g_j4%h^o%$xyfd_7$atdfgnb48&jgzc2^%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", "*"]

# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth', 'django.contrib.contenttypes',
    'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles', 'django_filters',
    'corsheaders', 'rest_framework', 'administrador', 'productos', 'usuario',
    'compras', 'informacion', 'autenticacion', ]

# implementar autenticación

REST_FRAMEWORK = {'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
                  'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
                  'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework_simplejwt.authentication.JWTAuthentication', ], }

MIDDLEWARE = ['django.middleware.security.SecurityMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
              'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware',
              'django.contrib.auth.middleware.AuthenticationMiddleware',
              'django.contrib.messages.middleware.MessageMiddleware',
              'django.middleware.clickjacking.XFrameOptionsMiddleware', 'corsheaders.middleware.CorsMiddleware', ]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [], 'APP_DIRS': True, 'OPTIONS': {
    'context_processors': ['django.template.context_processors.debug', 'django.template.context_processors.request',
                           'django.contrib.auth.context_processors.auth',
                           'django.contrib.messages.context_processors.messages', ], }, }, ]

WSGI_APPLICATION = 'backend.wsgi.application'

# luego se implementan variables de entorno
DATABASES = {'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
                            {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
                            {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
                            {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', }, ]
AUTH_USER_MODEL = 'autenticacion.UserData'

"""
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_WHITELIST = [
    u'http://localhost:3000',
    u'http://127.0.0.1:3000',
]
"""

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True
