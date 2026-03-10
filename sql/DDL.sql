/*  
    Joshua Cabalka, Jack Boland, Philip Gadsden
    Michael Curry
    CS340 
    2/10/2026
    Project 3 - SQL reset procedure to reset database to original.
 */


DROP PROCEDURE IF EXISTS sp_reset_ski_resort_db;
DELIMITER //

CREATE PROCEDURE sp_reset_ski_resort_db()
COMMENT 'Reset Ski Resort Gear Rental System schema + sample data'
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET FOREIGN_KEY_CHECKS = 1;
        SELECT 'Error: reset failed' AS result;
    END;

    SET FOREIGN_KEY_CHECKS = 0;
    START TRANSACTION;

    DROP TABLE IF EXISTS service_ticket_items;
    DROP TABLE IF EXISTS rental_order_items;
    DROP TABLE IF EXISTS service_tickets;
    DROP TABLE IF EXISTS rental_orders;
    DROP TABLE IF EXISTS gear_items;
    DROP TABLE IF EXISTS employees;
    DROP TABLE IF EXISTS customers;

    CREATE TABLE customers (
        customer_id INT AUTO_INCREMENT,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        email VARCHAR(255) NULL,
        phone VARCHAR(20) NULL,
        PRIMARY KEY (customer_id)
    );

    CREATE TABLE employees (
        employee_id INT AUTO_INCREMENT,
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
        size VARCHAR(20) NOT NULL,
        condition_grade ENUM('new', 'good', 'fair', 'needs_repair') NOT NULL,
        status ENUM('available', 'rented', 'in_service', 'retired') NOT NULL,
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
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
        FOREIGN KEY (created_by_employee_id) REFERENCES employees(employee_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    );

    CREATE TABLE service_tickets (
        service_ticket_id INT AUTO_INCREMENT,
        opened_by_employee_id INT NOT NULL,
        status ENUM('open', 'in_progress', 'completed', 'canceled') NOT NULL,
        created_at DATETIME NOT NULL,
        PRIMARY KEY (service_ticket_id),
        FOREIGN KEY (opened_by_employee_id) REFERENCES employees(employee_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    );

    CREATE TABLE rental_order_items (
        rental_order_id INT NOT NULL,
        gear_item_id INT NOT NULL,
        checked_out_at DATETIME NOT NULL,
        due_at DATETIME NOT NULL,
        returned_at DATETIME NULL,
        PRIMARY KEY (rental_order_id, gear_item_id),
        FOREIGN KEY (rental_order_id) REFERENCES rental_orders(rental_order_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
        FOREIGN KEY (gear_item_id) REFERENCES gear_items(gear_item_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    );

    CREATE TABLE service_ticket_items (
        service_ticket_id INT NOT NULL,
        gear_item_id INT NOT NULL,
        service_type ENUM('wax', 'tune', 'repair', 'binding_adjust', 'inspect') NOT NULL,
        started_at DATETIME NULL,
        completed_at DATETIME NULL,
        PRIMARY KEY (service_ticket_id, gear_item_id),
        FOREIGN KEY (service_ticket_id) REFERENCES service_tickets(service_ticket_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
        FOREIGN KEY (gear_item_id) REFERENCES gear_items(gear_item_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    );

    INSERT INTO customers (first_name, last_name, phone, email) VALUES
      ('John', 'Doe', '541-555-0101', 'john.doe@example.com'),
      ('Noah', 'Patel', NULL, 'noah.patel@example.com'),
      ('Mia', 'Johnson', '541-555-0103', NULL);

    INSERT INTO employees (first_name, last_name, role, is_active) VALUES
      ('Shaun', 'White', 'rental_associate', TRUE),
      ('Travis', 'Rice', 'service_tech', TRUE),
      ('Lindsey', 'Vonn', 'manager', FALSE);

    INSERT INTO gear_items (category, brand, model, serial_number, size, condition_grade, status, acquired_at) VALUES
      ('snowboard', 'Burton', 'Process', 'SNB-0001', '155', 'good', 'available', '2024-11-01 09:00:00'),
      ('boots', 'K2', 'Maysis', 'BTS-0101', '10', 'fair', 'rented', '2023-12-10 10:30:00'),
      ('helmet', 'Smith', 'Vantage', 'HLT-0201', 'M', 'new', 'in_service', '2024-10-15 14:00:00'),
      ('other', 'Dakine', 'Wrist Guard', 'OTH-0301', 'L', 'good', 'retired', '2022-01-05 08:15:00');

    INSERT INTO rental_orders (customer_id, created_by_employee_id, created_at) VALUES
      (1, 1, '2026-02-01 10:00:00'),
      (2, 1, '2026-02-02 11:15:00'),
      (3, 1, '2026-02-03 09:20:00');

    INSERT INTO rental_order_items (rental_order_id, gear_item_id, checked_out_at, due_at, returned_at) VALUES
      (1, 2, '2026-02-01 10:05:00', '2026-02-03 10:05:00', NULL),
      (2, 1, '2026-02-02 11:20:00', '2026-02-04 11:20:00', '2026-02-03 16:45:00'),
      (3, 1, '2026-02-03 09:25:00', '2026-02-05 09:25:00', NULL);

    INSERT INTO service_tickets (opened_by_employee_id, status, created_at) VALUES
      (2, 'open', '2026-02-01 08:30:00'),
      (2, 'in_progress', '2026-02-02 13:00:00'),
      (2, 'completed', '2026-02-03 15:10:00');

    INSERT INTO service_ticket_items (service_ticket_id, gear_item_id, service_type, started_at, completed_at) VALUES
      (1, 3, 'inspect', NULL, NULL),
      (2, 3, 'repair', '2026-02-02 13:15:00', NULL),
      (3, 3, 'wax', '2026-02-03 15:20:00', '2026-02-03 16:05:00');

    COMMIT;
    SET FOREIGN_KEY_CHECKS = 1;

    SELECT 'OK: database reset' AS result;
END //