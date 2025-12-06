"""
Appointment model - CRUD operations for Appointment table
This represents treatment sessions in the requirements
"""
from app.db.connection import get_connection
import pymysql
from datetime import datetime

def list_appointments(limit=None, offset=None, filters=None):
    """
    Get list of all appointments with optional filters
    
    Args:
        limit: Maximum number of records
        offset: Number of records to skip
        filters: Dictionary with filter criteria
            - doctor_id: Filter by doctor
            - patient_id: Filter by patient
            - status: Filter by status
            - start_date: Filter appointments from this date
            - end_date: Filter appointments to this date
            
    Returns:
        List of appointment dictionaries with patient, doctor, and billing info
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    a.*,
                    p.full_name as patient_name,
                    d.full_name as doctor_name,
                    d.specialization,
                    b.amount_due,
                    b.payment_status
                FROM Appointment a
                JOIN Patient p ON a.patient_id = p.patient_id
                JOIN Doctor d ON a.doctor_id = d.doctor_id
                LEFT JOIN Billing b ON a.appointment_id = b.appointment_id
            """
            params = []
            conditions = []
            
            if filters:
                if filters.get('doctor_id'):
                    conditions.append("a.doctor_id = %s")
                    params.append(filters['doctor_id'])
                
                if filters.get('patient_id'):
                    conditions.append("a.patient_id = %s")
                    params.append(filters['patient_id'])
                
                if filters.get('status'):
                    conditions.append("a.status = %s")
                    params.append(filters['status'])
                
                if filters.get('start_date'):
                    conditions.append("DATE(a.appointment_date) >= %s")
                    params.append(filters['start_date'])
                
                if filters.get('end_date'):
                    conditions.append("DATE(a.appointment_date) <= %s")
                    params.append(filters['end_date'])
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY a.appointment_date DESC"
            
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

def get_appointment(appointment_id):
    """
    Get single appointment by ID with all related info
    
    Args:
        appointment_id: Appointment ID
        
    Returns:
        Appointment dictionary or None
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    a.*,
                    p.full_name as patient_name,
                    p.phone_number as patient_phone,
                    d.full_name as doctor_name,
                    d.specialization,
                    b.amount_due,
                    b.payment_status,
                    b.bill_id
                FROM Appointment a
                JOIN Patient p ON a.patient_id = p.patient_id
                JOIN Doctor d ON a.doctor_id = d.doctor_id
                LEFT JOIN Billing b ON a.appointment_id = b.appointment_id
                WHERE a.appointment_id = %s
            """
            cursor.execute(query, (appointment_id,))
            return cursor.fetchone()
    finally:
        connection.close()

def create_appointment(data):
    """
    Create new appointment record
    
    Args:
        data: Dictionary with appointment data
            - patient_id (required)
            - doctor_id (required)
            - appointment_date (required): YYYY-MM-DD HH:MM:SS
            - reason (optional)
            - status (optional): Scheduled, Completed, Cancelled
            - amount_due (optional): If provided, creates billing record
            
    Returns:
        New appointment ID
        
    Raises:
        ValueError: If required fields are missing or invalid
    """
    # Validation
    if not data.get('patient_id'):
        raise ValueError("Patient is required")
    
    if not data.get('doctor_id'):
        raise ValueError("Doctor is required")
    
    if not data.get('appointment_date'):
        raise ValueError("Appointment date is required")
    
    # Validate datetime format
    try:
        datetime.strptime(data['appointment_date'], '%Y-%m-%d %H:%M:%S')
    except ValueError:
        # Try date only format
        try:
            date_obj = datetime.strptime(data['appointment_date'], '%Y-%m-%d')
            data['appointment_date'] = date_obj.strftime('%Y-%m-%d 09:00:00')
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD or YYYY-MM-DD HH:MM:SS")
    
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Verify patient exists
            cursor.execute("SELECT patient_id FROM Patient WHERE patient_id = %s", 
                          (data['patient_id'],))
            if not cursor.fetchone():
                raise ValueError("Patient ID does not exist")
            
            # Verify doctor exists
            cursor.execute("SELECT doctor_id FROM Doctor WHERE doctor_id = %s", 
                          (data['doctor_id'],))
            if not cursor.fetchone():
                raise ValueError("Doctor ID does not exist")
            
            # Insert appointment
            query = """
                INSERT INTO Appointment 
                (patient_id, doctor_id, appointment_date, reason, status)
                VALUES (%s, %s, %s, %s, %s)
            """
            status = data.get('status', 'Scheduled')
            if status not in ['Scheduled', 'Completed', 'Cancelled']:
                status = 'Scheduled'
            
            cursor.execute(query, (
                data['patient_id'],
                data['doctor_id'],
                data['appointment_date'],
                data.get('reason', '').strip() or None,
                status
            ))
            
            appointment_id = cursor.lastrowid
            
            # Create billing record if amount provided
            if data.get('amount_due'):
                try:
                    amount = float(data['amount_due'])
                    if amount > 0:
                        billing_query = """
                            INSERT INTO Billing 
                            (patient_id, appointment_id, amount_due, amount_paid, payment_status)
                            VALUES (%s, %s, %s, 0, 'Unpaid')
                        """
                        cursor.execute(billing_query, (
                            data['patient_id'],
                            appointment_id,
                            amount
                        ))
                except (ValueError, TypeError):
                    pass  # Skip billing if amount invalid
            
            connection.commit()
            return appointment_id
    except pymysql.IntegrityError as e:
        connection.rollback()
        raise ValueError(f"Database error: {str(e)}")
    finally:
        connection.close()

def update_appointment(appointment_id, data):
    """
    Update existing appointment record
    
    Args:
        appointment_id: Appointment ID to update
        data: Dictionary with updated appointment data
        
    Returns:
        Number of affected rows
    """
    # Validation
    if 'appointment_date' in data:
        try:
            datetime.strptime(data['appointment_date'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            try:
                date_obj = datetime.strptime(data['appointment_date'], '%Y-%m-%d')
                data['appointment_date'] = date_obj.strftime('%Y-%m-%d 09:00:00')
            except ValueError:
                raise ValueError("Invalid date format")
    
    if 'status' in data and data['status'] not in ['Scheduled', 'Completed', 'Cancelled']:
        raise ValueError("Invalid status. Must be Scheduled, Completed, or Cancelled")
    
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            fields = []
            values = []
            
            for field in ['patient_id', 'doctor_id', 'appointment_date', 'reason', 'status']:
                if field in data:
                    # Verify IDs exist
                    if field == 'patient_id':
                        cursor.execute("SELECT patient_id FROM Patient WHERE patient_id = %s", 
                                      (data[field],))
                        if not cursor.fetchone():
                            raise ValueError("Patient ID does not exist")
                    elif field == 'doctor_id':
                        cursor.execute("SELECT doctor_id FROM Doctor WHERE doctor_id = %s", 
                                      (data[field],))
                        if not cursor.fetchone():
                            raise ValueError("Doctor ID does not exist")
                    
                    fields.append(f"{field} = %s")
                    value = data[field]
                    if isinstance(value, str) and field != 'appointment_date':
                        value = value.strip() or None
                    values.append(value)
            
            if not fields:
                return 0
            
            values.append(appointment_id)
            query = f"UPDATE Appointment SET {', '.join(fields)} WHERE appointment_id = %s"
            
            cursor.execute(query, values)
            connection.commit()
            return cursor.rowcount
    except pymysql.IntegrityError as e:
        connection.rollback()
        raise ValueError(f"Database error: {str(e)}")
    finally:
        connection.close()

def delete_appointment(appointment_id):
    """
    Delete appointment record
    
    Args:
        appointment_id: Appointment ID to delete
        
    Returns:
        Number of affected rows
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Delete related billing records first
            cursor.execute("DELETE FROM Billing WHERE appointment_id = %s", 
                          (appointment_id,))
            
            # Delete related medical records
            cursor.execute("DELETE FROM Medical_Record WHERE appointment_id = %s", 
                          (appointment_id,))
            
            # Delete appointment
            cursor.execute("DELETE FROM Appointment WHERE appointment_id = %s", 
                          (appointment_id,))
            
            connection.commit()
            return cursor.rowcount
    except pymysql.IntegrityError:
        connection.rollback()
        raise ValueError("Cannot delete appointment due to related records")
    finally:
        connection.close()

def get_appointment_count():
    """Get total number of appointments"""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as count FROM Appointment")
            result = cursor.fetchone()
            return result['count']
    finally:
        connection.close()
