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
    """Execute SQL statements from a file (handles DELIMITER blocks)"""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    delimiter = ';'
    buffer = []
    in_comment = False
    
    def execute_stmt(stmt_text):
        """Helper to execute a single statement with error handling"""
        if not stmt_text or stmt_text.startswith('--'):
            return
        try:
            cursor.execute(stmt_text)
        except Exception as e:
            err_msg = str(e).lower()
            if 'duplicate entry' not in err_msg and 'already exists' not in err_msg:
                print(f"Warning: {e}")
    
    for line in lines:
        stripped = line.strip()
        
        # Handle multi-line comments
        if '/*' in stripped:
            in_comment = True
        if in_comment:
            if '*/' in stripped:
                in_comment = False
            continue
        
        # Handle DELIMITER directive
        if stripped.upper().startswith('DELIMITER '):
            # Flush buffer before changing delimiter
            if buffer:
                stmt = ''.join(buffer).strip()
                if delimiter and stmt.endswith(delimiter):
                    stmt = stmt[:-len(delimiter)].strip()
                execute_stmt(stmt)
                buffer = []
            delimiter = stripped.split()[1] if len(stripped.split()) > 1 else ';'
            continue
        
        # Skip empty lines and comments
        if not stripped or stripped.startswith('--'):
            continue
        
        buffer.append(line)
        
        # Check if statement ends with current delimiter
        joined = ''.join(buffer).rstrip()
        if delimiter and joined.endswith(delimiter):
            stmt = joined[:-len(delimiter)].strip()
            execute_stmt(stmt)
            buffer = []
    
    # Execute remaining buffer
    if buffer:
        stmt = ''.join(buffer).strip()
        if delimiter and stmt.endswith(delimiter):
            stmt = stmt[:-len(delimiter)].strip()
        execute_stmt(stmt)

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

def test_triggers(connection):
    """Test billing triggers (auto-update payment_status)"""
    print("\n" + "="*80)
    print("TRIGGER TEST: Auto-update Payment Status")
    print("="*80)
    
    try:
        cursor = connection.cursor()
        
        # Test 1: Insert new billing record with full payment
        print("\n1. Testing INSERT trigger (Full Payment):")
        cursor.execute("""
            INSERT INTO Billing (patient_id, appointment_id, amount_due, amount_paid, payment_method)
            VALUES (1, 90, 500000, 500000, 'cash')
        """)
        connection.commit()
        
        cursor.execute("SELECT bill_id, amount_due, amount_paid, payment_status, payment_date FROM Billing WHERE appointment_id = 90")
        result = cursor.fetchone()
        if result:
            print(f"   Bill ID: {result[0]}, Amount Due: {result[1]}, Amount Paid: {result[2]}")
            print(f"   → Payment Status: {result[3]} (Expected: Paid)")
            print(f"   → Payment Date: {result[4]} (Auto-set by trigger)")
        
        # Test 2: Update billing record to partial payment
        print("\n2. Testing UPDATE trigger (Partial Payment):")
        cursor.execute("""
            UPDATE Billing 
            SET amount_paid = 250000 
            WHERE appointment_id = 90
        """)
        connection.commit()
        
        cursor.execute("SELECT amount_due, amount_paid, payment_status FROM Billing WHERE appointment_id = 90")
        result = cursor.fetchone()
        if result:
            print(f"   Amount Due: {result[0]}, Amount Paid: {result[1]}")
            print(f"   → Payment Status: {result[2]} (Expected: Partially Paid)")
        
        # Test 3: Update to unpaid
        print("\n3. Testing UPDATE trigger (Unpaid):")
        cursor.execute("""
            UPDATE Billing 
            SET amount_paid = 0 
            WHERE appointment_id = 90
        """)
        connection.commit()
        
        cursor.execute("SELECT amount_due, amount_paid, payment_status FROM Billing WHERE appointment_id = 90")
        result = cursor.fetchone()
        if result:
            print(f"   Amount Due: {result[0]}, Amount Paid: {result[1]}")
            print(f"   → Payment Status: {result[2]} (Expected: Unpaid)")
        
        # Cleanup test data
        cursor.execute("DELETE FROM Billing WHERE appointment_id = 90")
        connection.commit()
        print("\n✓ Trigger test completed (test data cleaned up)")
        
        cursor.close()
    except Exception as e:
        print(f"✗ Error testing triggers: {e}")

def verify_database_objects(connection):
    """Verify that all views, procedures, and triggers exist"""
    print("\n" + "="*80)
    print("DATABASE OBJECTS VERIFICATION")
    print("="*80)
    
    try:
        cursor = connection.cursor()
        
        # Check Views
        print("\n📊 VIEWS:")
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.VIEWS 
            WHERE TABLE_SCHEMA = 'hospital_manager'
            ORDER BY TABLE_NAME
        """)
        views = cursor.fetchall()
        if views:
            for i, view in enumerate(views, 1):
                print(f"   {i}. {view[0]}")
        else:
            print("   ✗ No views found")
        
        # Check Stored Procedures
        print("\n⚙️  STORED PROCEDURES:")
        cursor.execute("""
            SELECT ROUTINE_NAME 
            FROM INFORMATION_SCHEMA.ROUTINES 
            WHERE ROUTINE_SCHEMA = 'hospital_manager' 
            AND ROUTINE_TYPE = 'PROCEDURE'
            ORDER BY ROUTINE_NAME
        """)
        procedures = cursor.fetchall()
        if procedures:
            for i, proc in enumerate(procedures, 1):
                print(f"   {i}. {proc[0]}")
        else:
            print("   ✗ No procedures found")
        
        # Check Triggers
        print("\n🔔 TRIGGERS:")
        cursor.execute("""
            SELECT TRIGGER_NAME, EVENT_MANIPULATION, EVENT_OBJECT_TABLE
            FROM INFORMATION_SCHEMA.TRIGGERS 
            WHERE TRIGGER_SCHEMA = 'hospital_manager'
            ORDER BY TRIGGER_NAME
        """)
        triggers = cursor.fetchall()
        if triggers:
            for i, trig in enumerate(triggers, 1):
                print(f"   {i}. {trig[0]} ({trig[1]} on {trig[2]})")
        else:
            print("   ✗ No triggers found")
        
        print(f"\n✓ Total: {len(views)} views, {len(procedures)} procedures, {len(triggers)} triggers")
        cursor.close()
    except Exception as e:
        print(f"✗ Error verifying database objects: {e}")

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
        # Verify database objects first
        verify_database_objects(connection)
        
        print("\n\n### QUERYING VIEWS ###\n")
        df_revenue = query_view_department_revenue(connection)
        df_appointments = query_view_patient_appointments(connection, limit=10)
        df_unpaid = query_view_unpaid_bills(connection)
        
        print("\n\n### CALLING STORED PROCEDURES ###\n")
        df_monthly = call_procedure_monthly_revenue(connection, year=2025, month=11)
        
        # Test triggers
        test_triggers(connection)
        
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
