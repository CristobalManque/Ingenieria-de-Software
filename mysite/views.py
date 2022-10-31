from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from . import auth

bp = Blueprint('index', __name__)

@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
@auth.login_required
def index():
    return render_template("index.html")