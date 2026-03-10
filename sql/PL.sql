DELIMITER //

-- CUSTOMERS
DROP PROCEDURE IF EXISTS customers_add//
CREATE PROCEDURE customers_add(
    IN p_first_name VARCHAR(100),
    IN p_last_name  VARCHAR(100),
    IN p_email      VARCHAR(255),
    IN p_phone      VARCHAR(20)
)
BEGIN
    INSERT INTO customers (first_name, last_name, email, phone)
    VALUES (p_first_name, p_last_name, p_email, p_phone);
END//

DROP PROCEDURE IF EXISTS customers_update//
CREATE PROCEDURE customers_update(
    IN p_first_name  VARCHAR(100),
    IN p_last_name   VARCHAR(100),
    IN p_email       VARCHAR(255),
    IN p_phone       VARCHAR(20),
    IN p_customer_id INT
)
BEGIN
    UPDATE customers
    SET first_name = p_first_name,
        last_name  = p_last_name,
        email      = p_email,
        phone      = p_phone
    WHERE customer_id = p_customer_id;
END//

DROP PROCEDURE IF EXISTS customers_delete//
CREATE PROCEDURE customers_delete(IN p_customer_id INT)
BEGIN
    DELETE FROM customers
    WHERE customer_id = p_customer_id;
END//


-- EMPLOYEES
DROP PROCEDURE IF EXISTS employees_add//
CREATE PROCEDURE employees_add(
    IN p_first_name VARCHAR(100),
    IN p_last_name  VARCHAR(100),
    IN p_role       VARCHAR(50),
    IN p_is_active  TINYINT
)
BEGIN
    INSERT INTO employees (first_name, last_name, role, is_active)
    VALUES (p_first_name, p_last_name, p_role, p_is_active);
END//

DROP PROCEDURE IF EXISTS employees_update//
CREATE PROCEDURE employees_update(
    IN p_first_name  VARCHAR(100),
    IN p_last_name   VARCHAR(100),
    IN p_role        VARCHAR(50),
    IN p_is_active   TINYINT,
    IN p_employee_id INT
)
BEGIN
    UPDATE employees
    SET first_name = p_first_name,
        last_name  = p_last_name,
        role       = p_role,
        is_active  = p_is_active
    WHERE employee_id = p_employee_id;
END//

DROP PROCEDURE IF EXISTS employees_delete//
CREATE PROCEDURE employees_delete(IN p_employee_id INT)
BEGIN
    DELETE FROM employees
    WHERE employee_id = p_employee_id;
END//


-- GEAR ITEMS
DROP PROCEDURE IF EXISTS gear_items_add//
CREATE PROCEDURE gear_items_add(
    IN p_category        VARCHAR(20),
    IN p_brand           VARCHAR(100),
    IN p_model           VARCHAR(100),
    IN p_serial_number   VARCHAR(100),
    IN p_size            VARCHAR(20),
    IN p_condition_grade VARCHAR(20),
    IN p_status          VARCHAR(20),
    IN p_acquired_at     DATETIME
)
BEGIN
    INSERT INTO gear_items
      (category, brand, model, serial_number, size, condition_grade, status, acquired_at)
    VALUES
      (p_category, p_brand, p_model, p_serial_number, p_size, p_condition_grade, p_status, p_acquired_at);
END//

DROP PROCEDURE IF EXISTS gear_items_update//
CREATE PROCEDURE gear_items_update(
    IN p_category        VARCHAR(20),
    IN p_brand           VARCHAR(100),
    IN p_model           VARCHAR(100),
    IN p_serial_number   VARCHAR(100),
    IN p_size            VARCHAR(20),
    IN p_condition_grade VARCHAR(20),
    IN p_status          VARCHAR(20),
    IN p_acquired_at     DATETIME,
    IN p_gear_item_id    INT
)
BEGIN
    UPDATE gear_items
    SET category        = p_category,
        brand           = p_brand,
        model           = p_model,
        serial_number   = p_serial_number,
        size            = p_size,
        condition_grade = p_condition_grade,
        status          = p_status,
        acquired_at     = p_acquired_at
    WHERE gear_item_id = p_gear_item_id;
END//

DROP PROCEDURE IF EXISTS gear_items_delete//
CREATE PROCEDURE gear_items_delete(IN p_gear_item_id INT)
BEGIN
    DELETE FROM gear_items
    WHERE gear_item_id = p_gear_item_id;
END//


-- RENTAL ORDERS
DROP PROCEDURE IF EXISTS rental_orders_add//
CREATE PROCEDURE rental_orders_add(
    IN p_customer_id            INT,
    IN p_created_by_employee_id INT,
    IN p_created_at             DATETIME
)
BEGIN
    INSERT INTO rental_orders (customer_id, created_by_employee_id, created_at)
    VALUES (p_customer_id, p_created_by_employee_id, p_created_at);
END//

DROP PROCEDURE IF EXISTS rental_orders_update//
CREATE PROCEDURE rental_orders_update(
    IN p_customer_id            INT,
    IN p_created_by_employee_id INT,
    IN p_created_at             DATETIME,
    IN p_rental_order_id        INT
)
BEGIN
    UPDATE rental_orders
    SET customer_id            = p_customer_id,
        created_by_employee_id = p_created_by_employee_id,
        created_at             = p_created_at
    WHERE rental_order_id = p_rental_order_id;
END//

DROP PROCEDURE IF EXISTS rental_orders_delete//
CREATE PROCEDURE rental_orders_delete(IN p_rental_order_id INT)
BEGIN
    DELETE FROM rental_orders
    WHERE rental_order_id = p_rental_order_id;
END//


-- RENTAL ORDER ITEMS (M:M)
DROP PROCEDURE IF EXISTS rental_order_items_add//
CREATE PROCEDURE rental_order_items_add(
    IN p_rental_order_id INT,
    IN p_gear_item_id    INT,
    IN p_checked_out_at  DATETIME,
    IN p_due_at          DATETIME,
    IN p_returned_at     DATETIME
)
BEGIN
    INSERT INTO rental_order_items
      (rental_order_id, gear_item_id, checked_out_at, due_at, returned_at)
    VALUES
      (p_rental_order_id, p_gear_item_id, p_checked_out_at, p_due_at, p_returned_at);
END//

DROP PROCEDURE IF EXISTS rental_order_items_update//
CREATE PROCEDURE rental_order_items_update(
    IN p_new_rental_order_id INT,
    IN p_new_gear_item_id    INT,
    IN p_checked_out_at      DATETIME,
    IN p_due_at              DATETIME,
    IN p_returned_at         DATETIME,
    IN p_old_rental_order_id INT,
    IN p_old_gear_item_id    INT
)
BEGIN
    UPDATE rental_order_items
    SET rental_order_id = p_new_rental_order_id,
        gear_item_id    = p_new_gear_item_id,
        checked_out_at  = p_checked_out_at,
        due_at          = p_due_at,
        returned_at     = p_returned_at
    WHERE rental_order_id = p_old_rental_order_id
      AND gear_item_id    = p_old_gear_item_id;
END//

DROP PROCEDURE IF EXISTS rental_order_items_delete//
CREATE PROCEDURE rental_order_items_delete(
    IN p_rental_order_id INT,
    IN p_gear_item_id    INT
)
BEGIN
    DELETE FROM rental_order_items
    WHERE rental_order_id = p_rental_order_id
      AND gear_item_id    = p_gear_item_id;
END//


-- SERVICE TICKETS
DROP PROCEDURE IF EXISTS service_tickets_add//
CREATE PROCEDURE service_tickets_add(
    IN p_opened_by_employee_id INT,
    IN p_status                VARCHAR(20),
    IN p_created_at             DATETIME
)
BEGIN
    INSERT INTO service_tickets (opened_by_employee_id, status, created_at)
    VALUES (p_opened_by_employee_id, p_status, p_created_at);
END//

DROP PROCEDURE IF EXISTS service_tickets_update//
CREATE PROCEDURE service_tickets_update(
    IN p_opened_by_employee_id INT,
    IN p_status                VARCHAR(20),
    IN p_created_at            DATETIME,
    IN p_service_ticket_id     INT
)
BEGIN
    UPDATE service_tickets
    SET opened_by_employee_id = p_opened_by_employee_id,
        status                = p_status,
        created_at            = p_created_at
    WHERE service_ticket_id = p_service_ticket_id;
END//

DROP PROCEDURE IF EXISTS service_tickets_delete//
CREATE PROCEDURE service_tickets_delete(IN p_service_ticket_id INT)
BEGIN
    DELETE FROM service_tickets
    WHERE service_ticket_id = p_service_ticket_id;
END//


-- SERVICE TICKET ITEMS (M:M)
DROP PROCEDURE IF EXISTS service_ticket_items_add//
CREATE PROCEDURE service_ticket_items_add(
    IN p_service_ticket_id INT,
    IN p_gear_item_id      INT,
    IN p_service_type      VARCHAR(30),
    IN p_started_at        DATETIME,
    IN p_completed_at      DATETIME
)
BEGIN
    INSERT INTO service_ticket_items
      (service_ticket_id, gear_item_id, service_type, started_at, completed_at)
    VALUES
      (p_service_ticket_id, p_gear_item_id, p_service_type, p_started_at, p_completed_at);
END//

DROP PROCEDURE IF EXISTS service_ticket_items_update//
CREATE PROCEDURE service_ticket_items_update(
    IN p_new_service_ticket_id INT,
    IN p_new_gear_item_id      INT,
    IN p_service_type          VARCHAR(30),
    IN p_started_at            DATETIME,
    IN p_completed_at          DATETIME,
    IN p_old_service_ticket_id INT,
    IN p_old_gear_item_id      INT
)
BEGIN
    UPDATE service_ticket_items
    SET service_ticket_id = p_new_service_ticket_id,
        gear_item_id      = p_new_gear_item_id,
        service_type      = p_service_type,
        started_at        = p_started_at,
        completed_at      = p_completed_at
    WHERE service_ticket_id = p_old_service_ticket_id
      AND gear_item_id      = p_old_gear_item_id;
END//

DROP PROCEDURE IF EXISTS service_ticket_items_delete//
CREATE PROCEDURE service_ticket_items_delete(
    IN p_service_ticket_id INT,
    IN p_gear_item_id      INT
)
BEGIN
    DELETE FROM service_ticket_items
    WHERE service_ticket_id = p_service_ticket_id
      AND gear_item_id      = p_gear_item_id;
END//

DELIMITER ;