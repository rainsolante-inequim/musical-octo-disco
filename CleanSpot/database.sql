CREATE DATABASE IF NOT EXISTS cleanspot;
USE cleanspot;

CREATE TABLE IF NOT EXISTS waste_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    disposal_method TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS waste_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    waste_type VARCHAR(100) NOT NULL,
    location VARCHAR(255) NOT NULL,
    description TEXT,
    image VARCHAR(255),
    report_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'Reported'
);

INSERT INTO waste_items (item_name, category, disposal_method) VALUES
('Banana Peel', 'Biodegradable', 'Place in the biodegradable/compost bin.'),
('Food Scraps', 'Biodegradable', 'Place in the biodegradable or compost bin.'),
('Plastic Bottle', 'Recyclable', 'Empty, clean if possible, and place in the recyclable bin.'),
('Cardboard', 'Recyclable', 'Keep dry and place in the recyclable bin.'),
('Glass Bottle', 'Recyclable', 'Handle carefully and place in the appropriate glass recycling container.'),
('Used Tissue', 'Residual', 'Place in the residual waste bin.'),
('Battery', 'Special Waste', 'Bring to an appropriate hazardous/special-waste collection point.');

