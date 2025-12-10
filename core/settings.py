from pathlib import Path
from environ import Env

from datetime import timedelta


BASE_DIR = Path(__file__).resolve().parent.parent
env = Env()
Env.read_env(BASE_DIR / '.env')
SECRET_KEY = env('SECRET_KEY')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/



# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'django_filters',
    'library',
    'Meta_Admin.apps.MetaAdminConfig',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'mydatabase',
#         'USER': 'mydatabaseuser',
#         'PASSWORD': 'mypassword',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)   # на всякий случай создаём папку


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "default": {
            "format": "[{levelname}] {asctime} {name}: {message}",
            "style": "{",
        },
        "verbose": {
            "format": "[{asctime}] {levelname} {name}: {message}",
            "style": "{",
        },
    },

    "handlers": {
        # 1) Логи работы сервера -> консоль
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },

        # Общий лог проекта
        "file_project": {
            "class": "logging.FileHandler",
            "filename": str(LOG_DIR / "project.log"),
            "formatter": "default",
        },

        # Ошибки (можно оставить как было)
        "file_errors": {
            "class": "logging.FileHandler",
            "filename": str(LOG_DIR / "errors.log"),
            "formatter": "default",
            "level": "ERROR",
        },

        # 2) HTTP-запросы -> logs/http_logs.log
        "http_file": {
            "class": "logging.FileHandler",
            "filename": str(LOG_DIR / "http_logs.log"),
            "formatter": "verbose",
        },

        # 3) SQL-запросы -> logs/db_logs.log
        "db_file": {
            "class": "logging.FileHandler",
            "filename": str(LOG_DIR / "db_logs.log"),
            "formatter": "verbose",
        },
    },

    "loggers": {
        # Общие логи Django
        "django": {
            "handlers": ["console", "file_project"],
            "level": "INFO",
        },

        # Логи работы dev-сервера (runserver) -> консоль
        "django.server": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },

        # HTTP-запросы и ответы -> http_logs.log
        "django.request": {
            "handlers": ["http_file", "file_errors"],
            "level": "INFO",
            "propagate": False,
        },

        # SQL-запросы -> db_logs.log
        "django.db.backends": {
            "handlers": ["db_file"],
            "level": "DEBUG",    # чтобы видеть все запросы
            "propagate": False,
        },

        # проектный логгер
        "project": {
            "handlers": ["console", "file_project"],
            "level": "INFO",
        },
    },
}


REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],

    "DEFAULT_PAGINATION_CLASS": "library.pagination.DefaultCursorPagination",
        "PAGE_SIZE": 5,

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',

        'rest_framework_simplejwt.authentication.JWTAuthentication',


    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        'rest_framework.permissions.AllowAny',
    ],
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,

    'AUTH_HEADER_TYPES': ('Bearer',),
}
