from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location on Google Maps(URL)', validators=[DataRequired(), URL(message="Please enter a valid URL.")])
    open_time = StringField('Opening Time e.g.8AM', validators=[DataRequired()])
    close = StringField('Opening Time e.g.5:30PM', validators=[DataRequired()])
    rating_options = [("☕️", "☕️"), ("☕️☕️", "☕️☕️"), ("☕️☕️☕️", "☕️☕️☕️"), ("☕️☕️☕️☕️", "☕️☕️☕️☕️"), ("☕️☕️☕️☕️☕️", "☕️☕️☕️☕️☕️")]
    rating = SelectField('Coffee Rating', choices=rating_options, validators=[DataRequired()])
    wifi_options = [("❌", "❌"), ("💪", "💪"), ("💪💪", "💪💪"), ("💪💪💪", "💪💪💪"), ("💪💪💪💪", "💪💪💪💪"), ("💪💪💪💪💪", "💪💪💪💪💪")]
    wifi = SelectField('Wifi Strength Rating', choices=wifi_options, validators=[DataRequired()])
    power_options = [("❌", "❌"), ("🔌", "🔌"), ("🔌🔌", "🔌🔌"), ("🔌🔌🔌", "🔌🔌🔌"), ("🔌🔌🔌🔌", "🔌🔌🔌🔌"), ("🔌🔌🔌🔌🔌", "🔌🔌🔌🔌🔌")]
    power = SelectField('Power Socket Availability', choices=power_options , validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        cafe = form.cafe.data
        location = form.location.data
        open_time = form.open_time.data
        close = form.close.data
        rating = form.rating.data
        wifi = form.wifi.data
        power = form.power.data
        with open("cafe-data.csv", "a", newline='') as new_cafe:
            new_cafe.write(f"\n{cafe},{location},{open_time},{close},{rating},"
                           f"{wifi},{power}")
    return render_template('add.html', form=form)

@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)

if __name__ == '__main__':
    app.run(debug=True)
