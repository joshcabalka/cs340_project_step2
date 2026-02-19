/*  
    Joshua Cabalka, Jack Boland, Philip Gadsden
    Michael Curry
    CS340 
    2/10/2026
    Project 3 - Ski Resort Gear Rental System
    This file contains all of the DML used by the frontend app.py
    Each query block starts with --name: query_key
    app.py loads and executes queries by these names
 */

-- name: db_reset
CALL sp_reset_ski_resort_db();

-- CUSTOMERS

-- name: customers_browse
SELECT customer_id, first_name, last_name, email, phone
FROM customers
ORDER BY customer_id;

-- name: customers_add
INSERT INTO customers (first_name, last_name, email, phone)
VALUES (%s, %s, %s, %s);

-- name: customers_update
UPDATE customers
SET first_name = %s,
    last_name = %s,
    email = %s,
    phone = %s
WHERE customer_id = %s;

-- name: customers_delete
DELETE FROM customers
WHERE customer_id = %s;


-- EMPLOYEES

-- name: employees_browse
SELECT employee_id, first_name, last_name, role, is_active
FROM employees
ORDER BY employee_id;

-- name: employees_add
INSERT INTO employees (first_name, last_name, role, is_active)
VALUES (%s, %s, %s, %s);

-- name: employees_update
UPDATE employees
SET first_name = %s,
    last_name = %s,
    role = %s,
    is_active = %s
WHERE employee_id = %s;

-- name: employees_delete
DELETE FROM employees
WHERE employee_id = %s;


-- GEAR ITEMS

-- name: gear_items_browse
SELECT gear_item_id,
       category,
       brand,
       model,
       serial_number,
       size,
       condition_grade,
       status,
       acquired_at
FROM gear_items
ORDER BY gear_item_id;

-- name: gear_items_add
INSERT INTO gear_items
(category, brand, model, serial_number, size, condition_grade, status, acquired_at)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);

-- name: gear_items_update
UPDATE gear_items
SET category = %s,
    brand = %s,
    model = %s,
    serial_number = %s,
    size = %s,
    condition_grade = %s,
    status = %s,
    acquired_at = %s
WHERE gear_item_id = %s;

-- name: gear_items_delete
DELETE FROM gear_items
WHERE gear_item_id = %s;


-- =========================================================
-- RENTAL ORDERS
-- =========================================================

-- name: rental_orders_browse
SELECT rental_order_id,
       customer_id,
       created_by_employee_id,
       created_at
FROM rental_orders
ORDER BY rental_order_id;

-- name: rental_orders_customers_dropdown
SELECT customer_id, first_name, last_name
FROM customers
ORDER BY customer_id;

-- name: rental_orders_employees_dropdown
SELECT employee_id, first_name, last_name, role
FROM employees
ORDER BY employee_id;

-- name: rental_orders_add
INSERT INTO rental_orders (customer_id, created_by_employee_id, created_at)
VALUES (%s, %s, %s);

-- name: rental_orders_update
UPDATE rental_orders
SET customer_id = %s,
    created_by_employee_id = %s,
    created_at = %s
WHERE rental_order_id = %s;

-- name: rental_orders_delete
DELETE FROM rental_orders
WHERE rental_order_id = %s;


-- RENTAL ORDER ITEMS (COMPOSITE PK: rental_order_id, gear_item_id)

-- name: rental_order_items_browse
SELECT rental_order_id,
       gear_item_id,
       checked_out_at,
       due_at,
       returned_at
FROM rental_order_items
ORDER BY rental_order_id, gear_item_id;

-- name: rental_order_items_rental_orders_dropdown
SELECT rental_order_id, customer_id
FROM rental_orders
ORDER BY rental_order_id DESC;

-- name: rental_order_items_gear_items_dropdown
SELECT gear_item_id, category, brand, model
FROM gear_items
ORDER BY gear_item_id;

-- name: rental_order_items_add
INSERT INTO rental_order_items
(rental_order_id, gear_item_id, checked_out_at, due_at, returned_at)
VALUES (%s, %s, %s, %s, %s);

-- name: rental_order_items_update
UPDATE rental_order_items
SET rental_order_id = %s,
    gear_item_id = %s,
    checked_out_at = %s,
    due_at = %s,
    returned_at = %s
WHERE rental_order_id = %s
  AND gear_item_id = %s;

-- name: rental_order_items_delete
DELETE FROM rental_order_items
WHERE rental_order_id = %s
  AND gear_item_id = %s;


-- SERVICE TICKETS

-- name: service_tickets_browse
SELECT service_ticket_id,
       opened_by_employee_id,
       status,
       created_at
FROM service_tickets
ORDER BY service_ticket_id;

-- name: service_tickets_employees_dropdown
SELECT employee_id, first_name, last_name, role
FROM employees
ORDER BY employee_id;

-- name: service_tickets_add
INSERT INTO service_tickets (opened_by_employee_id, status, created_at)
VALUES (%s, %s, %s);

-- name: service_tickets_update
UPDATE service_tickets
SET opened_by_employee_id = %s,
    status = %s,
    created_at = %s
WHERE service_ticket_id = %s;

-- name: service_tickets_delete
DELETE FROM service_tickets
WHERE service_ticket_id = %s;


-- SERVICE TICKET ITEMS (COMPOSITE PK: service_ticket_id, gear_item_id)

-- name: service_ticket_items_browse
SELECT service_ticket_id,
       gear_item_id,
       service_type,
       started_at,
       completed_at
FROM service_ticket_items
ORDER BY service_ticket_id, gear_item_id;

-- name: service_ticket_items_service_tickets_dropdown
SELECT service_ticket_id, status
FROM service_tickets
ORDER BY service_ticket_id DESC;

-- name: service_ticket_items_gear_items_dropdown
SELECT gear_item_id, category, brand, model
FROM gear_items
ORDER BY gear_item_id;

-- name: service_ticket_items_add
INSERT INTO service_ticket_items
(service_ticket_id, gear_item_id, service_type, started_at, completed_at)
VALUES (%s, %s, %s, %s, %s);

-- name: service_ticket_items_update
UPDATE service_ticket_items
SET service_ticket_id = %s,
    gear_item_id = %s,
    service_type = %s,
    started_at = %s,
    completed_at = %s
WHERE service_ticket_id = %s
  AND gear_item_id = %s;

-- name: service_ticket_items_delete
DELETE FROM service_ticket_items
WHERE service_ticket_id = %s
  AND gear_item_id = %s;
