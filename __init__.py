
from flask import Flask, request, flash, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify
import requests
# from . import db, list

#
app = Flask(__name__)
db = SQLAlchemy()


class info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    reponame = db.Column(db.String(100))


def create_app(test_config=None):

    global app,db

    POSTGRES = {
        'user': 'areeb_dev',
        'pw': 'pass',
        'db': 'areeb_dev',
        'host': 'localhost',
        'port': '5432',
    }

    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
    %(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    db.init_app(app)
    app.config['SECRET_KEY'] = "secret"

    @app.route("/hello")
    def main():
        return 'Hello World !'

    @app.route('/')
    def show_all():
        return render_template('index.html', posts=info.query.all())

    @app.route('/new', methods=['GET', 'POST'])
    def new():

        if request.method == 'POST':
            u = info(username=request.form['name'], reponame=request.form['repo'])

            db.session.add(u)
            db.session.commit()

            flash('Record was successfully added')
            return redirect(url_for('show_all'))

        return render_template('new.html')

    @app.route('/repo/<name>', methods=['GET'])
    def detail(name):

        if request.method == 'GET':
            return render_template('detail.html', rows=info.query.filter_by(username=name))

