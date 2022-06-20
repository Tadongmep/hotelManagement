from flask import (
    Blueprint, flash, g, redirect, request, session, url_for, jsonify
)

from flaskr.auth import login_required

from flaskr.db import get_db

bp = Blueprint('admin', __name__)

@bp.route('/testConnectBackend', methods=('GET', 'POST'))
def notification():
    return jsonify({"foo": 1})

@bp.route('/hotelRegister', methods=('GET', 'POST'))
@login_required
def hotel_register():
    if g.user['position'] == 'admin' and request.method == 'POST': #suggest POST
        name = request.get_json().get('name')
        address = request.get_json().get('address')
        db = get_db()
        error = None

        if not name:
            error = "The hotel's name is required."
            return jsonify({'message': 'register failed. ' + error}), 200
        elif not address:
            error = "The hotel's adress is required."
            return jsonify({'message': 'register failed. ' + error}), 200
        
        if error is None:
            try:
                db.execute(
                    "INSERT INTO hotel (name, address) VALUES (@0, @1)",
                    (name, address),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Hotel {name} is already registered."
                return jsonify({'message': 'hotel register failed. ' + error}), 200 
            else:
                return jsonify({'message': 'hotel register successful'}), 201 
    else:
        return jsonify({'message': 'hotel register require admin acc or HTTP Methods wrong.'}), 200 
    return jsonify({'message': 'register failed'}), 400

@bp.route('/getHotel', methods=('GET', 'POST'))
@login_required
def get_hotel():
    if g.user['position'] == 'admin':
        message = []
        
        hotels = get_db().execute(
            'SELECT * FROM hotel'
        ).fetchall()
        for hotel in hotels:
            temp = {}
            temp['id'] = hotel['id']
            temp['name'] = hotel['name']
            temp['address'] = hotel['address']
            message.append(temp)

        return jsonify({'message': message}), 200
    
    return jsonify({'message': 'get hotel information failed, require admin acc'}), 200

@bp.route('/getRoom', methods=('GET', 'POST'))
@login_required
def get_room():
    if g.user['position'] == 'admin':
        message = []
        
        rooms = get_db().execute(
            'SELECT * FROM rooms'
        ).fetchall()
        for room in rooms:
            temp = {}
            temp['id'] = room['id']
            temp['belonging_to'] = room['belonging_to']
            temp['kind_of_room'] = room['kind_of_room']
            temp['room_name'] = room['room_name']
            temp['created'] = room['created']
            message.append(temp)

        return jsonify({'message': message}), 200
    
    return jsonify({'message': 'get room information failed, require admin acc'}), 200

@bp.route('/updateHotel', methods=('GET', 'POST'))
@login_required
def update_hotel():
    if g.user['position'] == 'admin' and request.method == 'POST':
        id = request.args.get('id')
        name = request.get_json().get('name')
        address = request.get_json().get('address')
        error = None

        if not name:
            error = 'Name is required.'
            return jsonify({'message': 'update failed. ' + error}), 200
        elif not address:
            error = 'address is required.'
            return jsonify({'message': 'update failed. ' + error}), 200

        if error is None:
            db = get_db()
            db.execute(
                'UPDATE hotel SET name = ?, address = ?'
                ' WHERE id = ?',
                (name, address, id)
            )
            db.commit()
            return jsonify({'message': 'update successful.'}), 200

    return jsonify({'message': 'update hotel information failed, require admin acc or HTTP Methods wrong.'}), 200

@bp.route('/deleteHotel', methods=('POST',))
@login_required
def delete_hotel():
    if g.user['position'] == 'admin' and request.method == 'POST':
        id = request.args.get('id')
        db = get_db()
        db.execute('DELETE FROM hotel WHERE id = ?', (id,))
        db.commit()
        return jsonify({'message': 'delete successful.'}), 200
    
    return jsonify({'message': 'delete hotel information failed, require admin acc or HTTP Methods wrong.'}), 200

@bp.route('/createRoom', methods=('GET', 'POST'))
@login_required
def create_room():
    if g.user['position'] == 'admin' and request.method == 'POST': #suggest POST
        belonging_to = request.get_json().get('belonging_to')
        kind_of_room = request.get_json().get('kind_of_room')
        room_name = request.get_json().get('room_name')
        error = None

        if not belonging_to:
            error = "Hotel's name is required."
            return jsonify({'message': error}), 200
        elif not kind_of_room:
            error = 'Kind is required.'
            return jsonify({'message': error}), 200
        elif not room_name:
            error = "Room's name is required."
            return jsonify({'message': error}), 200
        elif belonging_to:
            hotel = get_db().execute(
                'SELECT * FROM hotel WHERE name = ?', (belonging_to,)
            ).fetchone()
            if hotel is None:
                error = 'Hotel is not exsit.'
                return jsonify({'message': error}), 200

        if error is None:
            db = get_db()
            db.execute(
                'INSERT INTO rooms (belonging_to, kind_of_room, room_name)'
                ' VALUES (@0, @1, @2)',
                (belonging_to, kind_of_room, room_name)
            )
            db.commit()
            return jsonify({'message': 'room created.'}), 201

    return jsonify({'message': 'room create failed, require admin acc'}), 200

@bp.route('/updateRoom', methods=('GET', 'POST'))
@login_required
def update_room():
    if g.user['position'] == 'admin' and request.method == 'POST':
        id = request.args.get('id')
        belonging_to = request.get_json().get('belonging_to')
        kind_of_room = request.get_json().get('kind_of_room')
        room_name = request.get_json().get('room_name')
        error = None
        if room_name:
            room = get_db().execute(
                'SELECT * FROM rooms WHERE room_name = ?', (room_name,)
            ).fetchone()
            if str(room['id']) != id:
                error = "Room's name is exsit."
                return jsonify({'message': error}), 200
        if not belonging_to:
            error = "Hotel's name is required."
            return jsonify({'message': error}), 200
        elif not kind_of_room:
            error = 'Kind is required.'
            return jsonify({'message': error}), 200
        elif not room_name:
            error = "Room's name is required."
            return jsonify({'message': error}), 200
        elif belonging_to:
            hotel = get_db().execute(
                'SELECT * FROM hotel WHERE name = ?', (belonging_to,)
            ).fetchone()
            if hotel is None:
                error = 'Hotel is not exsit.'
                return jsonify({'message': error}), 200

        if error is None:
            db = get_db()
            db.execute(
                'UPDATE rooms SET belonging_to = ?, kind_of_room = ?, room_name = ?'
                ' WHERE id = ?',
                (belonging_to, kind_of_room, room_name, id)
            )
            db.commit()
            return jsonify({'message': 'update successful.'}), 200

    return jsonify({'message': 'update room information failed, require admin acc or HTTP Methods wrong.'}), 200

@bp.route('/deleteRoom', methods=('POST',))
@login_required
def delete_room():
    if g.user['position'] == 'admin' and request.method == 'POST':
        id = request.args.get('id')
        db = get_db()
        db.execute('DELETE FROM rooms WHERE id = ?', (id,))
        db.commit()
        return jsonify({'message': 'delete successful.'}), 200
    
    return jsonify({'message': 'delete room information failed, require admin acc or HTTP Methods wrong.'}), 200
