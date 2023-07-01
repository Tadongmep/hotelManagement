from flask import (
    Blueprint, flash, g, redirect, request, session, url_for, jsonify
)

from flaskr.auth import login_required

from flaskr.db import get_db

import datetime

bp = Blueprint('operationReceptionist', __name__)

@bp.route('/getRoomInformation', methods=('GET', 'POST'))
@login_required
def get_room_information():
    message = 'something wrong!'
    id = None
    if request.args.get('id'):
        id = request.args.get('id')
    if g.user['position'] == 'receptionist' and request.method == 'GET':
    # print(g.user['working_at'])
        message = []

        working_at = g.user['working_at']
        room = None
        if id:
            rooms = get_db().execute(
                    'SELECT * FROM rooms WHERE belonging_to = @0 and id = @1', (working_at, id)
                ).fetchall()
        else:
            rooms = get_db().execute(
                    'SELECT * FROM rooms WHERE belonging_to = @0', (working_at,)
                ).fetchall()
        for room in rooms:
            temp = {}
            temp['id'] = room['id']
            temp['kind_of_room'] = room['kind_of_room']
            temp['room_name'] = room['room_name']
            temp['status'] = room['status']
            temp['guest_name'] = room['guest_name']
            temp['more_infor'] = room['more_infor']
            message.append(temp)

        return jsonify({'message': message}), 200
    return jsonify({'message': message}), 200

@bp.route('/updateRoomInformation', methods=('GET', 'POST'))
@login_required
def update_room():
    if g.user['position'] == 'receptionist' and request.method == 'POST':
        id = request.args.get('id')
        status = request.get_json().get('status')
        guest_name = request.get_json().get('guest_name')
        more_infor = request.get_json().get('more_infor')
        error = None
        
        if not status:
            error = "status is required."
            return jsonify({'message': error}), 200
        elif not guest_name:
            error = 'guest name is required.'
            return jsonify({'message': error}), 200

        if error is None:
            db = get_db()
            db.execute(
                'UPDATE rooms SET status = ?, guest_name = ?, more_infor = ?'
                ' WHERE id = ?',
                (status, guest_name, more_infor, id)
            )
            db.commit()
            return jsonify({'message': 'update successful.'}), 200

    return jsonify({'message': 'update room information failed, require admin acc or HTTP Methods wrong.'}), 200
