
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, distinct

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite") 

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
#Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__) 

@app.route("/")
def welcome():
   return (
       f"Welcome to the Hawaii Climate Analysis API!<br/>"
       f"Available Routes:<br/>"
       f"/api/v1.0/precipitation<br/>"
       f"/api/v1.0/stations<br/>"
       f"/api/v1.0/tobs<br/>"
       f"/api/v1.0/<start_date><br/>"
       f"/api/v1.0/<start_date>/<end_date><br/>"
   )
@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()

        # Convert object to a list
    prcp_list={}
    for item in results:
        prcp_list[results[0]]=results[1]     
    
    # Return jsonified list
    return (jsonify(prcp_list))

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station)

        # Convert object to a list
    station_list=[]
    for sublist in stations:
        for item in sublist:
            station_list.append(item)
    
    # Return jsonified list
    return (jsonify(station_list))   

@app.route("/api/v1.0/tobs")
def tobs():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results_2 = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= prev_year).all()

        # Convert object to a list
    tobs_list=[]
    for sublist in results_2: 
        for item in sublist:
            tobs_list.append(item)
    
    # Return jsonified list
    return (jsonify(tobs_list))

@app.route("/api/v1.0/<start_date>")
@app.route("/api/v1.0/<start_date>/<end_date>") 
def start_end(start_date=None, end_date=None):
    """Return a list of min, avg, max for specific dates"""
    selections = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end_date:
        results= session.query(*selections).filter(Measurement.date >= start_date).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    
    results = session.query(*selections).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    temps_2 = list(np.ravel(results))
    return jsonify(temps_2)


if __name__ == "__main__":
    app.run(debug=True)       


