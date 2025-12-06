CREATE DATABASE IF NOT EXISTS hospital_manager;
USE hospital_manager;

CREATE TABLE Department (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE,
    location VARCHAR(100),
    head_of_department VARCHAR(100)
);

CREATE TABLE Doctor (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES Department(department_id)
);

CREATE TABLE Patient (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    gender ENUM('Male','Female','Other') NOT NULL,
    date_of_birth DATE NOT NULL,
    phone_number VARCHAR(20),
    email VARCHAR(100),
    address VARCHAR(255),
    emergency_contact VARCHAR(100),
    date_registered DATE DEFAULT (CURRENT_DATE)
);

CREATE TABLE Appointment (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date DATETIME NOT NULL,
    reason VARCHAR(255),
    status ENUM('Scheduled', 'Completed', 'Cancelled') DEFAULT 'Scheduled',
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctor(doctor_id)
);

CREATE TABLE Medical_Record (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    appointment_id INT NOT NULL,
    diagnosis VARCHAR(255),
    prescription TEXT,
    treatment_notes TEXT,
    follow_up_date DATE,
    FOREIGN KEY (appointment_id) REFERENCES Appointment(appointment_id)
);

CREATE TABLE Billing (
    bill_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    appointment_id INT NOT NULL,
    amount_due DECIMAL(10,2) NOT NULL,
    amount_paid DECIMAL(10,2) DEFAULT 0,
    payment_date DATE,
    payment_status ENUM('Unpaid','Partially Paid','Paid') DEFAULT 'Unpaid',
    payment_method ENUM('cash','card','insurance'),
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id),
    FOREIGN KEY (appointment_id) REFERENCES Appointment(appointment_id)
);

CREATE TABLE Staff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    position VARCHAR(100),
    phone_number VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    assigned_department INT,
    FOREIGN KEY (assigned_department) REFERENCES Department(department_id)
);
