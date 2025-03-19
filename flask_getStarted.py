from app import create_app, db
from app.models import (
    User,
)  # Importa los modelos después de que se ha creado la aplicación
from app.user_views import user_blueprint

app = create_app()
with app.app_context():
    db.create_all()  # Crea las tablas si no existen

app.register_blueprint(user_blueprint)
if __name__ == "__main__":
    app.run(debug=True)
