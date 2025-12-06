USE hospital_manager;

DROP VIEW IF EXISTS v_patient_appointments;
CREATE VIEW v_patient_appointments AS
SELECT
    a.appointment_id,
    a.appointment_date,
    a.status,
    p.patient_id,
    p.full_name AS patient_name,
    d.doctor_id,
    d.full_name AS doctor_name,
    d.specialization,
    dept.department_id,
    dept.department_name
FROM Appointment a
JOIN Patient p ON a.patient_id = p.patient_id
JOIN Doctor d ON a.doctor_id = d.doctor_id
JOIN Department dept ON d.department_id = dept.department_id;

DROP VIEW IF EXISTS v_department_revenue;
CREATE VIEW v_department_revenue AS
SELECT
    dept.department_id,
    dept.department_name,
    COUNT(DISTINCT a.appointment_id) AS total_appointments,
    SUM(b.amount_due) AS total_revenue,
    SUM(b.amount_paid) AS total_paid,
    SUM(b.amount_due - b.amount_paid) AS total_outstanding
FROM Department dept
JOIN Doctor d ON d.department_id = dept.department_id
JOIN Appointment a ON a.doctor_id = d.doctor_id
JOIN Billing b ON b.appointment_id = a.appointment_id
GROUP BY dept.department_id, dept.department_name;

DROP VIEW IF EXISTS v_unpaid_bills;
CREATE VIEW v_unpaid_bills AS
SELECT
    b.bill_id,
    b.patient_id,
    p.full_name AS patient_name,
    b.appointment_id,
    a.appointment_date,
    b.amount_due,
    b.amount_paid,
    (b.amount_due - b.amount_paid) AS outstanding_amount,
    b.payment_status,
    b.payment_method,
    d.doctor_id,
    d.full_name AS doctor_name,
    dept.department_id,
    dept.department_name
FROM Billing b
JOIN Patient p ON b.patient_id = p.patient_id
JOIN Appointment a ON b.appointment_id = a.appointment_id
JOIN Doctor d ON a.doctor_id = d.doctor_id
JOIN Department dept ON d.department_id = dept.department_id
WHERE b.payment_status IN ('Unpaid', 'Partially Paid');

DELIMITER //

DROP PROCEDURE IF EXISTS sp_create_appointment //
CREATE PROCEDURE sp_create_appointment(
    IN p_patient_id INT,
    IN p_doctor_id INT,
    IN p_appointment_date DATETIME,
    IN p_reason VARCHAR(255),
    OUT p_new_appointment_id INT
)
BEGIN
    INSERT INTO Appointment (patient_id, doctor_id, appointment_date, reason, status)
    VALUES (p_patient_id, p_doctor_id, p_appointment_date, p_reason, 'Scheduled');

    SET p_new_appointment_id = LAST_INSERT_ID();
END //

DROP PROCEDURE IF EXISTS sp_monthly_revenue_by_department //
CREATE PROCEDURE sp_monthly_revenue_by_department(
    IN p_year INT,
    IN p_month INT
)
BEGIN
    SELECT
        dept.department_id,
        dept.department_name,
        COUNT(DISTINCT a.appointment_id) AS appointments_count,
        SUM(b.amount_due) AS total_revenue,
        SUM(b.amount_paid) AS total_paid,
        SUM(b.amount_due - b.amount_paid) AS outstanding_amount
    FROM Department dept
    JOIN Doctor d ON d.department_id = dept.department_id
    JOIN Appointment a ON a.doctor_id = d.doctor_id
    JOIN Billing b ON b.appointment_id = a.appointment_id
    WHERE YEAR(a.appointment_date) = p_year
      AND MONTH(a.appointment_date) = p_month
    GROUP BY dept.department_id, dept.department_name
    ORDER BY total_revenue DESC;
END //

DELIMITER ;

DELIMITER //

DROP TRIGGER IF EXISTS trg_billing_set_status_before_ins //
CREATE TRIGGER trg_billing_set_status_before_ins
BEFORE INSERT ON Billing
FOR EACH ROW
BEGIN
    IF NEW.amount_paid IS NULL THEN
        SET NEW.amount_paid = 0;
    END IF;

    IF NEW.amount_paid >= NEW.amount_due THEN
        SET NEW.payment_status = 'Paid';
        IF NEW.payment_date IS NULL THEN
            SET NEW.payment_date = CURDATE();
        END IF;
    ELSEIF NEW.amount_paid > 0 THEN
        SET NEW.payment_status = 'Partially Paid';
        IF NEW.payment_date IS NULL THEN
            SET NEW.payment_date = CURDATE();
        END IF;
    ELSE
        SET NEW.payment_status = 'Unpaid';
    END IF;
END //

DROP TRIGGER IF EXISTS trg_billing_set_status_before_upd //
CREATE TRIGGER trg_billing_set_status_before_upd
BEFORE UPDATE ON Billing
FOR EACH ROW
BEGIN
    IF NEW.amount_paid IS NULL THEN
        SET NEW.amount_paid = 0;
    END IF;

    IF NEW.amount_paid >= NEW.amount_due THEN
        SET NEW.payment_status = 'Paid';
        IF NEW.payment_date IS NULL THEN
            SET NEW.payment_date = CURDATE();
        END IF;
    ELSEIF NEW.amount_paid > 0 THEN
        SET NEW.payment_status = 'Partially Paid';
        IF NEW.payment_date IS NULL THEN
            SET NEW.payment_date = CURDATE();
        END IF;
    ELSE
        SET NEW.payment_status = 'Unpaid';
    END IF;
END //

DELIMITER ;
