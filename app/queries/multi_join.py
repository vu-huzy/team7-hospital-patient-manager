"""
Multi-table Join Query - Complex join across 4+ tables
Shows comprehensive view of patient care including departments
"""
from app.db.connection import get_connection

def get_patient_doctor_treatments():
    """
    Multi-table JOIN query across Patient, Doctor, Appointment, Billing, and Department
    
    Returns comprehensive treatment information including:
    - Patient details
    - Doctor details with department
    - Treatment details
    - Billing information
    
    Returns:
        List of dictionaries with complete treatment records
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    p.patient_id,
                    p.full_name AS patient_name,
                    p.gender AS patient_gender,
                    p.phone_number AS patient_phone,
                    d.doctor_id,
                    d.full_name AS doctor_name,
                    d.specialization AS treatment_type,
                    d.phone_number AS doctor_phone,
                    dep.department_name,
                    dep.location AS department_location,
                    a.appointment_id,
                    a.appointment_date AS treatment_date,
                    a.reason AS treatment_reason,
                    a.status AS appointment_status,
                    b.bill_id,
                    b.amount_due AS cost,
                    b.amount_paid,
                    b.payment_status,
                    b.payment_method,
                    b.payment_date,
                    (b.amount_due - b.amount_paid) AS balance_due
                FROM Patient p
                INNER JOIN Appointment a ON p.patient_id = a.patient_id
                INNER JOIN Doctor d ON a.doctor_id = d.doctor_id
                LEFT JOIN Department dep ON d.department_id = dep.department_id
                LEFT JOIN Billing b ON a.appointment_id = b.appointment_id
                ORDER BY a.appointment_date DESC, p.patient_id
            """
            cursor.execute(query)
            return cursor.fetchall()
    finally:
        connection.close()

def get_department_performance():
    """
    Multi-table join to analyze department performance
    
    Returns:
        Department statistics including patient count, revenue, appointments
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    dep.department_id,
                    dep.department_name,
                    dep.location,
                    dep.head_of_department,
                    COUNT(DISTINCT d.doctor_id) AS doctor_count,
                    COUNT(DISTINCT a.patient_id) AS patient_count,
                    COUNT(a.appointment_id) AS total_appointments,
                    COALESCE(SUM(b.amount_due), 0) AS total_revenue,
                    COALESCE(SUM(b.amount_paid), 0) AS total_collected,
                    COALESCE(AVG(b.amount_due), 0) AS avg_treatment_cost
                FROM Department dep
                LEFT JOIN Doctor d ON dep.department_id = d.department_id
                LEFT JOIN Appointment a ON d.doctor_id = a.doctor_id
                LEFT JOIN Billing b ON a.appointment_id = b.appointment_id
                GROUP BY dep.department_id, dep.department_name, 
                         dep.location, dep.head_of_department
                ORDER BY total_revenue DESC
            """
            cursor.execute(query)
            return cursor.fetchall()
    finally:
        connection.close()

def get_doctor_patient_summary():
    """
    Multi-table join showing doctor workload and patient relationships
    
    Returns:
        Doctor statistics with patient counts and revenue
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    d.doctor_id,
                    d.full_name AS doctor_name,
                    d.specialization,
                    dep.department_name,
                    COUNT(DISTINCT a.patient_id) AS unique_patients,
                    COUNT(a.appointment_id) AS total_appointments,
                    COUNT(CASE WHEN a.status = 'Completed' THEN 1 END) AS completed_appointments,
                    COUNT(CASE WHEN a.status = 'Scheduled' THEN 1 END) AS scheduled_appointments,
                    COALESCE(SUM(b.amount_due), 0) AS total_revenue,
                    COALESCE(AVG(b.amount_due), 0) AS avg_cost_per_visit
                FROM Doctor d
                LEFT JOIN Department dep ON d.department_id = dep.department_id
                LEFT JOIN Appointment a ON d.doctor_id = a.doctor_id
                LEFT JOIN Billing b ON a.appointment_id = b.appointment_id
                GROUP BY d.doctor_id, d.full_name, d.specialization, dep.department_name
                ORDER BY total_appointments DESC
            """
            cursor.execute(query)
            return cursor.fetchall()
    finally:
        connection.close()

def get_patient_visit_history():
    """
    Multi-table join showing complete patient visit history
    
    Returns:
        Patient visit history with all related information
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    p.patient_id,
                    p.full_name AS patient_name,
                    COUNT(a.appointment_id) AS total_visits,
                    MIN(a.appointment_date) AS first_visit,
                    MAX(a.appointment_date) AS last_visit,
                    COUNT(DISTINCT d.doctor_id) AS doctors_seen,
                    COUNT(DISTINCT dep.department_id) AS departments_visited,
                    COALESCE(SUM(b.amount_due), 0) AS total_spent,
                    COALESCE(SUM(b.amount_paid), 0) AS total_paid,
                    COALESCE(SUM(b.amount_due - b.amount_paid), 0) AS outstanding_balance
                FROM Patient p
                LEFT JOIN Appointment a ON p.patient_id = a.patient_id
                LEFT JOIN Doctor d ON a.doctor_id = d.doctor_id
                LEFT JOIN Department dep ON d.department_id = dep.department_id
                LEFT JOIN Billing b ON a.appointment_id = b.appointment_id
                GROUP BY p.patient_id, p.full_name
                HAVING total_visits > 0
                ORDER BY total_visits DESC, total_spent DESC
            """
            cursor.execute(query)
            return cursor.fetchall()
    finally:
        connection.close()
