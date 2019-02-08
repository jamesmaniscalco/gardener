import os, numpy

from flask import Flask, render_template
from werkzeug.contrib.fixers import ProxyFix

from . import db


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')    # global configuration
    app.config.from_pyfile('config.py', silent=True)    # instance-specific configuration

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def home():
        # get the last hour of data
        from . import db
        d = db.get_db()
        sensors = d.execute('select * from sensors').fetchall()
        time_data = []
        moisture_data = []
        sensor_names = []
        for sensor in sensors:
            db_output = d.execute("select datetime(timestamp, 'localtime'), voltage from readings where sensor_id={} and timestamp > datetime('now', '-5 day')".format(sensor[0])).fetchall()
            raw_data = numpy.array(db_output).transpose()
            # limit to 100 lines or fewer
            if len(raw_data[0]) > 1000:
                idx = numpy.round(numpy.linspace(0, len(raw_data[0]) - 1, 100)).astype(int)
            else:
                idx = numpy.arange(len(raw_data[0]))
            time_data.append(raw_data[0,idx].tolist())
            # moisture = (voltage - low_limit)/(high_limit - low_limit)
            m = (numpy.array([float(mm) for mm in raw_data[1,idx]]) - sensor[3]) / (sensor[2] - sensor[3]) * 100  # convert to percentage
            moisture_data.append(m.tolist())
            sensor_names.append('sensor {}'.format(sensor[0]))
        return render_template("home.html", time_data=time_data, moisture_data=moisture_data, sensor_names=sensor_names)

    # WSGI setup
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # database connections
#    from . import db
    db.init_app(app)

    return app

    
