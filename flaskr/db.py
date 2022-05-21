import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

@click.command('create-admin-acc')
@with_appcontext
def create_admin_acc_command():
    username = 'admin'
    password = '123456'
    name = 'admin'
    phone = '123456'
    working_at = 'top'
    position = 'admin'
    db = get_db()
    db.execute(
        "INSERT INTO account (username, password, name, phone, working_at, position) VALUES (?, ?, ?, ?, ?, ?)",
        (username, password, name, phone, working_at, position),
    )
    db.commit()
    click.echo('Initialized admin.')

def generate_employee(position, work_place, number_employee):
    for number in range(number_employee):
        infor = {
            'username' : str(position) + str(number+1),
            'password' : '123456',
            'name' : 'example name ' + str(position) + str(number+1),
            'phone' : '123456',
            'working_at' : str(work_place),
            'position' : str(position)
        }
        db = get_db()
        db.execute(
            "INSERT INTO account (username, password, name, phone, working_at, position) VALUES (?, ?, ?, ?, ?, ?)",
            (infor['username'], infor['password'], infor['name'], infor['phone'], infor['working_at'], infor['position']),
        )
        db.commit()

def generate_hotel(name, address):
    db = get_db()
    db.execute(
        "INSERT INTO hotel (name, address) VALUES (@0, @1)",
        (name, address),
    )
    db.commit()

def generate_room(hotel_name, kind_of_room, room_name):
    db = get_db()
    db.execute(
        'INSERT INTO rooms (belonging_to, kind_of_room, room_name)'
        ' VALUES (@0, @1, @2)',
        (hotel_name, kind_of_room, room_name)
    )
    db.commit()

def generate_roster(position, staff_id, staff_name, start_time, work_hour, date, report, created_by_id):
    db = get_db()
    db.execute(
        "INSERT INTO roster (position, staff_id, staff_name, start_time, work_hour, date, report, created_by_id) VALUES (@0, @1, @2, @3, @4, @5, @6, @7)",
        (position, staff_id, staff_name, start_time, work_hour, date, report, created_by_id),
        )
    db.commit()

@click.command('create-sample-data')
@with_appcontext
def create_sample_data_command():

    generate_hotel('khach san A Dong', '12, Tien An, tp Bac Ninh')
    generate_hotel('khach san Phuong Trang', '134, Nguyen Trai, Ninh Xa, tp Bac Ninh')
    generate_room('khach san A Dong', 'Standard', '301')
    generate_room('khach san A Dong', 'Standard', '302')
    generate_room('khach san A Dong', 'Standard', '303')
    generate_room('khach san A Dong', 'Standard', '304')
    generate_room('khach san A Dong', 'Standard', '305')
    generate_room('khach san A Dong', 'Standard', '306')
    generate_room('khach san A Dong', 'Standard', '307')
    generate_room('khach san A Dong', 'Standard', '308')
    generate_room('khach san A Dong', 'Standard', '401')
    generate_room('khach san A Dong', 'Standard', '402')
    generate_room('khach san A Dong', 'Superior', '403')
    generate_room('khach san A Dong', 'Superior', '404')
    generate_room('khach san A Dong', 'Superior', '405')
    generate_room('khach san A Dong', 'Superior', '406')
    generate_room('khach san A Dong', 'Deluxe', '501')
    generate_room('khach san A Dong', 'Deluxe', '502')
    generate_room('khach san A Dong', 'Deluxe', '503')
    generate_room('khach san A Dong', 'Suite', '504')
    generate_room('khach san A Dong', 'Suite', '601')
    generate_room('khach san A Dong', 'Suite', '602')
    generate_employee('hotel manager', 'khach san A Dong', 1)
    generate_employee('chef', 'khach san A Dong',1)
    generate_employee('human resource', 'khach san A Dong',1)
    generate_employee('laundry', 'khach san A Dong',4)
    generate_employee('gardener', 'khach san A Dong',2)
    generate_employee('baby sitter', 'khach san A Dong',4)
    generate_employee('linen room', 'khach san A Dong',3)
    generate_employee('public area cleaner', 'khach san A Dong',1)
    generate_employee('housekeeping', 'khach san A Dong',3)
    generate_employee('receptionist', 'khach san A Dong',1)
    generate_employee('cashier', 'khach san A Dong',1)
    generate_employee('concierge', 'khach san A Dong',1)
    generate_employee('bell man', 'khach san A Dong',3)
    generate_employee('door man', 'khach san A Dong',2)
    generate_employee('waiter', 'khach san A Dong',2)
    generate_employee('cook assistant', 'khach san A Dong',4)
    generate_employee('bartender', 'khach san A Dong',2)
    generate_employee('food runner', 'khach san A Dong',3)
    generate_employee('steward', 'khach san A Dong',2)
    
    click.echo('Initialized sample data.')

@click.command('create-roster')
@with_appcontext
def create_roster_command():
    generate_roster('gardener', '9', 'example name gardener1', '7AM', '6hours', '20/5/2022', 'No', '4')
    generate_roster('baby sitter', '11', 'example name baby sitter1', '7AM', '6hours', '20/5/2022', 'No', '4')
    generate_roster('linen room', '15', 'example name linen room1', '7AM', '6hours', '20/5/2022', 'No', '4')
    generate_roster('public area cleaner', '18', 'example name public area cleaner1', '7AM', '6hours', '20/5/2022', 'No', '4')
    generate_roster('housekeeping', '19', 'example name housekeeping1', '7AM', '6hours', '20/5/2022', 'No', '4')
    generate_roster('receptionist', '22', 'example name receptionist1', '7AM', '6hours', '20/5/2022', 'No', '4')
    generate_roster('cashier', '23', 'example name cashier1', '7AM', '6hours', '20/5/2022', 'No', '4')
    generate_roster('concierge', '24', 'example name concierge1', '7AM', '6hours', '20/5/2022', 'No', '4')
    generate_roster('bell man', '25', 'example name bell man1', '7AM', '6hours', '20/5/2022', 'No', '4')
    generate_roster('door man', '28', 'example name door man1', '7AM', '6hours', '20/5/2022', 'No', '4')
    generate_roster('waiter', '30', 'example name waiter1', '7AM', '6hours', '20/5/2022', 'No', '4')
    generate_roster('cook assistant', '32', 'example name cook assistant1', '7AM', '6hours', '20/5/2022', 'No', '4')
    generate_roster('bartender', '36', 'example name bartender1', '7AM', '6hours', '20/5/2022', 'No', '4')
    generate_roster('food runner', '38', 'example name food runner1', '7AM', '6hours', '20/5/2022', 'No', '4')
    generate_roster('steward', '41', 'example name food steward1', '7AM', '6hours', '20/5/2022', 'No', '4')
    click.echo('Initialized roster.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(create_admin_acc_command)
    app.cli.add_command(create_sample_data_command)
    app.cli.add_command(create_roster_command)