from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, FloatField, SelectField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_wtf.file import FileAllowed
from app.models import User

class FuelRecordForm(FlaskForm):
    date = DateField('Fecha', validators=[DataRequired()])
    guide_number = StringField('Número de Guía', validators=[DataRequired()])
    license_plate = StringField('Patente', validators=[DataRequired()])
    service_station = StringField('Estación de Servicio', validators=[DataRequired()])
    supply = SelectField('Suministro', choices=[
        ('DIESEL', 'DIESEL'), 
        ('BLUEMAX', 'BLUEMAX')], 
        validators=[DataRequired()])
    kilometers = IntegerField('Kilómetros', validators=[DataRequired()])
    consumption = FloatField('Consumo (Lt)', validators=[DataRequired()])
    image = FileField('Imagen de la Guía', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Solo imágenes permitidas')])