import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()
os.makedirs('charts', exist_ok=True)

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'charset': 'utf8mb4'
}

def execute_sql_file(cursor, filepath):
    """Execute SQL statements from a file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    statements = sql_content.split(';')
    for statement in statements:
        statement = statement.strip()
        if statement and not statement.startswith('--'):
            try:
                cursor.execute(statement)
            except Exception as e:
                if 'already exists' not in str(e).lower():
                    print(f"Warning: {e}")

def init_database():
    """Initialize database with schema and data"""
    print("="*80)
    print("DATABASE INITIALIZATION")
    print("="*80)
    
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        cursor.execute("CREATE DATABASE IF NOT EXISTS hospital_manager")
        cursor.execute("USE hospital_manager")
        print("✓ Database created/connected")
        
        schema_path = os.path.join('app', 'db', 'schema.sql')
        seed_path = os.path.join('app', 'db', 'seed.sql')
        views_path = os.path.join('app', 'db', 'views_procedures.sql')
        
        if os.path.exists(schema_path):
            execute_sql_file(cursor, schema_path)
            connection.commit()
            print("✓ Schema loaded")
        
        if os.path.exists(seed_path):
            execute_sql_file(cursor, seed_path)
            connection.commit()
            print("✓ Sample data loaded")
        
        if os.path.exists(views_path):
            execute_sql_file(cursor, views_path)
            connection.commit()
            print("✓ Views and procedures loaded")
        
        cursor.close()
        connection.close()
        print("✓ Database initialization complete\n")
        return True
        
    except Exception as e:
        print(f"✗ Database initialization error: {e}")
        return False

def get_db_connection():
    """Establish connection to MySQL database"""
    try:
        config = DB_CONFIG.copy()
        config['database'] = 'hospital_manager'
        connection = pymysql.connect(**config)
        print("✓ Connected to database\n")
        return connection
    except pymysql.Error as e:
        print(f"✗ Connection error: {e}")
        return None

def close_db_connection(connection):
    """Close database connection"""
    if connection:
        connection.close()
        print("\n✓ Connection closed")

def query_view_department_revenue(connection):
    print("="*80)
    print("VIEW 1: Department Revenue Summary")
    print("="*80)
    
    try:
        query = "SELECT * FROM v_department_revenue ORDER BY total_revenue DESC"
        df = pd.read_sql(query, connection)
        
        if df.empty:
            print("No revenue data found.")
            return None
        
        print(df.to_string(index=False))
        print(f"\nTotal Departments: {len(df)}")
        print(f"Total Revenue: ${df['total_revenue'].sum():,.2f}")
        print(f"Total Paid: ${df['total_paid'].sum():,.2f}")
        print(f"Outstanding: ${df['total_outstanding'].sum():,.2f}")
        return df
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

def query_view_patient_appointments(connection, limit=10):
    print("\n" + "="*80)
    print("VIEW 2: Recent Patient Appointments")
    print("="*80)
    
    try:
        query = f"SELECT * FROM v_patient_appointments LIMIT {limit}"
        df = pd.read_sql(query, connection)
        
        if df.empty:
            print("No appointments found.")
            return None
        
        print(df.to_string(index=False))
        print(f"\nTotal Appointments: {len(df)}")
        return df
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

def query_view_unpaid_bills(connection):
    print("\n" + "="*80)
    print("VIEW 3: Outstanding Bills")
    print("="*80)
    
    try:
        query = "SELECT * FROM v_unpaid_bills ORDER BY outstanding_amount DESC"
        df = pd.read_sql(query, connection)
        
        if df.empty:
            print("No unpaid bills found.")
            return None
        
        print(df.to_string(index=False))
        print(f"\nTotal Unpaid Bills: {len(df)}")
        print(f"Total Outstanding: ${df['outstanding_amount'].sum():,.2f}")
        return df
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

def call_procedure_monthly_revenue(connection, year=2025, month=11):
    print("\n" + "="*80)
    print(f"PROCEDURE: Monthly Revenue Report ({month}/{year})")
    print("="*80)
    
    try:
        cursor = connection.cursor()
        cursor.callproc('sp_monthly_revenue_by_department', [year, month])
        
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(results, columns=columns)
        
        if df.empty:
            print("No revenue data for this period.")
            cursor.close()
            return None
        
        print(df.to_string(index=False))
        print(f"\nTotal Revenue for {month}/{year}: ${df['total_revenue'].sum():,.2f}")
        cursor.close()
        return df
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

def custom_query_department_stats(connection):
    print("\n" + "="*80)
    print("CUSTOM QUERY: Department Statistics")
    print("="*80)
    
    try:
        query = """
        SELECT 
            d.department_name,
            d.location,
            COUNT(DISTINCT doc.doctor_id) AS total_doctors,
            COUNT(DISTINCT a.appointment_id) AS total_appointments,
            COUNT(DISTINCT a.patient_id) AS unique_patients,
            SUM(CASE WHEN a.status = 'Completed' THEN 1 ELSE 0 END) AS completed,
            SUM(CASE WHEN a.status = 'Scheduled' THEN 1 ELSE 0 END) AS scheduled,
            SUM(CASE WHEN a.status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled
        FROM Department d
        LEFT JOIN Doctor doc ON d.department_id = doc.department_id
        LEFT JOIN Appointment a ON doc.doctor_id = a.doctor_id
        GROUP BY d.department_id, d.department_name, d.location
        ORDER BY total_appointments DESC
        """
        
        df = pd.read_sql(query, connection)
        if df.empty:
            print("No data found.")
            return None
        
        print(df.to_string(index=False))
        return df
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

def custom_query_doctor_performance(connection):
    print("\n" + "="*80)
    print("CUSTOM QUERY: Doctor Performance Report")
    print("="*80)
    
    try:
        query = """
        SELECT 
            doc.doctor_id,
            doc.full_name AS doctor_name,
            doc.specialization,
            dept.department_name,
            COUNT(DISTINCT a.appointment_id) AS total_appointments,
            COUNT(DISTINCT a.patient_id) AS unique_patients,
            SUM(b.amount_due) AS total_revenue_generated,
            SUM(b.amount_paid) AS total_collected,
            AVG(b.amount_due) AS avg_billing_amount
        FROM Doctor doc
        LEFT JOIN Department dept ON doc.department_id = dept.department_id
        LEFT JOIN Appointment a ON doc.doctor_id = a.doctor_id
        LEFT JOIN Billing b ON a.appointment_id = b.appointment_id
        GROUP BY doc.doctor_id, doc.full_name, doc.specialization, dept.department_name
        ORDER BY total_appointments DESC
        """
        
        df = pd.read_sql(query, connection)
        if df.empty:
            print("No data found.")
            return None
        
        print(df.to_string(index=False))
        return df
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

def visualize_department_revenue(df_revenue):
    print("\n" + "="*80)
    print("VISUALIZATION: Department Revenue (Bar Chart)")
    print("="*80)
    
    try:
        if df_revenue is None or df_revenue.empty:
            print("✗ No data available")
            return
        
        plt.figure(figsize=(12, 6))
        
        departments = df_revenue['department_name']
        revenue = df_revenue['total_revenue']
        paid = df_revenue['total_paid']
        outstanding = df_revenue['total_outstanding']
        
        x = range(len(departments))
        width = 0.25
        
        plt.bar([i - width for i in x], revenue, width, label='Total Revenue', color='#3498db')
        plt.bar(x, paid, width, label='Paid', color='#2ecc71')
        plt.bar([i + width for i in x], outstanding, width, label='Outstanding', color='#e74c3c')
        
        plt.xlabel('Department', fontsize=12)
        plt.ylabel('Amount ($)', fontsize=12)
        plt.title('Department Revenue Analysis', fontsize=14, fontweight='bold')
        plt.xticks(x, departments, rotation=45, ha='right')
        plt.legend()
        plt.tight_layout()
        
        filename = 'charts/department_revenue.png'
        plt.savefig(filename, dpi=300)
        plt.close()
        print(f"✓ Chart saved: {filename}")
    except Exception as e:
        print(f"✗ Error: {e}")

def visualize_monthly_revenue_trend(df_procedure):
    print("\n" + "="*80)
    print("VISUALIZATION: Monthly Revenue by Department")
    print("="*80)
    
    try:
        if df_procedure is None or df_procedure.empty:
            print("✗ No data available")
            return
        
        plt.figure(figsize=(10, 6))
        
        departments = df_procedure['department_name']
        revenue = df_procedure['total_revenue']
        
        plt.plot(departments, revenue, marker='o', linewidth=2, markersize=8, color='#3498db')
        plt.fill_between(range(len(departments)), revenue, alpha=0.3, color='#3498db')
        
        plt.xlabel('Department', fontsize=12)
        plt.ylabel('Revenue ($)', fontsize=12)
        plt.title('Monthly Revenue Trend by Department', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        filename = 'charts/monthly_revenue_trend.png'
        plt.savefig(filename, dpi=300)
        plt.close()
        print(f"✓ Chart saved: {filename}")
    except Exception as e:
        print(f"✗ Error: {e}")

def visualize_doctor_performance(df_doctor):
    print("\n" + "="*80)
    print("VISUALIZATION: Top Doctors by Appointments")
    print("="*80)
    
    try:
        if df_doctor is None or df_doctor.empty:
            print("✗ No data available")
            return
        
        df_top = df_doctor.nlargest(10, 'total_appointments')
        
        plt.figure(figsize=(12, 8))
        
        doctors = df_top['doctor_name']
        appointments = df_top['total_appointments']
        colors = plt.cm.viridis(appointments / appointments.max())
        
        plt.barh(doctors, appointments, color=colors)
        plt.xlabel('Total Appointments', fontsize=12)
        plt.ylabel('Doctor Name', fontsize=12)
        plt.title('Top 10 Doctors by Appointment Count', fontsize=14, fontweight='bold')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        
        filename = 'charts/doctor_performance.png'
        plt.savefig(filename, dpi=300)
        plt.close()
        print(f"✓ Chart saved: {filename}")
    except Exception as e:
        print(f"✗ Error: {e}")

def visualize_appointment_status(connection):
    print("\n" + "="*80)
    print("VISUALIZATION: Appointment Status Distribution")
    print("="*80)
    
    try:
        query = "SELECT status, COUNT(*) AS count FROM Appointment GROUP BY status"
        df = pd.read_sql(query, connection)
        
        if df.empty:
            print("✗ No data found")
            return
        
        plt.figure(figsize=(8, 8))
        
        colors = ['#2ecc71', '#3498db', '#e74c3c']
        explode = [0.1] + [0] * (len(df) - 1)
        
        plt.pie(df['count'], labels=df['status'], autopct='%1.1f%%', 
                startangle=90, colors=colors[:len(df)], explode=explode, shadow=True)
        plt.title('Appointment Status Distribution', fontsize=14, fontweight='bold')
        plt.axis('equal')
        
        filename = 'charts/appointment_status.png'
        plt.savefig(filename, dpi=300)
        plt.close()
        print(f"✓ Chart saved: {filename}")
    except Exception as e:
        print(f"✗ Error: {e}")

def main():
    print("\n" + "="*80)
    print("HOSPITAL PATIENT MANAGER")
    print("Database Application with Python & MySQL")
    print("="*80 + "\n")
    
    if not init_database():
        print("Database initialization failed. Please check your MySQL connection.")
        return
    
    connection = get_db_connection()
    if not connection:
        return
    
    try:
        print("### QUERYING VIEWS ###\n")
        df_revenue = query_view_department_revenue(connection)
        df_appointments = query_view_patient_appointments(connection, limit=10)
        df_unpaid = query_view_unpaid_bills(connection)
        
        print("\n\n### CALLING STORED PROCEDURES ###\n")
        df_monthly = call_procedure_monthly_revenue(connection, year=2025, month=11)
        
        print("\n\n### CUSTOM SQL QUERIES ###\n")
        df_dept_stats = custom_query_department_stats(connection)
        df_doctor_perf = custom_query_doctor_performance(connection)
        
        print("\n\n### DATA VISUALIZATION ###\n")
        visualize_department_revenue(df_revenue)
        visualize_monthly_revenue_trend(df_monthly)
        visualize_doctor_performance(df_doctor_perf)
        visualize_appointment_status(connection)
        
        print("\n" + "="*80)
        print("✓ Program completed successfully!")
        print("="*80)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
    finally:
        close_db_connection(connection)

if __name__ == "__main__":
    main()
