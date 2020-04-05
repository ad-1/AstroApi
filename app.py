import os
from forms import CelestialDataForm
from flask import Flask, url_for, render_template, flash, redirect, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '71fc8da29cac1c1abbe3e08ba0d4f4c4'

# init db
db = SQLAlchemy(app)

# init ma
ma = Marshmallow(app)


# celestial body database model
class Body(db.Model):
    """ Celestial body database model """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    radius = db.Column(db.Integer, unique=False, nullable=False)
    mass = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return 'Body({})'.format(self.name)


# celestial body marshmallow schema
class BodySchema(ma.Schema):
    class Meta:
        fields = ('name', 'radius', 'mass') # model = Body


body_schema = BodySchema()

# home page route
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    bodies = Body.query.all()
    return render_template('index.html', bodies=bodies)

# add a new body
@app.route('/add_body', methods=['GET', 'POST'])
def add_body():
    form = CelestialDataForm()
    if form.validate_on_submit():
        body = Body(name=form.name.data, radius=form.radius.data, mass=form.mass.data)
        flash('Data added for {}!'.format(form.name.data), 'success')
        db.session.add(body)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_body.html', form=form)

# get all bodies
@app.route('/bodies', methods=['GET'])
def get_bodies():
    body = Body.query.all()
    body_schemas = BodySchema(many=True)
    output = body_schemas.dump(body)
    return jsonify(output)

# get single body
@app.route('/body/<int:id>')
def body(id):
    body = Body.query.get_or_404(id)
    return body_schema.jsonify(body)

# update body
@app.route('/update/<int:id>', methods=['PUT'])
def update(id):
    body = Body.query.get_or_404(id)
    name = request.json['name']
    mass = request.json['mass']
    radius = request.json['radius']
    body.name = name
    body.mass = mass
    body.radius = radius
    db.session.commit()
    return body_schema.jsonify(body)

# delete body
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    body = Body.query.get_or_404(id)
    db.session.delete(body)
    db.session.commit()
    return body_schema.jsonify(body)

# run server
if __name__ == '__main__':
    app.run(debug=True)
