/*
    CS340 Project Step 2 - Ski Resort Gear Rental System
    Group 80: Joshua Cabalka, Jack Boland, Philip Gadsden
*/

CREATE TABLE customers (
    customer_id AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) NULL,
    email VARCHAR(255) NULL,
    PRIMARY KEY (customer_id)
);

CREATE TABLE employees (
    employee_id AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (employee_id)
);

CREATE TABLE gear_items (
    gear_item_id INT AUTO_INCREMENT,
    category ENUM('snowboard', 'boots', 'helmet', 'other') NOT NULL,
    brand VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    serial_number VARCHAR(100) NOT NULL,
    size VARCHAR(50) NOT NULL,
    condition_grade ENUM('new', 'good', 'fair', 'needs_repair') NOT NULL,
    status ENUM('available', 'rented', 'in_service','retired') NOT NULL,
    acquired_at DATETIME NOT NULL,
    PRIMARY KEY (gear_item_id),
    UNIQUE (serial_number)
);

CREATE TABLE rental_orders (
    rental_order_id INT AUTO_INCREMENT,
    customer_id INT NOT NULL,
    created_by_employee_id INT NOT NULL,
    created_at DATETIME NOT NULL,
    PRIMARY KEY (rental_order_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (created_by_employee_id) REFERENCES employees(employee_id)
);

CREATE TABLE service_tickets (
    service_ticket_id INT AUTO_INCREMENT,
    opened_by_employee_id INT NOT NULL,
    status ENUM('open', 'in_progress', 'completed', 'canceled') NOT NULL,
    created_at DATETIME NOT NULL,
    PRIMARY KEY (service_ticket_id),
    FOREIGN KEY (opened_by_employee_id) REFERENCES employees(employee_id)
);

CREATE TABLE rental_order_items(
    rental_order_id INT NOT NULL,
    gear_item_id INT NOT NULL,
    checked_out_at DATETIME NOT NULL,
    due_at DATETIME NOT NULL,
    returned_at DATETIME NULL,
    PRIMARY KEY (rental_order_id, gear_item_id),
    FOREIGN KEY (rental_order_id) REFERENCES rental_orders(rental_order_id),
    FOREIGN KEY (gear_item_id) REFERENCES gear_items(gear_item_id)
);

CREATE TABLE service_ticket_items (
    service_ticket_id INT NOT NULL,
    gear_item_id INT NOT NULL,
    service_type ENUM('wax', 'tune', 'repair', 'binding_adjust', 'inspect') NOT NULL,
    started_at DATETIME NULL,
    completed_at DATETIME NULL,
    PRIMARY KEY (service_ticket_id, gear_item_id),
    FOREIGN KEY (service_ticket_id) REFERENCES service_tickets(service_ticket_id),
    FOREIGN KEY (gear_item_id) REFERENCES gear_items(gear_item_id)
);

INSERT INTO customers (first_name, last_name, phone, email)
VALUES
(),
(),
(),

INSERT INTO employees (first_name, last_name, role, is_active)
VALUES
(),
(),
(),

INSERT INTO gear_items (category, brand, model, serial_number, size, condition_grade, status, acquired_at)
VALUES
(),
(),
(),
();

INSERT INTO rental_orders (customer_id, created_by_employee_id, created_at)
VALUES
(),
(),
(),

INSERT INTO service_tickets (opened_by_employee_id, status, created_at)
VALUES
(),
(),
(),

INSERT INTO  service_ticket_items (service_ticket_id, gear_item_id, service_type, started_at, completed_at)
VALUES
(),
(),
(),
