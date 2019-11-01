from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, desc
import numpy as np
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")
conn = engine.connect()

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

##########################################################################################################
# Flask Setup
###########################################################################################################
app = Flask(__name__)
############################################################################################################
@app.route("/")
def welcome():
     return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
      )
############################################################################################################
@app.route("/api/v1.0/precipitation")
def precipitation():


    
    date_max_mnth = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    max_date = dt.datetime.strptime(date_max_mnth, "%Y-%m-%d")
    year_diff = max_date - dt.timedelta(days=365)
    rain = session.query(Measurement.date, Measurement.prcp).\
       filter(Measurement.date >year_diff).\
       order_by(Measurement.date).all()
 

#using source from github for dictionary to make a dictionary
#https://github.com/davidwjones/AdvancedDataHomework/blob/master/app.py


    rain_totals = []
    for result in rain:
        row = {}
        row["date"] = rain[0]
        row["prcp"] = rain[1]
        rain_totals.append(row)

    return jsonify(rain_totals)

###########################################################################################################
#Leveraging code to use .bind  https://docs.sqlalchemy.org/en/13/orm/session_api.html:  
#bind � An optional Engine or Connection to which this Session should be bound. 
#When specified, all SQL operations performed by this session will execute via this connectable
#Will see if this is a better way to bind?

@app.route("/api/v1.0/stations")
def stations():
    stations_query = session.query(Station.name, Station.station)
    stations = pd.read_sql(stations_query.statement, stations_query.session.bind)
    return jsonify(stations.to_dict())

##############################################################################################################

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temperatures for prior year"""
    date_max_mnth = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    max_date = dt.datetime.strptime(date_max_mnth, "%Y-%m-%d")
    year_diff = max_date - dt.timedelta(days=365)
    temp = session.query(Measurement.date, Measurement.tobs).\
       filter(Measurement.date >year_diff).\
       order_by(Measurement.date).all() 



    temp_totals = []
    for result in temp:
         row = {}
         row["date"] = temp[0]
         row["tobs"] = temp[1]
         temp_totals.append(row)

    return jsonify(temp_totals)


####################################################################################################################
#Source is class activity: SMU-DAL-DATA-PT-08-2019-U-C\01-Lesson-Plans\10-Advanced-Data-Storage-and-Retrieval\3\Activities\08-Ins_Variable_Rule\Solved.

@app.route("/api/v1.0/<start>")
def temp_obs_date(startdate):
       
    """Return a JSON list of tmin, tmax, tavg for the dates in range of start date and end date"""
    
    return jsonify(session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= startdate).all())


@app.route("/api/v1.0/<start>/<end>")
def temp_obs_range(startdate, enddate):
    
    return jsonify(session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= startdate).filter(Measurement.date <= enddate).all())


if __name__ == "__main__":
    app.run(debug=True)





