# Joshua Cabalka, Jack Boland, Philip Gadsden
# Michael Curry
# CS340 
# 2/10/2026
# Project 3 - Ski Resort Gear Rental System
# This file starts a flask web app, connects to the MySQL database,
# Defines one page per entity and supports Browse/Add/Update/Delete operations

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
from dotenv import load_dotenv


load_dotenv()
# Setup Flask app
app = Flask(__name__)

# Server connection details TODO: update info
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", "3306"))
}

# Create and return a new MySQL connection object
# One connection per operation
def open_database_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Execute a SELECT  query and return rows as dictionaries
def run_select(sql_query_text, sql_query_parameters=()):
    database_connection = open_database_connection()
    dictionary_cursor = database_connection.cursor(dictionary=True)
    dictionary_cursor.execute(sql_query_text, sql_query_parameters)
    selected_rows = dictionary_cursor.fetchall()
    dictionary_cursor.close()
    database_connection.close()
    return selected_rows

# Run INSERT/UPDATE/DELETE query and commit
def run_action(sql_query_text, sql_query_parameters=()):
    database_connection = open_database_connection()
    action_cursor = database_connection.cursor()
    action_cursor.execute(sql_query_text, sql_query_parameters)
    database_connection.commit()
    action_cursor.close()
    database_connection.close()

# Render homepage with nav links
@app.route("/")
def render_index_page():
    return render_template("index.html")

#CUSTOMER ROUTES

# Browse customer records
@app.route("/customers", methods=["GET"])
def render_customers_page():
    customer_rows = run_select("SELECT * FROM customers ORDER BY customer_id")
    return render_template("customers.html", rows=customer_rows)

# Add one customer record from submitted form
@app.route("/customers/add", methods=["POST"])
def add_customer_record():
    customer_first_name = request.form.get("first_name", "").strip()
    customer_last_name = request.form.get("last_name", "").strip()
    customer_email = request.form.get("email", "").strip() or None
    customer_phone = request.form.get("phone", "").strip() or None

    # Take the data that was input and insert it into the database
    # Uses parameterized queries
    run_action(
        """
        INSERT INTO customers (first_name, last_name, email, phone)
        VALUES (%s, %s, %s, %s)
        """,
        (customer_first_name, customer_last_name, customer_email, customer_phone),
    )
    return redirect(url_for("render_customers_page"))

# Update one customer record by customer_id
@app.route("/customers/update", methods=["POST"])
def update_customer_record():
    target_customer_id = request.form.get("customer_id")
    updated_first_name = request.form.get("first_name", "").strip()
    updated_last_name = request.form.get("last_name", "").strip()
    updated_email = request.form.get("email", "").strip() or None
    updated_phone = request.form.get("phone")

    # Take the input data and insert it into the database using parameterized SQL queries
    run_action(
        """
        UPDATE customers
        SET first_name = %s, last_name = %s, email = %s, phone = %s
        WHERE customer_id = %s
        """,
        (updated_first_name, updated_last_name, updated_email, updated_phone, target_customer_id),
    )
    return redirect(url_for("render_customers_page"))

# Delete one customer record by customer_id
@app.route("/customers/delete", methods=["POST"])
def delete_customer_record():
    customer_id_to_delete = request.form.get("customer_id")
    run_action("DELETE FROM customers WHERE customer_id = %s", (customer_id_to_delete,))
    return redirect(url_for("render_customers_page"))

#EMPLOYEE ROUTES

# Browse employee records
@app.route("/employees", methods=["GET"])
def render_employees_page():
    employee_rows = run_select("SELECT * FROM employees ORDER BY employee_id")
    return render_template("employees.html", rows=employee_rows)

# Add one employee record
@app.route("/employees/add", methods=["POST"])
def add_employee_record():
    employee_first_name = request.form.get("first_name", "").strip()
    employee_last_name = request.form.get("last_name", "").strip()
    employee_role = request.form.get("role", "").strip()
    employee_is_active_text = request.form.get("is_active", "1")
    employee_is_active = 1 if employee_is_active_text in ("1", "true", "True", "on", "yes") else 0

    # Take the input data and insert it into the database using parameterized SQL queries
    run_action(
        """
        INSERT INTO employees (first_name, last_name, role, is_active)
        VALUES (%s, %s, %s, %s)
        """,
        (employee_first_name, employee_last_name, employee_role, employee_is_active),
    )
    return redirect(url_for("render_employees_page"))

# Update one employee record by employee_id
@app.route("/employees/update", methods=["POST"])
def update_employee_record():
    target_employee_id = request.form.get("employee_id")
    updated_first_name = request.form.get("first_name", "").strip()
    updated_last_name = request.form.get("last_name", "").strip()
    updated_role = request.form.get("role", "").strip()
    updated_is_active_text = request.form.get("is_active", "1")
    updated_is_active = 1 if updated_is_active_text in ("1", "true", "True", "on", "yes") else 0

    # Take the input data and insert it into the database using parameterized SQL queries
    run_action(
        """
        UPDATE employees
        SET first_name = %s, last_name = %s, role = %s, is_active = %s
        WHERE employee_id = %s
        """,
        (updated_first_name, updated_last_name, updated_role, updated_is_active, target_employee_id),
    )
    return redirect(url_for("render_employees_page"))

# Delete one employee record by employee_id
@app.route("/employees/delete", methods=["POST"])
def delete_employee_record():
    employee_id_to_delete = request.form.get("employee_id")
    # Take the input data and delete that specific employee
    run_action("DELETE FROM employees WHERE employee_id = %s", (employee_id_to_delete,))
    return redirect(url_for("render_employees_page"))

# GEAR ITEMS ROUTES

# Browse gear_items records
@app.route("/gear_items", methods=["GET"])
def render_gear_items_page():
    gear_item_rows = run_select("SELECT * FROM gear_items ORDER BY gear_item_id")
    return render_template("gear_items.html", rows=gear_item_rows)

# Add one gear_items record
@app.route("/gear_items/add", methods=["POST"])
def add_gear_item_record():
    gear_item_category = request.form.get("category", "").strip()
    gear_item_brand = request.form.get("brand", "").strip()
    gear_item_model = request.form.get("model", "").strip()
    gear_item_serial_number = request.form.get("serial_number", "").strip()
    gear_item_size = request.form.get("size", "").strip()
    gear_item_condition_grade = request.form.get("condition_grade", "").strip()
    gear_item_status = request.form.get("status", "").strip()
    gear_item_acquired_at = request.form.get("acquired_at", "").strip()

    # Take the input data and add it to the database using parameterized SQL queries
    run_action(
        """
        INSERT INTO gear_items
        (category, brand, model, serial_number, size, condition_grade, status, acquired_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            gear_item_category,
            gear_item_brand,
            gear_item_model,
            gear_item_serial_number,
            gear_item_size,
            gear_item_condition_grade,
            gear_item_status,
            gear_item_acquired_at,
        ),
    )
    return redirect(url_for("render_gear_items_page"))

# Update one gear_items record by gear_item_id
@app.route("/gear_items/update", methods=["POST"])
def update_gear_item_record():
    target_gear_item_id = request.form.get("gear_item_id")
    updated_category = request.form.get("category", "").strip()
    updated_brand = request.form.get("brand", "").strip()
    updated_model = request.form.get("model", "").strip()
    updated_serial_number = request.form.get("serial_number", "").strip()
    updated_size = request.form.get("size", "").strip()
    updated_condition_grade = request.form.get("condition_grade", "").strip()
    updated_status = request.form.get("status", "").strip()
    updated_acquired_at = request.form.get("acquired_at", "").strip()

    # Take the input data and update the database using parameterized SQL queries
    run_action(
        """
        UPDATE gear_items
        SET category = %s, brand = %s, model = %s, serial_number = %s, size = %s,
        condition_grade = %s, status = %s, acquired_at = %s
        WHERE gear_item_id = %s
        """,
        (
            updated_category,
            updated_brand,
            updated_model,
            updated_serial_number,
            updated_size,
            updated_condition_grade,
            updated_status,
            updated_acquired_at,
            target_gear_item_id,
        ),
    )
    return redirect(url_for("render_gear_items_page"))

# Delete one gear_items record by gear_item_id
@app.route("/gear_items/delete", methods=["POST"])
def delete_gear_item_record():
    gear_item_id_to_delete = request.form.get("gear_item_id")
    # Take the input id and delete that specific item record
    run_action("DELETE FROM gear_items WHERE gear_item_id = %s", (gear_item_id_to_delete,))
    return redirect(url_for("render_gear_items_page"))

# RENTAL ORDERS ROUTES

# Browse rental orders
@app.route("/rental_orders", methods=["GET"])
def render_rental_orders_page():
    #TODO SELECT rental_orders
    return render_template("rental_orders.html", rows=rental_order_rows)

# Add one rental_orders record
@app.route("/rental_orders/add", methods=["POST"])
def add_rental_order_record():
    #TODO INSERT into rental_orders
    return redirect(url_for("render_rental_orders_page"))

# Update one rental_orders record by rental_order_id
@app.route("/rental_orders/update", methods=["POST"])
def update_rental_order_record():
    #TODO UPDATE rental_orders
    return redirect(url_for("render_rental_orders_page"))

# Delete one rental_orders record by rental_order_id
@app.route("/rental_orders/delete", methods=["POST"])
def delete_rental_order_record():
    #TODO DELETE from rental_orders
    return redirect(url_for("render_rental_orders_page"))

# RENTAL ORDER ITEMS ROUTES

# Browse rental_order_items records
@app.route("/rental_order_items", methods=["GET"])
def render_rental_order_items_page():
    # SELECT rental_order_items
    return render_template("rental_order_items.html", rows=rental_order_item_rows)

# Add one rental_order_items record
@app.route("/rental_order_items/add", methods=["POST"])
def add_rental_order_item_record():
    #TODO INSERT into rental_order_items
    return redirect(url_for("render_rental_order_items_page"))

# Update one rental_order_items record by rental_order_item_id
@app.route("/rental_order_items/update", methods=["POST"])
def update_rental_order_item_record():
    #TODO UPDATE rental_order_items
    return redirect(url_for("render_rental_order_items_page"))

# Delete one rental_order_items record by rental_order_item_id
@app.route("/rental_order_items/delete", methods=["POST"])
def delete_rental_order_item_record():
    #TODO DELETE from rental_order_items
    return redirect(url_for("render_rental_order_items_page"))

# SERVICE TICKETS ROUTES

# Browse service_tickets records
@app.route("/service_tickets", methods=["GET"])
def render_service_tickets_page():
    #TODO SELECT service_tickets
    return render_template("service_tickets.html", rows=service_ticket_rows)

# Add one service_tickets record
@app.route("/service_tickets/add", methods=["POST"])
def add_service_ticket_record():
    #TODO INSERT into service_tickets
    return redirect(url_for("render_service_tickets_page"))

# Update one service_tickets record by service_ticket_id
@app.route("/service_tickets/update", methods=["POST"])
def update_service_ticket_record():
    #TODO UPDATE service_tickets
    return redirect(url_for("render_service_tickets_page"))

# Delete one service_tickets record by service_ticket_id
@app.route("/service_tickets/delete", methods=["POST"])
def delete_service_ticket_record():
    #TODO DELETE from service_tickets
    return redirect(url_for("render_service_tickets_page"))

# SERVICE TICKET ITEMS ROUTES

# Browse service_ticket_items records
@app.route("/service_ticket_items", methods=["GET"])
def render_service_ticket_items_page():
    #TODO SELECT service_ticket_items
    return render_template("service_ticket_items.html", rows=service_ticket_item_rows)

# Add one service_ticket_items record
@app.route("/service_ticket_items/add", methods=["POST"])
def add_service_ticket_item_record():
    #TODO INSERT into service_ticket_items
    return redirect(url_for("render_service_ticket_items_page"))

# Update one service_ticket_items record by service_ticket_item_id
@app.route("/service_ticket_items/update", methods=["POST"])
def update_service_ticket_item_record():
    #TODO UPDATE service_ticket_items
    return redirect(url_for("render_service_ticket_items_page"))

# Delete one service_ticket_items record by service_ticket_item_id
@app.route("/service_ticket_items/delete", methods=["POST"])
def delete_service_ticket_item_record():
    #TODO DELETE from service_ticket_items
    return redirect(url_for("render_service_ticket_items_page"))


# APP START
if __name__ == "__main__":
    # Debug true while developing
    app.run(host="0.0.0.0", port=int(os.getenv("APP_PORT", "8317")), debug=True)




