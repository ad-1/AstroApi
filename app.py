import os
import json
from collections import namedtuple
from forms import CelestialDataForm
from flask import Flask, url_for, render_template, flash, redirect, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '71fc8da29cac1c1abbe3e08ba0d4f4c4'

# init db
db = SQLAlchemy(app)

# init ma
ma = Marshmallow(app)


# celestial body database model
class Body(db.Model):
    name = db.Column(db.String(20), primary_key=True, unique=True, nullable=False)
    radius = db.Column(db.Integer, unique=False)
    mass = db.Column(db.Integer, unique=False)
    sidereal_rotation_period = db.Column(db.Integer)
    inclination_of_equator_to_orbit_plane = db.Float(db.Integer)
    semimajor_axis = db.Column(db.Integer)
    eccentricity = db.Column(db.Float)
    inclination_orbit_to_ecliptic_plane = db.Column(db.Float)
    orbit_sidereal_period = db.Column(db.Float)
    gravitational_parameter = db.Column(db.Integer)
    sphere_of_influence = db.Column(db.Integer)

    def __init__(self, dict):
        # allows model to be initialised with json schema matching parameters
        vars(self).update(dict)

    def __repr__(self):
        return 'Body({})'.format(self.name)


# celestial body marshmallow schema
class BodySchema(ma.ModelSchema):
    class Meta:
        model = Body


body_schema = BodySchema()

# home page route
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    bodies = Body.query.all()
    return render_template('index.html', bodies=bodies)

# api docs
@app.route('/docs', methods=['GET'])
def docs():
    return render_template('docs.html')

# add a new body
@app.route('/add', methods=['GET', 'POST'])
def add():
    form = CelestialDataForm()
    if form.validate_on_submit():
        body = json.loads(form.body.data, object_hook=Body)
        db.session.add(body)
        db.session.commit()
        flash('Data added for {}!'.format(body.name), 'success')
        return redirect(url_for('home'))
    return render_template('add.html', form=form)

# get all bodies
@app.route('/bodies', methods=['GET'])
def bodies():
    body = Body.query.all()
    body_schemas = BodySchema(many=True)
    output = body_schemas.dump(body)
    return jsonify(output)

# get single body
@app.route('/body/<string:name>')
def body(name):
    body = Body.query.get_or_404(name)
    return body_schema.jsonify(body)

# update body
@app.route('/update/<string:name>', methods=['PUT'])
def update(name):
    body = Body.query.get_or_404(name)
    body_updated = json.loads(request.data, object_hook=Body)
    body.gravity = body_updated.gravity
    flash('Data updated for {}!'.format(body.name), 'success')
    db.session.commit()
    return body_schema.jsonify(body)

# delete body
@app.route('/delete/<string:name>', methods=['DELETE'])
def delete(name):
    body = Body.query.get_or_404(name)
    db.session.delete(body)
    db.session.commit()
    return body_schema.jsonify(body)

# calculate weight on body
@app.route('/weight_for_mass_<int:mass>_on_<string:name>', methods=['GET'])
def weight_on(mass, name):
    body = Body.query.filter_by(name=name).first()
    weight = mass * body.gravity
    return jsonify({'weight': weight})

# serve static js file
@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

# run server
if __name__ == '__main__':
    app.run(debug=True)
