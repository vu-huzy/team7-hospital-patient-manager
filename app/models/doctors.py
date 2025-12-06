"""
Doctor model - CRUD operations for Doctor table
"""
from app.db.connection import get_connection
import pymysql

def list_doctors(limit=None, offset=None, search=None):
    """
    Get list of all doctors with optional pagination
    
    Args:
        limit: Maximum number of records to return
        offset: Number of records to skip
        search: Search term for doctor name or specialization
        
    Returns:
        List of doctor dictionaries with department info
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT d.*, dep.department_name, dep.location 
                FROM Doctor d
                LEFT JOIN Department dep ON d.department_id = dep.department_id
            """
            params = []
            
            if search:
                query += " WHERE d.full_name LIKE %s OR d.specialization LIKE %s"
                params.extend([f"%{search}%", f"%{search}%"])
            
            query += " ORDER BY d.doctor_id DESC"
            
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

def get_doctor(doctor_id):
    """
    Get single doctor by ID with department info
    
    Args:
        doctor_id: Doctor ID
        
    Returns:
        Doctor dictionary or None
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT d.*, dep.department_name, dep.location 
                FROM Doctor d
                LEFT JOIN Department dep ON d.department_id = dep.department_id
                WHERE d.doctor_id = %s
            """
            cursor.execute(query, (doctor_id,))
            return cursor.fetchone()
    finally:
        connection.close()

def create_doctor(data):
    """
    Create new doctor record
    
    Args:
        data: Dictionary with doctor data
            - full_name (required)
            - specialization (required)
            - phone_number (optional)
            - email (optional)
            - department_id (optional)
            
    Returns:
        New doctor ID
        
    Raises:
        ValueError: If required fields are missing or invalid
    """
    # Validation
    if not data.get('full_name') or not data.get('full_name').strip():
        raise ValueError("Doctor name is required")
    
    if not data.get('specialization') or not data.get('specialization').strip():
        raise ValueError("Specialization is required")
    
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                INSERT INTO Doctor 
                (full_name, specialization, phone_number, email, department_id)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                data['full_name'].strip(),
                data['specialization'].strip(),
                data.get('phone_number', '').strip() or None,
                data.get('email', '').strip() or None,
                data.get('department_id') or None
            ))
            connection.commit()
            return cursor.lastrowid
    except pymysql.IntegrityError as e:
        connection.rollback()
        if 'Duplicate entry' in str(e):
            raise ValueError("Email already exists")
        if 'foreign key constraint' in str(e).lower():
            raise ValueError("Invalid department ID")
        raise
    finally:
        connection.close()

def update_doctor(doctor_id, data):
    """
    Update existing doctor record
    
    Args:
        doctor_id: Doctor ID to update
        data: Dictionary with updated doctor data
        
    Returns:
        Number of affected rows
    """
    # Validation
    if 'full_name' in data and (not data['full_name'] or not data['full_name'].strip()):
        raise ValueError("Doctor name cannot be empty")
    
    if 'specialization' in data and (not data['specialization'] or not data['specialization'].strip()):
        raise ValueError("Specialization cannot be empty")
    
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            fields = []
            values = []
            
            for field in ['full_name', 'specialization', 'phone_number', 'email', 'department_id']:
                if field in data:
                    fields.append(f"{field} = %s")
                    value = data[field]
                    if isinstance(value, str):
                        value = value.strip() or None
                    values.append(value)
            
            if not fields:
                return 0
            
            values.append(doctor_id)
            query = f"UPDATE Doctor SET {', '.join(fields)} WHERE doctor_id = %s"
            
            cursor.execute(query, values)
            connection.commit()
            return cursor.rowcount
    except pymysql.IntegrityError as e:
        connection.rollback()
        if 'Duplicate entry' in str(e):
            raise ValueError("Email already exists")
        if 'foreign key constraint' in str(e).lower():
            raise ValueError("Invalid department ID")
        raise
    finally:
        connection.close()

def delete_doctor(doctor_id):
    """
    Delete doctor record
    
    Args:
        doctor_id: Doctor ID to delete
        
    Returns:
        Number of affected rows
        
    Raises:
        ValueError: If doctor has related appointments
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Check for related appointments
            cursor.execute(
                "SELECT COUNT(*) as count FROM Appointment WHERE doctor_id = %s",
                (doctor_id,)
            )
            result = cursor.fetchone()
            if result['count'] > 0:
                raise ValueError(
                    f"Cannot delete doctor. {result['count']} appointment(s) exist. "
                    "Delete appointments first."
                )
            
            query = "DELETE FROM Doctor WHERE doctor_id = %s"
            cursor.execute(query, (doctor_id,))
            connection.commit()
            return cursor.rowcount
    except pymysql.IntegrityError:
        connection.rollback()
        raise ValueError("Cannot delete doctor due to related records")
    finally:
        connection.close()

def get_doctor_count():
    """Get total number of doctors"""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as count FROM Doctor")
            result = cursor.fetchone()
            return result['count']
    finally:
        connection.close()

def list_departments():
    """Get all departments for dropdown"""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Department ORDER BY department_name")
            return cursor.fetchall()
    finally:
        connection.close()
