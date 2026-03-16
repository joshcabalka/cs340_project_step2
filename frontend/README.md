# Ski Resort Gear Rental System (CS340 Group 80)

## Live website
http://classwork.engr.oregonstate.edu:40405/

## Technology
Flask (Python) for the backend, HTML/Jinja templates for the UI, and MariaDB/MySQL for the database. All create, update, and delete operations are executed using stored procedures.

## Project structure
frontend/
- app.py
- templates/
- static/
- requirements.txt

sql/
- dml.sql
- project_step2.sql
- sql_reset.sql
- sql_procedures.sql

## Run / setup notes

### 1) Environment variables (.env)
Create a `.env` file (*do not commit it*). Required variables:

DB_HOST=
DB_USER=
DB_PASSWORD=
DB_NAME=
DB_PORT=3306
APP_PORT=40405

### 2) Compile stored procedures (MariaDB)
From a MariaDB prompt connected to your project database:

SOURCE /path/to/sql/sql_reset.sql;
SOURCE /path/to/sql/sql_procedures.sql;

Reset the DB (either from the UI or manually):

CALL sp_reset_ski_resort_db();

### 3) Install dependencies
From the repo root:

python3 -m venv .venv
source .venv/bin/activate
pip install -r frontend/requirements.txt

### 4) Run locally (foreground)
From the repo root:

source .venv/bin/activate
python frontend/app.py

### 5) Run on ENGR server (keep running after logout)
From the repo root:

cd frontend
source ../.venv/bin/activate
nohup python app.py > nohup.out 2>&1 &

To stop it later:

ps -u "$USER" -f | grep -E "python.*app\.py" | grep -v grep
kill <PID>

## Reset behavior
The Reset button on the index page calls the reset stored procedure and restores the schema and sample data back to the original state. You can verify by adding/updating a record, clicking Reset, and refreshing the page to see the data reverted.

## Citations / originality
Unless otherwise stated, code in this project is original work by the project team.

Any code that is not original (starter code, external snippets, or AI-assisted code) is cited in the relevant source file near where it appears.

### Citation for use of AI tools (format used in this project)

The following templates contain an AI citation block in this format:

<!-- Citation for use of AI tools:
     Date: 2026-03-12
     Prompts used to generate: Keep the existing update dropdown for customer_id,
     but auto-populate the selected customer's current values in the update form before submission.
     AI Source URL: https://chatgpt.com/ -->

Files that include an AI citation block:
- `frontend/templates/customers.html`
- `frontend/templates/employees.html`
- `frontend/templates/gear_items.html`