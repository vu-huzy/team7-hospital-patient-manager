"""
Left Join Query - All Patients with Optional Treatments
Shows ALL patients including those without any appointments
"""
from app.db.connection import get_connection

def get_patients_with_optional_treatments():
    """
    LEFT JOIN query to get all patients with their treatments (if any)
    
    Returns ALL patients, including those who haven't had appointments yet.
    For patients without appointments, treatment fields will be NULL.
    
    Returns:
        List of dictionaries with patient and optional treatment information
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    p.patient_id,
                    p.full_name AS patient_name,
                    p.gender,
                    p.date_of_birth,
                    p.phone_number,
                    p.email,
                    p.address,
                    p.date_registered,
                    a.appointment_id,
                    a.appointment_date AS treatment_date,
                    a.reason,
                    a.status,
                    d.full_name AS doctor_name,
                    d.specialization AS treatment_type,
                    b.amount_due AS cost,
                    b.payment_status
                FROM Patient p
                LEFT JOIN Appointment a ON p.patient_id = a.patient_id
                LEFT JOIN Doctor d ON a.doctor_id = d.doctor_id
                LEFT JOIN Billing b ON a.appointment_id = b.appointment_id
                ORDER BY p.patient_id, a.appointment_date DESC
            """
            cursor.execute(query)
            return cursor.fetchall()
    finally:
        connection.close()

def get_patients_without_treatments():
    """
    Get list of patients who have never had an appointment
    
    Returns:
        List of patients with no appointments
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    p.patient_id,
                    p.full_name AS patient_name,
                    p.gender,
                    p.date_of_birth,
                    p.phone_number,
                    p.email,
                    p.date_registered,
                    DATEDIFF(CURDATE(), p.date_registered) as days_since_registration
                FROM Patient p
                LEFT JOIN Appointment a ON p.patient_id = a.patient_id
                WHERE a.appointment_id IS NULL
                ORDER BY p.date_registered DESC
            """
            cursor.execute(query)
            return cursor.fetchall()
    finally:
        connection.close()

def get_patient_treatment_summary():
    """
    Get summary of patients with and without treatments
    
    Returns:
        Dictionary with counts
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    COUNT(DISTINCT p.patient_id) as total_patients,
                    COUNT(DISTINCT CASE WHEN a.appointment_id IS NOT NULL 
                          THEN p.patient_id END) as patients_with_treatments,
                    COUNT(DISTINCT CASE WHEN a.appointment_id IS NULL 
                          THEN p.patient_id END) as patients_without_treatments
                FROM Patient p
                LEFT JOIN Appointment a ON p.patient_id = a.patient_id
            """
            cursor.execute(query)
            return cursor.fetchone()
    finally:
        connection.close()
