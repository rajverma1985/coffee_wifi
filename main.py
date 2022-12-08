from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms_components import TimeField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

ratings = ["☕️", "💪", "✘", "🔌"]


def rate():
    rating_list = []
    for n in ratings:
        icons = []
        for i in range(1, 6):
            icons.append(n * i)
        rating_list.append(icons)
    return rating_list


rating = rate()


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    cafe_location_on_google_maps = StringField('Cafe Location On Google Maps', validators=[DataRequired(), URL()])
    opening_time = TimeField("Opening Time", validators=[DataRequired()])
    closing_time = TimeField("Closing Time", validators=[DataRequired()])
    coffee_rating = SelectField(choices=rating[0])
    wifi_strength_rating = SelectField(choices=rating[1])
    power_socket_availability = SelectField(choices=rating[3])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open("cafe-data.csv", mode="a") as data:
            data.write(f"\n{form.cafe.data},"
                       f"{form.cafe_location_on_google_maps.data},"
                       f"{form.opening_time.data},"
                       f"{form.closing_time.data},"
                       f"{form.coffee_rating.data},"
                       f"{form.wifi_strength_rating.data},"
                       f"{form.power_socket_availability.data}")
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
