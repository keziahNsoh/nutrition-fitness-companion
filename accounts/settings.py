import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Use the environment variables in your settings
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key")
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# Email settings
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

# Database settings
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "keziah"),
        "USER": os.getenv("DB_USER", "default_user"),
        "PASSWORD": os.getenv("DB_PASSWORD", "default_password"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

STATIC_URL = "/static/"

# Add this line to specify the location for collected static files
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Authentication
AUTH_USER_MODEL = "accounts.CustomUser"

# Email backend settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"  # For Gmail
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # Default "from" address for emails
