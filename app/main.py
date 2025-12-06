# -*- coding: utf-8 -*-
import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

# Create charts directory if it doesn't exist
os.makedirs('charts', exist_ok=True)

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'hospital_manager'),
    'charset': 'utf8mb4'
}

def get_db_connection():
    """Establish connection to MySQL database"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        print("✓ Successfully connected to MySQL database\n")
        return connection
    except pymysql.Error as e:
        print(f"✗ Error connecting to MySQL: {e}")
        return None

def close_db_connection(connection):
    """Close database connection safely"""
    if connection:
        connection.close()
        print("\n✓ Database connection closed")

def query_view_department_revenue(connection):
    """Query v_department_revenue view"""
    print("="*80)
    print("VIEW 1: v_department_revenue - Revenue Summary by Department")
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
        print(f"✗ Error querying view: {e}")
        return None

def query_view_patient_appointments(connection, limit=10):
    """Query v_patient_appointments view"""
    print("\n" + "="*80)
    print("VIEW 2: v_patient_appointments - Recent Patient Appointments")
    print("="*80)
    
    try:
        query = f"SELECT * FROM v_patient_appointments LIMIT {limit}"
        df = pd.read_sql(query, connection)
        
        if df.empty:
            print("No appointments found.")
            return None
        
        print(df.to_string(index=False))
        print(f"\nTotal Appointments Shown: {len(df)}")
        
        return df
        
    except Exception as e:
        print(f"✗ Error querying view: {e}")
        return None

def query_view_unpaid_bills(connection):
    """Query v_unpaid_bills view"""
    print("\n" + "="*80)
    print("VIEW 3: v_unpaid_bills - Outstanding Bills")
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
        print(f"✗ Error querying view: {e}")
        return None

def call_procedure_monthly_revenue(connection, year=2025, month=1):
    """Call sp_monthly_revenue_by_department stored procedure"""
    print("\n" + "="*80)
    print(f"PROCEDURE: sp_monthly_revenue_by_department({year}, {month})")
    print("="*80)
    
    try:
        cursor = connection.cursor()
        cursor.callproc('sp_monthly_revenue_by_department', [year, month])
        
        # Fetch results with column names
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
        print(f"✗ Error calling stored procedure: {e}")
        return None

def custom_query_department_stats(connection):
    """Custom JOIN query: Department statistics"""
    print("\n" + "="*80)
    print("CUSTOM QUERY 1: Department Statistics (with JOIN)")
    print("="*80)
    
    try:
        query = """
        SELECT 
            d.department_name,
            d.location,
            COUNT(DISTINCT doc.doctor_id) AS total_doctors,
            COUNT(DISTINCT a.appointment_id) AS total_appointments,
            COUNT(DISTINCT a.patient_id) AS unique_patients,
            SUM(CASE WHEN a.status = 'Completed' THEN 1 ELSE 0 END) AS completed_appointments,
            SUM(CASE WHEN a.status = 'Scheduled' THEN 1 ELSE 0 END) AS scheduled_appointments,
            SUM(CASE WHEN a.status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_appointments
        FROM Department d
        LEFT JOIN Doctor doc ON d.department_id = doc.department_id
        LEFT JOIN Appointment a ON doc.doctor_id = a.doctor_id
        GROUP BY d.department_id, d.department_name, d.location
        ORDER BY total_appointments DESC
        """
        
        df = pd.read_sql(query, connection)
        
        if df.empty:
            print("No department data found.")
            return None
        
        print(df.to_string(index=False))
        print(f"\nTotal Departments: {len(df)}")
        
        return df
        
    except Exception as e:
        print(f"✗ Error executing custom query: {e}")
        return None

def custom_query_doctor_performance(connection):
    """Custom query: Doctor performance metrics"""
    print("\n" + "="*80)
    print("CUSTOM QUERY 2: Doctor Performance Report")
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
            print("No doctor data found.")
            return None
        
        print(df.to_string(index=False))
        print(f"\nTotal Doctors: {len(df)}")
        
        return df
        
    except Exception as e:
        print(f"✗ Error executing custom query: {e}")
        return None

def visualize_department_revenue(df_revenue):
    """Create bar chart for department revenue"""
    print("\n" + "="*80)
    print("VISUALIZATION 1: Department Revenue (Bar Chart)")
    print("="*80)
    
    try:
        if df_revenue is None or df_revenue.empty:
            print("✗ No data available for visualization")
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
        
        print(f"✓ Chart saved as: {filename}")
        
    except Exception as e:
        print(f"✗ Error creating visualization: {e}")

def visualize_monthly_revenue_trend(df_procedure):
    """Create line chart from stored procedure results"""
    print("\n" + "="*80)
    print("VISUALIZATION 2: Monthly Revenue by Department (Line Chart)")
    print("="*80)
    
    try:
        if df_procedure is None or df_procedure.empty:
            print("✗ No data available for visualization")
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
        
        print(f"✓ Chart saved as: {filename}")
        
    except Exception as e:
        print(f"✗ Error creating visualization: {e}")

def visualize_doctor_performance(df_doctor):
    """Create horizontal bar chart for doctor performance"""
    print("\n" + "="*80)
    print("VISUALIZATION 3: Doctor Performance (Horizontal Bar Chart)")
    print("="*80)
    
    try:
        if df_doctor is None or df_doctor.empty:
            print("✗ No data available for visualization")
            return
        
        # Top 10 doctors by appointments
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
        
        print(f"✓ Chart saved as: {filename}")
        
    except Exception as e:
        print(f"✗ Error creating visualization: {e}")

def visualize_appointment_status(connection):
    """Create pie chart for appointment status distribution"""
    print("\n" + "="*80)
    print("VISUALIZATION 4: Appointment Status Distribution (Pie Chart)")
    print("="*80)
    
    try:
        query = """
        SELECT 
            status,
            COUNT(*) AS count
        FROM Appointment
        GROUP BY status
        """
        
        df = pd.read_sql(query, connection)
        
        if df.empty:
            print("✗ No appointment data found")
            return
        
        plt.figure(figsize=(8, 8))
        
        colors = ['#2ecc71', '#3498db', '#e74c3c']
        # Dynamic explode based on number of statuses
        explode = [0.1] + [0] * (len(df) - 1)
        
        plt.pie(df['count'], labels=df['status'], autopct='%1.1f%%', 
                startangle=90, colors=colors[:len(df)], explode=explode, shadow=True)
        plt.title('Appointment Status Distribution', fontsize=14, fontweight='bold')
        plt.axis('equal')
        
        filename = 'charts/appointment_status.png'
        plt.savefig(filename, dpi=300)
        plt.close()
        
        print(f"✓ Chart saved as: {filename}")
        
    except Exception as e:
        print(f"✗ Error creating visualization: {e}")

def main():
    """Main program execution"""
    print("\n" + "="*80)
    print("HOSPITAL PATIENT MANAGER - PYTHON PROGRAM")
    print("Part D: Database Connection, Query Execution, and Visualization")
    print("="*80 + "\n")
    
    # Connect to database
    connection = get_db_connection()
    if not connection:
        return
    
    try:
        # Part 1: Query Views
        print("\n### PART D.1: QUERYING VIEWS ###\n")
        df_revenue = query_view_department_revenue(connection)
        df_appointments = query_view_patient_appointments(connection, limit=10)
        df_unpaid = query_view_unpaid_bills(connection)
        
        # Part 2: Call Stored Procedures
        print("\n\n### PART D.2: CALLING STORED PROCEDURES ###\n")
        df_monthly = call_procedure_monthly_revenue(connection, year=2025, month=1)
        
        # Part 3: Custom SQL Queries
        print("\n\n### PART D.3: CUSTOM SQL QUERIES ###\n")
        df_dept_stats = custom_query_department_stats(connection)
        df_doctor_perf = custom_query_doctor_performance(connection)
        
        # Part 4: Data Visualizations
        print("\n\n### PART D.4: DATA VISUALIZATION ###\n")
        visualize_department_revenue(df_revenue)
        visualize_monthly_revenue_trend(df_monthly)
        visualize_doctor_performance(df_doctor_perf)
        visualize_appointment_status(connection)
        
        print("\n" + "="*80)
        print("✓ Program execution completed successfully!")
        print("="*80)
        
    except Exception as e:
        print(f"\n✗ Error during execution: {e}")
    
    finally:
        close_db_connection(connection)

if __name__ == "__main__":
    main()
