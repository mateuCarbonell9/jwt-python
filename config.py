import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()


class Config:
    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI", "mysql+pymysql://root:root@localhost/prueba_flask"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración de JWT
    SECRET_KEY = os.getenv(
        "SECRET_KEY", "jwt-secret-key"
    )  # Puedes establecer una clave predeterminada, pero lo ideal es que esté en el .env
