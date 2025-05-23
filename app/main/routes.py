from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from app.models import FuelRecord
from app import db
from app.main import bp
from app.main.forms import FuelRecordForm
from werkzeug.utils import secure_filename
import os

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    recent_records = FuelRecord.query.filter_by(user_id=current_user.id).order_by(FuelRecord.date.desc()).limit(5).all()
    return render_template('main/dashboard.html', title='Home', recent_records=recent_records)

@bp.route('/dashboard')
@login_required
def dashboard():
    recent_records = FuelRecord.query.filter_by(user_id=current_user.id).order_by(FuelRecord.date.desc()).limit(5).all()
    return render_template('main/dashboard.html', title='Dashboard', recent_records=recent_records)

@bp.route('/fuel/new', methods=['GET', 'POST'])
@login_required
def new_fuel_record():
    form = FuelRecordForm()
    if form.validate_on_submit():
        record = FuelRecord(
            guide_number=form.guide_number.data,
            license_plate=form.license_plate.data,
            service_station=form.service_station.data,
            supply=form.supply.data,
            kilometers=form.kilometers.data,
            consumption=form.consumption.data,
            user_id=current_user.id
        )
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            record.image_filename = filename
        db.session.add(record)
        db.session.commit()
        flash('Registro de combustible guardado exitosamente')
        return redirect(url_for('main.dashboard'))
    return render_template('main/add_record.html', title='Nuevo Registro', form=form)

@bp.route('/fuel/history')
@login_required
def fuel_history():
    page = request.args.get('page', 1, type=int)
    records = FuelRecord.query.filter_by(user_id=current_user.id).order_by(FuelRecord.date.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('main/list_record.html', title='Historial', records=records)

@bp.route('/fuel/summary')
@login_required
def fuel_summary():
    records = FuelRecord.query.filter_by(user_id=current_user.id).all()
    monthly_data = {}
    for record in records:
        month = record.date.strftime('%Y-%m')
        if month not in monthly_data:
            monthly_data[month] = record.monthly_summary()
    return render_template('main/monthly_report.html', title='Resumen Mensual', monthly_data=monthly_data)

@bp.route('/fuel/delete/<int:id>', methods=['POST'])
@login_required
def delete_record(id):
    record = FuelRecord.query.get_or_404(id)
    if record.user_id != current_user.id and not current_user.is_admin:
        flash('No tienes permiso para eliminar este registro', 'danger')
        return redirect(url_for('main.fuel_history'))
    
    # Eliminar la imagen si existe
    if record.image_filename:
        try:
            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], record.image_filename))
        except OSError:
            pass  # Ignorar si el archivo no existe
    
    db.session.delete(record)
    db.session.commit()
    flash('Registro eliminado exitosamente', 'success')
    return redirect(url_for('main.fuel_history')) 