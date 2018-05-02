from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from .db import get_db

bp = Blueprint('list', __name__)


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT *'
        ' FROM user where username=  "abc" '
    ).fetchall()
    return render_template('list/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        user = request.form['username']
        repo = request.form['reponame']

        db = get_db()
        db.execute(
            'INSERT INTO user (username, reponame)'
            ' VALUES (?, ?)',
            (user, repo)
        )
        db.commit()
        return redirect(url_for('list.index'))

    return render_template('list/create.html')


@bp.route('/repo/<name>', methods=['GET'])
def detail(name):

    if request.method == 'GET':

        db = get_db()
        rows = db.execute(
            'select * from user where username = ? ', [name]
        ).fetchall()
        return render_template('list/detail.html', rows=rows)
