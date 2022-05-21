from flask import (
    Blueprint, flash, g, redirect, request, session, url_for, jsonify
)

from flaskr.db import get_db

from flaskr.auth import login_required

bp = Blueprint('otherOperation', __name__)

@bp.route('/getEmployeesInfor', methods=('GET', 'POST'))
@login_required
def get_employee_infor():
    message = []
    employees = get_db().execute(
        'SELECT * FROM account WHERE working_at =?',
        (g.user['working_at'],)
    ).fetchall()
    for employee in employees:
        temp = {}
        temp['id'] = employee['id']
        temp['name'] = employee['name']
        temp['phone'] = employee['phone']
        temp['position'] = employee['position']
        message.append(temp)

    return jsonify({'message': message}), 200

@bp.route('/getRosterInfor', methods=('GET', 'POST'))
@login_required
def get_roster_infor():
    message = []
    rosters = get_db().execute(
        'SELECT * FROM roster WHERE staff_id IN (SELECT id FROM account WHERE working_at = ?)',
        (g.user['working_at'],)
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
        temp['report'] = roster['report']
        temp['created_by_id'] = roster['created_by_id']
        temp['created'] = roster['created']
        message.append(temp)

    return jsonify({'message': message}), 200


@bp.route('/getLaundryInfor', methods=('GET', 'POST'))
@login_required
def get_laundry_infor():
    message = []
    laundrys = get_db().execute(
        'SELECT * FROM laundry_monitoring WHERE staff_execute_id IN (SELECT id FROM account WHERE working_at = ?)',
        (g.user['working_at'],)
    ).fetchall()
    for laundry in laundrys:
        temp = {}
        temp['id'] = laundry['id']
        temp['belonging_room_id'] = laundry['belonging_room_id']
        temp['staff_execute_id'] = laundry['staff_execute_id']
        temp['status'] = laundry['status']
        temp['note'] = laundry['note']
        temp['created_by_id'] = laundry['created_by_id']
        temp['created'] = laundry['created']
        message.append(temp)

    return jsonify({'message': message}), 200

@bp.route('/getGardenerInfor', methods=('GET', 'POST'))
@login_required
def get_gardener_infor():
    message = []
    gardeners = get_db().execute(
        'SELECT * FROM gardener_monitoring WHERE staff_execute_id IN (SELECT id FROM account WHERE working_at = ?)',
        (g.user['working_at'],)
    ).fetchall()
    for gardener in gardeners:
        temp = {}
        temp['id'] = gardener['id']
        temp['staff_execute_id'] = gardener['staff_execute_id']
        temp['note'] = gardener['note']
        temp['created_by_id'] = gardener['created_by_id']
        temp['created'] = gardener['created']
        message.append(temp)

    return jsonify({'message': message}), 200

@bp.route('/getBabySitterInfor', methods=('GET', 'POST'))
@login_required
def get_baby_sitter_infor():
    message = []
    baby_sitters = get_db().execute(
        'SELECT * FROM baby_sitter_monitoring WHERE staff_execute_id IN (SELECT id FROM account WHERE working_at = ?)',
        (g.user['working_at'],)
    ).fetchall()
    for baby_sitter in baby_sitters:
        temp = {}
        temp['id'] = baby_sitter['id']
        temp['staff_execute_id'] = baby_sitter['staff_execute_id']
        temp['note'] = baby_sitter['note']
        temp['created_by_id'] = baby_sitter['created_by_id']
        temp['created'] = baby_sitter['created']
        message.append(temp)

    return jsonify({'message': message}), 200


@bp.route('/getPublicAreaCleanerInfor', methods=('GET', 'POST'))
@login_required
def get_public_area_cleaner_infor():
    message = []
    public_area_cleaners = get_db().execute(
        'SELECT * FROM public_area_cleaner_monitoring WHERE staff_execute_id IN (SELECT id FROM account WHERE working_at = ?)',
        (g.user['working_at'],)
    ).fetchall()
    for public_area_cleaner in public_area_cleaners:
        temp = {}
        temp['id'] = public_area_cleaner['id']
        temp['staff_execute_id'] = public_area_cleaner['staff_execute_id']
        temp['note'] = public_area_cleaner['note']
        temp['created_by_id'] = public_area_cleaner['created_by_id']
        temp['created'] = public_area_cleaner['created']
        message.append(temp)

    return jsonify({'message': message}), 200

@bp.route('/getDoorManInfor', methods=('GET', 'POST'))
@login_required
def get_door_man_infor():
    message = []
    door_mans = get_db().execute(
        'SELECT * FROM door_man_monitoring WHERE staff_execute_id IN (SELECT id FROM account WHERE working_at = ?)',
        (g.user['working_at'],)
    ).fetchall()
    for door_man in door_mans:
        temp = {}
        temp['id'] = door_man['id']
        temp['staff_execute_id'] = door_man['staff_execute_id']
        temp['note'] = door_man['note']
        temp['created_by_id'] = door_man['created_by_id']
        temp['created'] = door_man['created']
        message.append(temp)

    return jsonify({'message': message}), 200

@bp.route('/getCookAssistantInfor', methods=('GET', 'POST'))
@login_required
def get_cook_assistant_infor():
    message = []
    cook_assistants = get_db().execute(
        'SELECT * FROM cook_assistant_monitoring WHERE staff_execute_id IN (SELECT id FROM account WHERE working_at = ?)',
        (g.user['working_at'],)
    ).fetchall()
    for cook_assistant in cook_assistants:
        temp = {}
        temp['id'] = cook_assistant['id']
        temp['staff_execute_id'] = cook_assistant['staff_execute_id']
        temp['note'] = cook_assistant['note']
        temp['created_by_id'] = cook_assistant['created_by_id']
        temp['created'] = cook_assistant['created']
        message.append(temp)

    return jsonify({'message': message}), 200

@bp.route('/getBartenderInfor', methods=('GET', 'POST'))
@login_required
def get_bartender_infor():
    message = []
    bartenders = get_db().execute(
        'SELECT * FROM bartender_monitoring WHERE staff_execute_id IN (SELECT id FROM account WHERE working_at = ?)',
        (g.user['working_at'],)
    ).fetchall()
    for bartender in bartenders:
        temp = {}
        temp['id'] = bartender['id']
        temp['staff_execute_id'] = bartender['staff_execute_id']
        temp['note'] = bartender['note']
        temp['created_by_id'] = bartender['created_by_id']
        temp['created'] = bartender['created']
        message.append(temp)

    return jsonify({'message': message}), 200

@bp.route('/getFoodRunnerInfor', methods=('GET', 'POST'))
@login_required
def get_food_runner_infor():
    message = []
    food_runners = get_db().execute(
        'SELECT * FROM food_runner_monitoring WHERE staff_execute_id IN (SELECT id FROM account WHERE working_at = ?)',
        (g.user['working_at'],)
    ).fetchall()
    for food_runner in food_runners:
        temp = {}
        temp['id'] = food_runner['id']
        temp['staff_execute_id'] = food_runner['staff_execute_id']
        temp['note'] = food_runner['note']
        temp['created_by_id'] = food_runner['created_by_id']
        temp['created'] = food_runner['created']
        message.append(temp)

    return jsonify({'message': message}), 200

@bp.route('/getStewardInfor', methods=('GET', 'POST'))
@login_required
def get_steward_infor():
    message = []
    stewards = get_db().execute(
        'SELECT * FROM steward_monitoring WHERE staff_execute_id IN (SELECT id FROM account WHERE working_at = ?)',
        (g.user['working_at'],)
    ).fetchall()
    for steward in stewards:
        temp = {}
        temp['id'] = steward['id']
        temp['staff_execute_id'] = steward['staff_execute_id']
        temp['note'] = steward['note']
        temp['created_by_id'] = steward['created_by_id']
        temp['created'] = steward['created']
        message.append(temp)

    return jsonify({'message': message}), 200

@bp.route('/getLinenRoomInfor', methods=('GET', 'POST'))
@login_required
def get_linen_room_infor():
    message = []
    linen_rooms = get_db().execute(
        'SELECT * FROM linen_room_monitoring WHERE staff_execute_id IN (SELECT id FROM account WHERE working_at = ?)',
        (g.user['working_at'],)
    ).fetchall()
    for linen_room in linen_rooms:
        temp = {}
        temp['id'] = linen_room['id']
        temp['belonging_room_id'] = linen_room['belonging_room_id']
        temp['staff_execute_id'] = linen_room['staff_execute_id']
        temp['status'] = linen_room['status']
        temp['note'] = linen_room['note']
        temp['created_by_id'] = linen_room['created_by_id']
        temp['created'] = linen_room['created']
        message.append(temp)

    return jsonify({'message': message}), 200

@bp.route('/getReceptionistInfor', methods=('GET', 'POST'))
@login_required
def get_receptionist_infor():
    message = []
    receptionists = get_db().execute(
        'SELECT * FROM receptionist_monitoring WHERE staff_execute_id IN (SELECT id FROM account WHERE working_at = ?)',
        (g.user['working_at'],)
    ).fetchall()
    for receptionist in receptionists:
        temp = {}
        temp['id'] = receptionist['id']
        temp['staff_execute_id'] = receptionist['staff_execute_id']
        temp['number_of_check_in'] = receptionist['number_of_check_in']
        temp['number_of_check_out'] = receptionist['number_of_check_out']
        temp['note'] = receptionist['note']
        temp['created'] = receptionist['created']
        message.append(temp)

    return jsonify({'message': message}), 200

@bp.route('/getHousekeepingInfor', methods=('GET', 'POST'))
@login_required
def get_housekeeping_infor():
    message = []
    housekeepings = get_db().execute(
        'SELECT * FROM housekeeping_monitoring WHERE staff_execute_id IN (SELECT id FROM account WHERE working_at = ?)',
        (g.user['working_at'],)
    ).fetchall()
    for housekeeping in housekeepings:
        temp = {}
        temp['id'] = housekeeping['id']
        temp['belonging_room_id'] = housekeeping['belonging_room_id']
        temp['staff_execute_id'] = housekeeping['staff_execute_id']
        temp['room_status'] = housekeeping['room_status']
        temp['status'] = housekeeping['status']
        temp['note'] = housekeeping['note']
        temp['created_by_id'] = housekeeping['created_by_id']
        temp['created'] = housekeeping['created']
        message.append(temp)

    return jsonify({'message': message}), 200

@bp.route('/getConciergeInfor', methods=('GET', 'POST'))
@login_required
def get_concierge_infor():
    message = []
    concierges = get_db().execute(
        'SELECT * FROM concierge_monitoring WHERE staff_execute_id IN (SELECT id FROM account WHERE working_at = ?)',
        (g.user['working_at'],)
    ).fetchall()
    for concierge in concierges:
        temp = {}
        temp['id'] = concierge['id']
        temp['staff_execute_id'] = concierge['staff_execute_id']
        temp['note'] = concierge['note']
        temp['created'] = concierge['created']
        message.append(temp)

    return jsonify({'message': message}), 200

@bp.route('/getCashierInfor', methods=('GET', 'POST'))
@login_required
def get_cashier_infor():
    message = []
    cashiers = get_db().execute(
        'SELECT * FROM cashier_monitoring WHERE staff_execute_id IN (SELECT id FROM account WHERE working_at = ?)',
        (g.user['working_at'],)
    ).fetchall()
    for cashier in cashiers:
        temp = {}
        temp['id'] = cashier['id']
        temp['staff_execute_id'] = cashier['staff_execute_id']
        temp['note'] = cashier['note']
        temp['created'] = cashier['created']
        message.append(temp)

    return jsonify({'message': message}), 200

@bp.route('/getBellManInfor', methods=('GET', 'POST'))
@login_required
def get_bell_man_infor():
    message = []
    bell_mans = get_db().execute(
        'SELECT * FROM bell_man_monitoring WHERE staff_execute_id IN (SELECT id FROM account WHERE working_at = ?)',
        (g.user['working_at'],)
    ).fetchall()
    for bell_man in bell_mans:
        temp = {}
        temp['id'] = bell_man['id']
        temp['belonging_room_id'] = bell_man['belonging_room_id']
        temp['staff_execute_id'] = bell_man['staff_execute_id']
        temp['status'] = bell_man['status']
        temp['note'] = bell_man['note']
        temp['created_by_id'] = bell_man['created_by_id']
        temp['created'] = bell_man['created']
        message.append(temp)

    return jsonify({'message': message}), 200

@bp.route('/getChefInfor', methods=('GET', 'POST'))
@login_required
def get_chef_infor():
    message = []
    chefs = get_db().execute(
        'SELECT * FROM chef_monitoring WHERE staff_execute_id IN (SELECT id FROM account WHERE working_at = ?)',
        (g.user['working_at'],)
    ).fetchall()
    for chef in chefs:
        temp = {}
        temp['id'] = chef['id']
        temp['staff_execute_id'] = chef['staff_execute_id']
        temp['menu'] = chef['menu']
        temp['created'] = chef['created']
        message.append(temp)

    return jsonify({'message': message}), 200

@bp.route('/getWaiterInfor', methods=('GET', 'POST'))
@login_required
def get_waiter_infor():
    message = []
    waiters = get_db().execute(
        'SELECT * FROM waiter_monitoring WHERE staff_execute_id IN (SELECT id FROM account WHERE working_at = ?)',
        (g.user['working_at'],)
    ).fetchall()
    for waiter in waiters:
        temp = {}
        temp['id'] = waiter['id']
        temp['belonging_room_id'] = waiter['belonging_room_id']
        temp['staff_execute_id'] = waiter['staff_execute_id']
        temp['status'] = waiter['status']
        temp['note'] = waiter['note']
        temp['created_by_id'] = waiter['created_by_id']
        temp['created'] = waiter['created']
        message.append(temp)

    return jsonify({'message': message}), 200

