"""
SQL File Loader for Web Application
Loads and executes SQL queries from standalone .sql files
Reuses existing SQL files instead of rewriting queries
"""
import os
import re
from app.db.connection import get_connection

def load_sql_file(filepath):
    """Load SQL file and split into individual queries"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove USE database statements
    content = re.sub(r'USE\s+\w+;', '', content, flags=re.IGNORECASE)
    
    # Split by query comments (-- Query N: or -- N.)
    queries = []
    current_query = []
    in_query = False
    
    for line in content.split('\n'):
        stripped = line.strip()
        
        # Start of a new query
        if re.match(r'^--\s+(Query\s+\d+:|[\d]+\.)', stripped):
            if current_query and in_query:
                queries.append('\n'.join(current_query))
                current_query = []
            in_query = True
        elif stripped.startswith('--'):
            # Skip other comments
            continue
        elif in_query and stripped:
            current_query.append(line)
    
    # Add last query
    if current_query and in_query:
        queries.append('\n'.join(current_query))
    
    return queries

def execute_sql_query(query, params=None, fetch_one=False):
    """Execute a SQL query from file"""
    connection = get_connection()
    try:
        cursor = connection.cursor()
        
        # Replace placeholders
        if params:
            query = query.replace('?', '%s')
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch_one:
            result = cursor.fetchone()
        else:
            result = cursor.fetchall()
        
        cursor.close()
        return result
    finally:
        connection.close()

def execute_sql_update(query, params=None):
    """Execute INSERT/UPDATE/DELETE from SQL file"""
    connection = get_connection()
    try:
        cursor = connection.cursor()
        query = query.replace('?', '%s')
        cursor.execute(query, params or ())
        connection.commit()
        affected_rows = cursor.rowcount
        last_id = cursor.lastrowid
        cursor.close()
        return affected_rows, last_id
    finally:
        connection.close()

# ==================== PATIENTS ====================

def list_patients(search=None):
    """Query 1 from patients.sql"""
    queries = load_sql_file('app/models/patients.sql')
    query = queries[0]  # Query 1: List all patients
    
    if search:
        query = query.replace("'%search_term%'", "%s")
        return execute_sql_query(query, (f'%{search}%',))
    else:
        # Remove WHERE clause if no search
        query = re.sub(r'WHERE.*', 'ORDER BY patient_id DESC', query, flags=re.DOTALL)
        return execute_sql_query(query)

def get_patient(patient_id):
    """Query 2 from patients.sql"""
    queries = load_sql_file('app/models/patients.sql')
    query = queries[1]  # Query 2: Get single patient
    return execute_sql_query(query, (patient_id,), fetch_one=True)

def create_patient(data):
    """Query 5 from patients.sql"""
    queries = load_sql_file('app/models/patients.sql')
    query = queries[4]  # Query 5: Insert new patient
    
    # Extract INSERT statement
    match = re.search(r'INSERT INTO.*?;', query, re.DOTALL)
    if match:
        insert_query = match.group(0)
        params = (
            data['full_name'],
            data['gender'],
            data['date_of_birth'],
            data['phone_number'],
            data.get('email'),
            data.get('address'),
            data.get('emergency_contact')
        )
        _, patient_id = execute_sql_update(insert_query, params)
        return patient_id
    return None

def update_patient(patient_id, data):
    """Query 6 from patients.sql - dynamic UPDATE"""
    fields = []
    params = []
    
    for key, value in data.items():
        if value:
            fields.append(f"{key} = %s")
            params.append(value)
    
    if not fields:
        return 0
    
    params.append(patient_id)
    query = f"UPDATE Patient SET {', '.join(fields)} WHERE patient_id = %s"
    rows, _ = execute_sql_update(query, params)
    return rows

def delete_patient(patient_id):
    """Query 7 from patients.sql"""
    queries = load_sql_file('app/models/patients.sql')
    query = queries[6]  # Query 7: Delete patient
    rows, _ = execute_sql_update(query, (patient_id,))
    return rows

# ==================== DOCTORS ====================

def list_doctors(department_id=None, search=None):
    """Query 1 from doctors.sql"""
    queries = load_sql_file('app/models/doctors.sql')
    query = queries[0]  # Query 1: List all doctors
    
    conditions = []
    params = []
    
    if department_id:
        conditions.append("d.department_id = %s")
        params.append(department_id)
    
    if search:
        conditions.append("d.full_name LIKE %s")
        params.append(f"%{search}%")
    
    if conditions:
        query = query.replace("ORDER BY", f"WHERE {' AND '.join(conditions)} ORDER BY")
    
    return execute_sql_query(query, params if params else None)

def get_doctor(doctor_id):
    """Query 2 from doctors.sql"""
    queries = load_sql_file('app/models/doctors.sql')
    query = queries[1]  # Query 2: Get single doctor
    return execute_sql_query(query, (doctor_id,), fetch_one=True)

def create_doctor(data):
    """Query 5 from doctors.sql"""
    queries = load_sql_file('app/models/doctors.sql')
    query = queries[4]  # Query 5: Insert new doctor
    
    match = re.search(r'INSERT INTO.*?;', query, re.DOTALL)
    if match:
        insert_query = match.group(0)
        params = (
            data['full_name'],
            data['specialization'],
            data['phone_number'],
            data.get('email'),
            data['department_id']
        )
        _, doctor_id = execute_sql_update(insert_query, params)
        return doctor_id
    return None

def update_doctor(doctor_id, data):
    """Query 6 from doctors.sql - dynamic UPDATE"""
    fields = []
    params = []
    
    for key, value in data.items():
        if value:
            fields.append(f"{key} = %s")
            params.append(value)
    
    if not fields:
        return 0
    
    params.append(doctor_id)
    query = f"UPDATE Doctor SET {', '.join(fields)} WHERE doctor_id = %s"
    rows, _ = execute_sql_update(query, params)
    return rows

def delete_doctor(doctor_id):
    """Query 7 from doctors.sql"""
    queries = load_sql_file('app/models/doctors.sql')
    query = queries[6]  # Query 7: Delete doctor
    rows, _ = execute_sql_update(query, (doctor_id,))
    return rows

# ==================== APPOINTMENTS ====================

def list_appointments(filters=None, limit=None):
    """Query 1 from appointments.sql with billing info"""
    # Use custom query with billing join
    query = """
        SELECT 
            a.appointment_id,
            a.appointment_date,
            a.reason,
            a.status,
            p.full_name as patient_name,
            p.phone_number as patient_phone,
            d.full_name as doctor_name,
            d.specialization,
            dept.department_name,
            a.patient_id,
            a.doctor_id,
            b.amount_due,
            b.payment_status
        FROM Appointment a
        INNER JOIN Patient p ON a.patient_id = p.patient_id
        INNER JOIN Doctor d ON a.doctor_id = d.doctor_id
        INNER JOIN Department dept ON d.department_id = dept.department_id
        LEFT JOIN Billing b ON a.appointment_id = b.appointment_id
    """
    
    params = []
    conditions = []
    
    if filters:
        if filters.get('patient_id'):
            conditions.append("a.patient_id = %s")
            params.append(filters['patient_id'])
        
        if filters.get('doctor_id'):
            conditions.append("a.doctor_id = %s")
            params.append(filters['doctor_id'])
        
        if filters.get('status'):
            conditions.append("a.status = %s")
            params.append(filters['status'])
        
        if filters.get('date_from'):
            conditions.append("a.appointment_date >= %s")
            params.append(filters['date_from'])
        
        if filters.get('date_to'):
            conditions.append("a.appointment_date <= %s")
            params.append(filters['date_to'])
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    query += " ORDER BY a.appointment_date DESC"
    
    if limit:
        query += f" LIMIT {limit}"
    
    return execute_sql_query(query, params if params else None)

def get_appointment(appointment_id):
    """Query 2 from appointments.sql"""
    queries = load_sql_file('app/models/appointments.sql')
    query = queries[1]  # Query 2: Get single appointment
    return execute_sql_query(query, (appointment_id,), fetch_one=True)

def create_appointment(data):
    """Query 7 from appointments.sql"""
    queries = load_sql_file('app/models/appointments.sql')
    query = queries[6]  # Query 7: Insert new appointment
    
    match = re.search(r'INSERT INTO.*?;', query, re.DOTALL)
    if match:
        insert_query = match.group(0)
        params = (
            data['patient_id'],
            data['doctor_id'],
            data['appointment_date'],
            data['reason'],
            data.get('status', 'Scheduled')
        )
        _, appointment_id = execute_sql_update(insert_query, params)
        return appointment_id
    return None

def update_appointment(appointment_id, data):
    """Query 8 from appointments.sql - dynamic UPDATE"""
    fields = []
    params = []
    
    for key, value in data.items():
        if value:
            fields.append(f"{key} = %s")
            params.append(value)
    
    if not fields:
        return 0
    
    params.append(appointment_id)
    query = f"UPDATE Appointment SET {', '.join(fields)} WHERE appointment_id = %s"
    rows, _ = execute_sql_update(query, params)
    return rows

def delete_appointment(appointment_id):
    """Query 10 from appointments.sql"""
    queries = load_sql_file('app/models/appointments.sql')
    query = queries[9]  # Query 10: Delete appointment
    rows, _ = execute_sql_update(query, (appointment_id,))
    return rows

# ==================== DEPARTMENTS ====================

def list_departments():
    """List all departments"""
    query = "SELECT * FROM Department ORDER BY department_id"
    return execute_sql_query(query)

def get_department(department_id):
    """Get single department"""
    query = "SELECT * FROM Department WHERE department_id = %s"
    return execute_sql_query(query, (department_id,), fetch_one=True)

# ==================== REPORTING QUERIES ====================

def get_patient_treatments():
    """Query 1 from inner_join.sql"""
    queries = load_sql_file('app/queries/inner_join.sql')
    return execute_sql_query(queries[0])

def get_patient_treatments_summary():
    """Query 2 from inner_join.sql"""
    queries = load_sql_file('app/queries/inner_join.sql')
    return execute_sql_query(queries[1], fetch_one=True)

def get_patients_with_optional_treatments():
    """Query 1 from left_join.sql"""
    queries = load_sql_file('app/queries/left_join.sql')
    return execute_sql_query(queries[0])

def get_patient_treatment_summary():
    """Query 5 from left_join.sql"""
    queries = load_sql_file('app/queries/left_join.sql')
    return execute_sql_query(queries[4], fetch_one=True)

def get_patient_doctor_treatments():
    """Query 1 from multi_join.sql"""
    queries = load_sql_file('app/queries/multi_join.sql')
    return execute_sql_query(queries[0])

def get_department_performance():
    """Query 2 from multi_join.sql"""
    queries = load_sql_file('app/queries/multi_join.sql')
    return execute_sql_query(queries[1])

def get_high_cost_treatments():
    """Query 1 from high_cost.sql"""
    queries = load_sql_file('app/queries/high_cost.sql')
    return execute_sql_query(queries[0])

def get_cost_statistics():
    """Query 6 from high_cost.sql"""
    queries = load_sql_file('app/queries/high_cost.sql')
    return execute_sql_query(queries[5], fetch_one=True)
