import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return  (   
    
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end")

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
   
    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Measurement).all()
    all_results = []
    
    for precipitation in results:
        results_dict = {}
        results_dict["date"] = precipitation.date
        results_dict["percipitation"] = precipitation.prcp
        all_results.append(results_dict)
    return jsonify(all_results)

    
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    
    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(station).all()



    # Create a dictionary from the row data and append to a list of all_passengers
    all_stations = []
    for sta in results:
        results_dict = {}
        results_dict["station"] = sta.station
        all_stations.append(results_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    results=session.query(Measurement.date,Measurement.tobs).filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()
# create a dictionary for dates and temperature observations from a year from the last data point
    all_data = []
    for tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = tobs.date
        tobs_dict["tobs"]=tobs.tobs
        all_data.append(tobs_dict)
    return jsonify(all_data)

    

if __name__ == '__main__':
    app.run(debug=True)
