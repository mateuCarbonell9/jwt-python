from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from . import db
from .models import User
import jwt
import datetime
from config import Config  # Importamos la configuración
from flask_jwt_extended import jwt_required, get_jwt_identity

# Crear el blueprint para las rutas de usuario y autenticación
user_blueprint = Blueprint("user", __name__)


# Ruta para login
@user_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email_or_username = data.get("email_or_username")
    password = data.get("password")

    # Buscar usuario por email o username
    user = User.query.filter(
        (User.email == email_or_username) | (User.username == email_or_username)
    ).first()

    # Si el usuario no existe o la contraseña es incorrecta
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"message": "Credenciales inválidas"}), 401

    # Crear el token de acceso con 'identity' como string
    access_token = create_access_token(
        identity=str(user.id)
    )  # Aseguramos que sea una cadena

    return jsonify({"message": "Login exitoso", "access_token": access_token}), 200


@user_blueprint.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Obtener la identidad del usuario del JWT
    user_id = get_jwt_identity()

    return jsonify({"message": f"Bienvenido, usuario {user_id}!"}), 200


# Ruta para listar todos los usuarios
@user_blueprint.route("/users", methods=["GET"])
def user_list():
    users = User.query.all()
    return render_template("list.html", users=users)


# Ruta para crear un nuevo usuario
@user_blueprint.route("/create", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        # Obtener los datos del formulario
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Realizar el hash de la contraseña antes de guardarla
        password_hash = generate_password_hash(password)

        # Crear un nuevo usuario con el hash de la contraseña
        user = User(username=username, email=email, password_hash=password_hash)

        # Guardar el usuario en la base de datos
        db.session.add(user)
        db.session.commit()

        # Redirigir al detalle del usuario recién creado
        return redirect(url_for("user.user_detail", id=user.id))

    return render_template("create.html")


# Ruta para ver los detalles de un usuario específico
@user_blueprint.route("/user/<int:id>")
def user_detail(id):
    user = db.get_or_404(User, id)
    return render_template("detail.html", user=user)


# Ruta para eliminar un usuario
@user_blueprint.route("/user/<int:id>/delete", methods=["GET", "POST"])
def user_delete(id):
    user = db.get_or_404(
        User, id
    )  # Obtén el usuario por ID, o devuelve un error 404 si no existe.

    if request.method == "POST":
        db.session.delete(user)  # Elimina el usuario de la sesión.
        db.session.commit()  # Confirma los cambios en la base de datos.
        return redirect(url_for("user.user_list"))  # Redirige a la lista de usuarios.

    return render_template(
        "delete.html", user=user
    )  # Si es GET, muestra el formulario de confirmación.
