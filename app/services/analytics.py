"""
Analytics service - KPIs and dashboard data
"""
from app.db.connection import get_connection
from datetime import datetime, timedelta

def get_kpis():
    """
    Get key performance indicators for dashboard
    
    Returns:
        Dictionary with:
        - total_patients: Total number of registered patients
        - total_doctors: Total number of doctors
        - total_appointments: Total number of appointments
        - total_sessions: Alias for appointments (compatibility)
        - average_cost: Average billing amount
        - total_revenue: Total amount billed
        - total_collected: Total amount paid
        - outstanding_balance: Total unpaid amount
        - high_cost_count: Number of above-average specializations
        - scheduled_appointments: Number of upcoming appointments
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Get counts
            cursor.execute("SELECT COUNT(*) as count FROM Patient")
            total_patients = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM Doctor")
            total_doctors = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM Appointment")
            total_appointments = cursor.fetchone()['count']
            
            cursor.execute("""
                SELECT COUNT(*) as count FROM Appointment 
                WHERE status = 'Scheduled' AND appointment_date >= NOW()
            """)
            scheduled_appointments = cursor.fetchone()['count']
            
            # Get billing stats
            cursor.execute("""
                SELECT 
                    COALESCE(AVG(amount_due), 0) as avg_cost,
                    COALESCE(SUM(amount_due), 0) as total_revenue,
                    COALESCE(SUM(amount_paid), 0) as total_collected,
                    COALESCE(SUM(amount_due - amount_paid), 0) as outstanding
                FROM Billing
            """)
            billing_stats = cursor.fetchone()
            
            # Get high-cost count
            cursor.execute("""
                WITH OverallAverage AS (
                    SELECT AVG(amount_due) as avg_cost FROM Billing
                ),
                SpecializationCosts AS (
                    SELECT d.specialization, AVG(b.amount_due) AS avg_cost
                    FROM Doctor d
                    INNER JOIN Appointment a ON d.doctor_id = a.doctor_id
                    INNER JOIN Billing b ON a.appointment_id = b.appointment_id
                    GROUP BY d.specialization
                )
                SELECT COUNT(*) as count
                FROM SpecializationCosts sc
                CROSS JOIN OverallAverage oa
                WHERE sc.avg_cost > oa.avg_cost
            """)
            high_cost_result = cursor.fetchone()
            high_cost_count = high_cost_result['count'] if high_cost_result else 0
            
            return {
                'total_patients': total_patients,
                'total_doctors': total_doctors,
                'total_appointments': total_appointments,
                'total_sessions': total_appointments,  # Alias
                'average_cost': float(billing_stats['avg_cost']),
                'total_revenue': float(billing_stats['total_revenue']),
                'total_collected': float(billing_stats['total_collected']),
                'outstanding_balance': float(billing_stats['outstanding']),
                'high_cost_count': high_cost_count,
                'scheduled_appointments': scheduled_appointments
            }
    finally:
        connection.close()

def get_appointments_per_day(days=30):
    """
    Get number of appointments per day for chart
    
    Args:
        days: Number of days to look back
        
    Returns:
        List of dictionaries with date and appointment count
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    DATE(appointment_date) as date,
                    COUNT(*) as count,
                    COUNT(CASE WHEN status = 'Completed' THEN 1 END) as completed,
                    COUNT(CASE WHEN status = 'Scheduled' THEN 1 END) as scheduled,
                    COUNT(CASE WHEN status = 'Cancelled' THEN 1 END) as cancelled
                FROM Appointment
                WHERE appointment_date >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
                GROUP BY DATE(appointment_date)
                ORDER BY date
            """
            cursor.execute(query, (days,))
            return cursor.fetchall()
    finally:
        connection.close()

def get_revenue_per_month(months=6):
    """
    Get monthly revenue for trend analysis
    
    Args:
        months: Number of months to look back
        
    Returns:
        List of dictionaries with month and revenue
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    DATE_FORMAT(a.appointment_date, '%%Y-%%m') as month,
                    COUNT(a.appointment_id) as appointments,
                    COALESCE(SUM(b.amount_due), 0) as revenue,
                    COALESCE(SUM(b.amount_paid), 0) as collected
                FROM Appointment a
                LEFT JOIN Billing b ON a.appointment_id = b.appointment_id
                WHERE a.appointment_date >= DATE_SUB(CURDATE(), INTERVAL %s MONTH)
                GROUP BY DATE_FORMAT(a.appointment_date, '%%Y-%%m')
                ORDER BY month
            """
            cursor.execute(query, (months,))
            results = cursor.fetchall()
            
            # Convert Decimal to float
            for row in results:
                row['revenue'] = float(row['revenue'])
                row['collected'] = float(row['collected'])
            
            return results
    finally:
        connection.close()

def get_specialization_distribution():
    """
    Get appointment distribution by specialization
    
    Returns:
        List of dictionaries with specialization and count
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    d.specialization,
                    COUNT(a.appointment_id) as appointment_count,
                    COUNT(DISTINCT a.patient_id) as patient_count,
                    COALESCE(SUM(b.amount_due), 0) as revenue
                FROM Doctor d
                LEFT JOIN Appointment a ON d.doctor_id = a.doctor_id
                LEFT JOIN Billing b ON a.appointment_id = b.appointment_id
                GROUP BY d.specialization
                ORDER BY appointment_count DESC
            """
            cursor.execute(query)
            results = cursor.fetchall()
            
            # Convert Decimal to float
            for row in results:
                row['revenue'] = float(row['revenue'])
            
            return results
    finally:
        connection.close()

def get_doctor_performance():
    """
    Get top performing doctors by appointments and revenue
    
    Returns:
        List of top doctors with performance metrics
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    d.doctor_id,
                    d.full_name as doctor_name,
                    d.specialization,
                    COUNT(a.appointment_id) as total_appointments,
                    COUNT(DISTINCT a.patient_id) as unique_patients,
                    COALESCE(SUM(b.amount_due), 0) as total_revenue,
                    COALESCE(AVG(b.amount_due), 0) as avg_revenue_per_visit
                FROM Doctor d
                LEFT JOIN Appointment a ON d.doctor_id = a.doctor_id
                LEFT JOIN Billing b ON a.appointment_id = b.appointment_id
                GROUP BY d.doctor_id, d.full_name, d.specialization
                ORDER BY total_appointments DESC
                LIMIT 10
            """
            cursor.execute(query)
            results = cursor.fetchall()
            
            # Convert Decimal to float
            for row in results:
                row['total_revenue'] = float(row['total_revenue'])
                row['avg_revenue_per_visit'] = float(row['avg_revenue_per_visit'])
            
            return results
    finally:
        connection.close()

def get_payment_status_summary():
    """
    Get summary of payment statuses
    
    Returns:
        Dictionary with payment status counts and amounts
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    payment_status,
                    COUNT(*) as count,
                    SUM(amount_due) as total_due,
                    SUM(amount_paid) as total_paid
                FROM Billing
                GROUP BY payment_status
            """
            cursor.execute(query)
            results = cursor.fetchall()
            
            # Convert to dictionary format
            summary = {}
            for row in results:
                status = row['payment_status']
                summary[status] = {
                    'count': row['count'],
                    'total_due': float(row['total_due']),
                    'total_paid': float(row['total_paid'])
                }
            
            return summary
    finally:
        connection.close()

def get_recent_activity(limit=10):
    """
    Get recent appointments for activity feed
    
    Args:
        limit: Number of recent records to return
        
    Returns:
        List of recent appointments with details
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    a.appointment_id,
                    a.appointment_date,
                    a.status,
                    p.full_name as patient_name,
                    d.full_name as doctor_name,
                    d.specialization,
                    b.amount_due,
                    b.payment_status
                FROM Appointment a
                JOIN Patient p ON a.patient_id = p.patient_id
                JOIN Doctor d ON a.doctor_id = d.doctor_id
                LEFT JOIN Billing b ON a.appointment_id = b.appointment_id
                ORDER BY a.appointment_date DESC
                LIMIT %s
            """
            cursor.execute(query, (limit,))
            results = cursor.fetchall()
            
            # Convert Decimal to float
            for row in results:
                if row['amount_due']:
                    row['amount_due'] = float(row['amount_due'])
            
            return results
    finally:
        connection.close()
