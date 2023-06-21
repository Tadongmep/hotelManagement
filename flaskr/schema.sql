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
  status TEXT DEFAULT 'Ready',
    -- Occupied: Khách hiện đang ở trong phòng
    -- Stayover: Khách không phải trả phòng ngày hôm nay và sẽ còn lại ít nhất một đêm nữa.
    -- On-change: Khách đã check out, nhưng phòng vẫn chưa được làm sạch để bán.
    -- Do not Disturb: Khách đã yêu cầu không được làm phiền
    -- Cleaning in progress: Nhân viên buồng phòng hiện đang làm sạch phòng này.
    -- Sleep-out: Một khách được đăng ký vào phòng, nhưng giường đã không được sử dụng.
    -- On-Queue: Khách đã đến khách sạn, nhưng phòng chưa sẵn sàng. Trong những trường hợp như vậy, phòng được đưa vào xếp hạng Queue theo yêu cầu của nhân viên buồng phòng để ưu tiên các phòng đó trước tiên.
    -- Skipper: Khách đã rời khỏi khách sạn mà không được sắp xếp để giải quyết thanh toán.
    -- Vacant and ready: Phòng đã được làm sạch, kiểm tra và đã sẵn sàng cho khách đến.
    -- Out of Order (OOO): Phòng không được bán và các phòng này sẽ được khấu trừ khỏi hàng tồn kho của khách sạn. Một phòng có thể không hợp lệ vì nhiều lý do khác nhau, bao gồm nhu cầu bảo trì, tân trang và làm sạch tổng thể…
    -- Out of service (OOS): Các phòng không đảm bảo dịch vụ để phục vụ khách. Đây là biện pháp tạm thời và các lý do có thể là cầu chì, bóng đèn, TV, ấm đun nước… không hoạt động. Những phòng này không được chỉ định cho khách cho đến khi những vấn đề bảo trì nhỏ này được khắc phục.
    -- Lock out: Phòng đã bị khóa để khách không thể vào lại cho đến khi người đó được kiểm tra bởi nhân viên khách sạn.
    -- DNCO (không check out): Khách đã sắp xếp giải quyết các khoản phí mình và rời đi mà không thông báo cho lễ tân.
    -- Due Out: Phòng dự kiến sẽ trở thành phòng trống sau khi khách check out.
    -- Check-out: Khách đã thanh toán hóa đơn của mình, trả lại chìa khóa phòng và rời khách sạn.
    -- Late check-out: Khách đã yêu cầu và được phép trả phòng muộn hơn thời gian khởi hành bình thường/ tiêu chuẩn của khách sạn.

  guest_name TEXT,
  more_infor TEXT,
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