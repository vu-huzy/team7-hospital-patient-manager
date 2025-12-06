"""
Patient model - CRUD operations for Patient table
"""
from app.db.connection import get_connection
import pymysql
from datetime import datetime

def list_patients(limit=None, offset=None, search=None):
    """
    Get list of all patients with optional pagination
    
    Args:
        limit: Maximum number of records to return
        offset: Number of records to skip
        search: Search term for patient name
        
    Returns:
        List of patient dictionaries
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM Patient"
            params = []
            
            if search:
                query += " WHERE full_name LIKE %s"
                params.append(f"%{search}%")
            
            query += " ORDER BY patient_id DESC"
            
            if limit:
                query += " LIMIT %s"
                params.append(limit)
                
            if offset:
                query += " OFFSET %s"
                params.append(offset)
            
            cursor.execute(query, params if params else None)
            return cursor.fetchall()
    finally:
        connection.close()

def get_patient(patient_id):
    """
    Get single patient by ID
    
    Args:
        patient_id: Patient ID
        
    Returns:
        Patient dictionary or None
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM Patient WHERE patient_id = %s"
            cursor.execute(query, (patient_id,))
            return cursor.fetchone()
    finally:
        connection.close()

def create_patient(data):
    """
    Create new patient record
    
    Args:
        data: Dictionary with patient data
            - full_name (required)
            - gender (required): Male, Female, Other
            - date_of_birth (required): YYYY-MM-DD
            - phone_number (optional)
            - email (optional)
            - address (optional)
            - emergency_contact (optional)
            
    Returns:
        New patient ID
        
    Raises:
        ValueError: If required fields are missing or invalid
        pymysql.Error: If database error occurs
    """
    # Validation
    if not data.get('full_name') or not data.get('full_name').strip():
        raise ValueError("Patient name is required")
    
    if not data.get('gender') or data.get('gender') not in ['Male', 'Female', 'Other']:
        raise ValueError("Valid gender is required (Male, Female, Other)")
    
    if not data.get('date_of_birth'):
        raise ValueError("Date of birth is required")
    
    # Validate date format
    try:
        datetime.strptime(data['date_of_birth'], '%Y-%m-%d')
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")
    
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                INSERT INTO Patient 
                (full_name, gender, date_of_birth, phone_number, email, address, emergency_contact)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                data['full_name'].strip(),
                data['gender'],
                data['date_of_birth'],
                data.get('phone_number', '').strip() or None,
                data.get('email', '').strip() or None,
                data.get('address', '').strip() or None,
                data.get('emergency_contact', '').strip() or None
            ))
            connection.commit()
            return cursor.lastrowid
    except pymysql.IntegrityError as e:
        connection.rollback()
        if 'Duplicate entry' in str(e):
            raise ValueError("Email already exists")
        raise
    finally:
        connection.close()

def update_patient(patient_id, data):
    """
    Update existing patient record
    
    Args:
        patient_id: Patient ID to update
        data: Dictionary with updated patient data
        
    Returns:
        Number of affected rows
        
    Raises:
        ValueError: If validation fails
        pymysql.Error: If database error occurs
    """
    # Validation
    if 'full_name' in data and (not data['full_name'] or not data['full_name'].strip()):
        raise ValueError("Patient name cannot be empty")
    
    if 'gender' in data and data['gender'] not in ['Male', 'Female', 'Other']:
        raise ValueError("Valid gender is required (Male, Female, Other)")
    
    if 'date_of_birth' in data:
        try:
            datetime.strptime(data['date_of_birth'], '%Y-%m-%d')
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
    
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Build dynamic update query
            fields = []
            values = []
            
            for field in ['full_name', 'gender', 'date_of_birth', 'phone_number', 
                         'email', 'address', 'emergency_contact']:
                if field in data:
                    fields.append(f"{field} = %s")
                    value = data[field]
                    if isinstance(value, str):
                        value = value.strip() or None
                    values.append(value)
            
            if not fields:
                return 0
            
            values.append(patient_id)
            query = f"UPDATE Patient SET {', '.join(fields)} WHERE patient_id = %s"
            
            cursor.execute(query, values)
            connection.commit()
            return cursor.rowcount
    except pymysql.IntegrityError as e:
        connection.rollback()
        if 'Duplicate entry' in str(e):
            raise ValueError("Email already exists")
        raise
    finally:
        connection.close()

def delete_patient(patient_id):
    """
    Delete patient record
    
    Args:
        patient_id: Patient ID to delete
        
    Returns:
        Number of affected rows
        
    Raises:
        ValueError: If patient has related appointments
        pymysql.Error: If database error occurs
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Check for related appointments
            cursor.execute(
                "SELECT COUNT(*) as count FROM Appointment WHERE patient_id = %s",
                (patient_id,)
            )
            result = cursor.fetchone()
            if result['count'] > 0:
                raise ValueError(
                    f"Cannot delete patient. {result['count']} appointment(s) exist. "
                    "Delete appointments first."
                )
            
            # Delete patient
            query = "DELETE FROM Patient WHERE patient_id = %s"
            cursor.execute(query, (patient_id,))
            connection.commit()
            return cursor.rowcount
    except pymysql.IntegrityError as e:
        connection.rollback()
        raise ValueError("Cannot delete patient due to related records")
    finally:
        connection.close()

def get_patient_count():
    """Get total number of patients"""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as count FROM Patient")
            result = cursor.fetchone()
            return result['count']
    finally:
        connection.close()
