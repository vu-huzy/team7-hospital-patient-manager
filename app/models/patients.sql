-- Patient CRUD Operations
-- These queries can be executed independently via MySQL command line or GUI tools

-- 1. List all patients (with optional search by name)
-- Usage: Replace '%search_term%' with actual search value or remove WHERE clause
SELECT * FROM Patient
WHERE full_name LIKE '%search_term%'
ORDER BY patient_id DESC;

-- 2. Get single patient by ID
-- Usage: Replace ? with actual patient_id
SELECT * FROM Patient
WHERE patient_id = ?;

-- 3. Get patient count (for pagination)
SELECT COUNT(*) as total FROM Patient;

-- 4. Get patient count with search
-- Usage: Replace '%search_term%' with actual search value
SELECT COUNT(*) as total FROM Patient
WHERE full_name LIKE '%search_term%';

-- 5. Insert new patient
-- Usage: Replace values with actual data
INSERT INTO Patient (
    full_name, gender, date_of_birth, phone_number, 
    email, address, emergency_contact
) VALUES (
    'Patient Name', 'Male', '1990-01-01', '0912345678',
    'email@example.com', 'Address', '0987654321'
);

-- 6. Update patient
-- Usage: Replace values and patient_id
UPDATE Patient SET
    full_name = 'Updated Name',
    gender = 'Female',
    date_of_birth = '1990-01-01',
    phone_number = '0912345678',
    email = 'updated@example.com',
    address = 'Updated Address',
    emergency_contact = '0987654321'
WHERE patient_id = ?;

-- 7. Delete patient
-- Usage: Replace ? with actual patient_id
DELETE FROM Patient WHERE patient_id = ?;

-- 8. Get patient with appointment history
SELECT 
    p.*,
    COUNT(a.appointment_id) as total_appointments,
    MAX(a.appointment_date) as last_visit
FROM Patient p
LEFT JOIN Appointment a ON p.patient_id = a.patient_id
WHERE p.patient_id = ?
GROUP BY p.patient_id;

-- 9. Get patient medical history
SELECT 
    p.full_name,
    p.phone_number,
    a.appointment_date,
    d.full_name as doctor_name,
    dept.department_name,
    a.reason,
    a.status,
    mr.diagnosis,
    mr.prescription,
    b.amount_due,
    b.payment_status
FROM Patient p
LEFT JOIN Appointment a ON p.patient_id = a.patient_id
LEFT JOIN Doctor d ON a.doctor_id = d.doctor_id
LEFT JOIN Department dept ON d.department_id = dept.department_id
LEFT JOIN Medical_Record mr ON a.appointment_id = mr.appointment_id
LEFT JOIN Billing b ON a.appointment_id = b.appointment_id
WHERE p.patient_id = ?
ORDER BY a.appointment_date DESC;
