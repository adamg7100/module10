# Import the dependencies.
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
Base=automap_base()
Base.prepare(engine, reflect=True)
measurement = Base.classes.measurement
station = Base.classes.station

# reflect an existing database into a new model

# reflect the tables


# Save references to each table


# Create our session (link) from Python to the DB


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
    values = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date > '2016-08-22').\
    order_by(measurement.date).all()
    session.close()
    result={date:prcp for date,prcp in values}
    return jsonify(result)
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    active_stations = session.query(measurement.station,func.count(measurement.station)).\
    order_by(func.count(measurement.station).desc()).\
    group_by(measurement.station).all() 
    session.close()
    all_stations = list(np.ravel(active_stations))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session (engine)
    twelve_month_values = session.query(measurement.date,measurement.tobs).\
    filter(measurement.station == most_active_station_number).\
    filter(measurement.date > '2016-08-17').all()
    session.close()
    all_tobs = list(np.ravel(twelve_month_values))
    return jsonify(twelve_month_values)

@app.route("/api/v1.0/<start>")
def start_day(start):
    session = Session(engine)
    query_ = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    start_list=list(np.ravel(query_))
    session.close()
    return jsonify(start_list)
    
@app.route("/api/v1.0/<start>/<end>")
def start_end_day(start,end):
    session = Session(engine)
    query_ = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start,Measurement.date<= end).all()
    start_list=list(np.ravel(query_))
    session.close()
    return jsonify(start_list)        
if __name__ == '__main__':
    app.run(debug=True)