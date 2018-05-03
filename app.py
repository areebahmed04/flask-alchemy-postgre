# __
from flask import Flask, request, flash, redirect, render_template, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup


POSTGRES = {
        'user': 'areeb_dev',
        'pw': 'pass',
        'db': 'areeb_dev',
        'host': 'localhost',
        'port': '5432',
    }

db = SQLAlchemy()

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db.init_app(app)
app.config['SECRET_KEY'] = "secret"


def create_app():


    class info(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(100))
        reponame = db.Column(db.String(100))

    @app.route("/hello")
    def main():
        return 'Hello World !'


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

            soup = BeautifulSoup(render_template('detail.html', rows= info.query.filter_by(username=name)))
            d = dict()
            c=0
            for i in soup.findAll('h3'):
                d[c] = str(i)[4:-5]
                c+=1
            # print(d)

            return jsonify(d)
            # return type(info.query.filter_by(username=name))

    def shutdown_server():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    @app.route('/shutdown', methods=['GET'])
    def shutdown():
        shutdown_server()
        return 'Server shutting down...'

    return app

if __name__ == '__main__':
    print("SSS")
    app = create_app()
    app.run()

