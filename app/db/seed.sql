USE hospital_manager;

-- ===========================
-- 1. DEPARTMENT (5 records)
-- ===========================
INSERT INTO Department (department_name, location, head_of_department)
VALUES
('Cardiology', 'Building A', 'Dr. Nguyen Van A'),
('Neurology', 'Building B', 'Dr. Tran Thi B'),
('Pediatrics', 'Building C', 'Dr. Le Minh C'),
('Orthopedics', 'Building D', 'Dr. Pham Van D'),
('Dermatology', 'Building E', 'Dr. Hoang Thi E');



-- ===========================
-- 2. DOCTOR (10 records)
-- ===========================
INSERT INTO Doctor (full_name, specialization, phone_number, email, department_id)
VALUES
('Dr. Nguyen Quang Anh', 'Cardiology', '0905111222', 'anh.nguyen@hospital.com', 1),
('Dr. Tran Bao Long', 'Cardiology', '0912333444', 'long.tran@hospital.com', 1),
('Dr. Le Thi Trang', 'Neurology', '0933444555', 'trang.le@hospital.com', 2),
('Dr. Pham Minh Hieu', 'Neurology', '0988776655', 'hieu.pham@hospital.com', 2),
('Dr. Hoang Van Phuc', 'Pediatrics', '0905111999', 'phuc.hoang@hospital.com', 3),
('Dr. Nguyen Thu Ha', 'Pediatrics', '0912333555', 'ha.nguyen@hospital.com', 3),
('Dr. Tran Hoai Nam', 'Orthopedics', '0933666777', 'nam.tran@hospital.com', 4),
('Dr. Do Thi Mai', 'Orthopedics', '0988111223', 'mai.do@hospital.com', 4),
('Dr. Pham Quang Huy', 'Dermatology', '0905222333', 'huy.pham@hospital.com', 5),
('Dr. Le Thanh Tam', 'Dermatology', '0912444555', 'tam.le@hospital.com', 5);



-- ===========================
-- 3. PATIENT (20 records)
-- ===========================
INSERT INTO Patient (full_name, gender, date_of_birth, phone_number, email, address, emergency_contact)
VALUES
('Nguyen Van A', 'Male', '1990-04-11', '0912000001', 'a.nguyen@mail.com', 'Ha Noi', '0903000001'),
('Tran Thi B', 'Female', '1988-02-20', '0912000002', 'b.tran@mail.com', 'Hai Phong', '0903000002'),
('Le Van C', 'Male', '1995-06-15', '0912000003', 'c.le@mail.com', 'Da Nang', '0903000003'),
('Hoang Thi D', 'Female', '1999-12-05', '0912000004', 'd.hoang@mail.com', 'Ha Noi', '0903000004'),
('Pham Van E', 'Male', '1985-03-29', '0912000005', 'e.pham@mail.com', 'Hue', '0903000005'),
('Nguyen Thi F', 'Female', '1992-07-18', '0912000006', 'f.nguyen@mail.com', 'Ho Chi Minh', '0903000006'),
('Tran Van G', 'Male', '1980-01-02', '0912000007', 'g.tran@mail.com', 'Ninh Binh', '0903000007'),
('Le Thi H', 'Female', '2000-09-25', '0912000008', 'h.le@mail.com', 'Ha Noi', '0903000008'),
('Hoang Van I', 'Male', '1998-10-14', '0912000009', 'i.hoang@mail.com', 'Da Nang', '0903000009'),
('Pham Thi J', 'Female', '1987-11-19', '0912000010', 'j.pham@mail.com', 'Ha Tinh', '0903000010'),
('Nguyen Van K', 'Male', '1993-03-11', '0912000011', 'k.nguyen@mail.com', 'Ha Noi', '0903000011'),
('Tran Thi L', 'Female', '1994-07-21', '0912000012', 'l.tran@mail.com', 'Hai Duong', '0903000012'),
('Le Van M', 'Male', '1991-08-30', '0912000013', 'm.le@mail.com', 'Nam Dinh', '0903000013'),
('Hoang Thi N', 'Female', '1997-05-10', '0912000014', 'n.hoang@mail.com', 'Quang Ninh', '0903000014'),
('Pham Van O', 'Male', '1984-12-01', '0912000015', 'o.pham@mail.com', 'Thanh Hoa', '0903000015'),
('Nguyen Thi P', 'Female', '1990-02-08', '0912000016', 'p.nguyen@mail.com', 'Ha Noi', '0903000016'),
('Tran Van Q', 'Male', '1989-03-30', '0912000017', 'q.tran@mail.com', 'Hai Phong', '0903000017'),
('Le Thi R', 'Female', '1996-04-27', '0912000018', 'r.le@mail.com', 'Phu Tho', '0903000018'),
('Hoang Van S', 'Male', '1983-09-09', '0912000019', 's.hoang@mail.com', 'Ha Nam', '0903000019'),
('Pham Thi T', 'Female', '2001-11-11', '0912000020', 't.pham@mail.com', 'Ha Noi', '0903000020');



-- ===========================
-- 4. APPOINTMENT (30 records)
-- ===========================
INSERT INTO Appointment (patient_id, doctor_id, appointment_date, reason, status)
VALUES
(1, 1, '2025-01-05 09:00:00', 'Chest pain', 'Completed'),
(2, 1, '2025-01-06 10:00:00', 'Heart checkup', 'Completed'),
(3, 2, '2025-01-07 11:00:00', 'Cardio recheck', 'Completed'),
(4, 3, '2025-01-08 09:30:00', 'Headache', 'Completed'),
(5, 3, '2025-01-09 14:00:00', 'Migraine', 'Completed'),
(6, 4, '2025-01-10 15:00:00', 'Nerve issue', 'Completed'),
(7, 5, '2025-01-12 08:00:00', 'Fever', 'Completed'),
(8, 5, '2025-01-13 10:30:00', 'Cough', 'Completed'),
(9, 6, '2025-01-14 13:00:00', 'Pediatric visit', 'Completed'),
(10, 6, '2025-01-15 09:00:00', 'Child checkup', 'Completed'),
(11, 7, '2025-01-16 16:00:00', 'Bone pain', 'Completed'),
(12, 7, '2025-01-17 10:00:00', 'Joint pain', 'Completed'),
(13, 8, '2025-01-18 09:30:00', 'Back pain', 'Completed'),
(14, 8, '2025-01-19 11:00:00', 'Neck sprain', 'Completed'),
(15, 9, '2025-01-20 14:00:00', 'Skin rash', 'Completed'),
(16, 9, '2025-01-21 15:30:00', 'Skin allergy', 'Completed'),
(17, 10, '2025-01-22 10:00:00', 'Dermatitis', 'Completed'),
(18, 10, '2025-01-22 11:30:00', 'Acne issue', 'Completed'),
(19, 1, '2025-01-23 09:00:00', 'Heart recheck', 'Completed'),
(20, 1, '2025-01-24 10:00:00', 'Short breath', 'Completed'),
(2, 2, '2025-01-24 11:00:00', 'High blood pressure', 'Completed'),
(3, 4, '2025-01-24 13:00:00', 'Numbness', 'Completed'),
(5, 6, '2025-01-24 14:00:00', 'Kid consultation', 'Completed'),
(8, 7, '2025-01-24 15:00:00', 'Injury', 'Completed'),
(10, 9, '2025-01-24 16:00:00', 'Skin check', 'Completed'),
(12, 10, '2025-01-24 17:00:00', 'Allergy test', 'Completed'),
(14, 8, '2025-01-25 09:30:00', 'Back issue', 'Completed'),
(16, 7, '2025-01-25 11:00:00', 'Pain relief', 'Completed'),
(18, 5, '2025-01-25 13:30:00', 'Cough fever', 'Completed'),
(20, 3, '2025-01-25 14:30:00', 'Head pain', 'Completed');



-- ===========================
-- 5. MEDICAL RECORD (20 records)
-- ===========================
INSERT INTO Medical_Record (appointment_id, diagnosis, prescription, treatment_notes, follow_up_date)
VALUES
(1, 'Chest pain', 'Paracetamol', 'Rest 3 days', '2025-01-12'),
(2, 'Heart checkup', 'Aspirin', 'Avoid stress', '2025-01-14'),
(3, 'Cardio issue', 'Beta blockers', 'Monitor heart rate', '2025-01-15'),
(4, 'Headache', 'Ibuprofen', 'Hydration', '2025-01-16'),
(5, 'Migraine', 'Triptan', 'Avoid bright lights', '2025-01-17'),
(6, 'Nerve issue', 'Vitamin B12', 'Massage', '2025-01-18'),
(7, 'Fever', 'Tylenol', 'Rest', '2025-01-19'),
(8, 'Cough', 'Cough syrup', 'Keep warm', '2025-01-20'),
(9, 'Cold', 'Vitamin C', 'Drink warm water', '2025-01-21'),
(10, 'Checkup', 'None', 'Normal', '2025-02-01'),
(11, 'Bone pain', 'Calcium', 'Physiotherapy', '2025-02-02'),
(12, 'Joint pain', 'Painkiller', 'Exercise lightly', '2025-02-03'),
(13, 'Back pain', 'Muscle relaxant', 'Avoid lifting', '2025-02-04'),
(14, 'Neck sprain', 'Anti-inflammatory', 'Neck support', '2025-02-05'),
(15, 'Skin rash', 'Cream', 'Avoid dust', '2025-02-06'),
(16, 'Allergy', 'Antihistamine', 'Avoid allergens', '2025-02-07'),
(17, 'Dermatitis', 'Topical cream', 'Avoid chemicals', '2025-02-08'),
(18, 'Acne', 'Acne gel', 'Wash face daily', '2025-02-09'),
(19, 'Heart recheck', 'Aspirin', 'Healthy diet', '2025-02-10'),
(20, 'Short breath', 'Spray', 'Breathing exercise', '2025-02-11');



-- ===========================
-- 6. BILLING (30 records)
-- ===========================
INSERT INTO Billing (patient_id, appointment_id, amount_due, amount_paid, payment_date, payment_status, payment_method)
VALUES
(1, 1, 300000, 300000, '2025-01-05', 'Paid', 'cash'),
(2, 2, 350000, 350000, '2025-01-06', 'Paid', 'card'),
(3, 3, 250000, 200000, '2025-01-07', 'Partially Paid', 'cash'),
(4, 4, 200000, 200000, '2025-01-08', 'Paid', 'insurance'),
(5, 5, 220000, 0, NULL, 'Unpaid', 'cash'),
(6, 6, 300000, 100000, '2025-01-10', 'Partially Paid', 'cash'),
(7, 7, 150000, 150000, '2025-01-12', 'Paid', 'card'),
(8, 8, 180000, 180000, '2025-01-13', 'Paid', 'cash'),
(9, 9, 140000, 140000, '2025-01-14', 'Paid', 'cash'),
(10, 10, 200000, 200000, '2025-01-15', 'Paid', 'insurance'),
(11, 11, 400000, 0, NULL, 'Unpaid', 'cash'),
(12, 12, 320000, 320000, '2025-01-17', 'Paid', 'card'),
(13, 13, 280000, 280000, '2025-01-18', 'Paid', 'cash'),
(14, 14, 250000, 250000, '2025-01-19', 'Paid', 'cash'),
(15, 15, 230000, 200000, '2025-01-20', 'Partially Paid', 'cash'),
(16, 16, 260000, 260000, '2025-01-21', 'Paid', 'insurance'),
(17, 17, 170000, 170000, '2025-01-22', 'Paid', 'cash'),
(18, 18, 150000, 150000, '2025-01-22', 'Paid', 'card'),
(19, 19, 350000, 350000, '2025-01-23', 'Paid', 'cash'),
(20, 20, 300000, 300000, '2025-01-24', 'Paid', 'card'),
(2, 21, 200000, 200000, '2025-01-24', 'Paid', 'cash'),
(3, 22, 180000, 0, NULL, 'Unpaid', 'cash'),
(5, 23, 160000, 160000, '2025-01-24', 'Paid', 'insurance'),
(8, 24, 210000, 210000, '2025-01-24', 'Paid', 'card'),
(10, 25, 190000, 150000, '2025-01-24', 'Partially Paid', 'card'),
(12, 26, 260000, 260000, '2025-01-24', 'Paid', 'cash'),
(14, 27, 200000, 200000, '2025-01-25', 'Paid', 'cash'),
(16, 28, 240000, 240000, '2025-01-25', 'Paid', 'card'),
(18, 29, 170000, 170000, '2025-01-25', 'Paid', 'cash'),
(20, 30, 250000, 250000, '2025-01-25', 'Paid', 'insurance');



-- ===========================
-- 7. STAFF (5 records)
-- ===========================
INSERT INTO Staff (full_name, position, phone_number, email, assigned_department)
VALUES
('Nguyen Thanh Hai', 'Receptionist', '0912333000', 'hai.nguyen@hospital.com', 1),
('Tran Thi Minh', 'Nurse', '0912333111', 'minh.tran@hospital.com', 2),
('Pham Quoc Bao', 'Cashier', '0912333222', 'bao.pham@hospital.com', 3),
('Hoang Anh Kiet', 'Admin', '0912333333', 'kiet.hoang@hospital.com', 4),
('Le Thi Kim', 'Manager', '0912333444', 'kim.le@hospital.com', 5);
