-- ==========================================
-- CREATE DATABASE + SELECT IT
-- ==========================================

CREATE DATABASE IF NOT EXISTS traffic_app;
USE traffic_app;

-- ==========================================
-- TABLES WITH DUPLICATE PROTECTION
-- ==========================================

CREATE TABLE IF NOT EXISTS locations (
  location_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  label VARCHAR(100) NOT NULL,
  address_text VARCHAR(255),
  lat DECIMAL(9,6),
  lng DECIMAL(9,6),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (label, address_text)
);

CREATE TABLE IF NOT EXISTS users (
  user_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  home_location_id BIGINT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (home_location_id)
    REFERENCES locations(location_id)
    ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS routes (
  route_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  origin_location_id BIGINT NOT NULL,
  destination_location_id BIGINT NOT NULL,
  active BOOLEAN DEFAULT TRUE,
  UNIQUE (origin_location_id, destination_location_id),
  FOREIGN KEY (origin_location_id)
    REFERENCES locations(location_id),
  FOREIGN KEY (destination_location_id)
    REFERENCES locations(location_id)
);

CREATE TABLE IF NOT EXISTS traffic_observations (
  obs_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  route_id BIGINT NOT NULL,
  observed_at DATETIME NOT NULL,
  duration_seconds INT NOT NULL,
  distance_meters INT,
  source VARCHAR(40) DEFAULT 'mock',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (route_id, observed_at),
  FOREIGN KEY (route_id)
    REFERENCES routes(route_id)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS courses (
  course_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  school VARCHAR(120),
  code VARCHAR(30) NOT NULL,
  title VARCHAR(200) NOT NULL,
  UNIQUE (school, code)
);

CREATE TABLE IF NOT EXISTS course_meetings (
  meeting_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  course_id BIGINT NOT NULL,
  location_id BIGINT NOT NULL,
  day_of_week TINYINT NOT NULL,
  start_time TIME NOT NULL,
  end_time TIME NOT NULL,
  UNIQUE (course_id, day_of_week, start_time),
  FOREIGN KEY (course_id)
    REFERENCES courses(course_id)
    ON DELETE CASCADE,
  FOREIGN KEY (location_id)
    REFERENCES locations(location_id)
);

CREATE TABLE IF NOT EXISTS user_courses (
  user_course_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT NOT NULL,
  course_id BIGINT NOT NULL,
  term VARCHAR(40) NOT NULL,
  UNIQUE (user_id, course_id, term),
  FOREIGN KEY (user_id)
    REFERENCES users(user_id)
    ON DELETE CASCADE,
  FOREIGN KEY (course_id)
    REFERENCES courses(course_id)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS trip_plans (
  trip_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT NOT NULL,
  from_location_id BIGINT NOT NULL,
  to_location_id BIGINT NOT NULL,
  arrive_by DATETIME NOT NULL,
  buffer_minutes INT DEFAULT 10,
  recommended_departure DATETIME,
  status ENUM('planned','sent','cancelled') DEFAULT 'planned',
  UNIQUE (user_id, arrive_by),
  FOREIGN KEY (user_id)
    REFERENCES users(user_id)
    ON DELETE CASCADE,
  FOREIGN KEY (from_location_id)
    REFERENCES locations(location_id),
  FOREIGN KEY (to_location_id)
    REFERENCES locations(location_id)
);

CREATE TABLE IF NOT EXISTS notifications (
  notification_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  trip_id BIGINT NOT NULL,
  scheduled_for DATETIME NOT NULL,
  sent_at DATETIME,
  channel ENUM('push','email','sms') DEFAULT 'push',
  result ENUM('success','fail'),
  UNIQUE (trip_id, scheduled_for),
  FOREIGN KEY (trip_id)
    REFERENCES trip_plans(trip_id)
    ON DELETE CASCADE
);

-- ==========================================
-- SAMPLE DATA (SAFE TO RUN MULTIPLE TIMES)
-- ==========================================

INSERT IGNORE INTO locations (label, address_text, lat, lng) VALUES
('Home', '123 Main St, Duluth, GA', 34.002000, -84.144000),
('Campus', '400 Park Place, Atlanta, GA', 33.775000, -84.390000),
('Atlanta Downtown', 'Downtown Atlanta, GA', 33.749000, -84.388000);

INSERT IGNORE INTO users (name, email, home_location_id)
VALUES ('Student One', 'student1@example.com', 1);

INSERT IGNORE INTO routes (name, origin_location_id, destination_location_id)
VALUES ('Home to Downtown', 1, 3);

INSERT IGNORE INTO traffic_observations 
(route_id, observed_at, duration_seconds, distance_meters)
VALUES
(1, NOW() - INTERVAL 30 MINUTE, 2100, 45000),
(1, NOW() - INTERVAL 10 MINUTE, 2700, 45000);

INSERT IGNORE INTO courses (school, code, title)
VALUES ('Georgia State University', 'CSC3000', 'Software Engineering');

INSERT IGNORE INTO course_meetings 
(course_id, location_id, day_of_week, start_time, end_time)
VALUES (1, 2, 1, '09:30:00', '10:45:00');

INSERT IGNORE INTO user_courses (user_id, course_id, term)
VALUES (1, 1, 'Spring 2026');