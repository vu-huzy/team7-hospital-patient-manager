"""
Flask Routes - All application routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, Response
from datetime import datetime
import csv
import io

# Import models
from app.models import patients, doctors, appointments

# Import queries
from app.queries import inner_join, left_join, multi_join, high_cost

# Import services
from app.services import analytics, search

bp = Blueprint('main', __name__)

# ==================== HOME / DASHBOARD ====================

@bp.route('/')
@bp.route('/dashboard')
def dashboard():
    """Dashboard with KPIs and charts"""
    try:
        kpis = analytics.get_kpis()
        appointments_data = analytics.get_appointments_per_day(30)
        specialization_data = analytics.get_specialization_distribution()
        recent_activity = analytics.get_recent_activity(10)
        
        return render_template('dashboard.html',
                             kpis=kpis,
                             appointments_data=appointments_data,
                             specialization_data=specialization_data,
                             recent_activity=recent_activity)
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'danger')
        return render_template('dashboard.html', kpis={}, 
                             appointments_data=[], specialization_data=[],
                             recent_activity=[])

# ==================== PATIENTS ====================

@bp.route('/patients')
def list_patients():
    """List all patients"""
    try:
        search_term = request.args.get('search', '')
        patient_list = patients.list_patients(search=search_term if search_term else None)
        return render_template('patients.html', 
                             patients=patient_list,
                             search_term=search_term)
    except Exception as e:
        flash(f'Error loading patients: {str(e)}', 'danger')
        return render_template('patients.html', patients=[], search_term='')

@bp.route('/patients/<int:patient_id>')
def view_patient(patient_id):
    """View single patient details"""
    try:
        patient = patients.get_patient(patient_id)
        if not patient:
            flash('Patient not found', 'warning')
            return redirect(url_for('main.list_patients'))
        
        # Get patient's appointments
        patient_appointments = appointments.list_appointments(
            filters={'patient_id': patient_id}
        )
        
        return render_template('patient_detail.html',
                             patient=patient,
                             appointments=patient_appointments)
    except Exception as e:
        flash(f'Error loading patient: {str(e)}', 'danger')
        return redirect(url_for('main.list_patients'))

@bp.route('/patients/create', methods=['POST'])
def create_patient():
    """Create new patient"""
    try:
        data = {
            'full_name': request.form.get('full_name', '').strip(),
            'gender': request.form.get('gender'),
            'date_of_birth': request.form.get('date_of_birth'),
            'phone_number': request.form.get('phone_number', '').strip(),
            'email': request.form.get('email', '').strip(),
            'address': request.form.get('address', '').strip(),
            'emergency_contact': request.form.get('emergency_contact', '').strip()
        }
        
        patient_id = patients.create_patient(data)
        flash(f'Patient created successfully! ID: {patient_id}', 'success')
        
    except ValueError as e:
        flash(str(e), 'danger')
    except Exception as e:
        flash(f'Error creating patient: {str(e)}', 'danger')
    
    return redirect(url_for('main.list_patients'))

@bp.route('/patients/<int:patient_id>/update', methods=['POST'])
def update_patient(patient_id):
    """Update patient"""
    try:
        data = {
            'full_name': request.form.get('full_name', '').strip(),
            'gender': request.form.get('gender'),
            'date_of_birth': request.form.get('date_of_birth'),
            'phone_number': request.form.get('phone_number', '').strip(),
            'email': request.form.get('email', '').strip(),
            'address': request.form.get('address', '').strip(),
            'emergency_contact': request.form.get('emergency_contact', '').strip()
        }
        
        # Remove empty values
        data = {k: v for k, v in data.items() if v}
        
        rows = patients.update_patient(patient_id, data)
        if rows > 0:
            flash('Patient updated successfully!', 'success')
        else:
            flash('No changes made', 'info')
            
    except ValueError as e:
        flash(str(e), 'danger')
    except Exception as e:
        flash(f'Error updating patient: {str(e)}', 'danger')
    
    return redirect(url_for('main.list_patients'))

@bp.route('/patients/<int:patient_id>/delete', methods=['POST'])
def delete_patient(patient_id):
    """Delete patient"""
    try:
        rows = patients.delete_patient(patient_id)
        if rows > 0:
            flash('Patient deleted successfully!', 'success')
        else:
            flash('Patient not found', 'warning')
            
    except ValueError as e:
        flash(str(e), 'danger')
    except Exception as e:
        flash(f'Error deleting patient: {str(e)}', 'danger')
    
    return redirect(url_for('main.list_patients'))

# ==================== DOCTORS ====================

@bp.route('/doctors')
def list_doctors():
    """List all doctors"""
    try:
        search_term = request.args.get('search', '')
        doctor_list = doctors.list_doctors(search=search_term if search_term else None)
        departments = doctors.list_departments()
        
        return render_template('doctors.html',
                             doctors=doctor_list,
                             departments=departments,
                             search_term=search_term)
    except Exception as e:
        flash(f'Error loading doctors: {str(e)}', 'danger')
        return render_template('doctors.html', doctors=[], departments=[], search_term='')

@bp.route('/doctors/<int:doctor_id>')
def view_doctor(doctor_id):
    """View single doctor details"""
    try:
        doctor = doctors.get_doctor(doctor_id)
        if not doctor:
            flash('Doctor not found', 'warning')
            return redirect(url_for('main.list_doctors'))
        
        # Get doctor's appointments
        doctor_appointments = appointments.list_appointments(
            filters={'doctor_id': doctor_id}
        )
        
        return render_template('doctor_detail.html',
                             doctor=doctor,
                             appointments=doctor_appointments)
    except Exception as e:
        flash(f'Error loading doctor: {str(e)}', 'danger')
        return redirect(url_for('main.list_doctors'))

@bp.route('/doctors/create', methods=['POST'])
def create_doctor():
    """Create new doctor"""
    try:
        data = {
            'full_name': request.form.get('full_name', '').strip(),
            'specialization': request.form.get('specialization', '').strip(),
            'phone_number': request.form.get('phone_number', '').strip(),
            'email': request.form.get('email', '').strip(),
            'department_id': request.form.get('department_id') or None
        }
        
        doctor_id = doctors.create_doctor(data)
        flash(f'Doctor created successfully! ID: {doctor_id}', 'success')
        
    except ValueError as e:
        flash(str(e), 'danger')
    except Exception as e:
        flash(f'Error creating doctor: {str(e)}', 'danger')
    
    return redirect(url_for('main.list_doctors'))

@bp.route('/doctors/<int:doctor_id>/update', methods=['POST'])
def update_doctor(doctor_id):
    """Update doctor"""
    try:
        data = {
            'full_name': request.form.get('full_name', '').strip(),
            'specialization': request.form.get('specialization', '').strip(),
            'phone_number': request.form.get('phone_number', '').strip(),
            'email': request.form.get('email', '').strip(),
            'department_id': request.form.get('department_id') or None
        }
        
        # Remove empty values
        data = {k: v for k, v in data.items() if v}
        
        rows = doctors.update_doctor(doctor_id, data)
        if rows > 0:
            flash('Doctor updated successfully!', 'success')
        else:
            flash('No changes made', 'info')
            
    except ValueError as e:
        flash(str(e), 'danger')
    except Exception as e:
        flash(f'Error updating doctor: {str(e)}', 'danger')
    
    return redirect(url_for('main.list_doctors'))

@bp.route('/doctors/<int:doctor_id>/delete', methods=['POST'])
def delete_doctor(doctor_id):
    """Delete doctor"""
    try:
        rows = doctors.delete_doctor(doctor_id)
        if rows > 0:
            flash('Doctor deleted successfully!', 'success')
        else:
            flash('Doctor not found', 'warning')
            
    except ValueError as e:
        flash(str(e), 'danger')
    except Exception as e:
        flash(f'Error deleting doctor: {str(e)}', 'danger')
    
    return redirect(url_for('main.list_doctors'))

# ==================== APPOINTMENTS (SESSIONS) ====================

@bp.route('/appointments')
@bp.route('/sessions')
def list_appointments():
    """List all appointments/sessions"""
    try:
        # Get filter parameters
        filters = {}
        if request.args.get('doctor_id'):
            filters['doctor_id'] = request.args.get('doctor_id')
        if request.args.get('status'):
            filters['status'] = request.args.get('status')
        if request.args.get('start_date'):
            filters['start_date'] = request.args.get('start_date')
        if request.args.get('end_date'):
            filters['end_date'] = request.args.get('end_date')
        
        appointment_list = appointments.list_appointments(filters=filters if filters else None)
        doctor_list = doctors.list_doctors()
        patient_list = patients.list_patients()
        
        return render_template('appointments.html',
                             appointments=appointment_list,
                             doctors=doctor_list,
                             patients=patient_list,
                             filters=filters)
    except Exception as e:
        flash(f'Error loading appointments: {str(e)}', 'danger')
        return render_template('appointments.html', 
                             appointments=[], doctors=[], patients=[], filters={})

@bp.route('/appointments/create', methods=['POST'])
def create_appointment():
    """Create new appointment"""
    try:
        # Get form data
        appointment_date = request.form.get('appointment_date', '').strip()
        appointment_time = request.form.get('appointment_time', '09:00')
        
        # Combine date and time
        if appointment_date:
            full_datetime = f"{appointment_date} {appointment_time}:00"
        else:
            raise ValueError("Appointment date is required")
        
        data = {
            'patient_id': request.form.get('patient_id'),
            'doctor_id': request.form.get('doctor_id'),
            'appointment_date': full_datetime,
            'reason': request.form.get('reason', '').strip(),
            'status': request.form.get('status', 'Scheduled'),
            'amount_due': request.form.get('amount_due', '').strip()
        }
        
        appointment_id = appointments.create_appointment(data)
        flash(f'Appointment created successfully! ID: {appointment_id}', 'success')
        
    except ValueError as e:
        flash(str(e), 'danger')
    except Exception as e:
        flash(f'Error creating appointment: {str(e)}', 'danger')
    
    return redirect(url_for('main.list_appointments'))

@bp.route('/appointments/<int:appointment_id>/update', methods=['POST'])
def update_appointment(appointment_id):
    """Update appointment"""
    try:
        data = {}
        
        # Handle date/time update
        appointment_date = request.form.get('appointment_date', '').strip()
        appointment_time = request.form.get('appointment_time', '')
        
        if appointment_date:
            if appointment_time:
                data['appointment_date'] = f"{appointment_date} {appointment_time}:00"
            else:
                data['appointment_date'] = f"{appointment_date} 09:00:00"
        
        if request.form.get('patient_id'):
            data['patient_id'] = request.form.get('patient_id')
        if request.form.get('doctor_id'):
            data['doctor_id'] = request.form.get('doctor_id')
        if request.form.get('reason'):
            data['reason'] = request.form.get('reason').strip()
        if request.form.get('status'):
            data['status'] = request.form.get('status')
        
        rows = appointments.update_appointment(appointment_id, data)
        if rows > 0:
            flash('Appointment updated successfully!', 'success')
        else:
            flash('No changes made', 'info')
            
    except ValueError as e:
        flash(str(e), 'danger')
    except Exception as e:
        flash(f'Error updating appointment: {str(e)}', 'danger')
    
    return redirect(url_for('main.list_appointments'))

@bp.route('/appointments/<int:appointment_id>/delete', methods=['POST'])
def delete_appointment(appointment_id):
    """Delete appointment"""
    try:
        rows = appointments.delete_appointment(appointment_id)
        if rows > 0:
            flash('Appointment deleted successfully!', 'success')
        else:
            flash('Appointment not found', 'warning')
            
    except ValueError as e:
        flash(str(e), 'danger')
    except Exception as e:
        flash(f'Error deleting appointment: {str(e)}', 'danger')
    
    return redirect(url_for('main.list_appointments'))

# ==================== REPORTS ====================

@bp.route('/reports')
def reports():
    """Reports page with multiple report types"""
    try:
        report_type = request.args.get('type', 'inner')
        
        if report_type == 'inner':
            data = inner_join.get_patient_treatments()
            summary = inner_join.get_patient_treatments_summary()
            title = "Patient Treatments (Inner Join)"
            description = "Shows all patients with completed treatments and billing"
        elif report_type == 'left':
            data = left_join.get_patients_with_optional_treatments()
            summary = left_join.get_patient_treatment_summary()
            title = "All Patients with Optional Treatments (Left Join)"
            description = "Shows all patients, including those without appointments"
        elif report_type == 'multi':
            data = multi_join.get_patient_doctor_treatments()
            summary = None
            title = "Complete Treatment Records (Multi-table Join)"
            description = "Comprehensive view across patients, doctors, departments, and billing"
        elif report_type == 'high_cost':
            data = high_cost.get_high_cost_treatments()
            summary = high_cost.get_cost_statistics()
            title = "High Cost Treatments"
            description = "Treatment types with above-average costs"
        elif report_type == 'department':
            data = multi_join.get_department_performance()
            summary = None
            title = "Department Performance"
            description = "Analysis of department metrics and revenue"
        else:
            data = []
            summary = None
            title = "Unknown Report"
            description = ""
        
        return render_template('reports.html',
                             report_type=report_type,
                             data=data,
                             summary=summary,
                             title=title,
                             description=description)
    except Exception as e:
        flash(f'Error loading report: {str(e)}', 'danger')
        return render_template('reports.html',
                             report_type='inner',
                             data=[],
                             summary=None,
                             title="Error",
                             description=str(e))

@bp.route('/reports/<report_type>/export')
def export_report(report_type):
    """Export report to CSV"""
    try:
        # Get report data
        if report_type == 'inner':
            data = inner_join.get_patient_treatments()
            filename = 'patient_treatments.csv'
        elif report_type == 'left':
            data = left_join.get_patients_with_optional_treatments()
            filename = 'all_patients_treatments.csv'
        elif report_type == 'multi':
            data = multi_join.get_patient_doctor_treatments()
            filename = 'complete_treatment_records.csv'
        elif report_type == 'high_cost':
            data = high_cost.get_high_cost_treatments()
            filename = 'high_cost_treatments.csv'
        elif report_type == 'department':
            data = multi_join.get_department_performance()
            filename = 'department_performance.csv'
        else:
            flash('Invalid report type', 'danger')
            return redirect(url_for('main.reports'))
        
        if not data:
            flash('No data to export', 'warning')
            return redirect(url_for('main.reports', type=report_type))
        
        # Create CSV in memory
        output = io.StringIO()
        
        # Get headers from first row
        headers = list(data[0].keys())
        writer = csv.DictWriter(output, fieldnames=headers)
        writer.writeheader()
        
        # Write data
        for row in data:
            # Convert datetime objects to strings
            converted_row = {}
            for key, value in row.items():
                if isinstance(value, datetime):
                    converted_row[key] = value.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    converted_row[key] = value
            writer.writerow(converted_row)
        
        # Create response
        output.seek(0)
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename={filename}'}
        )
        
    except Exception as e:
        flash(f'Error exporting report: {str(e)}', 'danger')
        return redirect(url_for('main.reports'))

# ==================== SEARCH ====================

@bp.route('/search')
def search_page():
    """Search and filter page"""
    try:
        # Get search/filter parameters
        query = request.args.get('q', '').strip()
        
        filters = {
            'doctor_id': request.args.get('doctor_id'),
            'start_date': request.args.get('start_date'),
            'end_date': request.args.get('end_date'),
            'min_cost': request.args.get('min_cost'),
            'max_cost': request.args.get('max_cost'),
            'high_cost_only': request.args.get('high_cost_only') == 'on',
            'status': request.args.get('status'),
            'specialization': request.args.get('specialization')
        }
        
        # Remove None values
        filters = {k: v for k, v in filters.items() if v}
        
        # Get results
        if query:
            results = search.global_search(query)
        elif filters:
            results = search.filter_appointments(**filters)
        else:
            results = []
        
        # Get filter options
        filter_options = search.get_filter_options()
        
        return render_template('search.html',
                             query=query,
                             results=results,
                             filters=filters,
                             filter_options=filter_options)
    except Exception as e:
        flash(f'Error performing search: {str(e)}', 'danger')
        return render_template('search.html',
                             query='',
                             results=[],
                             filters={},
                             filter_options={})

# ==================== API ENDPOINTS ====================

@bp.route('/api/kpis')
def api_kpis():
    """API endpoint for KPIs"""
    try:
        kpis = analytics.get_kpis()
        return jsonify(kpis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/appointments-per-day')
def api_appointments_per_day():
    """API endpoint for appointments chart data"""
    try:
        days = request.args.get('days', 30, type=int)
        data = analytics.get_appointments_per_day(days)
        
        # Format for Chart.js
        labels = [row['date'].strftime('%Y-%m-%d') if hasattr(row['date'], 'strftime') 
                 else str(row['date']) for row in data]
        counts = [row['count'] for row in data]
        
        return jsonify({
            'labels': labels,
            'data': counts
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/specialization-distribution')
def api_specialization_distribution():
    """API endpoint for specialization chart data"""
    try:
        data = analytics.get_specialization_distribution()
        
        labels = [row['specialization'] for row in data]
        counts = [row['appointment_count'] for row in data]
        
        return jsonify({
            'labels': labels,
            'data': counts
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== ERROR HANDLERS ====================

@bp.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('404.html'), 404

@bp.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return render_template('500.html'), 500
