from flask import (
    Blueprint, flash, g, redirect, request, session, url_for, jsonify
)

from flaskr.auth import login_required

from flaskr.db import get_db

import datetime

bp = Blueprint('humanResource', __name__)

@bp.route('/getRosterByDay', methods=('GET', 'POST'))
def get_roster():
    message = []
    date = request.get_json().get('date')
    #print(type(date))
    if date is None:
        return jsonify({'message': 'date is require.'}), 200
    else:
        rosters = get_db().execute(
            'SELECT * FROM roster WHERE date = ?',
            (date,)
        ).fetchall()
        for roster in rosters:
            temp = {}
            temp['id'] = roster['id']
            temp['position'] = roster['position']
            temp['staff_id'] = roster['staff_id']
            temp['staff_name'] = roster['staff_name']
            temp['start_time'] = roster['start_time']
            temp['work_hour'] = roster['work_hour']
            temp['date'] = roster['date']
            temp['created_by_id'] = roster['created_by_id']
            message.append(temp)
    return jsonify({'message': message}), 200

def add_to_monitor(position, staff_execute_id, created_by_id):
    posititons = [
        'gardener',
        'baby sitter',
        'public area cleaner',
        'door man',
        'cook assistant',
        'bartender',
        'food runner',
        'steward',
        ]
    if position in posititons and staff_execute_id and created_by_id is not None:
        query = position
        if position == 'baby sitter':
            query = "baby_sitter"
        elif position == 'public area cleaner':
            query = "public_area_cleaner"
        elif position == 'door man':
            query = "door_man"
        elif position == 'cook assistant':
            query = "cook_assistant"
        elif position == 'food runner':
            query = "food_runner"
            
        get_db().execute(
        "INSERT INTO " + query + "_monitoring (staff_execute_id, created_by_id) VALUES (@0, @1)",
        (staff_execute_id, created_by_id),
        )
        get_db().commit()
    else:
        pass
    return jsonify({'message': "added"}), 200

@bp.route('/createRoster', methods=('GET', 'POST'))
@login_required
def create_roster():
    # request_data = request.get_json()['work_hour'] # get_json get data from body like using postman while .args.get is get data from url parameter
    # print(g.user['id'])
    if g.user['position'] == 'human resource' and request.method == 'POST':
        position = request.get_json().get('position')
        staff_id = request.get_json().get('staff_id').strip()
        staff_name = request.get_json().get('staff_name')
        start_time = request.get_json().get('start_time').strip()
        work_hour = request.get_json().get('work_hour').strip()
        date = request.get_json().get('date').strip()
        report = request.get_json().get('report')
        created_by_id = str(g.user['id'])
        db = get_db()
        error = None
        
        if not position or len(position) == 0:
            error = "Position is required."
            return jsonify({'message': 'create failed. ' + error}), 200
        elif not staff_id or len(staff_id) == 0:
            error = "Staff's identifier is required. In case the name is duplicate."
            return jsonify({'message': 'create failed. ' + error}), 200
        elif not staff_name or len(staff_name) == 0:
            error = "Staff's name is required."
            return jsonify({'message': 'create failed. ' + error}), 200
        elif not start_time or len(start_time) == 0:
            error = "Start time is required."
            return jsonify({'message': 'create failed. ' + error}), 200
        elif not work_hour or len(work_hour) == 0:
            error = "Work hour is required."
            return jsonify({'message': 'create failed. ' + error}), 200
        elif not date or len(date) == 0:
            error = "Date is required."
            return jsonify({'message': 'create failed. ' + error}), 200
        elif not created_by_id:
            error = "Creator's id is required."
            return jsonify({'message': 'create failed. ' + error}), 200
        if staff_id and staff_name and position:
            employee = get_db().execute(
                'SELECT * FROM account WHERE id=?',
                (staff_id,),
            ).fetchone()
            if (employee['name'] != staff_name) or (employee['position'] != position):
                error = "Employee's information is not match."
                return jsonify({'message': 'create failed. ' + error}), 200
        
        if error is None:
            roster = get_db().execute(
                'SELECT * FROM roster WHERE staff_id=? AND start_time=? AND work_hour=? AND date=?',
                (staff_id, start_time, work_hour, date),
                ).fetchone()
            if roster:
                return jsonify({'message': 'create failed. Duplicate information.'}), 200
            else:
                try:
                    db.execute(
                        "INSERT INTO roster (position, staff_id, staff_name, start_time, work_hour, date, report, created_by_id) VALUES (@0, @1, @2, @3, @4, @5, @6, @7)",
                        (position, staff_id, staff_name, start_time, work_hour, date, report, created_by_id),
                    )
                    db.commit()
                    add_to_monitor(position, staff_id, created_by_id)
                    # get_db().execute(
                    #     "INSERT INTO " + position + "_monitoring (staff_execute_id, created_by_id) VALUES (@0, @1)",
                    #     (staff_id, created_by_id),
                    #     )
                    # get_db().commit()
                except db.IntegrityError:
                    error = f"It is already created."
                    return jsonify({'message': 'Create failed. ' + error}), 200 
                else:
                    return jsonify({'message': 'Create successful'}), 201 
    else:
        return jsonify({'message': 'Create require human resource acc.'}), 200 
    return jsonify({'message': 'create failed'}), 400

@bp.route('/updateRoster', methods=('GET', 'POST'))
@login_required
def update_roster():
    if g.user['position'] == 'human resource' and request.method == 'POST':
        id = request.args.get('id')
        position = request.get_json().get('position')
        staff_id = request.get_json().get('staff_id').strip()
        staff_name = request.get_json().get('staff_name')
        start_time = request.get_json().get('start_time').strip()
        work_hour = request.get_json().get('work_hour').strip()
        date = request.get_json().get('date').strip()
        report = request.get_json().get('report')
        created_by_id = str(g.user['id'])
        db = get_db()
        error = None

        
        if not position or len(position) == 0:
            error = "Position is required."
            return jsonify({'message': 'update failed. ' + error}), 200
        if id is None:
            error = "Id is required. In case the name is duplicate."
            return jsonify({'message': 'update failed. ' + error}), 200
        elif not staff_id or len(staff_id) == 0:
            error = "Staff's identifier is required. In case the name is duplicate."
            return jsonify({'message': 'update failed. ' + error}), 200
        elif not staff_name or len(staff_name) == 0:
            error = "Staff's name is required."
            return jsonify({'message': 'update failed. ' + error}), 200
        elif not start_time or len(start_time) == 0:
            error = "Start time is required."
            return jsonify({'message': 'update failed. ' + error}), 200
        elif not work_hour or len(work_hour) == 0:
            error = "Work hour is required."
            return jsonify({'message': 'update failed. ' + error}), 200
        elif not date or len(date) == 0:
            error = "Date is required."
            return jsonify({'message': 'update failed. ' + error}), 200
        elif not created_by_id:
            error = "Creator's id is required."
            return jsonify({'message': 'update failed. ' + error}), 200
        if staff_id and staff_name and position:
            employee = get_db().execute(
                'SELECT * FROM account WHERE id=?',
                (staff_id,),
            ).fetchone()
            if employee['name'] != staff_name and employee['position'] !=position:
                error = "Employee's information is not match."
                return jsonify({'message': 'update failed. ' + error}), 200

        if error is None:
            roster = get_db().execute(
                'SELECT * FROM roster WHERE position=? AND staff_name=? AND staff_id=? AND start_time=? AND work_hour=? AND date=?',
                (position, staff_name, staff_id, start_time, work_hour, date),
                ).fetchone()
            if roster and str(roster['id']) != id:
                return jsonify({'message': 'create failed. Duplicate information.'}), 200
            elif roster is None:
                db = get_db()
                db.execute(
                    'UPDATE roster SET position = ?, staff_id = ?, staff_name = ?, start_time = ?, work_hour = ?, date = ?, report = ?'
                    ' WHERE id = ?',
                    (position, staff_id, staff_name, start_time, work_hour, date, report, id)
                )
                db.commit()
                return jsonify({'message': 'update successful.'}), 200
    elif request.method == 'POST':
        return jsonify({'message': 'update roster information failed, require human resource acc'}), 200
    return jsonify({'message': 'update failed'}), 400

@bp.route('/deleteRoster', methods=('POST',))
@login_required
def delete_roster():
    if g.user['position'] == 'human resource' and request.method == 'POST':
        id = request.args.get('id')
        db = get_db()
        db.execute('DELETE FROM roster WHERE id = ?', (id,))
        db.commit()
        return jsonify({'message': 'delete successful.'}), 200
    
    return jsonify({'message': 'delete roster information failed, require human resource acc'}), 200
  

####################################Note#####################################
# status co 4 trang thai: Not processed yet, processing, done, cancel
# lan luot cho 4 trang thai la chua xu li, dang xu li, da xu li xong, Huy

@bp.route('/createLaundryJob', methods=('GET', 'POST'))
@login_required
def create_laundry_job():
    if g.user['position'] == 'human resource' and request.method == 'POST':
        belonging_room_id = request.get_json().get('belonging_room_id').strip()
        status = request.get_json().get('status')
        staff_execute_id = request.get_json().get('staff_execute_id').strip()
        note = request.get_json().get('note')
        created_by_id = str(g.user['id'])
        db = get_db()
        error = None
        current_date = str(datetime.datetime.now().day) + "/" + str(datetime.datetime.now().month) + "/" + str(datetime.datetime.now().year)

        if not belonging_room_id:
            error = "Room is required."
            return jsonify({'message': 'create failed. ' + error}), 200
        elif not status:
            error = "Status is required. In case the name is duplicate."
            return jsonify({'message': 'create failed. ' + error}), 200
        elif not staff_execute_id:
            error = "Staff's identifier is required."
            return jsonify({'message': 'create failed. ' + error}), 200
        elif not created_by_id:
            error = "Creator's id is required."
            return jsonify({'message': 'create failed. ' + error}), 200
        if belonging_room_id:
            hotel = get_db().execute(
                    'SELECT * FROM account WHERE id=?',
                    (created_by_id,),
                    ).fetchone()
            room = get_db().execute(
                    'SELECT * FROM rooms WHERE id=? AND belonging_to = ?',
                    (belonging_room_id, hotel['working_at'],),
                    ).fetchone()
            if not room:
                error = "Room's id is not belong to hotel."
                return jsonify({'message': 'update failed. ' + error}), 200
        if staff_execute_id:
            position = get_db().execute(
                    'SELECT * FROM account WHERE id=?',
                    (staff_execute_id,),
                    ).fetchone()
            if position['position'] != "laundry":
                error = "Employee do not work for this position."
                return jsonify({'message': 'Create failed. ' + error}), 200


        if error is None:
            laundry = get_db().execute(
                'SELECT * FROM laundry_monitoring WHERE belonging_room_id=? AND staff_execute_id=? AND created_by_id=?',
                (belonging_room_id, staff_execute_id, created_by_id),
                ).fetchone()
            print(type(laundry))
            if laundry:
                roster = get_db().execute(
                    'SELECT * FROM roster WHERE staff_id=? AND date = ?',
                    (staff_execute_id, current_date,),
                    ).fetchone()
                print('have',type(roster))
                if roster is None:
                    return jsonify({'message': 'create failed. Employee is not exsit in roster.'}), 200
                if laundry['status'] == 'Not processed yet':
                    return jsonify({'message': 'create failed. Duplicate information.'}), 200
                return jsonify({'message': 'create failed. Duplicate information.'}), 200
            else:
                roster = get_db().execute(
                    'SELECT * FROM roster WHERE staff_id=? AND date = ?',
                    (staff_execute_id, current_date,),
                    ).fetchone()
                if roster is None:
                    return jsonify({'message': 'create failed. Employee is not exsit in roster.'}), 200
                try:
                    db.execute(
                        "INSERT INTO laundry_monitoring (belonging_room_id, status, staff_execute_id, note , created_by_id) VALUES (@0, @1, @2, @3, @4)",
                        (belonging_room_id, status, staff_execute_id, note , created_by_id),
                    )
                    db.commit()
                except db.IntegrityError:
                    error = f"It is already created."
                    return jsonify({'message': 'Create failed. ' + error}), 200 
                else:
                    return jsonify({'message': 'Create successful'}), 201 
    else:
        return jsonify({'message': 'Create require human resource acc.'}), 200 
    return jsonify({'message': 'create failed'}), 400

@bp.route('/updateLaundryJob', methods=('GET', 'POST'))
@login_required
def update_laundry_job():
    if g.user['position'] == 'human resource' and request.method == 'POST':
        id = request.args.get('id')
        belonging_room_id = request.get_json().get('belonging_room_id').strip()
        status = request.get_json().get('status')
        staff_execute_id = request.get_json().get('staff_execute_id').strip()
        note = request.get_json().get('note')
        created_by_id = str(g.user['id'])
        db = get_db()
        error = None
        current_date = str(datetime.datetime.now().day) + "/" + str(datetime.datetime.now().month) + "/" + str(datetime.datetime.now().year)

        if id is None:
            error = "Id is required. In case the name is duplicate."
            return jsonify({'message': 'update failed. ' + error}), 200
        if not belonging_room_id:
            error = "Room is required."
            return jsonify({'message': 'update failed. ' + error}), 200
        elif not status:
            error = "Status is required. In case the name is duplicate."
            return jsonify({'message': 'update failed. ' + error}), 200
        elif not staff_execute_id:
            error = "Staff's identifier is required."
            return jsonify({'message': 'update failed. ' + error}), 200
        elif not created_by_id:
            error = "Creator's id is required."
            return jsonify({'message': 'update failed. ' + error}), 200
        if belonging_room_id:
            hotel = get_db().execute(
                    'SELECT * FROM account WHERE id=?',
                    (created_by_id,),
                    ).fetchone()
            room = get_db().execute(
                    'SELECT * FROM rooms WHERE id=? AND belonging_to = ?',
                    (belonging_room_id, hotel['working_at'],),
                    ).fetchone()
            if not room:
                error = "Room's id is not belong to hotel."
                return jsonify({'message': 'update failed. ' + error}), 200
        if staff_execute_id:
            position = get_db().execute(
                    'SELECT * FROM account WHERE id=?',
                    (staff_execute_id,),
                    ).fetchone()
            if position['position'] != "laundry":
                error = "Employee do not work for this position."
                return jsonify({'message': 'Create failed. ' + error}), 200
            
        if error is None:
            roster = get_db().execute(
                    'SELECT * FROM roster WHERE staff_id=? AND date = ?',
                    (staff_execute_id, current_date,),
                    ).fetchone()
            if roster is None:
                return jsonify({'message': 'update failed. Employee is not exsit in roster.'}), 200
            try:
                db.execute(
                    'UPDATE laundry_monitoring SET belonging_room_id = ?, status = ?, staff_execute_id = ?, note = ?, created_by_id = ?'
                    ' WHERE id = ?',
                    (belonging_room_id, status, staff_execute_id, note, created_by_id, id),
                )
                db.commit()
            except db.IntegrityError:
                error = f"It is already created."
                return jsonify({'message': 'update failed. ' + error}), 200 
            else:
                return jsonify({'message': 'update successful'}), 201
                
    else:
        return jsonify({'message': 'update require human resource acc.'}), 200 
    return jsonify({'message': 'update failed'}), 400

@bp.route('/deleteLaundryJob', methods=('GET', 'POST'))
@login_required
def delete_laundry_job():
    if g.user['position'] == 'human resource' and request.method == 'POST':
        id = request.args.get('id')
        db = get_db()
        db.execute('DELETE FROM laundry_monitoring WHERE id = ?', (id,))
        db.commit()
        return jsonify({'message': 'delete successful.'}), 200
    
    return jsonify({'message': 'delete roster information failed, require human resource acc'}), 200

####################################Note####################################
# chuc nang dang can nhac de them

@bp.route('/createGardener', methods=('GET', 'POST'))
@login_required
def create_gardener_job():
    if g.user['position'] == 'human resource' and request.method == 'POST':
        staff_execute_id = request.get_json().get('staff_execute_id')
        note = request.get_json().get('status')
        created_by_id = str(g.user['id'])
        db = get_db()
        error = None

        if not staff_execute_id:
            error = "Staff's identifier is required."
            return jsonify({'message': 'create failed. ' + error}), 200
        elif not created_by_id:
            error = "Creator's id is required."
            return jsonify({'message': 'create failed. ' + error}), 200
        
        if error is None:
            roster = get_db().execute(
                'SELECT * FROM roster WHERE staff_id=?',
                (staff_execute_id,),
                ).fetchone()
            if roster is None:
                    return jsonify({'message': 'create failed. Employee is not exsit in roster.'}), 200
            try:
                db.execute(
                    "INSERT INTO gardener_monitoring (staff_execute_id, note, created_by_id) VALUES (@0, @1, @2)",
                    (staff_execute_id, note, created_by_id),
                )
                db.commit()
            except db.IntegrityError:
                error = f"It is already created."
                return jsonify({'message': 'Create failed. ' + error}), 200 
            else:
                return jsonify({'message': 'Create successful'}), 201 
    else:
        return jsonify({'message': 'Create require human resource acc.'}), 200 
    return jsonify({'message': 'create failed'}), 400

@bp.route('/updateGardener', methods=('GET', 'POST'))
@login_required
def update_gardener_job():
    if g.user['position'] == 'human resource' and request.method == 'POST':
        id = request.args.get('id')
        staff_execute_id = request.get_json().get('staff_execute_id')
        status = request.get_json().get('status')
        created_by_id = str(g.user['id'])
        db = get_db()
        error = None

        if id is None:
            error = "Id is required. In case the name is duplicate."
            return jsonify({'message': 'update failed. ' + error}), 200
        if not staff_execute_id:
            error = "Staff's identifier is required."
            return jsonify({'message': 'update failed. ' + error}), 200
        elif not status:
            error = "Status is required. In case the name is duplicate."
            return jsonify({'message': 'update failed. ' + error}), 200
        elif not created_by_id:
            error = "Creator's id is required."
            return jsonify({'message': 'update failed. ' + error}), 200
        
        if error is None:
            roster = get_db().execute(
                'SELECT * FROM roster WHERE staff_id=?',
                (staff_execute_id,),
                ).fetchone()
            if roster is None:
                    return jsonify({'message': 'update failed. Employee is not exsit in roster.'}), 200
            try:
                db.execute(
                    'UPDATE gardener_monitoring SET staff_execute_id = ?, status = ?, created_by_id = ?'
                    ' WHERE id = ?',
                    (staff_execute_id, status, created_by_id, id),
                )
                db.commit()
            except db.IntegrityError:
                error = f"It is already created."
                return jsonify({'message': 'update failed. ' + error}), 200 
            else:
                return jsonify({'message': 'update successful'}), 201 
    else:
        return jsonify({'message': 'update require human resource acc.'}), 200 
    return jsonify({'message': 'update failed'}), 400

@bp.route('/deleteGardenerJob', methods=('GET', 'POST'))
@login_required
def delete_gardener_job():
    if g.user['position'] == 'human resource' and request.method == 'POST':
        id = request.args.get('id')
        db = get_db()
        db.execute('DELETE FROM gardener_monitoring WHERE id = ?', (id,))
        db.commit()
        return jsonify({'message': 'delete successful.'}), 200
    
    return jsonify({'message': 'delete information failed, require human resource acc'}), 200

#############################################################################################

@bp.route('/createBellManJob', methods=('GET', 'POST'))
@login_required
def create_bell_man_job():
    if g.user['position'] == 'human resource' and request.method == 'POST':
        belonging_room_id = request.get_json().get('belonging_room_id').strip()
        status = request.get_json().get('status')
        staff_execute_id = request.get_json().get('staff_execute_id').strip()
        note = request.get_json().get('note')
        created_by_id = str(g.user['id'])
        db = get_db()
        error = None
        current_date = str(datetime.datetime.now().day) + "/" + str(datetime.datetime.now().month) + "/" + str(datetime.datetime.now().year)

        if not belonging_room_id:
            error = "Room is required."
            return jsonify({'message': 'create failed. ' + error}), 200
        elif not status:
            error = "Status is required. In case the name is duplicate."
            return jsonify({'message': 'create failed. ' + error}), 200
        elif not staff_execute_id:
            error = "Staff's identifier is required."
            return jsonify({'message': 'create failed. ' + error}), 200
        elif not created_by_id:
            error = "Creator's id is required."
            return jsonify({'message': 'create failed. ' + error}), 200
        if belonging_room_id:
            hotel = get_db().execute(
                    'SELECT * FROM account WHERE id=?',
                    (created_by_id,),
                    ).fetchone()
            room = get_db().execute(
                    'SELECT * FROM rooms WHERE id=? AND belonging_to = ?',
                    (belonging_room_id, hotel['working_at'],),
                    ).fetchone()
            if not room:
                error = "Room's id is not belong to hotel."
                return jsonify({'message': 'create failed. ' + error}), 200
        if staff_execute_id:
            position = get_db().execute(
                    'SELECT * FROM account WHERE id=?',
                    (staff_execute_id,),
                    ).fetchone()
            
            if position['position'] != "bell man":
                error = "Employee do not work for this position."
                return jsonify({'message': 'Create failed. ' + error}), 200


        if error is None:
            bellman = get_db().execute(
                'SELECT * FROM bell_man_monitoring WHERE belonging_room_id=? AND staff_execute_id=? AND created_by_id=?',
                (belonging_room_id, staff_execute_id, created_by_id),
                ).fetchone()
            if bellman is not None:
                roster = get_db().execute(
                    'SELECT * FROM roster WHERE staff_id=? AND date=?',
                    (staff_execute_id, current_date ,),
                    ).fetchone()
                if roster is None:
                    return jsonify({'message': 'create failed. Employee is not exsit in roster.'}), 200
                if bellman['status'] == 'Not processed yet':
                    return jsonify({'message': 'create failed. Duplicate information.'}), 200
                return jsonify({'message': 'create failed. Duplicate information.'}), 200
            else:
                roster = get_db().execute(
                    'SELECT * FROM roster WHERE staff_id=? AND date=?',
                    (staff_execute_id, current_date ,),
                    ).fetchone()
                if roster is None:
                    return jsonify({'message': 'create failed. Employee is not exsit in roster.'}), 200
                try:
                    db.execute(
                        "INSERT INTO bell_man_monitoring (belonging_room_id, status, staff_execute_id, note , created_by_id) VALUES (@0, @1, @2, @3, @4)",
                        (belonging_room_id, status, staff_execute_id, note , created_by_id),
                    )
                    db.commit()
                except db.IntegrityError:
                    error = f"It is already created."
                    return jsonify({'message': 'Create failed. ' + error}), 200 
                else:
                    return jsonify({'message': 'Create successful'}), 201 
    else:
        return jsonify({'message': 'Create require human resource acc.'}), 200 
    return jsonify({'message': 'create failed'}), 400

@bp.route('/updateBellManJob', methods=('GET', 'POST'))
@login_required
def update_bell_man_job():
    if g.user['position'] == 'human resource' and request.method == 'POST':
        id = request.args.get('id')
        belonging_room_id = request.get_json().get('belonging_room_id').strip()
        status = request.get_json().get('status')
        staff_execute_id = request.get_json().get('staff_execute_id').strip()
        note = request.get_json().get('note')
        created_by_id = str(g.user['id'])
        db = get_db()
        error = None
        current_date = str(datetime.datetime.now().day) + "/" + str(datetime.datetime.now().month) + "/" + str(datetime.datetime.now().year)

        if id is None:
            error = "Id is required. In case the name is duplicate."
            return jsonify({'message': 'update failed. ' + error}), 200
        if not belonging_room_id:
            error = "Room is required."
            return jsonify({'message': 'update failed. ' + error}), 200
        elif not status:
            error = "Status is required. In case the name is duplicate."
            return jsonify({'message': 'update failed. ' + error}), 200
        elif not staff_execute_id:
            error = "Staff's identifier is required."
            return jsonify({'message': 'update failed. ' + error}), 200
        elif not created_by_id:
            error = "Creator's id is required."
            return jsonify({'message': 'update failed. ' + error}), 200
        elif belonging_room_id:
            hotel = get_db().execute(
                    'SELECT * FROM account WHERE id=?',
                    (created_by_id,),
                    ).fetchone()
            room = get_db().execute(
                    'SELECT * FROM rooms WHERE id=? AND belonging_to = ?',
                    (belonging_room_id, hotel['working_at'],),
                    ).fetchone()
            if not room:
                error = "Room's id is not belong to hotel."
                return jsonify({'message': 'update failed. ' + error}), 200
        elif staff_execute_id:
            position = get_db().execute(
                    'SELECT * FROM account WHERE id=?',
                    (staff_execute_id,),
                    ).fetchone()
            if position['position'] != "bell man":
                error = "Employee do not work for this position."
                return jsonify({'message': 'update failed. ' + error}), 200
            
        if error is None:
            roster = get_db().execute(
                    'SELECT * FROM roster WHERE staff_id=? AND date = ?',
                    (staff_execute_id, current_date,),
                    ).fetchone()
            
            if roster is None:
                return jsonify({'message': 'update failed. Employee is not exsit in roster.'}), 200
            try:
                db.execute(
                    'UPDATE bell_man_monitoring SET belonging_room_id = ?, status = ?, staff_execute_id = ?, note = ?, created_by_id = ?'
                    ' WHERE id = ?',
                    (belonging_room_id, status, staff_execute_id, note, created_by_id, id),
                )
                db.commit()
            except db.IntegrityError:
                error = f"It is already created."
                return jsonify({'message': 'update failed. ' + error}), 200 
            else:
                return jsonify({'message': 'update successful'}), 201
                
    else:
        return jsonify({'message': 'update require human resource acc.'}), 200 
    return jsonify({'message': 'update failed'}), 400

@bp.route('/deleteBellManJob', methods=('GET', 'POST'))
@login_required
def delete_bell_man_job():
    if g.user['position'] == 'human resource' and request.method == 'POST':
        id = request.args.get('id')
        db = get_db()
        db.execute('DELETE FROM bell_man_monitoring WHERE id = ?', (id,))
        db.commit()
        return jsonify({'message': 'delete successful.'}), 200
    
    return jsonify({'message': 'delete information failed, require human resource acc'}), 200


############   auto gen for laundry if linnen create first    ########################

# def auto_add_to_laundry_job(belonging_room_id, status, staff_execute_id, note, created_by_id):
#     error = None

#     if staff_execute_id:
#             position = get_db().execute(
#                     'SELECT * FROM account WHERE id=?',
#                     (staff_execute_id,),
#                     ).fetchone()
#             if position['position'] != "laundry":
#                 error = "Employee do not work for this position."
#                 return jsonify({'message': 'Create failed. ' + error}), 200
#     else:
#         error = "There are no employees for this job yet."
#         return jsonify({'message': 'Create failed. ' + error}), 200

#     laundry = get_db().execute(
#         'SELECT * FROM laundry_monitoring WHERE belonging_room_id=? AND status = ? AND staff_execute_id=? AND created_by_id=?',
#         (belonging_room_id, status, staff_execute_id, created_by_id),
#         ).fetchone()
#     if laundry is None:
#         get_db().execute(
#             "INSERT INTO laundry_monitoring (belonging_room_id, status, staff_execute_id, note , created_by_id) VALUES (@0, @1, @2, @3, @4)",
#             (belonging_room_id, status, staff_execute_id, note , created_by_id),
#             )
#         get_db().commit()


@bp.route('/createLinenRoomJob', methods=('GET', 'POST'))
@login_required
def create_linen_room_job():
    if g.user['position'] == 'human resource' and request.method == 'POST':
        belonging_room_id = request.get_json().get('belonging_room_id').strip()
        status = request.get_json().get('status')
        staff_execute_id = request.get_json().get('staff_execute_id').strip()
        staff_laundry_id = request.get_json().get('staff_laundry_id').strip()
        note = request.get_json().get('note')
        created_by_id = str(g.user['id'])
        db = get_db()
        error = None
        current_date = str(datetime.datetime.now().day) + "/" + str(datetime.datetime.now().month) + "/" + str(datetime.datetime.now().year)

        if not belonging_room_id:
            error = "Room is required."
            return jsonify({'message': 'create failed. ' + error}), 200
        elif not status:
            error = "Status is required. In case the name is duplicate."
            return jsonify({'message': 'create failed. ' + error}), 200
        elif not staff_execute_id:
            error = "Staff's identifier is required."
            return jsonify({'message': 'create failed. ' + error}), 200
        elif not created_by_id:
            error = "Creator's id is required."
            return jsonify({'message': 'create failed. ' + error}), 200
        if belonging_room_id:
            hotel = get_db().execute(
                    'SELECT * FROM account WHERE id=?',
                    (created_by_id,),
                    ).fetchone()
            room = get_db().execute(
                    'SELECT * FROM rooms WHERE id=? AND belonging_to = ?',
                    (belonging_room_id, hotel['working_at'],),
                    ).fetchone()
            if not room:
                error = "Room's id is not belong to hotel."
                return jsonify({'message': 'update failed. ' + error}), 200
        if staff_execute_id:
            position = get_db().execute(
                    'SELECT * FROM account WHERE id=?',
                    (staff_execute_id,),
                    ).fetchone()
            if position['position'] != "linen room":
                error = "Employee do not work for this position."
                return jsonify({'message': 'Create failed. ' + error}), 200
        print(staff_laundry_id, type(staff_laundry_id))
        

        if error is None:
            linen_room = get_db().execute(
                'SELECT * FROM linen_room_monitoring WHERE belonging_room_id=? AND staff_execute_id=? AND created_by_id=?',
                (belonging_room_id, staff_execute_id, created_by_id),
                ).fetchone()
            #print(type(laundry))
            if linen_room:
                roster = get_db().execute(
                    'SELECT * FROM roster WHERE staff_id=? AND date = ?',
                    (staff_execute_id, current_date,),
                    ).fetchone()
                print('have',type(roster))
                if roster is None:
                    return jsonify({'message': 'create failed. Employee is not exsit in roster.'}), 200
                if linen_room['status'] == 'Not processed yet':
                    return jsonify({'message': 'create failed. Duplicate linen job information.'}), 200
                return jsonify({'message': 'create failed. Duplicate linen job information.'}), 200
            else:
                roster = get_db().execute(
                    'SELECT * FROM roster WHERE staff_id=? AND date = ?',
                    (staff_execute_id, current_date,),
                    ).fetchone()
                if roster is None:
                    return jsonify({'message': 'create failed. Employee is not exsit in roster.'}), 200
                try:
                    if  staff_laundry_id and len(staff_laundry_id) > 0:
                        print('have laundry id')

                        position = get_db().execute(
                            'SELECT * FROM account WHERE id=?',
                            (staff_laundry_id,),
                            ).fetchone()
                        if position['position'] != "laundry":
                            return jsonify({'message': "Create failed. Laundry's id do not work for this position."}), 200

                        roster = get_db().execute(
                            'SELECT * FROM roster WHERE staff_id=? AND date = ?',
                            (staff_laundry_id, current_date,),
                            ).fetchone()
                        if roster is None:
                            return jsonify({'message': 'create failed. Employee is not exsit in roster.'}), 200

                        laundry = get_db().execute(
                            'SELECT * FROM laundry_monitoring WHERE belonging_room_id=? AND status = ? AND staff_execute_id=? AND created_by_id=?',
                            (belonging_room_id, status, staff_laundry_id, created_by_id),
                            ).fetchone()
                        if laundry is None:
                            print('chua co landry job')
                            get_db().execute(
                                "INSERT INTO laundry_monitoring (belonging_room_id, status, staff_execute_id, note , created_by_id) VALUES (@0, @1, @2, @3, @4)",
                                (belonging_room_id, status, staff_laundry_id, note , created_by_id),
                                )
                            get_db().commit()
                            db.execute(
                                "INSERT INTO linen_room_monitoring (belonging_room_id, status, staff_execute_id, note , created_by_id) VALUES (@0, @1, @2, @3, @4)",
                                (belonging_room_id, status, staff_execute_id, note , created_by_id),
                                )
                            db.commit()
                            return jsonify({'message': 'Create successful for both linen and laundry.'}), 200
                        else:
                            return jsonify({'message': 'Laundry job exsit. Create successful for linen only.'}), 200
                    else:
                        print('no laudry id')
                            
                        db.execute(
                            "INSERT INTO linen_room_monitoring (belonging_room_id, status, staff_execute_id, note , created_by_id) VALUES (@0, @1, @2, @3, @4)",
                            (belonging_room_id, status, staff_execute_id, note , created_by_id),
                            )
                        db.commit()

                except db.IntegrityError:
                    error = f"It is already created."
                    return jsonify({'message': 'Create failed. ' + error}), 200 
                else:
                    return jsonify({'message': 'Create successful for linen. There are no employees for laundry job yet so create it later.'}), 201 
    else:
        return jsonify({'message': 'Create require human resource acc.'}), 200 
    return jsonify({'message': 'create failed'}), 400

@bp.route('/updateLinenRoomJob', methods=('GET', 'POST'))
@login_required
def update_linen_room_job():
    if g.user['position'] == 'human resource' and request.method == 'POST':
        id = request.args.get('id')
        belonging_room_id = request.get_json().get('belonging_room_id')
        status = request.get_json().get('status')
        staff_execute_id = request.get_json().get('staff_execute_id')
        note = request.get_json().get('note')
        created_by_id = str(g.user['id'])
        db = get_db()
        error = None
        current_date = str(datetime.datetime.now().day) + "/" + str(datetime.datetime.now().month) + "/" + str(datetime.datetime.now().year)

        if id is None:
            error = "Id is required. In case the name is duplicate."
            return jsonify({'message': 'update failed. ' + error}), 200
        if not belonging_room_id:
            error = "Room is required."
            return jsonify({'message': 'update failed. ' + error}), 200
        elif not status:
            error = "Status is required. In case the name is duplicate."
            return jsonify({'message': 'update failed. ' + error}), 200
        elif not staff_execute_id:
            error = "Staff's identifier is required."
            return jsonify({'message': 'update failed. ' + error}), 200
        elif not created_by_id:
            error = "Creator's id is required."
            return jsonify({'message': 'update failed. ' + error}), 200
        if belonging_room_id:
            hotel = get_db().execute(
                    'SELECT * FROM account WHERE id=?',
                    (created_by_id,),
                    ).fetchone()
            room = get_db().execute(
                    'SELECT * FROM rooms WHERE id=? AND belonging_to = ?',
                    (belonging_room_id, hotel['working_at'],),
                    ).fetchone()
            if not room:
                error = "Room's id is not belong to hotel."
                return jsonify({'message': 'update failed. ' + error}), 200
        if staff_execute_id:
            position = get_db().execute(
                    'SELECT * FROM account WHERE id=?',
                    (staff_execute_id,),
                    ).fetchone()
            if position['position'] != "linen room":
                error = "Employee do not work for this position."
                return jsonify({'message': 'update failed. ' + error}), 200
            
        if error is None:
            roster = get_db().execute(
                    'SELECT * FROM roster WHERE staff_id=? AND date = ?',
                    (staff_execute_id, current_date,),
                    ).fetchone()
            if roster is None:
                return jsonify({'message': 'update failed. Employee is not exsit in roster.'}), 200
            try:
                db.execute(
                    'UPDATE linen_room_monitoring SET belonging_room_id = ?, status = ?, staff_execute_id = ?, note = ?, created_by_id = ?'
                    ' WHERE id = ?',
                    (belonging_room_id, status, staff_execute_id, note, created_by_id, id),
                )
                db.commit()
            except db.IntegrityError:
                error = f"It is already created."
                return jsonify({'message': 'update failed. ' + error}), 200 
            else:
                return jsonify({'message': 'update successful'}), 201
                
    else:
        return jsonify({'message': 'update require human resource acc.'}), 200 
    return jsonify({'message': 'update failed'}), 400

@bp.route('/deleteLinenRoomJob', methods=('GET', 'POST'))
@login_required
def delete_linen_room_job():
    if g.user['position'] == 'human resource' and request.method == 'POST':
        id = request.args.get('id')
        db = get_db()
        db.execute('DELETE FROM linen_room_monitoring WHERE id = ?', (id,))
        db.commit()
        return jsonify({'message': 'delete successful.'}), 200
    
    return jsonify({'message': 'delete information failed, require human resource acc'}), 200

@bp.route('/createHousekeepingJob', methods=('GET', 'POST'))
@login_required
def create_housekeeping_job():
    if g.user['position'] == 'human resource' and request.method == 'POST':
        belonging_room_id = request.get_json().get('belonging_room_id').strip()
        room_status = ""
        status = request.get_json().get('status')
        staff_execute_id = request.get_json().get('staff_execute_id').strip()
        note = request.get_json().get('note')
        created_by_id = str(g.user['id'])
        db = get_db()
        error = None
        current_date = str(datetime.datetime.now().day) + "/" + str(datetime.datetime.now().month) + "/" + str(datetime.datetime.now().year)

        if not belonging_room_id:
            error = "Room is required."
            return jsonify({'message': 'create failed. ' + error}), 200
        elif not status:
            error = "Status is required. In case the name is duplicate."
            return jsonify({'message': 'create failed. ' + error}), 200
        elif not staff_execute_id:
            error = "Staff's identifier is required."
            return jsonify({'message': 'create failed. ' + error}), 200
        elif not created_by_id:
            error = "Creator's id is required."
            return jsonify({'message': 'create failed. ' + error}), 200
        if belonging_room_id:
            hotel = get_db().execute(
                    'SELECT * FROM account WHERE id=?',
                    (created_by_id,),
                    ).fetchone()
            room = get_db().execute(
                    'SELECT * FROM rooms WHERE id=? AND belonging_to = ?',
                    (belonging_room_id, hotel['working_at'],),
                    ).fetchone()
            if not room:
                error = "Room's id is not belong to hotel."
                return jsonify({'message': 'create failed. ' + error}), 200
        if staff_execute_id:
            position = get_db().execute(
                    'SELECT * FROM account WHERE id=?',
                    (staff_execute_id,),
                    ).fetchone()
            
            if position['position'] != "housekeeping":
                error = "Employee do not work for this position."
                return jsonify({'message': 'Create failed. ' + error}), 200


        if error is None:
            housekeeping = get_db().execute(
                'SELECT * FROM housekeeping_monitoring WHERE belonging_room_id=? AND staff_execute_id=? AND created_by_id=?',
                (belonging_room_id, staff_execute_id, created_by_id),
                ).fetchone()
            if housekeeping is not None:
                roster = get_db().execute(
                    'SELECT * FROM roster WHERE staff_id=? AND date=?',
                    (staff_execute_id, current_date ,),
                    ).fetchone()
                if roster is None:
                    return jsonify({'message': 'create failed. Employee is not exsit in roster.'}), 200
                if housekeeping['status'] == 'Not processed yet':
                    return jsonify({'message': 'create failed. Duplicate information.'}), 200
                return jsonify({'message': 'create failed. Duplicate information.'}), 200
            else:
                roster = get_db().execute(
                    'SELECT * FROM roster WHERE staff_id=? AND date=?',
                    (staff_execute_id, current_date ,),
                    ).fetchone()
                if roster is None:
                    return jsonify({'message': 'create failed. Employee is not exsit in roster.'}), 200
                try:
                    db.execute(
                        "INSERT INTO housekeeping_monitoring (belonging_room_id, room_status, status, staff_execute_id, note , created_by_id) VALUES (@0, @1, @2, @3, @4, @5)",
                        (belonging_room_id, room_status , status, staff_execute_id, note , created_by_id),
                        )
                    db.commit()
                except db.IntegrityError:
                   error = f"It is already created."
                   return jsonify({'message': 'Create failed. ' + error}), 200 
                else:
                    return jsonify({'message': 'Create successful'}), 201 
    else:
        return jsonify({'message': 'Create require human resource acc.'}), 200 
    return jsonify({'message': 'create failed'}), 400

@bp.route('/updateHousekeepingJob', methods=('GET', 'POST'))
@login_required
def update_housekeeping_job():
    if g.user['position'] == 'human resource' and request.method == 'POST':
        id = request.args.get('id')
        belonging_room_id = request.get_json().get('belonging_room_id').strip()
        status = request.get_json().get('status')
        staff_execute_id = request.get_json().get('staff_execute_id').strip()
        note = request.get_json().get('note')
        created_by_id = str(g.user['id'])
        db = get_db()
        error = None
        current_date = str(datetime.datetime.now().day) + "/" + str(datetime.datetime.now().month) + "/" + str(datetime.datetime.now().year)

        if id is None:
            error = "Id is required. In case the name is duplicate."
            return jsonify({'message': 'update failed. ' + error}), 200
        if not belonging_room_id:
            error = "Room is required."
            return jsonify({'message': 'update failed. ' + error}), 200
        elif not status:
            error = "Status is required. In case the name is duplicate."
            return jsonify({'message': 'update failed. ' + error}), 200
        elif not staff_execute_id:
            error = "Staff's identifier is required."
            return jsonify({'message': 'update failed. ' + error}), 200
        elif not created_by_id:
            error = "Creator's id is required."
            return jsonify({'message': 'update failed. ' + error}), 200
        elif belonging_room_id:
            hotel = get_db().execute(
                    'SELECT * FROM account WHERE id=?',
                    (created_by_id,),
                    ).fetchone()
            room = get_db().execute(
                    'SELECT * FROM rooms WHERE id=? AND belonging_to = ?',
                    (belonging_room_id, hotel['working_at'],),
                    ).fetchone()
            if not room:
                error = "Room's id is not belong to hotel."
                return jsonify({'message': 'update failed. ' + error}), 200
        elif staff_execute_id:
            position = get_db().execute(
                    'SELECT * FROM account WHERE id=?',
                    (staff_execute_id,),
                    ).fetchone()
            if position['position'] != "housekeeping":
                error = "Employee do not work for this position."
                return jsonify({'message': 'update failed. ' + error}), 200
            
        if error is None:
            roster = get_db().execute(
                    'SELECT * FROM roster WHERE staff_id=? AND date = ?',
                    (staff_execute_id, current_date,),
                    ).fetchone()
            
            if roster is None:
                return jsonify({'message': 'update failed. Employee is not exsit in roster.'}), 200
            try:
                db.execute(
                    'UPDATE housekeeping_monitoring SET belonging_room_id = ?, status = ?, staff_execute_id = ?, note = ?, created_by_id = ?'
                    ' WHERE id = ?',
                    (belonging_room_id, status, staff_execute_id, note, created_by_id, id),
                )
                db.commit()
            except db.IntegrityError:
                error = f"It is already created."
                return jsonify({'message': 'update failed. ' + error}), 200 
            else:
                return jsonify({'message': 'update successful'}), 201
                
    else:
        return jsonify({'message': 'update require human resource acc.'}), 200 
    return jsonify({'message': 'update failed'}), 400

@bp.route('/deleteHousekeepingJob', methods=('GET', 'POST'))
@login_required
def delete_housekeeping_job():
    if g.user['position'] == 'human resource' and request.method == 'POST':
        id = request.args.get('id')
        db = get_db()
        db.execute('DELETE FROM housekeeping_monitoring WHERE id = ?', (id,))
        db.commit()
        return jsonify({'message': 'delete successful.'}), 200
    
    return jsonify({'message': 'delete information failed, require human resource acc'}), 200

@bp.route('/createWaiterJob', methods=('GET', 'POST'))
@login_required
def create_waiter_job():
    if g.user['position'] == 'human resource' and request.method == 'POST':
        belonging_room_id = request.get_json().get('belonging_room_id').strip()
        status = request.get_json().get('status')
        staff_execute_id = request.get_json().get('staff_execute_id').strip()
        note = request.get_json().get('note')
        created_by_id = str(g.user['id'])
        db = get_db()
        error = None
        current_date = str(datetime.datetime.now().day) + "/" + str(datetime.datetime.now().month) + "/" + str(datetime.datetime.now().year)

        if not belonging_room_id:
            error = "Room is required."
            return jsonify({'message': 'create failed. ' + error}), 200
        elif not status:
            error = "Status is required. In case the name is duplicate."
            return jsonify({'message': 'create failed. ' + error}), 200
        elif not staff_execute_id:
            error = "Staff's identifier is required."
            return jsonify({'message': 'create failed. ' + error}), 200
        elif not created_by_id:
            error = "Creator's id is required."
            return jsonify({'message': 'create failed. ' + error}), 200
        if belonging_room_id:
            hotel = get_db().execute(
                    'SELECT * FROM account WHERE id=?',
                    (created_by_id,),
                    ).fetchone()
            room = get_db().execute(
                    'SELECT * FROM rooms WHERE id=? AND belonging_to = ?',
                    (belonging_room_id, hotel['working_at'],),
                    ).fetchone()
            if not room:
                error = "Room's id is not belong to hotel."
                return jsonify({'message': 'create failed. ' + error}), 200
        if staff_execute_id:
            position = get_db().execute(
                    'SELECT * FROM account WHERE id=?',
                    (staff_execute_id,),
                    ).fetchone()
            
            if position['position'] != "waiter":
                error = "Employee do not work for this position."
                return jsonify({'message': 'Create failed. ' + error}), 200


        if error is None:
            waiter = get_db().execute(
                'SELECT * FROM waiter_monitoring WHERE belonging_room_id=? AND staff_execute_id=? AND created_by_id=?',
                (belonging_room_id, staff_execute_id, created_by_id),
                ).fetchone()
            if waiter is not None:
                roster = get_db().execute(
                    'SELECT * FROM roster WHERE staff_id=? AND date=?',
                    (staff_execute_id, current_date ,),
                    ).fetchone()
                if roster is None:
                    return jsonify({'message': 'create failed. Employee is not exsit in roster.'}), 200
                if waiter['status'] == 'Not processed yet':
                    return jsonify({'message': 'create failed. Duplicate information.'}), 200
                return jsonify({'message': 'create failed. Duplicate information.'}), 200
            else:
                roster = get_db().execute(
                    'SELECT * FROM roster WHERE staff_id=? AND date=?',
                    (staff_execute_id, current_date ,),
                    ).fetchone()
                if roster is None:
                    return jsonify({'message': 'create failed. Employee is not exsit in roster.'}), 200
                try:
                    db.execute(
                        "INSERT INTO waiter_monitoring (belonging_room_id, status, staff_execute_id, note , created_by_id) VALUES (@0, @1, @2, @3, @4)",
                        (belonging_room_id, status, staff_execute_id, note , created_by_id),
                    )
                    db.commit()
                except db.IntegrityError:
                    error = f"It is already created."
                    return jsonify({'message': 'Create failed. ' + error}), 200 
                else:
                    return jsonify({'message': 'Create successful'}), 201 
    else:
        return jsonify({'message': 'Create require human resource acc.'}), 200 
    return jsonify({'message': 'create failed'}), 400

@bp.route('/updateWaiterJob', methods=('GET', 'POST'))
@login_required
def update_waiter_job():
    if g.user['position'] == 'human resource' and request.method == 'POST':
        id = request.args.get('id')
        belonging_room_id = request.get_json().get('belonging_room_id').strip()
        status = request.get_json().get('status')
        staff_execute_id = request.get_json().get('staff_execute_id').strip()
        note = request.get_json().get('note')
        created_by_id = str(g.user['id'])
        db = get_db()
        error = None
        current_date = str(datetime.datetime.now().day) + "/" + str(datetime.datetime.now().month) + "/" + str(datetime.datetime.now().year)

        if id is None:
            error = "Id is required. In case the name is duplicate."
            return jsonify({'message': 'update failed. ' + error}), 200
        if not belonging_room_id:
            error = "Room is required."
            return jsonify({'message': 'update failed. ' + error}), 200
        elif not status:
            error = "Status is required. In case the name is duplicate."
            return jsonify({'message': 'update failed. ' + error}), 200
        elif not staff_execute_id:
            error = "Staff's identifier is required."
            return jsonify({'message': 'update failed. ' + error}), 200
        elif not created_by_id:
            error = "Creator's id is required."
            return jsonify({'message': 'update failed. ' + error}), 200
        elif belonging_room_id:
            hotel = get_db().execute(
                    'SELECT * FROM account WHERE id=?',
                    (created_by_id,),
                    ).fetchone()
            room = get_db().execute(
                    'SELECT * FROM rooms WHERE id=? AND belonging_to = ?',
                    (belonging_room_id, hotel['working_at'],),
                    ).fetchone()
            if not room:
                error = "Room's id is not belong to hotel."
                return jsonify({'message': 'update failed. ' + error}), 200
        elif staff_execute_id:
            position = get_db().execute(
                    'SELECT * FROM account WHERE id=?',
                    (staff_execute_id,),
                    ).fetchone()
            if position['position'] != "waiter":
                error = "Employee do not work for this position."
                return jsonify({'message': 'update failed. ' + error}), 200
            
        if error is None:
            roster = get_db().execute(
                    'SELECT * FROM roster WHERE staff_id=? AND date = ?',
                    (staff_execute_id, current_date,),
                    ).fetchone()
            
            if roster is None:
                return jsonify({'message': 'update failed. Employee is not exsit in roster.'}), 200
            try:
                db.execute(
                    'UPDATE waiter_monitoring SET belonging_room_id = ?, status = ?, staff_execute_id = ?, note = ?, created_by_id = ?'
                    ' WHERE id = ?',
                    (belonging_room_id, status, staff_execute_id, note, created_by_id, id),
                )
                db.commit()
            except db.IntegrityError:
                error = f"It is already created."
                return jsonify({'message': 'update failed. ' + error}), 200 
            else:
                return jsonify({'message': 'update successful'}), 201
                
    else:
        return jsonify({'message': 'update require human resource acc.'}), 200 
    return jsonify({'message': 'update failed'}), 400

@bp.route('/deleteWaiterJob', methods=('GET', 'POST'))
@login_required
def delete_waiter_job():
    if g.user['position'] == 'human resource' and request.method == 'POST':
        id = request.args.get('id')
        db = get_db()
        db.execute('DELETE FROM waiter_monitoring WHERE id = ?', (id,))
        db.commit()
        return jsonify({'message': 'delete successful.'}), 200
    
    return jsonify({'message': 'delete information failed, require human resource acc'}), 200

