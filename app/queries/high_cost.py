"""
High Cost Treatments Query
Identifies treatments/specializations with costs above average
"""
from app.db.connection import get_connection

def get_high_cost_treatments():
    """
    Get treatments (by specialization/doctor) where cost > average
    
    Returns treatments with:
    - Specialization (treatment type)
    - Average cost for that specialization
    - Number of appointments
    - Number of unique patients
    - Comparison to overall average
    
    Only returns specializations with above-average costs
    
    Returns:
        List of high-cost treatment types
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                WITH OverallAverage AS (
                    SELECT AVG(amount_due) as avg_cost
                    FROM Billing
                ),
                SpecializationCosts AS (
                    SELECT 
                        d.specialization AS treatment_name,
                        COUNT(DISTINCT a.appointment_id) AS appointment_count,
                        COUNT(DISTINCT a.patient_id) AS patient_count,
                        AVG(b.amount_due) AS avg_cost,
                        MIN(b.amount_due) AS min_cost,
                        MAX(b.amount_due) AS max_cost,
                        SUM(b.amount_due) AS total_revenue
                    FROM Doctor d
                    INNER JOIN Appointment a ON d.doctor_id = a.doctor_id
                    INNER JOIN Billing b ON a.appointment_id = b.appointment_id
                    GROUP BY d.specialization
                )
                SELECT 
                    sc.treatment_name,
                    sc.avg_cost AS cost,
                    sc.min_cost,
                    sc.max_cost,
                    sc.total_revenue,
                    sc.appointment_count,
                    sc.patient_count,
                    oa.avg_cost AS overall_average,
                    ROUND((sc.avg_cost - oa.avg_cost) / oa.avg_cost * 100, 2) AS percent_above_avg
                FROM SpecializationCosts sc
                CROSS JOIN OverallAverage oa
                WHERE sc.avg_cost > oa.avg_cost
                ORDER BY sc.avg_cost DESC
            """
            cursor.execute(query)
            return cursor.fetchall()
    finally:
        connection.close()

def get_high_cost_doctors():
    """
    Get individual doctors whose average billing is above overall average
    
    Returns:
        List of doctors with above-average treatment costs
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                WITH OverallAverage AS (
                    SELECT AVG(amount_due) as avg_cost
                    FROM Billing
                ),
                DoctorCosts AS (
                    SELECT 
                        d.doctor_id,
                        d.full_name AS doctor_name,
                        d.specialization,
                        COUNT(DISTINCT a.appointment_id) AS appointment_count,
                        COUNT(DISTINCT a.patient_id) AS patient_count,
                        AVG(b.amount_due) AS avg_cost,
                        MAX(b.amount_due) AS max_cost,
                        SUM(b.amount_due) AS total_revenue
                    FROM Doctor d
                    INNER JOIN Appointment a ON d.doctor_id = a.doctor_id
                    INNER JOIN Billing b ON a.appointment_id = b.appointment_id
                    GROUP BY d.doctor_id, d.full_name, d.specialization
                )
                SELECT 
                    dc.doctor_id,
                    dc.doctor_name,
                    dc.specialization,
                    dc.avg_cost AS cost,
                    dc.max_cost,
                    dc.total_revenue,
                    dc.appointment_count,
                    dc.patient_count,
                    oa.avg_cost AS overall_average,
                    ROUND((dc.avg_cost - oa.avg_cost) / oa.avg_cost * 100, 2) AS percent_above_avg
                FROM DoctorCosts dc
                CROSS JOIN OverallAverage oa
                WHERE dc.avg_cost > oa.avg_cost
                ORDER BY dc.avg_cost DESC
            """
            cursor.execute(query)
            return cursor.fetchall()
    finally:
        connection.close()

def get_high_cost_patients():
    """
    Get patients with total spending above average
    
    Returns:
        List of patients who have spent more than average
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                WITH PatientTotalCosts AS (
                    SELECT 
                        p.patient_id,
                        p.full_name AS patient_name,
                        COUNT(a.appointment_id) AS visit_count,
                        SUM(b.amount_due) AS total_cost,
                        AVG(b.amount_due) AS avg_cost_per_visit,
                        SUM(b.amount_paid) AS total_paid,
                        SUM(b.amount_due - b.amount_paid) AS outstanding_balance
                    FROM Patient p
                    INNER JOIN Appointment a ON p.patient_id = a.patient_id
                    INNER JOIN Billing b ON a.appointment_id = b.appointment_id
                    GROUP BY p.patient_id, p.full_name
                ),
                OverallAverage AS (
                    SELECT AVG(total_cost) as avg_total_cost
                    FROM PatientTotalCosts
                )
                SELECT 
                    ptc.patient_id,
                    ptc.patient_name,
                    ptc.visit_count,
                    ptc.total_cost AS cost,
                    ptc.avg_cost_per_visit,
                    ptc.total_paid,
                    ptc.outstanding_balance,
                    oa.avg_total_cost AS overall_average,
                    ROUND((ptc.total_cost - oa.avg_total_cost) / oa.avg_total_cost * 100, 2) 
                        AS percent_above_avg
                FROM PatientTotalCosts ptc
                CROSS JOIN OverallAverage oa
                WHERE ptc.total_cost > oa.avg_total_cost
                ORDER BY ptc.total_cost DESC
            """
            cursor.execute(query)
            return cursor.fetchall()
    finally:
        connection.close()

def get_cost_statistics():
    """
    Get overall cost statistics for context
    
    Returns:
        Dictionary with average, min, max costs
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    COUNT(*) as total_bills,
                    AVG(amount_due) as average_cost,
                    MIN(amount_due) as min_cost,
                    MAX(amount_due) as max_cost,
                    STDDEV(amount_due) as std_deviation,
                    SUM(amount_due) as total_billed,
                    SUM(amount_paid) as total_collected
                FROM Billing
            """
            cursor.execute(query)
            return cursor.fetchone()
    finally:
        connection.close()
