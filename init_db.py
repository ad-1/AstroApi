# init ADAPI database

import json
from app import Body
from app import db

db.create_all()
print('database created...')

data = {
    "name": "Earth",
    "gravity": 9.81,
    "mass": 5.972e+24,
    "radius": 6378,
    "sidereal_rotation_period": 23.9345,
    "inclination_of_equator_to_orbit_plane": 177.4,
    "semimajor_axis": 149.6e6,
    "eccentricity": 0.0167,
    "inclination_orbit_to_ecliptic_plane": 0,
    "orbit_sidereal_period" : 8766.144,
    "gravitational_parameter": 398600,
    "sphere_of_influence": 925000,
}

# data = {
#     "name": "Mercury",
#     "gravity": 3.7,
#     "mass": 330.2e21,
#     "radius": 2240,
#     "sidereal_rotation_period": 1407.6,
#     "inclination_of_equator_to_orbit_plane": 0.01,
#     "semimajor_axis": 57.91e6,
#     "eccentricity": 0.2056,
#     "inclination_orbit_to_ecliptic_plane": 7.0,
#     "orbit_sidereal_period" : 2111.28,
#     "gravitational_parameter": 22030,
#     "sphere_of_influence": 112000
# }

body = Body(data)

print('sample data...\n')
print(json.dumps(data, indent=4, sort_keys=True))
print('\nmodel created')

db.session.add(body)
print('data added')

db.session.commit()
print('session commit\n...finished\n')
