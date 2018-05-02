
from flask import Flask, request, flash, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify
import requests
from . import db, list


def create_app(test_config=None):

    app = Flask(__name__,instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    db = SQLAlchemy(app)

    class info(db.Model):
        id = db.Column('id', db.Integer, primary_key=True)
        username = db.Column(db.String(100))
        reponame = db.Column(db.String(100))

        def __init__(self, name, repo):
            self.username = name
            self.reponame = repo

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    app.register_blueprint(list.bp)
    app.add_url_rule('/', endpoint='index')

    db.create_all()

    return app


@app.route('/')
def show_all():
   return render_template('list/index.html', posts = info.query.all() )


@app.route('/new', methods=['GET', 'POST'])
def new():

    if request.method == 'POST':

        u = info(request.form['name'], request.form['repo'])

        db.session.add(u)
        db.session.commit()

        flash('Record was successfully added')
        return redirect(url_for('list/index.html'))

    return render_template('list/new.html')
