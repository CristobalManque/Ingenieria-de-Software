import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        nombre = request.form['name']
        direccion = request.form['direccion']
        tel = request.form['tel']
        mail = request.form['mail']
        password = request.form['password']
        tipo = request.form['tipo']
        db = get_db()
        error = None

        if not nombre:
            error = "El nombre es requerido."
        elif not direccion:
            error = "La direccion es requerida."
        elif not tel:
            error = "El telefono es requerido."
        elif not mail:
            error = "El mail es requerido."
        elif not password:
            error = "La contraseña es requerida."
        elif not tipo:
            error = "El tipo es requerido"

        if error is None:
            try:
                db.execute(
                    "INSERT INTO usuario (nombre, direccion, telefono, correo, password, tipo) VALUES (?, ?, ?, ?, ?, ?)",
                    (nombre, direccion, tel, mail, generate_password_hash(password), tipo),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {mail} is already registered."
                return render_template("auth/register.html", error = error)
            else:
                return redirect(url_for("auth.login"))

    return render_template('auth/register.html')

    
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':

        mail = request.form['mail']
        password = request.form['password']

        db = get_db()

        error = None
        user = db.execute(
            'SELECT * FROM usuario WHERE correo = ?', (mail,)
        ).fetchone()

        if user is None:
            error = 'Correo incorrecto.'
        elif not check_password_hash(user['password'], password):
            error = 'Contraseña incorrecta.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('vista.inicio'))

        else:
            return render_template("auth/login.html", error = error)
    
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM usuario WHERE id = ?', (user_id,)
        ).fetchone()
        
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view



