DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

DROP TABLE IF EXISTS hotel;
DROP TABLE IF EXISTS account;
DROP TABLE IF EXISTS rooms;
DROP TABLE IF EXISTS roster;
DROP TABLE IF EXISTS laundry_monitoring;
DROP TABLE IF EXISTS gardener_monitoring;
DROP TABLE IF EXISTS baby_sitter_monitoring;
DROP TABLE IF EXISTS linen_room_monitoring;
DROP TABLE IF EXISTS public_area_cleaner_monitoring;
DROP TABLE IF EXISTS housekeeping_monitoring;
DROP TABLE IF EXISTS receptionist_monitoring;
DROP TABLE IF EXISTS cashier_monitoring;
DROP TABLE IF EXISTS concierge_monitoring;
DROP TABLE IF EXISTS bell_man_monitoring;
DROP TABLE IF EXISTS door_man_monitoring;
DROP TABLE IF EXISTS chef_monitoring;
DROP TABLE IF EXISTS waiter_monitoring;
DROP TABLE IF EXISTS cook_assistant_monitoring;
DROP TABLE IF EXISTS bartender_monitoring;
DROP TABLE IF EXISTS food_runner_monitoring;
DROP TABLE IF EXISTS steward_monitoring;

CREATE TABLE hotel (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  address TEXT UNIQUE NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE account (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  name TEXT NOT NULL,
  phone TEXT NOT NULL,
  working_at TEXT NOT NULL,
  position TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (working_at) REFERENCES hotel (name)
);

CREATE TABLE rooms (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  belonging_to TEXT NOT NULL,
  kind_of_room TEXT NOT NULL,
  room_name TEXT UNIQUE NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (belonging_to) REFERENCES hotel (name)
);

CREATE TABLE roster ( -- get in4
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  position TEXT NOT NULL,
  staff_id TEXT NOT NULL,
  staff_name TEXT NOT NULL,
  start_time TEXT NOT NULL,
  work_hour TEXT NOT NULL,
  date TEXT NOT NULL,
  report TEXT,
  created_by_id TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (created_by_id) REFERENCES account (id),
  FOREIGN KEY (staff_name) REFERENCES account (name)
  FOREIGN KEY (staff_id) REFERENCES account (id)
);

CREATE TABLE laundry_monitoring ( -- da xong cho HR,  for the employees themselves -- get in4
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  belonging_room_id TEXT NOT NULL,
  staff_execute_id TEXT NOT NULL,
  -- shift_status TEXT NOT NULL,
  -- work_hour TEXT NOT NULL,
  status TEXT NOT NULL,
  note TEXT,
  created_by_id TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (belonging_room_id) REFERENCES rooms (id),
  FOREIGN KEY (created_by_id) REFERENCES account (id),
  FOREIGN KEY (staff_execute_id) REFERENCES account (id)
);

CREATE TABLE gardener_monitoring ( -- da xong cho HR,  for the employees themselves, get in4
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  staff_execute_id TEXT NOT NULL,
  -- shift_status TEXT NOT NULL,
  -- work_hour TEXT NOT NULL,
  note TEXT,
  created_by_id TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (created_by_id) REFERENCES account (id),
  FOREIGN KEY (staff_execute_id) REFERENCES account (id)
);

CREATE TABLE baby_sitter_monitoring ( -- da xong cho HR,  for the employees themselves, get in4
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  staff_execute_id TEXT NOT NULL,
  -- shift_status TEXT NOT NULL,
  -- work_hour TEXT NOT NULL,
  note TEXT,
  created_by_id TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (created_by_id) REFERENCES account (id),
  FOREIGN KEY (staff_execute_id) REFERENCES account (id)
);

CREATE TABLE linen_room_monitoring ( -- da xong cho HR, for the employees themselves, get in4
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  belonging_room_id TEXT NOT NULL,
  staff_execute_id TEXT NOT NULL,
  -- shift_status TEXT NOT NULL,
  -- work_hour TEXT NOT NULL,
  status TEXT NOT NULL,
  note TEXT,
  created_by_id TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (belonging_room_id) REFERENCES rooms (id),
  FOREIGN KEY (created_by_id) REFERENCES account (id),
  FOREIGN KEY (staff_execute_id) REFERENCES account (id)
);

CREATE TABLE public_area_cleaner_monitoring ( -- xong HR,  for the employees themselves, get in4
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  staff_execute_id TEXT NOT NULL,
  -- shift_status TEXT NOT NULL,
  -- work_hour TEXT NOT NULL,
  note TEXT,
  created_by_id TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (created_by_id) REFERENCES account (id),
  FOREIGN KEY (staff_execute_id) REFERENCES account (id)
);

CREATE TABLE housekeeping_monitoring ( -- xong HR,  for the employees themselves, get in4
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  belonging_room_id TEXT NOT NULL,
  staff_execute_id TEXT NOT NULL,
  room_status TEXT NOT NULL,
  -- shift_status TEXT NOT NULL,
  -- work_hour TEXT NOT NULL,
  status TEXT NOT NULL,
  note TEXT,
  created_by_id TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (belonging_room_id) REFERENCES rooms (id),
  FOREIGN KEY (created_by_id) REFERENCES account (id),
  FOREIGN KEY (staff_execute_id) REFERENCES account (id)
);

CREATE TABLE receptionist_monitoring ( --  for the employees themselves, get in4
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  staff_execute_id TEXT NOT NULL,
  number_of_check_in INT,
  number_of_check_out INT,
  -- shift_status TEXT NOT NULL,
  -- work_hour TEXT NOT NULL,
  note TEXT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (staff_execute_id) REFERENCES account (id)
);

CREATE TABLE cashier_monitoring (   --  for the employees themselves, get in4
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  staff_execute_id TEXT NOT NULL,
  -- shift_status TEXT NOT NULL,
  -- work_hour TEXT NOT NULL,
  note TEXT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (staff_execute_id) REFERENCES account (id)
);

CREATE TABLE concierge_monitoring ( --  for the employees themselves, get in4
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  staff_execute_id TEXT NOT NULL,
  -- shift_status TEXT NOT NULL,
  -- work_hour TEXT NOT NULL,
  note TEXT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (staff_execute_id) REFERENCES account (id)
);

CREATE TABLE bell_man_monitoring ( -- da xong cho HR, for the employees themselves, get in4
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  belonging_room_id TEXT NOT NULL,
  staff_execute_id TEXT NOT NULL,
  -- shift_status TEXT NOT NULL,
  -- work_hour TEXT NOT NULL,
  status TEXT NOT NULL,
  note TEXT,
  created_by_id TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (belonging_room_id) REFERENCES rooms (id),
  FOREIGN KEY (created_by_id) REFERENCES account (id),
  FOREIGN KEY (staff_execute_id) REFERENCES account (id)
);

CREATE TABLE door_man_monitoring ( -- xong HR,  for the employees themselves, get in4
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  staff_execute_id TEXT NOT NULL,
  -- shift_status TEXT NOT NULL,
  -- work_hour TEXT NOT NULL,
  note TEXT,
  created_by_id TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (created_by_id) REFERENCES account (id),
  FOREIGN KEY (staff_execute_id) REFERENCES account (id)
);

CREATE TABLE chef_monitoring (  --for the employees themselves
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  staff_execute_id TEXT NOT NULL,
  menu TEXT NOT NULL,
  -- shift_status TEXT NOT NULL,
  -- work_hour TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (staff_execute_id) REFERENCES account (id)
);

CREATE TABLE waiter_monitoring ( --xong HR  for the employees themselves
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  belonging_room_id TEXT,
  staff_execute_id TEXT NOT NULL,
  -- shift_status TEXT NOT NULL,
  -- work_hour TEXT NOT NULL,
  status TEXT NOT NULL,
  note TEXT,
  created_by_id TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (belonging_room_id) REFERENCES rooms (id),
  FOREIGN KEY (created_by_id) REFERENCES account (id),
  FOREIGN KEY (staff_execute_id) REFERENCES account (id)
);

CREATE TABLE cook_assistant_monitoring (-- xong HR,  for the employees themselves, get in4
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  staff_execute_id TEXT NOT NULL,
  -- shift_status TEXT NOT NULL,
  -- work_hour TEXT NOT NULL,
  note TEXT,
  created_by_id TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (created_by_id) REFERENCES account (id),
  FOREIGN KEY (staff_execute_id) REFERENCES account (id)
);

CREATE TABLE bartender_monitoring (-- xong HR,  for the employees themselves, get in4
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  staff_execute_id TEXT NOT NULL,
  -- shift_status TEXT NOT NULL,
  -- work_hour TEXT NOT NULL,
  note TEXT,
  created_by_id TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (created_by_id) REFERENCES account (id),
  FOREIGN KEY (staff_execute_id) REFERENCES account (id)
);

CREATE TABLE food_runner_monitoring (-- xong HR,  for the employees themselves, get in4
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  staff_execute_id TEXT NOT NULL,
  -- shift_status TEXT NOT NULL,
  -- work_hour TEXT NOT NULL,
  note TEXT,
  created_by_id TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (created_by_id) REFERENCES account (id),
  FOREIGN KEY (staff_execute_id) REFERENCES account (id)
);

CREATE TABLE steward_monitoring ( -- xong HR,  for the employees themselves, get in4
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  staff_execute_id TEXT NOT NULL,
  -- shift_status TEXT NOT NULL,
  -- work_hour TEXT NOT NULL,
  note TEXT,
  created_by_id TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (created_by_id) REFERENCES account (id),
  FOREIGN KEY (staff_execute_id) REFERENCES account (id)
);