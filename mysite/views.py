from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from flask_sqlalchemy import SQLAlchemy
from . import auth
from . import db
from mysite.db import read_db_row, read_db_col
from mysite.db import get_db

bp = Blueprint('vista', __name__)

@bp.route('/', methods=['GET'])
@auth.login_required
def inicio():
    if g.user['tipo'] == "cliente":
        return render_template("index.html", items = read_db_row("OCcliente"))
    else:
        return render_template("index.html", items = read_db_row("OCproveedor"))

@bp.route('/listaproductos', methods=['GET'])
@auth.login_required
def listaproductos():
    if g.user['tipo'] == "cliente":
        return render_template("listaproductos.html", items = db.read_db_row("producto"))

@bp.route('/ingresar', methods=('GET', 'POST'))
@auth.login_required
def ingresar():
    if request.method == 'POST':
        if g.user['tipo'] == "cliente":
            sku_p = request.form['sku_p']
            fecha = request.form['fecha']
            tmoneda = request.form['tmoneda']
            lugar = request.form['lugar']
            tpago = request.form['tpago']
        else:
            cliente = request.form['cliente']
            fecha = request.form['fecha']
            tmoneda = request.form['tmoneda']
            lugar = request.form['lugar']
            tpago = request.form['tpago']

        db = get_db()
        error = None

        if g.user['tipo'] == "cliente":
            if not sku_p:
                error = "error en sku"
            elif not fecha:
                error = "La fecha es requerida"
            elif not tmoneda:
                error = "El tipo de moneda es requerido"
            elif not lugar:
                error = "El lugar es requerido"
            elif not tpago:
                error = "El termino de pago es requerido"
        else:
            if not cliente:
                error = "Error en cliente"
            elif not fecha:
                error = "La fecha es requerida"
            elif not tmoneda:
                error = "El tipo de moneda es requerido"
            elif not lugar:
                error = "El lugar es requerido"
            elif not tpago:
                error = "El termino de pago es requerido"

        if error is None:
            try:
                if g.user['tipo'] == "cliente":
                    db.execute(
                        "INSERT INTO OCcliente (producto, fecha, tmoneda, lugar, tpago) VALUES (?, ?, ?, ?, ?)",
                        (sku_p, fecha, tmoneda, lugar, tpago),
                    )
                    db.commit()
                else:
                    db.execute(
                        "INSERT INTO OCproveedor (cliente, fecha, tmoneda, lugar, tpago) VALUES (?, ?, ?, ?, ?)",
                        (cliente, fecha, tmoneda, lugar, tpago),
                    )
                    db.commit()
            except:
                error = "Error"
                return render_template("ingresar.html", items = read_db_row("producto"), error=error)
            else:
                return redirect(url_for("vista.inicio"))

    if g.user['tipo'] == "cliente":
        return render_template("ingresar.html", items = read_db_row("producto"))
    else:
        return render_template("ingresar.html", items = read_db_row("OCcliente"))

@bp.route('/ingresarproducto', methods=('GET', 'POST'))
@auth.login_required
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

