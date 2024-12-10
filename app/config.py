class Config:
    """Основные настройки"""

    SECRET_KEY = "your-secret-key"
    DEBUG = True
    DATABASE_URI = "app/app.db"
    ADMIN_TEMPLATE_MODE = "bootstrap3"  # bootstrap2, bootstrap3, bootstrap4


config = Config()
