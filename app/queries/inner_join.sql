-- INNER JOIN Query - Patient Treatments
-- Shows all patients who have appointments with billing information
-- Only returns records where all relationships exist (INNER JOIN)

-- Query 1: Patient treatments with costs
SELECT 
    p.full_name AS patient_name,
    p.phone_number AS patient_phone,
    d.full_name AS doctor_name,
    d.specialization AS treatment_type,
    a.appointment_date AS treatment_date,
    a.reason,
    a.status,
    b.amount_due AS cost,
    b.payment_status
FROM Patient p
INNER JOIN Appointment a ON p.patient_id = a.patient_id
INNER JOIN Doctor d ON a.doctor_id = d.doctor_id
INNER JOIN Billing b ON a.appointment_id = b.appointment_id
ORDER BY a.appointment_date DESC;

-- Query 2: Patient treatments summary statistics
SELECT 
    COUNT(DISTINCT p.patient_id) as total_patients,
    COUNT(DISTINCT a.appointment_id) as total_treatments,
    SUM(b.amount_due) as total_cost,
    AVG(b.amount_due) as avg_cost_per_treatment,
    SUM(b.amount_paid) as total_paid,
    SUM(b.amount_due - b.amount_paid) as total_outstanding
FROM Patient p
INNER JOIN Appointment a ON p.patient_id = a.patient_id
INNER JOIN Doctor d ON a.doctor_id = d.doctor_id
INNER JOIN Billing b ON a.appointment_id = b.appointment_id;

-- Query 3: Completed treatments only
SELECT 
    p.full_name AS patient_name,
    d.full_name AS doctor_name,
    d.specialization,
    a.appointment_date,
    a.reason,
    mr.diagnosis,
    mr.prescription,
    b.amount_due,
    b.payment_status
FROM Patient p
INNER JOIN Appointment a ON p.patient_id = a.patient_id
INNER JOIN Doctor d ON a.doctor_id = d.doctor_id
INNER JOIN Billing b ON a.appointment_id = b.appointment_id
INNER JOIN Medical_Record mr ON a.appointment_id = mr.appointment_id
WHERE a.status = 'Completed'
ORDER BY a.appointment_date DESC;

-- Query 4: Treatments by specialization
SELECT 
    d.specialization,
    COUNT(*) as treatment_count,
    AVG(b.amount_due) as avg_cost,
    SUM(b.amount_due) as total_revenue
FROM Patient p
INNER JOIN Appointment a ON p.patient_id = a.patient_id
INNER JOIN Doctor d ON a.doctor_id = d.doctor_id
INNER JOIN Billing b ON a.appointment_id = b.appointment_id
GROUP BY d.specialization
ORDER BY treatment_count DESC;
