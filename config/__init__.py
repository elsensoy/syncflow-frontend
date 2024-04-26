import os

class Config:
    """Base configuration class."""
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    if not GEMINI_API_KEY:
        raise ValueError("API key for Gemini is not set.")

class ProductionConfig(Config):
    """Production configuration."""
    # ... add production specific settings ...

# ... add other environment configurations ...

def get_config():
    env = os.environ.get('FLASK_ENV', 'development')
    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        # ... add other environment mappings ...
    }
    return config_map[env]