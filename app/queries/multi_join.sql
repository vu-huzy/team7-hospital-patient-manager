-- MULTI JOIN Query - Complete Patient Journey
-- Shows comprehensive patient information across all related tables

-- Query 1: Complete patient treatment journey
SELECT 
    p.patient_id,
    p.full_name AS patient_name,
    p.phone_number AS patient_phone,
    p.email AS patient_email,
    a.appointment_id,
    a.appointment_date,
    a.reason AS visit_reason,
    a.status AS appointment_status,
    d.full_name AS doctor_name,
    d.specialization,
    dept.department_name,
    dept.location,
    mr.diagnosis,
    mr.prescription,
    mr.treatment_notes,
    mr.follow_up_date,
    b.amount_due,
    b.amount_paid,
    b.payment_status,
    b.payment_method,
    b.payment_date
FROM Patient p
INNER JOIN Appointment a ON p.patient_id = a.patient_id
INNER JOIN Doctor d ON a.doctor_id = d.doctor_id
INNER JOIN Department dept ON d.department_id = dept.department_id
LEFT JOIN Medical_Record mr ON a.appointment_id = mr.appointment_id
LEFT JOIN Billing b ON a.appointment_id = b.appointment_id
ORDER BY a.appointment_date DESC;

-- Query 2: Department performance with all metrics
SELECT 
    dept.department_id,
    dept.department_name,
    dept.location,
    dept.head_of_department,
    COUNT(DISTINCT d.doctor_id) AS total_doctors,
    COUNT(DISTINCT a.appointment_id) AS total_appointments,
    COUNT(DISTINCT p.patient_id) AS unique_patients,
    SUM(CASE WHEN a.status = 'Completed' THEN 1 ELSE 0 END) AS completed_appointments,
    SUM(CASE WHEN a.status = 'Scheduled' THEN 1 ELSE 0 END) AS scheduled_appointments,
    SUM(CASE WHEN a.status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_appointments,
    COALESCE(SUM(b.amount_due), 0) AS total_revenue,
    COALESCE(SUM(b.amount_paid), 0) AS total_collected,
    COALESCE(SUM(b.amount_due - b.amount_paid), 0) AS outstanding_amount
FROM Department dept
LEFT JOIN Doctor d ON dept.department_id = d.department_id
LEFT JOIN Appointment a ON d.doctor_id = a.doctor_id
LEFT JOIN Patient p ON a.patient_id = p.patient_id
LEFT JOIN Billing b ON a.appointment_id = b.appointment_id
GROUP BY dept.department_id
ORDER BY total_revenue DESC;

-- Query 3: Doctor performance with patient outcomes
SELECT 
    d.doctor_id,
    d.full_name AS doctor_name,
    d.specialization,
    dept.department_name,
    COUNT(DISTINCT a.appointment_id) AS total_appointments,
    COUNT(DISTINCT p.patient_id) AS unique_patients,
    SUM(CASE WHEN a.status = 'Completed' THEN 1 ELSE 0 END) AS completed,
    SUM(CASE WHEN a.status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled,
    ROUND(SUM(CASE WHEN a.status = 'Completed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS completion_rate,
    COALESCE(SUM(b.amount_due), 0) AS total_revenue_generated,
    COALESCE(SUM(b.amount_paid), 0) AS total_collected,
    COALESCE(AVG(b.amount_due), 0) AS avg_billing_per_visit,
    COUNT(DISTINCT mr.record_id) AS medical_records_completed
FROM Doctor d
INNER JOIN Department dept ON d.department_id = dept.department_id
LEFT JOIN Appointment a ON d.doctor_id = a.doctor_id
LEFT JOIN Patient p ON a.patient_id = p.patient_id
LEFT JOIN Billing b ON a.appointment_id = b.appointment_id
LEFT JOIN Medical_Record mr ON a.appointment_id = mr.appointment_id
GROUP BY d.doctor_id
ORDER BY total_appointments DESC;

-- Query 4: Patient financial summary across all visits
SELECT 
    p.patient_id,
    p.full_name AS patient_name,
    p.phone_number,
    COUNT(DISTINCT a.appointment_id) AS total_visits,
    COUNT(DISTINCT d.doctor_id) AS doctors_consulted,
    COUNT(DISTINCT dept.department_id) AS departments_visited,
    COALESCE(SUM(b.amount_due), 0) AS total_billed,
    COALESCE(SUM(b.amount_paid), 0) AS total_paid,
    COALESCE(SUM(b.amount_due - b.amount_paid), 0) AS outstanding_balance,
    CASE 
        WHEN SUM(b.amount_due - b.amount_paid) > 0 THEN 'Outstanding'
        WHEN SUM(b.amount_due) > 0 THEN 'Paid In Full'
        ELSE 'No Bills'
    END AS payment_status,
    COUNT(DISTINCT mr.record_id) AS medical_records
FROM Patient p
LEFT JOIN Appointment a ON p.patient_id = a.patient_id
LEFT JOIN Doctor d ON a.doctor_id = d.doctor_id
LEFT JOIN Department dept ON d.department_id = dept.department_id
LEFT JOIN Billing b ON a.appointment_id = b.appointment_id
LEFT JOIN Medical_Record mr ON a.appointment_id = mr.appointment_id
GROUP BY p.patient_id
ORDER BY outstanding_balance DESC;

-- Query 5: Monthly hospital activity report
SELECT 
    DATE_FORMAT(a.appointment_date, '%Y-%m') AS month,
    COUNT(DISTINCT a.appointment_id) AS total_appointments,
    COUNT(DISTINCT p.patient_id) AS unique_patients,
    COUNT(DISTINCT d.doctor_id) AS active_doctors,
    COUNT(DISTINCT dept.department_id) AS active_departments,
    SUM(CASE WHEN a.status = 'Completed' THEN 1 ELSE 0 END) AS completed,
    SUM(CASE WHEN a.status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled,
    COALESCE(SUM(b.amount_due), 0) AS total_revenue,
    COALESCE(SUM(b.amount_paid), 0) AS total_collected,
    COALESCE(SUM(b.amount_due - b.amount_paid), 0) AS outstanding
FROM Appointment a
INNER JOIN Patient p ON a.patient_id = p.patient_id
INNER JOIN Doctor d ON a.doctor_id = d.doctor_id
INNER JOIN Department dept ON d.department_id = dept.department_id
LEFT JOIN Billing b ON a.appointment_id = b.appointment_id
GROUP BY DATE_FORMAT(a.appointment_date, '%Y-%m')
ORDER BY month DESC;
