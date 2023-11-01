# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

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

# reflect an existing database into a new model

# reflect the tables


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
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


    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    # query results from your precipitation analysis
    last_twelve=dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    results = session.query(Measurement.date, func.avg(Measurement.prcp)).\
        filter(Measurement.date >= last_twelve).\
        group_by(Measurement.date).all()
    # put into dictionary

    percp_dict = []
    for date, percipitation in results:
        year_percp = {}
        year_percp["date"] = date
        year_percp["percipiation"] = percipitation
        percp_dict.append(year_percp)

    return jsonify(percp_dict)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    # query stations
    results = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).all()

    stations_list = list(np.ravel(results))

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    year_data=dt.date(2017, 8, 18) - dt.timedelta(days=365)


    results =session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= year_data).all()
    

    tobs_list = list(np.ravel(results))
    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
def start(start=None):
    start=dt.datetime.strptime(start,'%m%d%Y')
    session = Session(engine)
    results =session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs).\
              filter(Measurement.date == start)).all()
    results=list(np.ravel(results))
    
    return jsonify(results)

    
@app.route("/api/v1.0/start/end")
def startDateendDate(start=None, end=None):
    start=dt.datetime.strptime(start,'%m%d%Y')
    end=dt.datetime.strptime(end,'%m%d%Y')
    session = Session(engine)
    results =session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs).\
              filter(Measurement.date >= start).\
              filter(Measurement.date <= end)).all()
    results=list(np.ravel(results))
    session = Session(engine)


if __name__ == '__main__':
    app.run(debug=True)
