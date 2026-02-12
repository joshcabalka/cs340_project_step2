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
from pathlib import Path
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

# DML Query loader - loaded once at startup into SQL_QUERIES dict
def load_queries_from_dml(dml_file_path: Path):
    query_dict = {}
    current_key = None
    current_lines = []
    # Get each line from the dml file and isolate it
    with dml_file_path.open("r", encoding="utf-8") as dml_file:
        for raw_line in dml_file:
            line = raw_line.rstrip
            if line.strip().lower().startswith("-- name:"):
                # Save the previous query before moving onto the next
                if current_key is not None:
                    query_text = "\n".join(current_lines).strip()
                    if query_text:
                        query_dict[current_key] = query_text
                # Then we can start a new query
                current_key = line.split(":", 1)[1].strip()
                current_lines = []
            else:
                # Ignore line comments
                if current_key is not None:
                    current_lines.append(line)
    # Save the final query block
    if current_key is not None:
        query_text = "\n".join(current_lines).strip()
        if query_text:
            query_dict[current_key] = query_text
    return query_dict

# Project paths and load SQL at startup
BASE_DIR = Path(__file__).resolve().parent
DML_FILE_PATH = BASE_DIR.parent / "sql" / "dml.sql"
SQL_QUERIES = load_queries_from_dml(DML_FILE_PATH)

# Get the sql query for the given text
def get_sql(query_name: str) -> str:
    if query_name not in SQL_QUERIES:
        raise KeyError(f"Missing query '{query_name}' in {DML_FILE_PATH}")
    return SQL_QUERIES[query_name]

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

# Input helper function for converting blank input to None 
# Makes SQL store NULL for empty fields
def blank_to_none(value):
    if value is None:
        return None
    value = str(value).strip()
    return value if value != "" else None

# Convert common form checkbox/text to 1/0
def parse_active_flag(raw_value):
    return 1 if str(raw_value).strip().lower() in ("1", "true", "on", "yes") else 0
# Render homepage with nav links
@app.route("/")
def render_index_page():
    return render_template("index.html")

#CUSTOMER ROUTES

# Browse customer records
@app.route("/customers", methods=["GET"])
def render_customers_page():
    customer_rows = run_select(get_sql("customers_browse"))
    return render_template("customers.html", rows=customer_rows)

# Add one customer record from submitted form
@app.route("/customers/add", methods=["POST"])
def add_customer_record():
    customer_first_name = request.form.get("first_name", "").strip()
    customer_last_name = request.form.get("last_name", "").strip()
    customer_email = blank_to_none(request.form.get("email"))
    customer_phone = blank_to_none(request.form.get("phone"))

    # Take the data that was input and insert it into the database
    # Uses parameterized queries
    run_action(
        get_sql("customers_add"),
        (customer_first_name, customer_last_name, customer_email, customer_phone),
    )
    return redirect(url_for("render_customers_page"))

# Update one customer record by customer_id
@app.route("/customers/update", methods=["POST"])
def update_customer_record():
    target_customer_id = request.form.get("customer_id")
    updated_first_name = request.form.get("first_name", "").strip()
    updated_last_name = request.form.get("last_name", "").strip()
    updated_email = blank_to_none(request.form.get("email"))
    updated_phone = blank_to_none(request.form.get("phone"))

    # Take the input data and insert it into the database using parameterized SQL queries
    run_action(
        get_sql("customers_update"),
        (updated_first_name, updated_last_name, updated_email, updated_phone, target_customer_id),
    )
    return redirect(url_for("render_customers_page"))

# Delete one customer record by customer_id
@app.route("/customers/delete", methods=["POST"])
def delete_customer_record():
    customer_id_to_delete = request.form.get("customer_id")
    run_action(get_sql("customers_delete"), (customer_id_to_delete,))
    return redirect(url_for("render_customers_page"))

#EMPLOYEE ROUTES

# Browse employee records
@app.route("/employees", methods=["GET"])
def render_employees_page():
    employee_rows = run_select(get_sql("employees_browse"))
    return render_template("employees.html", rows=employee_rows)

# Add one employee record
@app.route("/employees/add", methods=["POST"])
def add_employee_record():
    employee_first_name = request.form.get("first_name", "").strip()
    employee_last_name = request.form.get("last_name", "").strip()
    employee_role = request.form.get("role", "").strip()
    employee_is_active_text = request.form.get("is_active", "1")
    employee_is_active = parse_active_flag(request.form.get("is_active", "1"))

    # Take the input data and insert it into the database using parameterized SQL queries
    run_action(
        get_sql("employees_add"),
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
    updated_is_active = parse_active_flag(request.form.get("is_active", "1"))

    # Take the input data and insert it into the database using parameterized SQL queries
    run_action(
        get_sql("employees_update"),
        (updated_first_name, updated_last_name, updated_role, updated_is_active, target_employee_id),
    )
    return redirect(url_for("render_employees_page"))

# Delete one employee record by employee_id
@app.route("/employees/delete", methods=["POST"])
def delete_employee_record():
    employee_id_to_delete = request.form.get("employee_id")
    # Take the input data and delete that specific employee
    run_action(get_sql("employees_delete"), (employee_id_to_delete,))
    return redirect(url_for("render_employees_page"))

# GEAR ITEMS ROUTES

# Browse gear_items records
@app.route("/gear_items", methods=["GET"])
def render_gear_items_page():
    gear_item_rows = run_select(get_sql("gear_items_browse"))
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
        get_sql("gear_items_add"),
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
        get_sql("gear_items_update"),
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
    run_action(get_sql("gear_items_delete"), (gear_item_id_to_delete,))
    return redirect(url_for("render_gear_items_page"))

# RENTAL ORDERS ROUTES

# Browse rental orders
@app.route("/rental_orders", methods=["GET"])
def render_rental_orders_page():
    # Select all rental orders
    rental_order_rows = run_select(get_sql("rental_orders_browse"))

    # Fetch customers for dropdown
    customers = run_select(get_sql("rental_orders_customers_dropdown"))

    # Fetch employees for dropdown
    employees = run_select(get_sql("rental_orders_employees_dropdown"))

    return render_template("rental_orders.html",
                           rows=rental_order_rows, customers=customers,
                           employees=employees)

# Add one rental_orders record
@app.route("/rental_orders/add", methods=["POST"])
def add_rental_order_record():
    rental_order_customer_id = request.form.get("customer_id")
    rental_order_created_by_employee_id = request.form.get("created_by_employee_id")
    rental_order_created_at = request.form.get("created_at", "").strip()
    # Take the input data and add it to the database using parameterized SQL queries
    run_action(
        get_sql("rental_orders_add"),
        (rental_order_customer_id, rental_order_created_by_employee_id, rental_order_created_at),
    )
    return redirect(url_for("render_rental_orders_page"))

# Update one rental_orders record by rental_order_id
@app.route("/rental_orders/update", methods=["POST"])
def update_rental_order_record():
    target_rental_order_id = request.form.get("rental_order_id")
    updated_customer_id = request.form.get("customer_id")
    updated_created_by_employee_id = request.form.get("created_by_employee_id")
    updated_created_at = request.form.get("created_at", "").strip()

    # Take the input data and update the database using parameterized SQL queries
    run_action(
        get_sql("rental_orders_update"),
        (updated_customer_id, updated_created_by_employee_id, updated_created_at, target_rental_order_id),
    )
    return redirect(url_for("render_rental_orders_page"))

# Delete one rental_orders record by rental_order_id
@app.route("/rental_orders/delete", methods=["POST"])
def delete_rental_order_record():
    rental_order_id_to_delete = request.form.get("rental_order_id")
    # Take the input data and delete that specific rental order 
    run_action(get_sql("rental_orders_delete"),
               (rental_order_id_to_delete,))

    return redirect(url_for("render_rental_orders_page"))

# RENTAL ORDER ITEMS ROUTES

# Browse rental_order_items records
@app.route("/rental_order_items", methods=["GET"])
def render_rental_order_items_page():
    # Select all rental_order_items records
    rental_order_item_rows = run_select(get_sql("rental_order_items_browse")
    )
    # Fetch rental_orders for dropdown
    rental_orders = run_select(get_sql("rental_order_items_rental_orders_dropdown"))
    # Fetch gear_items for dropdown
    gear_items = run_select(get_sql("rental_order_items_gear_items_dropdown"))

    return render_template("rental_order_items.html",
                           rows=rental_order_item_rows,
                           rental_orders=rental_orders,
                           gear_items=gear_items)


# Add one rental_order_items record
@app.route("/rental_order_items/add", methods=["POST"])
def add_rental_order_item_record():
    related_rental_order_id = request.form.get("rental_order_id")
    related_gear_item_id = request.form.get("gear_item_id")
    checked_out_at_value = request.form.get("checked_out_at", "").strip()
    due_at_value = request.form.get("due_at", "").strip()
    returned_at_value = blank_to_none(request.form.get("returned_at"))

    # Take the input data and add it to the database using parameterized SQL queries
    run_action(
       get_sql("rental_order_items_add"),
        (related_rental_order_id,
         related_gear_item_id,
         checked_out_at_value,
         due_at_value,
         returned_at_value),
    )
    return redirect(url_for("render_rental_order_items_page"))

# Update one rental_order_items record by rental_order_item_id
# This route has a composite PK: we use old keys in WHERE to find existing rows
# Use new keys in SET in case key values are changed
@app.route("/rental_order_items/update", methods=["POST"])
def update_rental_order_item_record():
    old_rental_order_id = request.form.get("old_rental_order_id")
    old_gear_item_id = request.form.get("old_gear_item_id")
    new_rental_order_id = request.form.get("rental_order_id")
    new_gear_item_id = request.form.get("gear_item_id")
    new_checked_out_at = request.form.get("checked_out_at", "").strip()
    new_due_at = request.form.get("due_at", "").strip()
    new_returned_at = blank_to_none(request.form.get("returned_at"))

    # Take the input data and update the database using parameterized SQL queries
    run_action(
        get_sql("rental_order_items_update"),
        (
            new_rental_order_id,
            new_gear_item_id,
            new_checked_out_at,
            new_due_at,
            new_returned_at,
            old_rental_order_id,
            old_gear_item_id,
        ),
    )
    return redirect(url_for("render_rental_order_items_page"))

# Delete one rental_order_items record by rental_order_item_id
# This route has a composite PK rule - delete requires both key values
# (rental_order_id AND gear_item_id)
@app.route("/rental_order_items/delete", methods=["POST"])
def delete_rental_order_item_record():
    rental_order_id_to_delete = request.form.get("rental_order_id")
    gear_item_id_to_delete = request.form.get("gear_item_id")

    run_action(
        get_sql("rental_order_items_delete"),
        (rental_order_id_to_delete, gear_item_id_to_delete)
    )
    return redirect(url_for("render_rental_order_items_page"))

# SERVICE TICKETS ROUTES

# Browse service_tickets records
@app.route("/service_tickets", methods=["GET"])
def render_service_tickets_page():
    # Select all service ticket records
    service_ticket_rows = run_select(get_sql("service_tickets_browse"))

    # Fetch employees for dropdown
    employees = run_select(get_sql("service_tickets_employees_dropdown"))

    return render_template("service_tickets.html", rows=service_ticket_rows, employees=employees)

# Add one service_tickets record
@app.route("/service_tickets/add", methods=["POST"])
def add_service_ticket_record():
    opened_by_employee_id_value = request.form.get("opened_by_employee_id")
    service_ticket_status = request.form.get("status", "").strip()
    service_ticket_created_at = request.form.get("created_at", "").strip()

    # Take the input data and add it to the database using parameterized SQL queries
    run_action(
        get_sql("service_tickets_add"),
        (opened_by_employee_id_value, service_ticket_status, service_ticket_created_at),
    )
    return redirect(url_for("render_service_tickets_page"))

# Update one service_tickets record by service_ticket_id
@app.route("/service_tickets/update", methods=["POST"])
def update_service_ticket_record():
    target_service_ticket_id = request.form.get("service_ticket_id")
    updated_opened_by_employee_id = request.form.get("opened_by_employee_id")
    updated_status = request.form.get("status", "").strip()
    updated_created_at = request.form.get("created_at", "").strip()

    # Take the input data and update the database using parameterized SQL queries
    run_action(
       get_sql("service_tickets_update"),
        (updated_opened_by_employee_id, updated_status, updated_created_at, target_service_ticket_id),
    )
    return redirect(url_for("render_service_tickets_page"))

# Delete one service_tickets record by service_ticket_id
@app.route("/service_tickets/delete", methods=["POST"])
def delete_service_ticket_record():
    service_ticket_id_to_delete = request.form.get("service_ticket_id")
    # Take the input and delete the specified record
    run_action(get_sql("service_tickets_delete"),
               (service_ticket_id_to_delete,))
    return redirect(url_for("render_service_tickets_page"))

# SERVICE TICKET ITEMS ROUTES

# Browse service_ticket_items records
@app.route("/service_ticket_items", methods=["GET"])
def render_service_ticket_items_page():
    # Select all service ticket records
    service_ticket_item_rows = run_select(get_sql("service_ticket_items_browse"))

    # Fetch service_tickets for dropdown
    service_tickets = run_select(get_sql("service_ticket_items_service_tickets_dropdown"))

    # Fetch gear_items for dropdown
    gear_items = run_select(get_sql("service_ticket_items_gear_items_dropdown"))

    return render_template(
        "service_ticket_items.html",
        rows=service_ticket_item_rows,
        service_tickets=service_tickets,
        gear_items=gear_items
    )

# Add one service_ticket_items record
@app.route("/service_ticket_items/add", methods=["POST"])
def add_service_ticket_item_record():
    related_service_ticket_id = request.form.get("service_ticket_id")
    related_gear_item_id = request.form.get("gear_item_id")
    service_type_value = request.form.get("service_type", "").strip()
    started_at_value = blank_to_none(request.form.get("started_at"))
    completed_at_value = blank_to_none(request.form.get("completed_at"))

    # Take the input data and add it to the database using parameterized SQL queries
    run_action(
        get_sql("service_ticket_items_add"),
        (related_service_ticket_id,
         related_gear_item_id,
         service_type_value,
         started_at_value, completed_at_value),
    )
    return redirect(url_for("render_service_ticket_items_page"))

# Update one service_ticket_items record by service_ticket_item_id
# This route uses a composite PK: Use old keys in WHERE to find existing row
# Use new keys in SET in case key values are changed
@app.route("/service_ticket_items/update", methods=["POST"])
def update_service_ticket_item_record():
    old_service_ticket_id = request.form.get("old_service_ticket_id")
    old_gear_item_id = request.form.get("old_gear_item_id")
    new_service_ticket_id = request.form.get("service_ticket_id")
    new_gear_item_id = request.form.get("gear_item_id")
    new_service_type = request.form.get("service_type", "").strip()
    new_started_at = blank_to_none(request.form.get("started_at"))
    new_completed_at = blank_to_none(request.form.get("completed_at"))

    # Take the input data and update the database using parameterized SQL queries
    run_action(
        get_sql("service_ticket_items_update"),
        (
            new_service_ticket_id,
            new_gear_item_id,
            new_service_type,
            new_started_at,
            new_completed_at,
            old_service_ticket_id,
            old_gear_item_id,
        ),
    )
    return redirect(url_for("render_service_ticket_items_page"))

# Delete one service_ticket_items record by service_ticket_item_id
# This route uses a composite PK: Delete requires both key values
@app.route("/service_ticket_items/delete", methods=["POST"])
def delete_service_ticket_item_record():
    service_ticket_id_to_delete = request.form.get("service_ticket_id")
    gear_item_id_to_delete = request.form.get("gear_item_id")

    # Take the input key values and delete the service ticket item records
    run_action(
        get_sql("service_ticket_items_delete"),
        (service_ticket_id_to_delete, gear_item_id_to_delete),
    )
    return redirect(url_for("render_service_ticket_items_page"))


# APP START
if __name__ == "__main__":
    # Debug true while developing
    app_port = int(os.getenv("APP_PORT", "40404"))
    app.run(host="0.0.0.0", port=app_port, debug=True)




