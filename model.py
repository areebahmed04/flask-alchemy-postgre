from flask import Flask, request, flash, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import current_app, g

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)


class info(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    reponame = db.Column(db.String(100), unique=True)


@app.route('/hello')
def hello():
    return 'Hello world'


@app.route('/')
def show_all():
   return render_template('index.html', posts = info.query.all() )


@app.route('/new', methods=['GET', 'POST'])
def new():

    if request.method == 'POST':

        u = info(username= request.form['name'], reponame=request.form['repo'])

        db.session.add(u)
        db.session.commit()

        flash('Record was successfully added')
        return redirect(url_for('show_all'))

    return render_template('new.html')


@app.route('/repo/<name>', methods=['GET'])
def detail(name):

    if request.method == 'GET':

        return render_template('list/detail.html', rows= info.query.filter_by(username=name))


if __name__ == '__main__':

    db.create_all()
    # n = db.session.query(info).delete()
    # db.session.commit()
    # user1 = info(username='abc', reponame='repo1')
    # db.session.add(user1)
    # print("SSS", info.query.all())
    app.run(debug=True)