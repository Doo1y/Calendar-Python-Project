from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, DateField, TimeField
from wtforms.widgets import DateInput, TimeInput
from wtforms.validators import DataRequired, ValidationError


class AppointmentsForm(FlaskForm):
  name = StringField('Name', validators=[DataRequired()])
  start_date = DateField('Start Date', widget=DateInput(), validators=[DataRequired()])
  start_time = TimeField('Start Time', widget=TimeInput(), validators=[DataRequired()])
  end_date = DateField('End Date', widget=DateInput(), validators=[DataRequired()])
  end_time = TimeField('End Time', widget=TimeInput(), validators=[DataRequired()])
  description = TextAreaField('Description', validators=[DataRequired()])
  private = BooleanField('Private')
  submit = SubmitField()

  def validate_end_date(form, field):
    start = datetime.combine(form.start_date.data, form.start_time.data)
    end = datetime.combine(field.data, form.end_time.data)
    if start >= end:
      msg = "End date/time must come after start date/time"
      raise ValidationError(msg)
