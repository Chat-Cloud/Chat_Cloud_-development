

show databases;

-- 데이터 베이스 생성
CREATE DATABASE ChatAnalysis;
USE ChatAnalysis;

-- Users 테이블
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    profile_img VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-------------------------------------------------------

-- ChatRooms 테이블
CREATE TABLE ChatRooms (
    room_id INT AUTO_INCREMENT PRIMARY KEY,
    room_name VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-------------------------------------------------------

-- RoomMembers (N:M 관계 테이블)
CREATE TABLE RoomMembers (
    room_id INT NOT NULL,
    user_id INT NOT NULL,
    joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    role VARCHAR(20) DEFAULT 'member',

    PRIMARY KEY (room_id, user_id),
    FOREIGN KEY (room_id) REFERENCES ChatRooms(room_id)
        ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
        ON DELETE CASCADE
);

-------------------------------------------------------

-- Messages 테이블
CREATE TABLE Messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    room_id INT NOT NULL,
    user_id INT,
    content TEXT,
    message_type ENUM('text','image','file') DEFAULT 'text',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (room_id) REFERENCES ChatRooms(room_id)
        ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
        ON DELETE SET NULL
);

-------------------------------------------------------

-- SentimentAnalysis 테이블
CREATE TABLE SentimentAnalysis (
    sentiment_id INT AUTO_INCREMENT PRIMARY KEY,
    message_id INT UNIQUE NOT NULL,
    sentiment_label ENUM('positive','neutral','negative') NOT NULL,
    positive_score FLOAT DEFAULT 0,
    negative_score FLOAT DEFAULT 0,
    neutral_score FLOAT DEFAULT 0,
    analyzed_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (message_id) REFERENCES Messages(message_id)
        ON DELETE CASCADE
);

-------------------------------------------------------

-- WordCloudResults 테이블
CREATE TABLE WordCloudResults (
    wc_id INT AUTO_INCREMENT PRIMARY KEY,
    room_id INT NOT NULL,
    start_date DATE,
    end_date DATE,
    keywords_json JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (room_id) REFERENCES ChatRooms(room_id)
        ON DELETE CASCADE
);

-------------------------------------------------------

-- ConversationStats 테이블
CREATE TABLE ConversationStats (
    stat_id INT AUTO_INCREMENT PRIMARY KEY,
    room_id INT NOT NULL,
    total_messages INT DEFAULT 0,
    most_active_user INT,
    peak_time VARCHAR(50),
    avg_message_length FLOAT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (room_id) REFERENCES ChatRooms(room_id)
        ON DELETE CASCADE,
    FOREIGN KEY (most_active_user) REFERENCES Users(user_id)
        ON DELETE SET NULL
);

show tables;