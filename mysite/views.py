from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from . import auth

bp = Blueprint('index', __name__)

@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
@auth.login_required
def index():
    return render_template("index.html")@auth.login_required
def ingresarproducto():
    if request.method == 'POST':
        sku = request.form['sku']
        nombre = request.form['nombre']
        fecha = request.form['fecha']
        cantidad = request.form['cantidad']
        preciou = request.form['preciou']

        db = get_db()
        error = None

        if not sku:
            error = "La sku es requerida"
        elif not nombre:
            error = "El nombre es requerido"
        elif not fecha:
            error = "El fecha es requerido"
        elif not cantidad:
            error = "El cantidad es requerido"
        elif not preciou:
            error = "El preciou es requerido"

        if error is None:
            try:
                db.execute(
                    "INSERT INTO producto (sku, nombre, fechaentrega, cantidad, precioU) VALUES (?, ?, ?, ?, ?)",
                    (sku, nombre, fecha, cantidad, preciou),
                )
                db.commit()
            except:
                error = "Error"
                return render_template("ingresarproducto.html", error=error)
            else:
                return redirect(url_for("vista.inicio"))

    return render_template("ingresarproducto.html")

