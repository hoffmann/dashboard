from flask import Flask, request, jsonify, url_for, redirect
from dashboard.database import db_session
from dashboard.models import Monitor
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session().remove()



@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/')
def api_index():
    return 'Hello World!'


@app.route('/api/monitor/', methods=["GET", "POST"])
def api_monitor_index():
    session = db_session()
    if request.method == "GET":
        monitors = [{"id":m.id, "name":m.name, "url": m.url, "interval": m.interval} for m in session.query(Monitor)] 
        return jsonify(monitors=monitors)

    else:
        data = request.json
        monitor = Monitor(name=data["name"], url=data["url"], interval=data["interval"])
        session.add(monitor)
        session.commit()

        return redirect(url_for("api_monitor", id=monitor.id))



@app.route('/api/monitor/<id>', methods=["GET", "POST", "DELETE"])
def api_monitor(id):
    return jsonify(data="ok")


