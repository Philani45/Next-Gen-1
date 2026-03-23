CREATE DATABASE IF NOT EXISTS traffic_app;
USE traffic_app;

-- USERS
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    home_address VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- LOCATIONS
-- stores searched places, class buildings, destinations, etc.
CREATE TABLE IF NOT EXISTS locations (
    location_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    location_name VARCHAR(150) NOT NULL,
    address VARCHAR(255),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- USER LOCATION HISTORY
-- locations the user searched/used
-- starred ones should display first in the app
CREATE TABLE IF NOT EXISTS user_location_history (
    history_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    location_id BIGINT NOT NULL,
    starred BOOLEAN DEFAULT FALSE,
    searched_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, location_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (location_id) REFERENCES locations(location_id) ON DELETE CASCADE
);

-- SCHEDULES
CREATE TABLE IF NOT EXISTS schedules (
    schedule_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    class_name VARCHAR(150) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- SCHEDULE MEETINGS
-- stores actual day/time/location for each class
-- one schedule can have many meetings
CREATE TABLE IF NOT EXISTS schedule_meetings (
    meeting_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    schedule_id BIGINT NOT NULL,
    day_of_week VARCHAR(20) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    location_id BIGINT,
    FOREIGN KEY (schedule_id) REFERENCES schedules(schedule_id) ON DELETE CASCADE,
    FOREIGN KEY (location_id) REFERENCES locations(location_id) ON DELETE SET NULL
);

-- ROUTES
-- between two locations
CREATE TABLE IF NOT EXISTS routes (
    route_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    start_location_id BIGINT NOT NULL,
    end_location_id BIGINT NOT NULL,
    route_name VARCHAR(150),
    roads_to_take TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (start_location_id) REFERENCES locations(location_id) ON DELETE CASCADE,
    FOREIGN KEY (end_location_id) REFERENCES locations(location_id) ON DELETE CASCADE
);

-- TRAFFIC OBSERVATIONS
-- stores traffic time for routes at certain times
CREATE TABLE IF NOT EXISTS traffic_observations (
    traffic_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    route_id BIGINT NOT NULL,
    observed_at DATETIME NOT NULL,
    duration_seconds INT NOT NULL,
    distance_meters INT,
    source VARCHAR(50) DEFAULT 'manual',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (route_id) REFERENCES routes(route_id) ON DELETE CASCADE
);

-- CLASS OPTIONS
CREATE TABLE IF NOT EXISTS class_options (
    option_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    class_name VARCHAR(150) NOT NULL,
    section_name VARCHAR(100),
    day_of_week VARCHAR(20) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    location_id BIGINT,
    recommended BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (location_id) REFERENCES locations(location_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS reminders (
    reminder_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    meeting_id BIGINT NOT NULL,
    leave_time DATETIME NOT NULL,
    reminder_time DATETIME NOT NULL,
    sent_status VARCHAR(20) DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (meeting_id) REFERENCES schedule_meetings(meeting_id) ON DELETE CASCADE
);