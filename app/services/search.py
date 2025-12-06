"""
Search and Filter service
Global search and advanced filtering for appointments
"""
from app.db.connection import get_connection

def global_search(keyword):
    """
    Global search across patients, doctors, and appointments
    
    Searches in:
    - Patient names
    - Doctor names
    - Specializations
    - Appointment reasons
    
    Args:
        keyword: Search term
        
    Returns:
        List of matching appointments with all details
    """
    if not keyword or not keyword.strip():
        return []
    
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    a.appointment_id,
                    a.appointment_date,
                    a.status,
                    a.reason,
                    p.patient_id,
                    p.full_name AS patient_name,
                    p.phone_number AS patient_phone,
                    d.doctor_id,
                    d.full_name AS doctor_name,
                    d.specialization AS treatment_type,
                    b.amount_due AS cost,
                    b.payment_status,
                    'appointment' as result_type
                FROM Appointment a
                JOIN Patient p ON a.patient_id = p.patient_id
                JOIN Doctor d ON a.doctor_id = d.doctor_id
                LEFT JOIN Billing b ON a.appointment_id = b.appointment_id
                WHERE 
                    p.full_name LIKE %s
                    OR d.full_name LIKE %s
                    OR d.specialization LIKE %s
                    OR a.reason LIKE %s
                ORDER BY a.appointment_date DESC
                LIMIT 100
            """
            search_pattern = f"%{keyword.strip()}%"
            cursor.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern))
            results = cursor.fetchall()
            
            # Convert Decimal to float
            for row in results:
                if row.get('cost'):
                    row['cost'] = float(row['cost'])
            
            return results
    finally:
        connection.close()

def filter_appointments(doctor_id=None, patient_id=None, start_date=None, 
                       end_date=None, min_cost=None, max_cost=None, 
                       high_cost_only=False, status=None, specialization=None):
    """
    Advanced filtering for appointments
    
    Args:
        doctor_id: Filter by specific doctor
        patient_id: Filter by specific patient
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        min_cost: Minimum cost threshold
        max_cost: Maximum cost threshold
        high_cost_only: Only show above-average cost appointments
        status: Filter by appointment status
        specialization: Filter by doctor specialization
        
    Returns:
        List of filtered appointments
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Base query
            query = """
                SELECT 
                    a.appointment_id,
                    a.appointment_date,
                    a.status,
                    a.reason,
                    p.patient_id,
                    p.full_name AS patient_name,
                    p.phone_number AS patient_phone,
                    p.email AS patient_email,
                    d.doctor_id,
                    d.full_name AS doctor_name,
                    d.specialization AS treatment_type,
                    b.bill_id,
                    b.amount_due AS cost,
                    b.amount_paid,
                    b.payment_status
                FROM Appointment a
                JOIN Patient p ON a.patient_id = p.patient_id
                JOIN Doctor d ON a.doctor_id = d.doctor_id
                LEFT JOIN Billing b ON a.appointment_id = b.appointment_id
            """
            
            conditions = []
            params = []
            
            # Build WHERE conditions
            if doctor_id:
                conditions.append("a.doctor_id = %s")
                params.append(doctor_id)
            
            if patient_id:
                conditions.append("a.patient_id = %s")
                params.append(patient_id)
            
            if start_date:
                conditions.append("DATE(a.appointment_date) >= %s")
                params.append(start_date)
            
            if end_date:
                conditions.append("DATE(a.appointment_date) <= %s")
                params.append(end_date)
            
            if min_cost:
                conditions.append("b.amount_due >= %s")
                params.append(min_cost)
            
            if max_cost:
                conditions.append("b.amount_due <= %s")
                params.append(max_cost)
            
            if status:
                conditions.append("a.status = %s")
                params.append(status)
            
            if specialization:
                conditions.append("d.specialization LIKE %s")
                params.append(f"%{specialization}%")
            
            if high_cost_only:
                # Add subquery for average cost
                conditions.append("""
                    b.amount_due > (SELECT AVG(amount_due) FROM Billing)
                """)
            
            # Add WHERE clause if conditions exist
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY a.appointment_date DESC LIMIT 500"
            
            cursor.execute(query, params if params else None)
            results = cursor.fetchall()
            
            # Convert Decimal to float
            for row in results:
                if row.get('cost'):
                    row['cost'] = float(row['cost'])
                if row.get('amount_paid'):
                    row['amount_paid'] = float(row['amount_paid'])
            
            return results
    finally:
        connection.close()

def search_patients(keyword):
    """
    Search for patients by name, phone, or email
    
    Args:
        keyword: Search term
        
    Returns:
        List of matching patients
    """
    if not keyword or not keyword.strip():
        return []
    
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    p.*,
                    COUNT(a.appointment_id) as appointment_count,
                    COALESCE(SUM(b.amount_due), 0) as total_spent
                FROM Patient p
                LEFT JOIN Appointment a ON p.patient_id = a.patient_id
                LEFT JOIN Billing b ON a.appointment_id = b.appointment_id
                WHERE 
                    p.full_name LIKE %s
                    OR p.phone_number LIKE %s
                    OR p.email LIKE %s
                GROUP BY p.patient_id
                ORDER BY p.full_name
                LIMIT 50
            """
            search_pattern = f"%{keyword.strip()}%"
            cursor.execute(query, (search_pattern, search_pattern, search_pattern))
            results = cursor.fetchall()
            
            for row in results:
                row['total_spent'] = float(row['total_spent'])
            
            return results
    finally:
        connection.close()

def search_doctors(keyword):
    """
    Search for doctors by name or specialization
    
    Args:
        keyword: Search term
        
    Returns:
        List of matching doctors
    """
    if not keyword or not keyword.strip():
        return []
    
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    d.*,
                    dep.department_name,
                    COUNT(a.appointment_id) as appointment_count,
                    COUNT(DISTINCT a.patient_id) as patient_count
                FROM Doctor d
                LEFT JOIN Department dep ON d.department_id = dep.department_id
                LEFT JOIN Appointment a ON d.doctor_id = a.doctor_id
                WHERE 
                    d.full_name LIKE %s
                    OR d.specialization LIKE %s
                GROUP BY d.doctor_id
                ORDER BY d.full_name
                LIMIT 50
            """
            search_pattern = f"%{keyword.strip()}%"
            cursor.execute(query, (search_pattern, search_pattern))
            return cursor.fetchall()
    finally:
        connection.close()

def get_filter_options():
    """
    Get available options for filter dropdowns
    
    Returns:
        Dictionary with lists of doctors, specializations, statuses
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Get doctors
            cursor.execute("""
                SELECT doctor_id, full_name, specialization 
                FROM Doctor 
                ORDER BY full_name
            """)
            doctors = cursor.fetchall()
            
            # Get unique specializations
            cursor.execute("""
                SELECT DISTINCT specialization 
                FROM Doctor 
                ORDER BY specialization
            """)
            specializations = [row['specialization'] for row in cursor.fetchall()]
            
            # Get statuses
            statuses = ['Scheduled', 'Completed', 'Cancelled']
            
            # Get payment statuses
            payment_statuses = ['Unpaid', 'Partially Paid', 'Paid']
            
            return {
                'doctors': doctors,
                'specializations': specializations,
                'statuses': statuses,
                'payment_statuses': payment_statuses
            }
    finally:
        connection.close()

def get_advanced_statistics(filters=None):
    """
    Get statistics based on current filters
    
    Args:
        filters: Same filter dictionary as filter_appointments
        
    Returns:
        Dictionary with statistical summary
    """
    results = filter_appointments(**(filters or {}))
    
    if not results:
        return {
            'total_appointments': 0,
            'total_cost': 0,
            'average_cost': 0,
            'unique_patients': 0,
            'unique_doctors': 0
        }
    
    total_cost = sum(row.get('cost', 0) or 0 for row in results)
    unique_patients = len(set(row['patient_id'] for row in results))
    unique_doctors = len(set(row['doctor_id'] for row in results))
    
    return {
        'total_appointments': len(results),
        'total_cost': total_cost,
        'average_cost': total_cost / len(results) if results else 0,
        'unique_patients': unique_patients,
        'unique_doctors': unique_doctors
    }
