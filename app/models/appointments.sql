-- Appointment CRUD Operations
-- These queries can be executed independently via MySQL command line or GUI tools

-- 1. List all appointments with full details
SELECT 
    a.appointment_id,
    a.appointment_date,
    a.reason,
    a.status,
    p.full_name as patient_name,
    p.phone_number as patient_phone,
    d.full_name as doctor_name,
    d.specialization,
    dept.department_name
FROM Appointment a
INNER JOIN Patient p ON a.patient_id = p.patient_id
INNER JOIN Doctor d ON a.doctor_id = d.doctor_id
INNER JOIN Department dept ON d.department_id = dept.department_id
ORDER BY a.appointment_date DESC;

-- 2. Get single appointment by ID
SELECT 
    a.*,
    p.full_name as patient_name,
    d.full_name as doctor_name,
    dept.department_name
FROM Appointment a
INNER JOIN Patient p ON a.patient_id = p.patient_id
INNER JOIN Doctor d ON a.doctor_id = d.doctor_id
INNER JOIN Department dept ON d.department_id = dept.department_id
WHERE a.appointment_id = ?;

-- 3. Get appointments by patient
SELECT 
    a.appointment_id,
    a.appointment_date,
    a.reason,
    a.status,
    d.full_name as doctor_name,
    dept.department_name
FROM Appointment a
INNER JOIN Doctor d ON a.doctor_id = d.doctor_id
INNER JOIN Department dept ON d.department_id = dept.department_id
WHERE a.patient_id = ?
ORDER BY a.appointment_date DESC;

-- 4. Get appointments by doctor
SELECT 
    a.appointment_id,
    a.appointment_date,
    a.reason,
    a.status,
    p.full_name as patient_name,
    p.phone_number
FROM Appointment a
INNER JOIN Patient p ON a.patient_id = p.patient_id
WHERE a.doctor_id = ?
ORDER BY a.appointment_date DESC;

-- 5. Get appointments by date range
-- Usage: Replace dates with actual values
SELECT 
    a.*,
    p.full_name as patient_name,
    d.full_name as doctor_name
FROM Appointment a
INNER JOIN Patient p ON a.patient_id = p.patient_id
INNER JOIN Doctor d ON a.doctor_id = d.doctor_id
WHERE a.appointment_date BETWEEN '2025-01-01' AND '2025-12-31'
ORDER BY a.appointment_date;

-- 6. Get appointments by status
-- Usage: Replace 'status' with 'Scheduled', 'Completed', or 'Cancelled'
SELECT 
    a.*,
    p.full_name as patient_name,
    d.full_name as doctor_name
FROM Appointment a
INNER JOIN Patient p ON a.patient_id = p.patient_id
INNER JOIN Doctor d ON a.doctor_id = d.doctor_id
WHERE a.status = 'status'
ORDER BY a.appointment_date DESC;

-- 7. Insert new appointment
INSERT INTO Appointment (
    patient_id, doctor_id, appointment_date, 
    reason, status
) VALUES (
    ?, ?, '2025-01-01 10:00:00',
    'Reason for visit', 'Scheduled'
);

-- 8. Update appointment
UPDATE Appointment SET
    patient_id = ?,
    doctor_id = ?,
    appointment_date = '2025-01-01 10:00:00',
    reason = 'Updated reason',
    status = 'Completed'
WHERE appointment_id = ?;

-- 9. Update appointment status only
UPDATE Appointment SET
    status = 'status'
WHERE appointment_id = ?;

-- 10. Delete appointment
DELETE FROM Appointment WHERE appointment_id = ?;

-- 11. Get today's appointments
SELECT 
    a.appointment_id,
    a.appointment_date,
    p.full_name as patient_name,
    p.phone_number,
    d.full_name as doctor_name,
    dept.department_name,
    a.reason,
    a.status
FROM Appointment a
INNER JOIN Patient p ON a.patient_id = p.patient_id
INNER JOIN Doctor d ON a.doctor_id = d.doctor_id
INNER JOIN Department dept ON d.department_id = dept.department_id
WHERE DATE(a.appointment_date) = CURDATE()
ORDER BY a.appointment_date;

-- 12. Get upcoming appointments (next 7 days)
SELECT 
    a.appointment_id,
    a.appointment_date,
    p.full_name as patient_name,
    d.full_name as doctor_name,
    dept.department_name,
    a.status
FROM Appointment a
INNER JOIN Patient p ON a.patient_id = p.patient_id
INNER JOIN Doctor d ON a.doctor_id = d.doctor_id
INNER JOIN Department dept ON d.department_id = dept.department_id
WHERE a.appointment_date BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 7 DAY)
  AND a.status = 'Scheduled'
ORDER BY a.appointment_date;
