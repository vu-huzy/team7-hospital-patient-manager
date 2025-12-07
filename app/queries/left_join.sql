-- LEFT JOIN Query - All Patients Including Those Without Appointments
-- Shows all patients, even those who haven't made appointments yet

-- Query 1: All patients with their appointment count (including zero)
SELECT 
    p.patient_id,
    p.full_name AS patient_name,
    p.phone_number,
    p.email,
    p.date_registered,
    COUNT(a.appointment_id) AS total_appointments,
    MAX(a.appointment_date) AS last_appointment_date,
    COALESCE(SUM(b.amount_due), 0) AS total_billed,
    COALESCE(SUM(b.amount_paid), 0) AS total_paid
FROM Patient p
LEFT JOIN Appointment a ON p.patient_id = a.patient_id
LEFT JOIN Billing b ON a.appointment_id = b.appointment_id
GROUP BY p.patient_id
ORDER BY total_appointments DESC;

-- Query 2: Patients without appointments (never visited)
SELECT 
    p.patient_id,
    p.full_name,
    p.phone_number,
    p.email,
    p.date_registered,
    DATEDIFF(CURDATE(), p.date_registered) as days_since_registration
FROM Patient p
LEFT JOIN Appointment a ON p.patient_id = a.patient_id
WHERE a.appointment_id IS NULL
ORDER BY p.date_registered;

-- Query 3: Patients with appointments but no medical records
SELECT 
    p.patient_id,
    p.full_name AS patient_name,
    a.appointment_id,
    a.appointment_date,
    a.status,
    d.full_name AS doctor_name
FROM Patient p
LEFT JOIN Appointment a ON p.patient_id = a.patient_id
LEFT JOIN Medical_Record mr ON a.appointment_id = mr.appointment_id
LEFT JOIN Doctor d ON a.doctor_id = d.doctor_id
WHERE a.appointment_id IS NOT NULL
  AND mr.record_id IS NULL
ORDER BY a.appointment_date DESC;

-- Query 4: All patients with billing status (including those with no bills)
SELECT 
    p.patient_id,
    p.full_name AS patient_name,
    p.phone_number,
    COUNT(a.appointment_id) AS total_appointments,
    COALESCE(SUM(b.amount_due), 0) AS total_due,
    COALESCE(SUM(b.amount_paid), 0) AS total_paid,
    COALESCE(SUM(b.amount_due - b.amount_paid), 0) AS outstanding_balance,
    CASE 
        WHEN SUM(b.amount_due - b.amount_paid) > 0 THEN 'Has Outstanding'
        WHEN SUM(b.amount_due) > 0 THEN 'Fully Paid'
        ELSE 'No Billing'
    END AS billing_status
FROM Patient p
LEFT JOIN Appointment a ON p.patient_id = a.patient_id
LEFT JOIN Billing b ON a.appointment_id = b.appointment_id
GROUP BY p.patient_id
ORDER BY outstanding_balance DESC;

-- Query 5: Patient engagement summary (all patients)
SELECT 
    p.patient_id,
    p.full_name,
    p.date_registered,
    COUNT(DISTINCT a.appointment_id) AS total_visits,
    COUNT(DISTINCT d.doctor_id) AS doctors_seen,
    COUNT(DISTINCT dept.department_id) AS departments_visited,
    CASE 
        WHEN COUNT(a.appointment_id) = 0 THEN 'Inactive'
        WHEN COUNT(a.appointment_id) <= 2 THEN 'Low Engagement'
        WHEN COUNT(a.appointment_id) <= 5 THEN 'Moderate Engagement'
        ELSE 'High Engagement'
    END AS engagement_level
FROM Patient p
LEFT JOIN Appointment a ON p.patient_id = a.patient_id
LEFT JOIN Doctor d ON a.doctor_id = d.doctor_id
LEFT JOIN Department dept ON d.department_id = dept.department_id
GROUP BY p.patient_id
ORDER BY total_visits DESC;
