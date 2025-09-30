"""
Configuración de Ferreterías Juan
SOLO para entorno educativo
"""

import os

class Config:
    # Configuración de Flask
    SECRET_KEY = 'ferreteria_juan_secret_key_123'  
    DEBUG = True 

    # Configuración de base de datos
    DB_CONFIG = {
        'host': 'localhost',
        'database': 'ferreteria_juan',
        'user': 'ferreteria_user',
        'password': 'ferreteria_pass123', 
        'port': 3306,
        'charset': 'utf8mb4',
        'autocommit': True
    }

    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {
        'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff',
        'php', 'py', 'js', 'html', 'htm', 'css', 'sh', 'bat', 'exe'
    }

    # Configuración de logging
    LOG_FILE = 'ferreteria_juan.log'
    LOG_LEVEL = 'DEBUG'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Configuración de seguridad 
    SESSION_COOKIE_SECURE = False  
    SESSION_COOKIE_HTTPONLY = False 
    PERMANENT_SESSION_LIFETIME = 3600 * 24  # 24 horas

    # URLs y rutas importantes
    BASE_URL = 'http://localhost'
    ADMIN_PATH = '/admin'

    # Credenciales por defecto 
    DEFAULT_ADMIN = {
        'username': 'admin',
        'password': 'admin123',  
        'email': 'admin@ferreteriajuan.com'
    }

    # Configuración de vulnerabilidades
    VULNERABILITIES = {
        'sql_injection': True,
        'xss_stored': True,
        'xss_reflected': True,
        'file_upload': True,
        'information_disclosure': True,
        'weak_authentication': True,
        'debug_endpoints': True
    }

class ProductionConfig(Config):
    """Configuración para producción (NO USAR - Solo referencia)"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'change-this-in-production'
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

class DevelopmentConfig(Config):
    """Configuración para desarrollo/laboratorio"""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    DEBUG = True
    DB_CONFIG = {
        'host': 'localhost',
        'database': 'ferreteria_juan_test',
        'user': 'ferreteria_user',
        'password': 'ferreteria_pass123',
        'port': 3306
    }

# Configuración por defecto 
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,  
    'testing': TestingConfig,
    'default': DevelopmentConfig  
}
