from flask import Flask, jsonify
from sqlHelper import SQLHelper

import pandas as pd
import numpy as np
import datetime as dt

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text, func

import datetime as dt
import sqlalchemy
import pandas as pd
import numpy as np

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
sql = SQLHelper()

#################################################
# Flask Routes
#################################################
    
 # Define Flask routes:
@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii's Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2016-08-23<br/>"
        f"/api/v1.0/2016-08-23/2016-12-31"
    )
#################################################
# Flask Routes
#################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    data = sql.get_last_12_months_precipitation()
    return jsonify(data)

@app.route("/api/v1.0/stations")
def stations():
    data = sql.get_stations()
    return jsonify(data)

@app.route("/api/v1.0/tobs")
def tobs():
    data = sql.get_tobs_most_active_station()
    return jsonify(data)

@app.route("/api/v1.0/<start>")
def temp_stats_start(start):
    data = sql.get_temp_stats(start)
    return jsonify(data)

@app.route("/api/v1.0/<start>/<end>")
def temp_stats_start_end(start, end):
    data = sql.get_temp_stats(start, end)
    return jsonify(data)

# Run the App
if __name__ == '__main__':
    app.run(debug=True)
