
def test_conn(app):
    assert (app.config['SQLALCHEMY_DATABASE_URI']=='postgresql://areeb_dev:pass@localhost:5432/areeb_dev')


def test_ping(client):

    res = client.get('http://127.0.0.1:5000/repo/u1')
    assert res.status_code == 200


def test_name_presence(client):

    res = client.get('http://127.0.0.1:5000/repo/testname')
    str = "testrepo"
    j = res.json
    for i in j.values():
        assert str in i


def test_return_size(client):

    res = client.get('http://127.0.0.1:5000/repo/u1')
    j = res.json
    assert len(j) > 0