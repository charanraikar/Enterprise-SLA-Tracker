CREATE DATABASE IF NOT EXISTS sla_tracker;
USE sla_tracker;

CREATE TABLE IF NOT EXISTS tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_name VARCHAR(120) NOT NULL,
    title VARCHAR(180) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(80) NOT NULL,
    priority VARCHAR(20) NOT NULL,
    status VARCHAR(30) NOT NULL,
    owner VARCHAR(120) NOT NULL,
    created_at DATETIME NOT NULL,
    due_at DATETIME NOT NULL,
    resolved_at DATETIME NULL,
    updated_at DATETIME NOT NULL
);

