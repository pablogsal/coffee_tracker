from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/pablogsal/webapps/coffee_tracker/htdocs/coffee.db'
db = SQLAlchemy(app)


class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    count = db.Column(db.Integer)

    def __init__(self):
        self.count = 0

@app.route("/del_coffee/")
def del_coffee():
    last = Visit.query.order_by(Visit.id.desc()).first()
    db.session.delete(last)
    db.session.commit()
    return jsonify(time=last.time,counter=last.count - 1)

@app.route("/add_coffee/")
def add_coffee():
    last = Visit.query.order_by(Visit.id.desc()).first()
    new = Visit()
    if not last:
        last = new
    print(last.count)
    new.time = datetime.datetime.now()
    new.count += last.count + 1
    db.session.add(new)
    db.session.commit()
    return jsonify(time=new.time,counter=new.count)

@app.route("/get_coffee/")
def get_coffee():
    coffee_rows = Visit.query.order_by(Visit.id.desc()).limit(5)
    coffee_list = {coffee.id:{'time':coffee.time.strftime('%Y-%m-%dT%H:%M:%S'),'count':coffee.count} for coffee in coffee_rows}
    return jsonify(coffee_list)


@app.route("/")
def hello():
    coffee_list= Visit.query.order_by(Visit.id.desc()).limit(5)
    return render_template('coffee.html',coffees = coffee_list)
