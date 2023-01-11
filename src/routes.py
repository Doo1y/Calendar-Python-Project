from flask import (Blueprint, render_template, redirect, url_for)
from datetime import datetime, timedelta
import psycopg2
import os
from src.forms import AppointmentsForm


bp = Blueprint('main', __name__, url_prefix='/')


CONNECTION_PARAMETERS = {
  'user': os.environ.get('DB_USER'),
  'password': os.environ.get('DB_PASS'),
  'dbname': os.environ.get('DB_NAME'),
  'host': os.environ.get('DB_HOST')
}

@bp.route('/', methods=['GET', 'POST'])
def main():
  d = datetime.now()
  url = url_for('.daily', year=d.year, month=d.month, day=d.day)
  return redirect(url)


@bp.route('/<int:year>/<int:month>/<int:day>', methods=['GET, POST'])
def daily(year, month, day):
  form = AppointmentsForm()
  if form.validate_on_submit():
    with psycopg2.connect(**CONNECTION_PARAMETERS) as conn:
      with conn.cursor() as cur:
        params = {
          'name': form.name.data,
          'start_datetime': datetime.combine(form.start_date.data, form.start_time.data),
          'end_datetime': datetime.combine(form.end_date.data, form.end_time.data),
          'description': form.description.data,
          'private': form.private.data
        }
        cur.execute('''
          INSERT INTO appointments (name, start_datetime, end_datetime, description, private)
          VALUES
            (%(name)s, %(start_datetime)s, %(end_datetime)s, %(description)s, %(private)s);
          ''', params)
  with psycopg2.connect(**CONNECTION_PARAMETERS) as conn:
    with conn.cursor() as cur:
      day = datetime(year, month, day)
      next_day = day + timedelta(days=1)
      cur.execute('''
        SELECT id, name, start_datetime, end_datetime 
        FROM
          appointments
        WHERE start_datetime BETWEEN %(day)s AND %(next_day)s
        ORDER BY
          start_datetime;
      ''', { 'day': day, 'next_day': next_day })
      rows = cur.fetchall()
      return render_template('index.html', rows=rows, form=form)