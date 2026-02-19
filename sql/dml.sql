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


-- CUSTOMERS

-- name: customers_browse
SELECT customer_id, first_name, last_name, email, phone
FROM customers
ORDER BY customer_id;

-- name: customers_add
CALL customers_add(%s, %s, %s, %s);

-- name: customers_update
CALL customers_update(%s, %s, %s, %s, %s);

-- name: customers_delete
CALL customers_delete(%s);


-- EMPLOYEES

-- name: employees_browse
SELECT employee_id, first_name, last_name, role, is_active
FROM employees
ORDER BY employee_id;

-- name: employees_add
CALL employees_add(%s, %s, %s, %s);

-- name: employees_update
CALL employees_update(%s, %s, %s, %s, %s);

-- name: employees_delete
CALL employees_delete(%s);


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
CALL gear_items_add(%s, %s, %s, %s, %s, %s, %s, %s);

-- name: gear_items_update
CALL gear_items_update(%s, %s, %s, %s, %s, %s, %s, %s, %s);

-- name: gear_items_delete
CALL gear_items_delete(%s);


-- RENTAL ORDERS

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
CALL rental_orders_add(%s, %s, %s);

-- name: rental_orders_update
CALL rental_orders_update(%s, %s, %s, %s);

-- name: rental_orders_delete
CALL rental_orders_delete(%s);


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
CALL rental_order_items_add(%s, %s, %s, %s, %s);

-- name: rental_order_items_update
CALL rental_order_items_update(%s, %s, %s, %s, %s, %s, %s);

-- name: rental_order_items_delete
CALL rental_order_items_delete(%s, %s);


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
CALL service_tickets_add(%s, %s, %s);

-- name: service_tickets_update
CALL service_tickets_update(%s, %s, %s, %s);

-- name: service_tickets_delete
CALL service_tickets_delete(%s);


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
CALL service_ticket_items_add(%s, %s, %s, %s, %s);

-- name: service_ticket_items_update
CALL service_ticket_items_update(%s, %s, %s, %s, %s, %s, %s);

-- name: service_ticket_items_delete
CALL service_ticket_items_delete(%s, %s);


-- DATABASE RESET

-- name: db_reset
CALL sp_reset_ski_resort_db();