# Hospital Patient Manager

A comprehensive hospital management system built with Python and MySQL.

## Team Information

**Team 7 Members:**
- Nguyen Tuan Anh - 11247260
- Tran Tuan Anh - 11247264
- Tran Minh Hoang - 11247292
- Vu Quoc Huy - 11247301

**University:** National Economics University  
**Faculty:** Data Science and Artificial Intelligence  
**Class:** AI66A

**Presentation Video:** https://www.youtube.com/watch?v=kpDl7LHAD3g

**Github Link :** https://github.com/vu-huzy/team7-hospital-patient-manager

## Features

- **MySQL Database**: 7 normalized tables (3NF)
- **3 Views**: Revenue reports, patient appointments, unpaid bills
- **2 Stored Procedures**: Create appointments, monthly revenue reports
- **2 Triggers**: Auto-update payment status
- **Standalone SQL Files**: CRUD operations and reporting queries (can run independently)
- **Python Program**: Database connection with data visualization
- **Flask Web Interface**: Complete CRUD operations

## Project Structure

```
hospital-patient-manager/

 app/                          # Main source code
    db/                       # Database module
       schema.sql            # 7 table definitions
       seed.sql              # Sample data
       views_procedures.sql  # Views, procedures, triggers
       connection.py         # Database connection
    models/                   # SQL CRUD operations (standalone)
       patients.sql          # Patient CRUD queries
       doctors.sql           # Doctor CRUD queries
       appointments.sql      # Appointment CRUD queries
    queries/                  # SQL reporting queries (standalone)
       inner_join.sql        # Patient treatments (INNER JOIN)
       left_join.sql         # All patients (LEFT JOIN)
       multi_join.sql        # Multi-table analysis
       high_cost.sql         # High-cost treatment analysis
    services/                 # Business logic
    ui/                       # Flask web interface
       templates/            # HTML templates
       static/               # CSS, JavaScript
 charts/                       # Auto-generated visualizations
 docs/                         # Report and slides
 .env                          # Configuration (not in Git)
 requirements.txt              # Python dependencies
 main.py                       # Main Python program (data analysis)
 run_web.py                    # Flask web app entry point
```

## Quick Start

### 1. System Requirements

- **Python 3.8+**
- **MySQL 8.0+**

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create .env file by .env.examples ( please to use your password )

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=hospital_manager
FLASK_ENV=development
SECRET_KEY=your-secret-key
```

### 4. Run Application

**Python Program (Data Analysis & Charts):**
```bash
python main.py
```

**Output:**
- Console displays data from Views, Procedures, and custom queries
- 4 PNG chart files created in the `charts/` folder:
  - `department_revenue.png` - Bar chart of revenue by department
  - `monthly_revenue_trend.png` - Line chart of revenue trends
  - `doctor_performance.png` - Horizontal bar chart of doctor performance
  - `appointment_status.png` - Pie chart of appointment status distribution

**Web Interface:**
```bash
python run_web.py
```
Then open the web link that on your cmd screen. 
http://127.0.0.1:5000

## Standalone SQL Files

All database queries are available as **standalone SQL files** that can be executed independently without Python.

### SQL Files Location

- **CRUD Operations**: `app/models/*.sql`
  - `patients.sql` - 9 patient management queries
  - `doctors.sql` - 10 doctor management queries  
  - `appointments.sql` - 12 appointment management queries

- **Reporting Queries**: `app/queries/*.sql`
  - `inner_join.sql` - 4 INNER JOIN queries (patient treatments)
  - `left_join.sql` - 5 LEFT JOIN queries (all patients including inactive)
  - `multi_join.sql` - 5 complex multi-table queries
  - `high_cost.sql` - 6 high-cost treatment analysis queries

### How to Use SQL Files

**Method 1: MySQL Command Line**
```bash
# Execute entire file
mysql -u root -p hospital_manager < app/models/patients.sql

# Execute specific query
mysql -u root -p hospital_manager -e "SELECT * FROM Patient LIMIT 5;"
```

**Method 2: MySQL Workbench**
1. Open MySQL Workbench and connect to database
2. Open SQL file: File → Open SQL Script → Select `app/models/patients.sql`
3. Select specific queries you want to run
4. Click Execute button (⚡) or press Ctrl+Shift+Enter

**Method 3: Python Integration**
```python
# Read and execute SQL file in Python
with open('app/models/patients.sql', 'r', encoding='utf-8') as f:
    queries = f.read().split(';')
    for query in queries:
        if query.strip():
            cursor.execute(query)
```


## Web Application (Flask)

**Files:** `run_web.py`, `app/ui/`

### Features

#### Dashboard (`/`)
- Display KPIs: Total patients, doctors, appointments, revenue
- Appointments per day chart (30 days)
- Specialization distribution chart
- Recent activities

#### Patient Management (`/patients`)
- List all patients
- Search by name
- Add new patient
- Edit patient information
- Delete patient (with confirmation)
- View details and medical history

#### Doctor Management (`/doctors`)
- List doctors by department
- Add/edit/delete doctors
- View work schedule
- Performance statistics

#### Appointment Management (`/appointments`)
- Create new appointment
- View calendar by day/week/month
- Update status (Scheduled/Completed/Cancelled)
- Cancel appointment

#### Reports (`/reports`)
- Revenue reports
- Outstanding bills report
- Patient statistics
- Export to CSV




