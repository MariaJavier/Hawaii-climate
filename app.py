# connect to a database using sqlalchemy
# use jupyter notebook for an analysis
# python can extract data, analyze and display output onto a dashboard or online

# import Flask
from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import pandas as pd
import numpy as np

engine = create_engine('sqlite:///../resources/hawaii.sqlite')


Base = automap_base()
Base.prepare(engine=engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(bind=engine)


#################################################
# Flask Setup
#################################################

# app runs the command to do the rendering
app = Flask(__name__)


#################################################
# Flask Routes
#################################################


@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Welcome to the Hawaii Vacation Analysis and Planning Site.<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        F"/api/v1.0/<start><br/>"
        f"/api/v1.0/<end><br/>"
    )
    
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'Precipitation' page...")
    return 
        f"Precipitation"

        results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-01', Measurement.date <= '2017-08-31').all()
        dictionary = pd.DataFrame(results).set_index('date').rename(columns={'prcp': 'precipitation'}).to_dict()

    return jsonify(dictionary)
    

@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'Station' page...")
    return "Station"
    results = list(np.ravel(session.quer(Station.station).all()))
    return jsonify(results)
    

@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'tobs' page...")
    return "tobs"
    
    # jsonify list of Temp Observations (tobs) for the previous year.
    
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23', Measurement.date <= '2017-08-23').all()
    tobs_dict = pd.DataFrame(results).set_index('date').rename(columns={'tobs': 'temperature_observations'})
    tobs_dict.temperature_observations = tobs_dict.temperature_observations.astype(float)
    tobs_dict = tobs_dict.to_dict()

    return jsonify(tobs_dict)

@app.route("/api/v1.0/<start>")
def start():
    print("Server received request for 'Start' page...")
    return "start date"

@app.route("/api/v1.0/<end>")
def end():
    print("Server received request for 'End' page...")
    return "end date"

    # Return a JSON list of the min, avg, max temp for a given start or start-end range.
    # When given start only, calc `TMIN`, `TAVG`, & `TMAX` for all dates >= to start date.
    # When given start & end date, calc the `TMIN`, `TAVG`, & `TMAX` for dates btwn start & end date inclusive.

    def temps(start, end='2017-08-23'):
        temp_by_date = session.query(Measurement.tobs).filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
        temp_by_date = np.ravel(temp_by_date)

        minimum = np.min(temp_by_date)
        average = np.average(temp_by_date)
        maximum = np.max(temp_by_date)
        return minimum, average, maximum

    minimum, average, maximum = calc_temps(start, end)
    dic = {"temp_min": minimum.astype(float), "temp_average": average.astype(float),"temp_max": maximum.astype(float)}
    return jsonify(dic)
    


if __name__ == "__main__":
    app.run(debug=True)