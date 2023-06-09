import os  # Para acceder a variables de entorno
from flask import Flask


# Para poder crear varias instancias de nuestra
# app definimos la funcion donde se crea la app
def create_app():
    app = Flask(__name__)

    # Usamos las variables de entorno para configurar nuestra app
    app.config.from_mapping(
        # Llave para sesion de nuestra app (cookie)
        SECRET_KEY="somekey",
        DATABASE_HOST=os.environ.get("FLASK_DATABASE_HOST"),
        DATABASE_PASSWORD=os.environ.get("FLASK_DATABASE_PASSWORD"),
        DATABASE_USER=os.environ.get("FLASK_DATABASE_USER"),
        DATABASE=os.environ.get("FLASK_DATABASE"),
    )

    # Llamo a la funcion init_app para definir el teardown
    from . import db

    db.init_app(app)

    # Registro los Blueprints

    from . import auth
    from . import toDo

    app.register_blueprint(auth.bp)
    app.register_blueprint(toDo.bp)

    @app.route("/test", methods=["GET"])
    def test():
        return "test OK", 200

    return app
