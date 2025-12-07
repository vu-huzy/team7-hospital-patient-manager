-- Doctor CRUD Operations
-- These queries can be executed independently via MySQL command line or GUI tools

-- 1. List all doctors with department info
SELECT 
    d.doctor_id,
    d.full_name,
    d.specialization,
    d.phone_number,
    d.email,
    dept.department_name,
    dept.location
FROM Doctor d
LEFT JOIN Department dept ON d.department_id = dept.department_id
ORDER BY d.doctor_id;

-- 2. Get single doctor by ID
SELECT 
    d.*,
    dept.department_name,
    dept.location
FROM Doctor d
LEFT JOIN Department dept ON d.department_id = dept.department_id
WHERE d.doctor_id = ?;

-- 3. Get doctors by department
-- Usage: Replace ? with department_id
SELECT * FROM Doctor
WHERE department_id = ?
ORDER BY full_name;

-- 4. Get doctors by specialization
-- Usage: Replace 'spec' with actual specialization
SELECT * FROM Doctor
WHERE specialization LIKE '%spec%'
ORDER BY full_name;

-- 5. Insert new doctor
INSERT INTO Doctor (
    full_name, specialization, phone_number, 
    email, department_id
) VALUES (
    'Doctor Name', 'Specialization', '0912345678',
    'doctor@hospital.com', ?
);

-- 6. Update doctor
UPDATE Doctor SET
    full_name = 'Updated Name',
    specialization = 'Updated Spec',
    phone_number = '0912345678',
    email = 'updated@hospital.com',
    department_id = ?
WHERE doctor_id = ?;

-- 7. Delete doctor
DELETE FROM Doctor WHERE doctor_id = ?;

-- 8. Get doctor workload statistics
SELECT 
    d.doctor_id,
    d.full_name,
    d.specialization,
    dept.department_name,
    COUNT(DISTINCT a.appointment_id) as total_appointments,
    COUNT(DISTINCT a.patient_id) as unique_patients,
    SUM(CASE WHEN a.status = 'Completed' THEN 1 ELSE 0 END) as completed_appointments,
    SUM(CASE WHEN a.status = 'Scheduled' THEN 1 ELSE 0 END) as scheduled_appointments,
    SUM(b.amount_due) as total_revenue
FROM Doctor d
LEFT JOIN Department dept ON d.department_id = dept.department_id
LEFT JOIN Appointment a ON d.doctor_id = a.doctor_id
LEFT JOIN Billing b ON a.appointment_id = b.appointment_id
WHERE d.doctor_id = ?
GROUP BY d.doctor_id;

-- 9. Get doctor's upcoming appointments
SELECT 
    a.appointment_id,
    a.appointment_date,
    p.full_name as patient_name,
    p.phone_number,
    a.reason,
    a.status
FROM Appointment a
INNER JOIN Patient p ON a.patient_id = p.patient_id
WHERE a.doctor_id = ?
  AND a.status = 'Scheduled'
  AND a.appointment_date >= CURDATE()
ORDER BY a.appointment_date;

-- 10. Get doctor performance summary
SELECT 
    d.doctor_id,
    d.full_name,
    COUNT(a.appointment_id) as total_appointments,
    AVG(b.amount_due) as avg_billing_amount,
    SUM(b.amount_due) as total_revenue,
    COUNT(DISTINCT p.patient_id) as unique_patients
FROM Doctor d
LEFT JOIN Appointment a ON d.doctor_id = a.doctor_id
LEFT JOIN Billing b ON a.appointment_id = b.appointment_id
LEFT JOIN Patient p ON a.patient_id = p.patient_id
WHERE d.doctor_id = ?
GROUP BY d.doctor_id;
