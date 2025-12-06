# Hospital Patient Manager

**Hệ thống quản lý bệnh viện** - Đồ án môn học Cơ sở dữ liệu

## 📋 Giới thiệu

Hospital Patient Manager là một hệ thống quản lý bệnh viện hoàn chỉnh được xây dựng với MySQL và Python, đáp ứng đầy đủ các yêu cầu của đồ án môn học Cơ sở dữ liệu.

### Tính năng chính

- **Cơ sở dữ liệu MySQL** với 7 bảng được chuẩn hóa đến dạng chuẩn 3NF
- **3 Views** phục vụ báo cáo và truy vấn nhanh
- **2 Stored Procedures** cho logic nghiệp vụ
- **2 Triggers** tự động cập nhật dữ liệu
- **Chương trình Python** kết nối database với visualization
- **Giao diện Web Flask** (tính năng bonus)

### Mục đích

Dự án được phát triển để đáp ứng các yêu cầu của đồ án môn học:
- Part A: Thiết kế ERD và chuẩn hóa database
- Part B: Xây dựng database trên MySQL
- Part C: Tạo Views, Stored Procedures, Triggers
- Part D: Kết nối Python với MySQL và visualization

## 🎯 Yêu cầu đề bài đã hoàn thành

### Part A - Phân tích và thiết kế Database
✅ Mô tả nghiệp vụ bệnh viện  
✅ Vẽ sơ đồ ERD (Entity-Relationship Diagram)  
✅ Chuẩn hóa database lên dạng chuẩn 3NF  
✅ Xác định functional dependencies  
✅ Thiết kế 7 bảng với khóa chính, khóa ngoại

### Part B - Cài đặt trên MySQL
✅ Tạo 7 bảng với đầy đủ ràng buộc (PRIMARY KEY, FOREIGN KEY, UNIQUE, NOT NULL)  
✅ Dữ liệu mẫu: 5 khoa, 10 bác sĩ, 20 bệnh nhân, 30 lịch hẹn  
✅ File SQL đầy đủ cho schema và data

### Part C - Views, Procedures, Triggers
✅ **3 Views:**
- `v_patient_appointments` - Chi tiết lịch hẹn bệnh nhân
- `v_department_revenue` - Doanh thu theo khoa
- `v_unpaid_bills` - Danh sách hóa đơn chưa thanh toán

✅ **2 Stored Procedures:**
- `sp_create_appointment` - Tạo lịch hẹn mới
- `sp_monthly_revenue_by_department` - Báo cáo doanh thu theo tháng

✅ **2 Triggers:**
- Tự động cập nhật trạng thái thanh toán khi INSERT
- Tự động cập nhật trạng thái thanh toán khi UPDATE

### Part D - Python Program
✅ Kết nối thành công với MySQL database  
✅ Truy vấn Views và hiển thị kết quả dạng bảng  
✅ Gọi Stored Procedures  
✅ Thực hiện các câu lệnh SQL phức tạp với JOIN  
✅ Visualization: 4 biểu đồ (bar chart, line chart, horizontal bar, pie chart)  
✅ Code modular, có xử lý lỗi và documentation

### Bonus - Web Application
✅ Giao diện web Flask đầy đủ CRUD  
✅ Dashboard với KPIs và biểu đồ  
✅ Tìm kiếm và báo cáo

## 📁 Cấu trúc dự án

```
hospital-patient-manager/
│
├── app/                                    # Thư mục chính chứa source code
│   ├── db/                                # Module database
│   │   ├── schema.sql                     # Định nghĩa 7 bảng database
│   │   ├── seed.sql                       # Dữ liệu mẫu (120 records)
│   │   ├── views_procedures.sql           # Views, Procedures, Triggers
│   │   ├── connection.py                  # Module kết nối database
│   │   └── __init__.py
│   │
│   ├── models/                            # Data models
│   │   ├── patients.py                    # CRUD cho bảng Patient
│   │   ├── doctors.py                     # CRUD cho bảng Doctor
│   │   ├── appointments.py                # CRUD cho bảng Appointment
│   │   └── __init__.py
│   │
│   ├── queries/                           # SQL queries
│   │   ├── inner_join.py                  # Queries với INNER JOIN
│   │   ├── left_join.py                   # Queries với LEFT JOIN
│   │   ├── multi_join.py                  # Queries nhiều bảng
│   │   ├── high_cost.py                   # Queries phức tạp
│   │   └── __init__.py
│   │
│   ├── services/                          # Business logic
│   │   ├── analytics.py                   # Phân tích dữ liệu
│   │   ├── search.py                      # Tìm kiếm
│   │   └── __init__.py
│   │
│   ├── ui/                                # Flask web interface
│   │   ├── templates/                     # HTML templates
│   │   │   ├── base.html
│   │   │   ├── dashboard.html
│   │   │   ├── patients.html
│   │   │   ├── doctors.html
│   │   │   ├── appointments.html
│   │   │   └── ...
│   │   ├── static/                        # CSS, JS, images
│   │   │   └── css/
│   │   │       └── style.css
│   │   ├── routes.py                      # Flask routes
│   │   └── __init__.py                    # Flask app factory
│   │
│   └── main.py                            # ⭐ Part D - Chương trình Python chính
│
├── charts/                                 # Biểu đồ được tạo tự động
│   ├── department_revenue.png             # Bar chart doanh thu
│   ├── monthly_revenue_trend.png          # Line chart xu hướng
│   ├── doctor_performance.png             # Horizontal bar hiệu suất bác sĩ
│   └── appointment_status.png             # Pie chart trạng thái lịch hẹn
│
├── docs/                                   # Tài liệu
│   ├── DATABASE_SETUP.md                  # Hướng dẫn setup database
│   └── README.md
│
├── tests/                                  # Unit tests (tùy chọn)
│   └── README.md
│
├── .env                                    # ⚠️ File cấu hình (KHÔNG push lên Git)
├── .env.example                           # Template cho .env
├── .gitignore                             # Quy tắc ignore cho Git
├── LICENSE                                # Giấy phép MIT
├── README.md                              # 📖 File này
├── requirements.txt                       # Python dependencies
└── run.py                                 # Entry point cho Flask web app
```

## 🗄️ Cấu trúc Database

### 7 Bảng chính

#### 1. Department (Khoa)
```sql
- department_id (PK)
- department_name (UNIQUE)
- location
- head_of_department
```

#### 2. Doctor (Bác sĩ)
```sql
- doctor_id (PK)
- full_name
- specialization
- phone_number
- email (UNIQUE)
- department_id (FK → Department)
```

#### 3. Patient (Bệnh nhân)
```sql
- patient_id (PK)
- full_name
- gender (ENUM)
- date_of_birth
- phone_number
- email
- address
- emergency_contact
- date_registered
```

#### 4. Appointment (Lịch hẹn)
```sql
- appointment_id (PK)
- patient_id (FK → Patient)
- doctor_id (FK → Doctor)
- appointment_date
- reason
- status (ENUM: Scheduled/Completed/Cancelled)
```

#### 5. Medical_Record (Hồ sơ bệnh án)
```sql
- record_id (PK)
- appointment_id (FK → Appointment)
- diagnosis
- prescription
- treatment_notes
- follow_up_date
```

#### 6. Billing (Hóa đơn)
```sql
- bill_id (PK)
- patient_id (FK → Patient)
- appointment_id (FK → Appointment)
- amount_due
- amount_paid
- payment_date
- payment_status (ENUM: Unpaid/Partially Paid/Paid)
- payment_method (ENUM: cash/card/insurance)
```

#### 7. Staff (Nhân viên)
```sql
- staff_id (PK)
- full_name
- position
- phone_number
- email (UNIQUE)
- assigned_department (FK → Department)
```

### 3 Views

#### v_patient_appointments
Hiển thị thông tin chi tiết về lịch hẹn của bệnh nhân kèm thông tin bác sĩ và khoa.

```sql
SELECT appointment_id, appointment_date, status,
       patient_name, doctor_name, specialization, department_name
FROM ...
```

#### v_department_revenue
Tổng hợp doanh thu theo từng khoa.

```sql
SELECT department_name, total_appointments,
       total_amount_due, total_amount_paid, total_outstanding
FROM ...
```

#### v_unpaid_bills
Danh sách các hóa đơn chưa thanh toán hoặc thanh toán một phần.

```sql
SELECT bill_id, patient_name, amount_due, amount_paid,
       amount_outstanding, payment_status
FROM ...
WHERE payment_status IN ('Unpaid', 'Partially Paid')
```

### 2 Stored Procedures

#### sp_create_appointment
Tạo lịch hẹn mới với các tham số đầu vào.

```sql
CALL sp_create_appointment(patient_id, doctor_id, appointment_date, reason);
```

#### sp_monthly_revenue_by_department
Báo cáo doanh thu theo tháng cho từng khoa.

```sql
CALL sp_monthly_revenue_by_department(year, month);
```

### 2 Triggers

#### trg_billing_set_status_before_ins
Tự động set trạng thái thanh toán khi INSERT record mới vào Billing.

#### trg_billing_set_status_before_upd
Tự động update trạng thái thanh toán khi UPDATE amount_paid trong Billing.

## 🚀 Cài đặt và Sử dụng

### Bước 1: Yêu cầu hệ thống

- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **MySQL 8.0+** ([Download](https://dev.mysql.com/downloads/mysql/))
- **Git** (tùy chọn) ([Download](https://git-scm.com/downloads))

Kiểm tra version:
```bash
python --version
mysql --version
```

### Bước 2: Clone hoặc tải project

**Từ Git:**
```bash
git clone https://github.com/your-username/hospital-patient-manager.git
cd hospital-patient-manager
```

**Hoặc tải ZIP và giải nén**

### Bước 3: Cài đặt Python dependencies

```bash
# Tạo virtual environment (khuyến nghị)
python -m venv venv

# Kích hoạt virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Cài đặt packages
pip install -r requirements.txt
```

**Dependencies sẽ được cài:**
- pymysql==1.1.2 (MySQL connector)
- pandas==2.3.0 (Data manipulation)
- matplotlib==3.10.3 (Visualization)
- python-dotenv==1.1.0 (Environment variables)
- seaborn==0.13.2 (Advanced visualization)
- flask==3.1.2 (Web framework)

### Bước 4: Thiết lập MySQL Database

#### Cách 1: Sử dụng MySQL Command Line

```bash
# Đăng nhập MySQL
mysql -u root -p

# Tạo database
CREATE DATABASE hospital_manager;
exit;

# Import schema (7 tables)
mysql -u root -p hospital_manager < app/db/schema.sql

# Import dữ liệu mẫu (120 records)
mysql -u root -p hospital_manager < app/db/seed.sql

# Import views, procedures, triggers
mysql -u root -p hospital_manager < app/db/views_procedures.sql
```

#### Cách 2: Sử dụng MySQL Workbench (Dễ hơn)

1. Mở **MySQL Workbench**
2. Kết nối đến MySQL Server
3. Tạo database mới:
   ```sql
   CREATE DATABASE hospital_manager;
   ```
4. Chọn database `hospital_manager`
5. **File → Open SQL Script** và thực thi theo thứ tự:
   - `app/db/schema.sql`
   - `app/db/seed.sql`
   - `app/db/views_procedures.sql`

#### Kiểm tra database đã setup đúng

```sql
USE hospital_manager;
SHOW TABLES;  -- Phải có 7 tables
SELECT COUNT(*) FROM Department;  -- Phải có 5 records
SELECT COUNT(*) FROM Doctor;      -- Phải có 10 records
SELECT COUNT(*) FROM Patient;     -- Phải có 20 records

-- Kiểm tra Views
SHOW FULL TABLES WHERE Table_type = 'VIEW';  -- Phải có 3 views

-- Kiểm tra Procedures
SHOW PROCEDURE STATUS WHERE Db = 'hospital_manager';  -- Phải có 2 procedures

-- Kiểm tra Triggers
SHOW TRIGGERS;  -- Phải có 2 triggers
```

### Bước 5: Cấu hình môi trường

```bash
# Copy file template
cp .env.example .env

# Chỉnh sửa file .env (dùng notepad hoặc text editor)
```

**Nội dung file `.env`:**
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password_here  ← Thay bằng mật khẩu MySQL của bạn
DB_NAME=hospital_manager
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
```

⚠️ **Quan trọng:** Thay `your_mysql_password_here` bằng mật khẩu MySQL thực của bạn!

### Bước 6: Chạy chương trình

#### Option 1: Chạy Part D - Python Program (BẮT BUỘC)

```bash
python app/main.py
```

**Kết quả mong đợi:**
```
================================================================================
HOSPITAL PATIENT MANAGER - PYTHON PROGRAM
Part D: Database Connection, Query Execution, and Visualization
================================================================================
✓ Successfully connected to MySQL database

### PART D.1: QUERYING VIEWS ###
================================================================================
VIEW 1: v_department_revenue - Revenue Summary by Department
================================================================================
 department_id department_name  total_appointments  total_revenue  ...
             4     Orthopedics                   7      1900000.0   ...
             1      Cardiology                   6      1750000.0   ...
...

✓ Chart saved as: charts/department_revenue.png
✓ Chart saved as: charts/monthly_revenue_trend.png
✓ Chart saved as: charts/doctor_performance.png
✓ Chart saved as: charts/appointment_status.png

================================================================================
✓ Program execution completed successfully!
================================================================================
```

**Output:**
- Console hiển thị dữ liệu từ Views, Procedures, và custom queries
- 4 file biểu đồ PNG được tạo trong thư mục `charts/`:
  - `department_revenue.png` - Bar chart doanh thu theo khoa
  - `monthly_revenue_trend.png` - Line chart xu hướng doanh thu
  - `doctor_performance.png` - Horizontal bar chart hiệu suất bác sĩ
  - `appointment_status.png` - Pie chart phân bố trạng thái lịch hẹn

#### Option 2: Chạy Web Application (BONUS)

```bash
python run.py
```

Sau đó mở trình duyệt tại: **http://127.0.0.1:5000**

**Chức năng Web App:**
- 📊 Dashboard với KPIs và biểu đồ realtime
- 👥 Quản lý bệnh nhân (CRUD: Create, Read, Update, Delete)
- 👨‍⚕️ Quản lý bác sĩ
- 📅 Quản lý lịch hẹn
- 🔍 Tìm kiếm và lọc dữ liệu
- 📈 Báo cáo và thống kê

## 📊 Chi tiết chương trình Python (Part D)

File: `app/main.py`

### Các chức năng chính

#### 1. Kết nối Database
```python
def get_db_connection():
    """Establish connection to MySQL database"""
    connection = pymysql.connect(**DB_CONFIG)
    return connection
```

#### 2. Truy vấn Views
```python
def query_view_department_revenue(connection):
    """Query v_department_revenue view"""
    query = "SELECT * FROM v_department_revenue ORDER BY total_revenue DESC"
    df = pd.read_sql(query, connection)
    print(df.to_string(index=False))
```

#### 3. Gọi Stored Procedures
```python
def call_procedure_monthly_revenue(connection, year=2025, month=1):
    """Call sp_monthly_revenue_by_department stored procedure"""
    cursor = connection.cursor()
    cursor.callproc('sp_monthly_revenue_by_department', [year, month])
    results = cursor.fetchall()
```

#### 4. Custom SQL Queries với JOIN
```python
def custom_query_department_stats(connection):
    """Custom JOIN query: Department statistics"""
    query = """
        SELECT 
            d.department_name,
            COUNT(DISTINCT doc.doctor_id) AS total_doctors,
            COUNT(DISTINCT a.appointment_id) AS total_appointments,
            COUNT(DISTINCT a.patient_id) AS unique_patients
        FROM Department d
        LEFT JOIN Doctor doc ON d.department_id = doc.department_id
        LEFT JOIN Appointment a ON doc.doctor_id = a.doctor_id
        GROUP BY d.department_id, d.department_name
    """
    df = pd.read_sql(query, connection)
```

#### 5. Data Visualization
```python
def visualize_department_revenue(df_revenue):
    """Create bar chart for department revenue"""
    plt.figure(figsize=(12, 6))
    plt.bar(departments, revenue, label='Total Revenue')
    plt.bar(departments, paid, label='Paid')
    plt.bar(departments, outstanding, label='Outstanding')
    plt.savefig('charts/department_revenue.png', dpi=300)
```

### Luồng thực thi

1. **Kết nối database** → Sử dụng thông tin từ `.env`
2. **Query 3 Views** → Hiển thị dữ liệu dạng table
3. **Call Stored Procedures** → Thực thi logic nghiệp vụ
4. **Custom Queries** → Phân tích dữ liệu với JOIN
5. **Visualization** → Tạo 4 biểu đồ PNG
6. **Đóng kết nối** → Clean up resources

## 🎨 Web Application (Flask)

File: `run.py`, `app/ui/`

### Tính năng

#### Dashboard (`/`)
- Hiển thị KPIs: Tổng bệnh nhân, bác sĩ, lịch hẹn, doanh thu
- Biểu đồ appointments per day (30 ngày)
- Biểu đồ phân bố chuyên khoa
- Hoạt động gần đây

#### Quản lý Bệnh nhân (`/patients`)
- Danh sách tất cả bệnh nhân
- Tìm kiếm theo tên
- Thêm bệnh nhân mới
- Sửa thông tin bệnh nhân
- Xóa bệnh nhân (với xác nhận)
- Xem chi tiết và lịch sử khám

#### Quản lý Bác sĩ (`/doctors`)
- Danh sách bác sĩ theo khoa
- Thêm/sửa/xóa bác sĩ
- Xem lịch làm việc
- Thống kê hiệu suất

#### Quản lý Lịch hẹn (`/appointments`)
- Đặt lịch hẹn mới
- Xem lịch theo ngày/tuần/tháng
- Cập nhật trạng thái (Scheduled/Completed/Cancelled)
- Hủy lịch hẹn

#### Báo cáo (`/reports`)
- Báo cáo doanh thu
- Báo cáo công nợ
- Thống kê bệnh nhân
- Export CSV

### Cấu trúc Routes

```python
@bp.route('/')
def dashboard():
    """Dashboard with KPIs and charts"""
    
@bp.route('/patients')
def list_patients():
    """List all patients"""
    
@bp.route('/patients/add', methods=['GET', 'POST'])
def add_patient():
    """Add new patient"""
    
@bp.route('/doctors')
def list_doctors():
    """List all doctors"""
    
@bp.route('/appointments')
def list_appointments():
    """List all appointments"""
```

## 🧪 Testing

### Kiểm tra Database

```sql
-- Test Views
SELECT * FROM v_patient_appointments LIMIT 5;
SELECT * FROM v_department_revenue;
SELECT * FROM v_unpaid_bills;

-- Test Stored Procedures
CALL sp_create_appointment(1, 1, '2025-12-10 10:00:00', 'Regular checkup');
CALL sp_monthly_revenue_by_department(2025, 12);

-- Test Triggers (tự động chạy khi INSERT/UPDATE Billing)
INSERT INTO Billing (patient_id, appointment_id, amount_due, amount_paid)
VALUES (1, 1, 500000, 500000);
-- → payment_status sẽ tự động = 'Paid'
```

### Kiểm tra Python Program

```bash
# Chạy và kiểm tra output
python app/main.py

# Kiểm tra charts được tạo
ls charts/*.png
# Phải có 4 files
```

### Kiểm tra Web App

```bash
python run.py
# Truy cập http://127.0.0.1:5000
# Test các chức năng CRUD
```

## 🐛 Xử lý lỗi thường gặp

### Lỗi: `ModuleNotFoundError: No module named 'pymysql'`
**Nguyên nhân:** Chưa cài dependencies  
**Giải pháp:**
```bash
pip install -r requirements.txt
```

### Lỗi: `Access denied for user 'root'@'localhost'`
**Nguyên nhân:** Sai mật khẩu MySQL trong `.env`  
**Giải pháp:** Kiểm tra và sửa `DB_PASSWORD` trong file `.env`

### Lỗi: `Unknown database 'hospital_manager'`
**Nguyên nhân:** Chưa tạo database  
**Giải pháp:**
```sql
CREATE DATABASE hospital_manager;
```

### Lỗi: `Table 'hospital_manager.Department' doesn't exist`
**Nguyên nhân:** Chưa import schema  
**Giải pháp:**
```bash
mysql -u root -p hospital_manager < app/db/schema.sql
mysql -u root -p hospital_manager < app/db/seed.sql
mysql -u root -p hospital_manager < app/db/views_procedures.sql
```

### Lỗi: `Table 'hospital_manager.v_department_revenue' doesn't exist`
**Nguyên nhân:** Chưa import views  
**Giải pháp:**
```bash
mysql -u root -p hospital_manager < app/db/views_procedures.sql
```

### Charts không được tạo
**Nguyên nhân:** Thiếu thư mục charts  
**Giải pháp:** Thư mục sẽ tự động tạo khi chạy `python app/main.py`

### Web app không chạy
**Nguyên nhân:** Thiếu Flask  
**Giải pháp:**
```bash
pip install flask
```

## 📝 Dữ liệu mẫu

### 5 Khoa (Departments)
1. Cardiology (Tim mạch) - Building A
2. Neurology (Thần kinh) - Building B
3. Pediatrics (Nhi khoa) - Building C
4. Orthopedics (Chỉnh hình) - Building D
5. Dermatology (Da liễu) - Building E

### 10 Bác sĩ (Doctors)
- Dr. Nguyen Quang Anh (Cardiology)
- Dr. Tran Bao Long (Cardiology)
- Dr. Le Thi Trang (Neurology)
- Dr. Pham Minh Hieu (Neurology)
- Dr. Hoang Van Phuc (Pediatrics)
- Dr. Nguyen Thu Ha (Pediatrics)
- Dr. Tran Hoai Nam (Orthopedics)
- Dr. Do Thi Mai (Orthopedics)
- Dr. Pham Quang Huy (Dermatology)
- Dr. Le Thanh Tam (Dermatology)

### 20 Bệnh nhân (Patients)
Bệnh nhân với đầy đủ thông tin demographics: họ tên, giới tính, ngày sinh, SĐT, email, địa chỉ, người liên hệ khẩn cấp.

### 30 Lịch hẹn (Appointments)
Lịch hẹn trong tháng 1/2025 với các trạng thái khác nhau.

### 30 Hóa đơn (Billing)
Hóa đơn với các trạng thái: Paid, Unpaid, Partially Paid.

## 🛠️ Công nghệ sử dụng

### Backend
- **MySQL 8.0** - Relational Database Management System
- **Python 3.12** - Programming Language
- **PyMySQL 1.1.2** - MySQL connector for Python
- **Flask 3.1.2** - Web Framework

### Data Processing & Visualization
- **Pandas 2.3.0** - Data manipulation and analysis
- **Matplotlib 3.10.3** - Static visualization
- **Seaborn 0.13.2** - Statistical visualization

### Development Tools
- **python-dotenv 1.1.0** - Environment variable management
- **Git** - Version control
- **MySQL Workbench** - Database design and management

## 📚 Tài liệu tham khảo

### Trong project
- `docs/DATABASE_SETUP.md` - Hướng dẫn chi tiết setup database
- `docs/README.md` - Tổng quan tài liệu
- `.env.example` - Template cấu hình
- `LICENSE` - MIT License

### Online Resources
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Python MySQL Tutorial](https://www.w3schools.com/python/python_mysql_getstarted.asp)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Documentation](https://matplotlib.org/stable/index.html)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 👨‍💻 Phát triển và Đóng góp

### Clone và Development

```bash
# Clone repository
git clone https://github.com/your-username/hospital-patient-manager.git
cd hospital-patient-manager

# Tạo branch mới
git checkout -b feature/your-feature-name

# Sau khi code xong
git add .
git commit -m "Add: your feature description"
git push origin feature/your-feature-name
```

### Code Style

- Python code tuân theo PEP 8
- SQL queries sử dụng uppercase cho keywords
- Comments bằng tiếng Việt hoặc tiếng Anh
- Docstrings cho tất cả functions

### Testing

Trước khi commit, test:
1. ✅ `python app/main.py` chạy không lỗi
2. ✅ Charts được tạo đầy đủ (4 files)
3. ✅ `python run.py` web app chạy được
4. ✅ Không có file .env trong git

## 📄 License

Dự án được phát hành dưới [MIT License](LICENSE).

Được tạo cho mục đích giáo dục - Database Course Project.

## 🙏 Credits

- **Phát triển bởi:** Hospital Patient Manager Team
- **Mục đích:** Đồ án môn học Cơ sở dữ liệu
- **Năm học:** 2024-2025
- **Framework:** Python, MySQL, Flask

## 📞 Liên hệ & Hỗ trợ

Nếu gặp vấn đề khi sử dụng:

1. **Đọc tài liệu:** Check `docs/DATABASE_SETUP.md`
2. **Kiểm tra Issues:** Tìm các vấn đề tương tự
3. **Tạo Issue mới:** Mô tả chi tiết lỗi và môi trường

## ⭐ Features Highlights

### Database Design Excellence
- ✅ Chuẩn hóa 3NF hoàn chỉnh
- ✅ Ràng buộc toàn vẹn đầy đủ
- ✅ Indexes tối ưu
- ✅ Foreign keys đúng chuẩn

### Python Program Quality
- ✅ Modular code structure
- ✅ Error handling đầy đủ
- ✅ Clean code & comments
- ✅ Professional visualizations

### Web Application
- ✅ Responsive design
- ✅ User-friendly interface
- ✅ Real-time data updates
- ✅ Complete CRUD operations

## 🎓 Học hỏi từ Project

Dự án này giúp bạn học:

1. **Database Design**: ERD, normalization, constraints
2. **SQL Advanced**: Views, stored procedures, triggers
3. **Python-MySQL**: Connection, queries, data manipulation
4. **Data Visualization**: Matplotlib, Pandas, Seaborn
5. **Web Development**: Flask, HTML, CSS, routing
6. **Best Practices**: Code organization, documentation, error handling
7. **Git & GitHub**: Version control, collaboration

## 🚀 Roadmap (Tính năng tương lai)

- [ ] Authentication & Authorization
- [ ] Email notifications
- [ ] SMS reminders
- [ ] Payment gateway integration
- [ ] Medical imaging storage
- [ ] Prescription management
- [ ] Lab test results
- [ ] API endpoints (REST API)
- [ ] Mobile app
- [ ] Report exports (PDF, Excel)

---

## ✅ Checklist hoàn thành Đồ án

- [x] Part A: ERD & Normalization
- [x] Part B: Database Implementation
- [x] Part C: Views, Procedures, Triggers
- [x] Part D: Python Program & Visualization
- [x] Bonus: Web Application
- [x] Documentation: README, SETUP guides
- [x] Testing: All features working
- [x] Clean code: Comments, structure
- [x] Ready for submission

---

**🎉 Project Status: COMPLETE & READY FOR SUBMISSION**

**Last Updated:** December 6, 2025  
**Version:** 1.0.0  
**Repository:** https://github.com/your-username/hospital-patient-manager

---

**Made with ❤️ for Database Course Project**
