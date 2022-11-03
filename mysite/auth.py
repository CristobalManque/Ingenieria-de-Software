import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from mysite.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        correo = request.form['correo']
        clave = request.form['clave']
        tipo = request.form['tipo']
        db = get_db()
        error = None

        if not nombre:
            error = 'El nombre es requerido.'
        elif not direccion:
            error ='La dirección es requerida.'
        elif not telefono:
            error ='El teléfono es requerido.'
        elif not correo:
            error ='El correo es requerido.'
        elif not clave:
            error = 'La clave es requerida.'
        elif not tipo:
            error = 'El tipo es requerido.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO usuario (nombre, direccion, telefono, correo, clave, tipo) VALUES (?, ?, ?, ?, ?, ?)",
                    (nombre,direccion,telefono,correo, generate_password_hash(clave),tipo))
                db.commit()
            except db.IntegrityError:
                error = "El correo ya se encuentra registrado."
                return render_template('auth/register.html', err = error)
            else:
                return redirect(url_for("auth.login"))
        
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        clave = request.form['clave']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM usuario WHERE correo = ?', (correo,)
        ).fetchone()

        if user is None:
            error = 'Incorrect correo.'
        elif not check_password_hash(user['clave'], clave):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index.index'))

        flash(error)

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