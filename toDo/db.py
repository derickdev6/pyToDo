import mysql.connector
import click  # Para ejecutar comandos en terminal
from flask import (
    current_app,
    g,
)  # g es una variable que se mantiene en toda la app, la usaremos para almacenar el usuario
from flask.cli import with_appcontext  # Para acceder a variables de la config de app
from .schema import instructions


# Si g no contiene db, creo el objeto db con las variables de entorno y lo retorno junto con el cursor
def get_db():
    if "db" not in g:
        g.db = mysql.connector.connect(
            host=current_app.config["DATABASE_HOST"],
            user=current_app.config["DATABASE_USER"],
            password=current_app.config["DATABASE_PASSWORD"],
            database=current_app.config["DATABASE"],
        )
        g.c = g.db.cursor(dictionary=True)
    return g.db, g.c


# Extrae la db de g y si su valor es distinto de none, cierra la conexion
def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db, c = get_db()

    for i in instructions:
        c.execute(i)

    db.commit()


# Inicia la base de datos
@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Database initialized")


# Define que cuando se haga termine de ejecutar la peticion llama la funcion close_db
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
