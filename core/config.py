from passlib.context import CryptContext
from datetime import datetime, timedelta


class Settings:
    # Obtenir la date et l'heure actuelles
    now = datetime.now()

    # Obtenir la date et l'heure du début de la journée
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)

    # Calculer la différence entre la fin de la journée et l'heure actuelle
    time_left = start_of_day + timedelta(days=1) - now

    # Convertir le temps restant en minutes
    minutes_left = time_left.total_seconds() // 60

    PROJECT_NAME: str = "Squelette"
    PROJECT_VERSION: str = "0.0.0"
    # DATABASE_URL: str = "postgresql://postgres:root@localhost/ats_db"
    DATABASE_URL: str = "postgresql://root:root@localhost/ats_db"
    SECRET_KEY = ""
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = minutes_left
    PWD_CONTEXT = pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


settings = Settings()
