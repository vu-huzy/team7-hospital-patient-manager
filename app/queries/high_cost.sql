-- HIGH COST TREATMENTS Query
-- Identifies expensive treatments and high-spending patients

-- Query 1: High cost treatments (above average)
SELECT 
    b.bill_id,
    p.full_name AS patient_name,
    p.phone_number,
    d.full_name AS doctor_name,
    d.specialization AS treatment_type,
    dept.department_name,
    a.appointment_date,
    a.reason,
    mr.diagnosis,
    b.amount_due AS cost,
    b.amount_paid,
    b.payment_status,
    (b.amount_due - (SELECT AVG(amount_due) FROM Billing)) AS above_average
FROM Billing b
INNER JOIN Appointment a ON b.appointment_id = a.appointment_id
INNER JOIN Patient p ON b.patient_id = p.patient_id
INNER JOIN Doctor d ON a.doctor_id = d.doctor_id
INNER JOIN Department dept ON d.department_id = dept.department_id
LEFT JOIN Medical_Record mr ON a.appointment_id = mr.appointment_id
WHERE b.amount_due > (SELECT AVG(amount_due) FROM Billing)
ORDER BY b.amount_due DESC;

-- Query 2: Top 10 most expensive treatments
SELECT 
    b.bill_id,
    p.full_name AS patient_name,
    d.full_name AS doctor_name,
    d.specialization,
    a.appointment_date,
    mr.diagnosis,
    b.amount_due AS cost,
    b.payment_status
FROM Billing b
INNER JOIN Appointment a ON b.appointment_id = a.appointment_id
INNER JOIN Patient p ON b.patient_id = p.patient_id
INNER JOIN Doctor d ON a.doctor_id = d.doctor_id
LEFT JOIN Medical_Record mr ON a.appointment_id = mr.appointment_id
ORDER BY b.amount_due DESC
LIMIT 10;

-- Query 3: High-spending patients (total billing > threshold)
SELECT 
    p.patient_id,
    p.full_name AS patient_name,
    p.phone_number,
    p.email,
    COUNT(DISTINCT a.appointment_id) AS total_visits,
    SUM(b.amount_due) AS total_spending,
    SUM(b.amount_paid) AS total_paid,
    SUM(b.amount_due - b.amount_paid) AS outstanding_balance,
    AVG(b.amount_due) AS avg_per_visit
FROM Patient p
INNER JOIN Appointment a ON p.patient_id = a.patient_id
INNER JOIN Billing b ON a.appointment_id = b.appointment_id
GROUP BY p.patient_id
HAVING SUM(b.amount_due) > 1000000
ORDER BY total_spending DESC;

-- Query 4: Expensive treatments by department
SELECT 
    dept.department_name,
    d.specialization,
    COUNT(*) AS treatment_count,
    MIN(b.amount_due) AS min_cost,
    MAX(b.amount_due) AS max_cost,
    AVG(b.amount_due) AS avg_cost,
    SUM(b.amount_due) AS total_revenue
FROM Billing b
INNER JOIN Appointment a ON b.appointment_id = a.appointment_id
INNER JOIN Doctor d ON a.doctor_id = d.doctor_id
INNER JOIN Department dept ON d.department_id = dept.department_id
GROUP BY dept.department_name, d.specialization
HAVING AVG(b.amount_due) > (SELECT AVG(amount_due) FROM Billing)
ORDER BY avg_cost DESC;

-- Query 5: High-cost unpaid treatments (risk analysis)
SELECT 
    b.bill_id,
    p.full_name AS patient_name,
    p.phone_number AS contact,
    d.full_name AS doctor_name,
    dept.department_name,
    a.appointment_date,
    b.amount_due,
    b.amount_paid,
    (b.amount_due - b.amount_paid) AS outstanding,
    b.payment_status,
    DATEDIFF(CURDATE(), a.appointment_date) AS days_overdue
FROM Billing b
INNER JOIN Appointment a ON b.appointment_id = a.appointment_id
INNER JOIN Patient p ON b.patient_id = p.patient_id
INNER JOIN Doctor d ON a.doctor_id = d.doctor_id
INNER JOIN Department dept ON d.department_id = dept.department_id
WHERE b.payment_status IN ('Unpaid', 'Partially Paid')
  AND b.amount_due > (SELECT AVG(amount_due) FROM Billing)
ORDER BY outstanding DESC;

-- Query 6: Treatment cost statistics by specialization
SELECT 
    d.specialization,
    COUNT(DISTINCT b.bill_id) AS total_treatments,
    COUNT(DISTINCT p.patient_id) AS unique_patients,
    MIN(b.amount_due) AS min_cost,
    MAX(b.amount_due) AS max_cost,
    AVG(b.amount_due) AS avg_cost,
    STDDEV(b.amount_due) AS cost_variation,
    SUM(b.amount_due) AS total_revenue,
    SUM(CASE WHEN b.amount_due > (SELECT AVG(amount_due) FROM Billing) THEN 1 ELSE 0 END) AS high_cost_count,
    ROUND(SUM(CASE WHEN b.amount_due > (SELECT AVG(amount_due) FROM Billing) THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS high_cost_percentage
FROM Billing b
INNER JOIN Appointment a ON b.appointment_id = a.appointment_id
INNER JOIN Doctor d ON a.doctor_id = d.doctor_id
INNER JOIN Patient p ON b.patient_id = p.patient_id
GROUP BY d.specialization
ORDER BY avg_cost DESC;
