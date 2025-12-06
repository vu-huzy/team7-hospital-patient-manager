"""
Inner Join Query - Patient Treatments
Shows all patients who have appointments with billing information
"""
from app.db.connection import get_connection

def get_patient_treatments():
    """
    INNER JOIN query to get patient treatments with costs
    
    Returns patients who have appointments with:
    - Patient name
    - Doctor name
    - Specialization (treatment type)
    - Appointment date
    - Cost (from billing)
    
    Only returns records where all relationships exist (INNER JOIN)
    
    Returns:
        List of dictionaries with treatment information
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    p.full_name AS patient_name,
                    p.phone_number AS patient_phone,
                    d.full_name AS doctor_name,
                    d.specialization AS treatment_type,
                    a.appointment_date AS treatment_date,
                    a.reason,
                    a.status,
                    b.amount_due AS cost,
                    b.payment_status
                FROM Patient p
                INNER JOIN Appointment a ON p.patient_id = a.patient_id
                INNER JOIN Doctor d ON a.doctor_id = d.doctor_id
                INNER JOIN Billing b ON a.appointment_id = b.appointment_id
                ORDER BY a.appointment_date DESC
            """
            cursor.execute(query)
            return cursor.fetchall()
    finally:
        connection.close()

def get_patient_treatments_summary():
    """
    Get summary statistics for patient treatments
    
    Returns:
        Dictionary with count, total cost, average cost
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    COUNT(*) as total_treatments,
                    SUM(b.amount_due) as total_cost,
                    AVG(b.amount_due) as average_cost,
                    COUNT(DISTINCT p.patient_id) as unique_patients,
                    COUNT(DISTINCT d.doctor_id) as unique_doctors
                FROM Patient p
                INNER JOIN Appointment a ON p.patient_id = a.patient_id
                INNER JOIN Doctor d ON a.doctor_id = d.doctor_id
                INNER JOIN Billing b ON a.appointment_id = b.appointment_id
            """
            cursor.execute(query)
            return cursor.fetchone()
    finally:
        connection.close()
