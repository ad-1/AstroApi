import os
from forms import CelestialDataForm
from flask import Flask, url_for, render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqllite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '71fc8da29cac1c1abbe3e08ba0d4f4c4'

# init db
db = SQLAlchemy(app)

objects = [
    {
        'object': 'sun',
        'radius': 696000,
        'mass': 1.989e30
    },
    {
        'object': 'mercury',
        'radius': 2440,
        'mass': 330.2e21
    }
]


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    return render_template('index.html', objects=objects)


@app.route('/addobject', methods=['GET', 'POST'])
def addobject():
    form = CelestialDataForm()
    if form.validate_on_submit():
        flash('Data added for {}!'.format(form.object.data), 'success')
        return redirect(url_for('home'))
    return render_template('addobject.html', form=form)


# run server
if __name__ == '__main__':
    app.run(debug=True)
