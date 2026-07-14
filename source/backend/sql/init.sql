-- 智教通数据库初始化脚本
-- 创建数据库
CREATE DATABASE IF NOT EXISTS zjiaotong CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE zjiaotong;

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('teacher', 'student', 'admin') NOT NULL,
    name VARCHAR(50),
    school VARCHAR(100),
    subject VARCHAR(50),
    grade VARCHAR(20),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 工具表
CREATE TABLE IF NOT EXISTS tools (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    category ENUM('文科', '理科', '通用') NOT NULL,
    subject VARCHAR(50),
    icon VARCHAR(50),
    prompt_template TEXT NOT NULL,
    interface_config JSON,
    creator_id INT,
    is_preset BOOLEAN DEFAULT FALSE,
    is_public BOOLEAN DEFAULT TRUE,
    share_code VARCHAR(20) UNIQUE,
    usage_count INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (creator_id) REFERENCES users(id)
);

-- 工具模板表
CREATE TABLE IF NOT EXISTS tool_templates (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    category ENUM('文科', '理科', '通用') NOT NULL,
    subject VARCHAR(50),
    description TEXT,
    prompt_template TEXT NOT NULL,
    default_config JSON,
    icon VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 使用记录表
CREATE TABLE IF NOT EXISTS usage_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    tool_id INT NOT NULL,
    input_text TEXT,
    output_text TEXT,
    session_id VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (tool_id) REFERENCES tools(id)
);

-- 收藏表
CREATE TABLE IF NOT EXISTS favorites (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    tool_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (tool_id) REFERENCES tools(id),
    UNIQUE KEY (user_id, tool_id)
);

-- 推荐规则表
CREATE TABLE IF NOT EXISTS recommend_rules (
    id INT PRIMARY KEY AUTO_INCREMENT,
    subject VARCHAR(50),
    need_type VARCHAR(50),
    tool_ids JSON,
    priority INT DEFAULT 0
);