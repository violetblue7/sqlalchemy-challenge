from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text, func

import datetime as dt
import sqlalchemy
import pandas as pd
import numpy as np


# Note this Class is created to separate out any Database logic
class SQLHelper():
    #################################################
    # Database Setup
    #################################################
    def __init__(self):
        self.engine = create_engine("sqlite:///hawaii.sqlite")
        self.Base = None
        self.init_base()

    def init_base(self):
        self.Base = automap_base()
        self.Base.prepare(self.engine, reflect=True)  # all tables are reflected

    #################################################
    # Database Queries
    #################################################

    def get_last_12_months_precipitation(self):
        Measurement = self.Base.classes.measurement
        session = Session(self.engine)

        # Calculate the date one year ago from '2017-08-23'
        start_date = dt.date(2016, 8, 23)
        twelve_months_ago = start_date + pd.DateOffset(months=12)

        # Query precipitation data for the last 12 months
        results = session.query(Measurement.date, Measurement.prcp)\
                         .filter(Measurement.date >= start_date).all()
        session.close()

        precipitation_dict = {date: prcp for date, prcp in results}
        return precipitation_dict

    def get_stations(self):
        Station = self.Base.classes.station
        session = Session(self.engine)

        results = session.query(Station.station).all()
        session.close()

        stations_list = [station for station, in results]
        return stations_list

    def get_tobs_most_active_station(self):
        Measurement = self.Base.classes.measurement
        session = Session(self.engine)

        most_active_station = session.query(Measurement.station)\
                                     .group_by(Measurement.station)\
                                     .order_by(func.count(Measurement.station).desc()).first()[0]

        # Calculate the date one year ago from '2017-08-23'
        start_date = dt.date(2016, 8, 23)
        prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

        results = session.query(Measurement.date, Measurement.tobs)\
                         .filter(Measurement.station == most_active_station)\
                         .filter(Measurement.date >= prev_year).all()

        session.close()

        tobs_list = [(date, tobs) for date, tobs in results]
        return tobs_list

    def get_temp_stats(self, start_date, end_date=None):
        Measurement = self.Base.classes.measurement
        session = Session(self.engine)

        if end_date:
            results = session.query(
                func.min(Measurement.tobs),
                func.avg(Measurement.tobs),
                func.max(Measurement.tobs)
            ).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
        else:
            results = session.query(
                func.min(Measurement.tobs),
                func.avg(Measurement.tobs),
                func.max(Measurement.tobs)
            ).filter(Measurement.date >= start_date).all()

        session.close()

        temp_stats = results[0]
        return {"TMIN": temp_stats[0], "TAVG": temp_stats[1], "TMAX": temp_stats[2]}
