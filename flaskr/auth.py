import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.args.get('username')
        password = request.args.get('password')
        name = request.args.get('name')
        phone = request.args.get('phone')
        working_at = request.args.get('working_at')
        position = request.args.get('position')
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
            return jsonify({'message': 'register failed. ' + error}), 200
        elif not password:
            error = 'Password is required.'
            return jsonify({'message': 'register failed. ' + error}), 200
        elif not name:
            error = 'Name is required.'
            return jsonify({'message': 'register failed. ' + error}), 200
        elif not phone:
            error = 'Phone is required.'
            return jsonify({'message': 'register failed. ' + error}), 200
        elif not working_at:
            error = 'Work place is required.'
            return jsonify({'message': 'register failed. ' + error}), 200
        elif not position:
            error = 'Position is required.'
            return jsonify({'message': 'register failed. ' + error}), 200
        elif working_at:
            hotel = db.execute(
                'SELECT * FROM hotel WHERE name = ?', (working_at,)
            ).fetchone()
            if hotel is None:
                error = "The hotel's name is not exsit, contact admin for help."

        if error is None:
            try:
                db.execute(
                    "INSERT INTO account (username, password, name, phone, working_at, position) VALUES (@0, @1, @2, @3, @4, @5)",
                    (username, password, name, phone, working_at, position),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return jsonify({'message': 'register successful'}), 201 #redirect(url_for("auth.login"))

        flash(error)

    return jsonify({'message': 'register failed. Reqire POST method'}), 400 #render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST': #suggest POST 
        username = request.args.get('username')
        password = request.args.get('password')
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM account WHERE username = @0', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
            return jsonify({'message': 'login failed. ' + error}), 200
        elif password is None:
        # not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
            return jsonify({'message': 'login failed. ' + error}), 200

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return jsonify({'message': 'login successful'}), 200
            #return redirect(url_for('index'))

        flash(error)

    return jsonify({'message': 'login failed.'}), 400 #render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM account WHERE id = @0', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return jsonify({'message': 'logout successful'}), 200
    
    # redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return jsonify({'message': 'you have not login yet'}), 200   #return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view