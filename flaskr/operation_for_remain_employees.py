from flask import (
    Blueprint, flash, g, redirect, request, session, url_for, jsonify
)

from flaskr.auth import login_required

from flaskr.db import get_db

import datetime

bp = Blueprint('operationForRemainEmployees', __name__)

@bp.route('/updateJobByEmployee', methods=('GET', 'POST'))
@login_required
def update_job_by_employee():
    id = request.args.get('id')
    status = request.get_json().get('status')
    room_status = request.get_json().get('room_status')
    note = request.get_json().get('note')
    error = None
    db = get_db()
    if g.user['position'] == 'laundry' and request.method == 'POST':
        if not status:
            error = 'status is required.'
            return jsonify({'message': 'update failed. ' + error}), 200
        
        if error is None:
            try:
                db.execute(
                    'UPDATE laundry_monitoring SET status = ?, note = ?'
                    ' WHERE id = ?',
                    (status, note, id,),
                    )
                db.commit()
            except db.IntegrityError:
                error = f"No record found or no permissions allowed."
                return jsonify({'message': 'update failed. ' + error}), 200 
    
    if g.user['position'] == 'linen room' and request.method == 'POST':
        if not status:
            error = 'status is required.'
            return jsonify({'message': 'update failed. ' + error}), 200
        
        if error is None:
            try:
                db.execute(
                    'UPDATE linen_room_monitoring SET status = ?, note = ?'
                    ' WHERE id = ?',
                    (status, note, id,),
                    )
                db.commit()
            except db.IntegrityError:
                error = f"No record found or no permissions allowed."
                return jsonify({'message': 'update failed. ' + error}), 200 

    if g.user['position'] == 'bell man' and request.method == 'POST':
        if not status:
            error = 'status is required.'
            return jsonify({'message': 'update failed. ' + error}), 200
        
        if error is None:
            try:
                db.execute(
                    'UPDATE bell_man_monitoring SET status = ?, note = ?'
                    ' WHERE id = ?',
                    (status, note, id,),
                    )
                db.commit()
            except db.IntegrityError:
                error = f"No record found or no permissions allowed."
                return jsonify({'message': 'update failed. ' + error}), 200 

    if g.user['position'] == 'gardener' and request.method == 'POST':       
        if error is None:
            try:
                db.execute(
                    'UPDATE gardener_monitoring SET note = ?'
                    ' WHERE id = ?',
                    (note, id,),
                    )
                db.commit()
            except db.IntegrityError:
                error = f"No record found or no permissions allowed."
                return jsonify({'message': 'update failed. ' + error}), 200                 

    if g.user['position'] == 'baby sitter' and request.method == 'POST':       
        if error is None:
            try:
                db.execute(
                    'UPDATE baby_sitter_monitoring SET note = ?'
                    ' WHERE id = ?',
                    (note, id,),
                    )
                db.commit()
            except db.IntegrityError:
                error = f"No record found or no permissions allowed."
                return jsonify({'message': 'update failed. ' + error}), 200  
    
    if g.user['position'] == 'public area cleaner' and request.method == 'POST':       
        if error is None:
            try:
                db.execute(
                    'UPDATE public_area_cleaner_monitoring SET note = ?'
                    ' WHERE id = ?',
                    (note, id,),
                    )
                db.commit()
            except db.IntegrityError:
                error = f"No record found or no permissions allowed."
                return jsonify({'message': 'update failed. ' + error}), 200  
    
    if g.user['position'] == 'door man' and request.method == 'POST':       
        if error is None:
            try:
                db.execute(
                    'UPDATE door_man_monitoring SET note = ?'
                    ' WHERE id = ?',
                    (note, id,),
                    )
                db.commit()
            except db.IntegrityError:
                error = f"No record found or no permissions allowed."
                return jsonify({'message': 'update failed. ' + error}), 200  
    
    if g.user['position'] == 'cook assistant' and request.method == 'POST':       
        if error is None:
            try:
                db.execute(
                    'UPDATE cook_assistant_monitoring SET note = ?'
                    ' WHERE id = ?',
                    (note, id,),
                    )
                db.commit()
            except db.IntegrityError:
                error = f"No record found or no permissions allowed."
                return jsonify({'message': 'update failed. ' + error}), 200  
    
    if g.user['position'] == 'bartender' and request.method == 'POST':       
        if error is None:
            try:
                db.execute(
                    'UPDATE bartender_monitoring SET note = ?'
                    ' WHERE id = ?',
                    (note, id,),
                    )
                db.commit()
            except db.IntegrityError:
                error = f"No record found or no permissions allowed."
                return jsonify({'message': 'update failed. ' + error}), 200  
    
    if g.user['position'] == 'food runner' and request.method == 'POST':       
        if error is None:
            try:
                db.execute(
                    'UPDATE food_runner_monitoring SET note = ?'
                    ' WHERE id = ?',
                    (note, id,),
                    )
                db.commit()
            except db.IntegrityError:
                error = f"No record found or no permissions allowed."
                return jsonify({'message': 'update failed. ' + error}), 200  
    
    if g.user['position'] == 'steward' and request.method == 'POST':       
        if error is None:
            try:
                db.execute(
                    'UPDATE steward_monitoring SET note = ?'
                    ' WHERE id = ?',
                    (note, id,),
                    )
                db.commit()
            except db.IntegrityError:
                error = f"No record found or no permissions allowed."
                return jsonify({'message': 'update failed. ' + error}), 200  

    if g.user['position'] == 'housekeeping' and request.method == 'POST':
        if not room_status:
            error = 'status is required.'
            return jsonify({'message': 'update failed. ' + error}), 200

        if not status:
            error = 'status is required.'
            return jsonify({'message': 'update failed. ' + error}), 200
        
        if error is None:
            try:
                db.execute(
                    'UPDATE housekeeping_monitoring SET room_status = ?, status = ?, note = ?'
                    ' WHERE id = ?',
                    (room_status, status, note, id,),
                    )
                db.commit()
            except db.IntegrityError:
                error = f"No record found or no permissions allowed."
                return jsonify({'message': 'update failed. ' + error}), 200 

@bp.route('/createReceptionistDailyNote', methods=('GET', 'POST'))
@login_required
def create_receptionist_daily_note():
    if g.user['position'] == 'receptionist' and request.method == 'POST':
        staff_execute_id = str(g.user['id'])
        number_of_check_in = request.get_json().get('number_of_check_in')
        number_of_check_out = request.get_json().get('number_of_check_out')
        note = request.get_json().get('note')
        get_time = datetime.date.today()
        current_date = str(get_time) + " 00:00:00"

        db = get_db()

        receptionist = db.execute(
                    'SELECT * FROM receptionist_monitoring WHERE created>?',
                    (current_date,),
                    ).fetchone()
        if receptionist is None:
            db.execute(
                "INSERT INTO receptionist_monitoring (staff_execute_id, number_of_check_in, number_of_check_out, note) VALUES (@0, @1, @2, @3)",
                (staff_execute_id, number_of_check_in, number_of_check_out, note,),
                )
            db.commit()
            return jsonify({'message': 'Create successful.'}), 200 
        else:
            return jsonify({'message': 'Record is exsit. Update information instead.'}), 200 
    return jsonify({'message': 'Create failed.'}), 400

@bp.route('/updateReceptionistDailyNote', methods=('GET', 'POST'))
@login_required
def update_receptionist_daily_note():
    if g.user['position'] == 'receptionist' and request.method == 'POST':
        id = request.args.get('id')
        staff_execute_id = str(g.user['id'])
        number_of_check_in = request.get_json().get('number_of_check_in')
        number_of_check_out = request.get_json().get('number_of_check_out')
        note = request.get_json().get('note')
        error = None

        db = get_db()

        if id is None:
            error = "Id is required. In case the name is duplicate."
            return jsonify({'message': 'update failed. ' + error}), 200
        
        if error is None:
            db.execute(
                'UPDATE receptionist_monitoring SET staff_execute_id = ?, number_of_check_in = ?, number_of_check_out = ?, note = ?'
                ' WHERE id = ?',
                (staff_execute_id, number_of_check_in, number_of_check_out, note, id,),
                )
            db.commit()
            return jsonify({'message': 'Update successful.'}), 200 
    return jsonify({'message': 'Update failed.'}), 400

@bp.route('/deleteReceptionistDailyNote', methods=('GET', 'POST'))
@login_required
def delete_receptionist_daily_note():
    if g.user['position'] == 'receptionist' and request.method == 'POST':
        id = request.args.get('id')
        db = get_db()
        db.execute('DELETE FROM receptionist_monitoring WHERE id = ?', (id,))
        db.commit()
        return jsonify({'message': 'delete successful.'}), 200
    
    return jsonify({'message': 'delete information failed, require human resource acc'}), 200

@bp.route('/createCashierDailyNote', methods=('GET', 'POST'))
@login_required
def create_cashier_daily_note():
    if g.user['position'] == 'cashier' and request.method == 'POST':
        staff_execute_id = str(g.user['id'])
        note = request.get_json().get('note')
        get_time = datetime.date.today()
        current_date = str(get_time) + " 00:00:00"

        db = get_db()

        receptionist = db.execute(
                    'SELECT * FROM cashier_monitoring WHERE created>?',
                    (current_date,),
                    ).fetchone()
        if receptionist is None:
            db.execute(
                "INSERT INTO cashier_monitoring (staff_execute_id, note) VALUES (@0, @1)",
                (staff_execute_id, note,),
                )
            db.commit()
            return jsonify({'message': 'Create successful.'}), 200 
        else:
            return jsonify({'message': 'Record is exsit. Update information instead.'}), 200 
    return jsonify({'message': 'Create failed.'}), 400

@bp.route('/updateCashierDailyNote', methods=('GET', 'POST'))
@login_required
def update_cashier_daily_note():
    if g.user['position'] == 'cashier' and request.method == 'POST':
        id = request.args.get('id')
        staff_execute_id = str(g.user['id'])
        note = request.get_json().get('note')
        error = None

        db = get_db()

        if id is None:
            error = "Id is required. In case the name is duplicate."
            return jsonify({'message': 'update failed. ' + error}), 200
        
        if error is None:
            db.execute(
                'UPDATE cashier_monitoring SET staff_execute_id = ?, note = ?'
                ' WHERE id = ?',
                (staff_execute_id, note, id,),
                )
            db.commit()
            return jsonify({'message': 'Update successful.'}), 200 
    return jsonify({'message': 'Update failed.'}), 400

@bp.route('/deleteCashierDailyNote', methods=('GET', 'POST'))
@login_required
def delete_cashier_daily_note():
    if g.user['position'] == 'cashier' and request.method == 'POST':
        id = request.args.get('id')
        db = get_db()
        db.execute('DELETE FROM cashier_monitoring WHERE id = ?', (id,))
        db.commit()
        return jsonify({'message': 'delete successful.'}), 200
    
    return jsonify({'message': 'delete information failed, require human resource acc'}), 200

@bp.route('/createConciergeDailyNote', methods=('GET', 'POST'))
@login_required
def create_concierge_daily_note():
    if g.user['position'] == 'concierge' and request.method == 'POST':
        staff_execute_id = str(g.user['id'])
        note = request.get_json().get('note')
        get_time = datetime.date.today()
        current_date = str(get_time) + " 00:00:00"

        db = get_db()

        receptionist = db.execute(
                    'SELECT * FROM concierge_monitoring WHERE created>?',
                    (current_date,),
                    ).fetchone()
        if receptionist is None:
            db.execute(
                "INSERT INTO concierge_monitoring (staff_execute_id, note) VALUES (@0, @1)",
                (staff_execute_id, note,),
                )
            db.commit()
            return jsonify({'message': 'Create successful.'}), 200 
        else:
            return jsonify({'message': 'Record is exsit. Update information instead.'}), 200 
    return jsonify({'message': 'Create failed.'}), 400

@bp.route('/updateConciergeDailyNote', methods=('GET', 'POST'))
@login_required
def update_concierge_daily_note():
    if g.user['position'] == 'concierge' and request.method == 'POST':
        id = request.args.get('id')
        staff_execute_id = str(g.user['id'])
        note = request.get_json().get('note')
        error = None

        db = get_db()

        if id is None:
            error = "Id is required. In case the name is duplicate."
            return jsonify({'message': 'update failed. ' + error}), 200
        
        if error is None:
            db.execute(
                'UPDATE concierge_monitoring SET staff_execute_id = ?, note = ?'
                ' WHERE id = ?',
                (staff_execute_id, note, id,),
                )
            db.commit()
            return jsonify({'message': 'Update successful.'}), 200 
    return jsonify({'message': 'Update failed.'}), 400

@bp.route('/deleteConciergeDailyNote', methods=('GET', 'POST'))
@login_required
def delete_concierge_daily_note():
    if g.user['position'] == 'concierge' and request.method == 'POST':
        id = request.args.get('id')
        db = get_db()
        db.execute('DELETE FROM concierge_monitoring WHERE id = ?', (id,))
        db.commit()
        return jsonify({'message': 'delete successful.'}), 200
    
    return jsonify({'message': 'delete information failed, require human resource acc'}), 200

@bp.route('/createMenuByChef', methods=('GET', 'POST'))
@login_required
def create_menu_by_chef():
    if g.user['position'] == 'chef' and request.method == 'POST':
        staff_execute_id = str(g.user['id'])
        menu = request.get_json().get('menu')
        get_time = datetime.date.today()
        current_date = str(get_time) + " 00:00:00"
        error = None

        db = get_db()

        if menu is None:
            error = "Menu is required."
            return jsonify({'message': 'create failed. ' + error}), 200

        if error is None:
            db.execute(
                "INSERT INTO chef_monitoring (staff_execute_id, menu) VALUES (@0, @1)",
                (staff_execute_id, menu,),
                )
            db.commit()
            return jsonify({'message': 'Create successful.'}), 200 
        else:
            return jsonify({'message': 'Record is exsit. Update information instead.'}), 200 
    return jsonify({'message': 'Create failed.'}), 400

@bp.route('/updateMenuByChef', methods=('GET', 'POST'))
@login_required
def update_menu_by_chef():
    if g.user['position'] == 'chef' and request.method == 'POST':
        id = request.args.get('id')
        staff_execute_id = str(g.user['id'])
        menu = request.get_json().get('menu')
        error = None

        db = get_db()

        if id is None:
            error = "Id is required. In case the name is duplicate."
            return jsonify({'message': 'update failed. ' + error}), 200
        
        if error is None:
            db.execute(
                'UPDATE chef_monitoring SET staff_execute_id = ?, menu = ?'
                ' WHERE id = ?',
                (staff_execute_id, menu, id,),
                )
            db.commit()
            return jsonify({'message': 'Update successful.'}), 200 
    return jsonify({'message': 'Update failed.'}), 400

@bp.route('/deleteMenuByChef', methods=('GET', 'POST'))
@login_required
def delete_menu_by_chef():
    if g.user['position'] == 'chef' and request.method == 'POST':
        id = request.args.get('id')
        db = get_db()
        db.execute('DELETE FROM chef_monitoring WHERE id = ?', (id,))
        db.commit()
        return jsonify({'message': 'delete successful.'}), 200
    
    return jsonify({'message': 'delete information failed, require human resource acc'}), 200
