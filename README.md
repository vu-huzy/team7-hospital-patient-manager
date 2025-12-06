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

## Features

- **MySQL Database**: 7 normalized tables (3NF)
- **3 Views**: Revenue reports, patient appointments, unpaid bills
- **2 Stored Procedures**: Create appointments, monthly revenue reports
- **2 Triggers**: Auto-update payment status
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
    models/                   # Data models (CRUD operations)
    queries/                  # SQL queries (JOIN operations)
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

## Technology Stack

- **MySQL 8.0** - Database Management System
- **Python 3.12** - Programming Language
- **PyMySQL 1.1.2** - MySQL Connector
- **Flask 3.1.2** - Web Framework
- **Pandas 2.3.0** - Data Manipulation
- **Matplotlib 3.10.3** - Data Visualization
- **Seaborn 0.13.2** - Statistical Visualization



