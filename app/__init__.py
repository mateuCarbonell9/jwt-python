from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config
import mysql.connector

# Inicialización de la base de datos
db = SQLAlchemy()

# Creación de la instancia de Migrate
migrate = Migrate()

# Instancia de JWTManager para la gestión de tokens JWT
jwt = JWTManager()


def create_db():
    """Función para crear la base de datos si no existe"""
    config = {
        "user": "root",
        "password": "root",
        "host": "localhost",
    }

    try:
        # Conectar al servidor de MySQL
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Intentar crear la base de datos
        cursor.execute("CREATE DATABASE IF NOT EXISTS prueba_flask")
        print("Base de datos creada o ya existe.")
    except mysql.connector.Error as err:
        print(f"Error al crear la base de datos: {err}")
    finally:
        cursor.close()
        conn.close()


def create_app():
    # Llamamos a la función para crear la base de datos antes de iniciar la app
    create_db()

    # Crear la instancia de Flask
    app = Flask(__name__)
    app.config.from_object(
        Config
    )  # Cargar las configuraciones desde el archivo config.py

    # Inicializar Migrate, JWT y la base de datos
    migrate.init_app(app, db)
    jwt.init_app(app)  # Inicializar JWT

    # Configuración de la base de datos
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mysql+pymysql://root:root@localhost/prueba_flask"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializamos la base de datos
    db.init_app(app)

    return app
