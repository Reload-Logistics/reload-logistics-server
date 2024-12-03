

from pathlib import Path
from datetime import timedelta
# import django_heroku
import dj_database_url
import os
from decouple import config
# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", cast=str)

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool, default=True)

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "matols-logistics-services-6e660bee869e.herokuapp.com",]


# Application definition

INSTALLED_APPS = [
 
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",

    # 3rd party packages 
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "django_rest_passwordreset",
    "django_json_widget",

    # apps 
    "user.apps.UserConfig",
    "booking.apps.BookingConfig",
    "booking_pending.apps.BookingPendingConfig",
    "feed_back.apps.FeedBackConfig",
    "frequently_asked_questions.apps.FrequentlyAskedQuestionsConfig",
    "contact_us.apps.ContactUsConfig",

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [ os.path.join(BASE_DIR, "templates"),],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if(DEBUG):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": dj_database_url.config(default=config("DATABASE_URL", cast=str, default = ""))
    }
    

REST_FRAMEWORK = {
    
    "EXCEPTION_HANDLER": "utils.custom_exception_handler.custom_exception_handler",
    
    "DEFAULT_AUTHENTICATION_CLASSES": [
       "rest_framework_simplejwt.authentication.JWTAuthentication",
    #    "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ]

}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Harare"

USE_I18N = True
USE_L10N = True
USE_TZ = True

# settings for cors 
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://\w+\matols-logistics-services-6e660bee869e.herokuapp.com/\.com$",
]

CORS_ALLOWED_ORIGINS = ["http://localhost:8000", "http://127.0.0.1:8000", "https://matols-logistics-services-6e660bee869e.herokuapp.com"]

# storage settings 
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

AUTH_USER_MODEL = "user.User"



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )

# media files (all formats)
MEDIA_ROOT = "media/"
MEDIA_URL = os.path.join(BASE_DIR, MEDIA_ROOT)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# simple jwt settings 
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=60),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer", ),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "account_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=60),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

# email settings 
EMAIL_HOST = config("EMAIL_HOST", cast=str)
EMAIL_PORT = config("EMAIL_PORT", cast=str, default="465")
EMAIL_HOST_USER = config("EMAIL_HOST_USER", cast=str)
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", cast=str)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
#EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool, default=True)
EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool, default=False)
