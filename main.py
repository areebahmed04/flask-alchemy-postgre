from flask import jsonify, Flask
import requests


app = Flask(__name__)


class Repo:

    def __init__(self, url_name):
        self.url = url_name

    def get_repo(self):
        res = requests.get(self.url)
        j = res.json()
        d = dict()
        count = 0
        for i in j:
            d[count] = i["full_name"]
            count += 1
        return jsonify(d)


@app.route('/repo/<name>', methods=['GET'])
def index(name):

    url = "https://api.github.com/users/" + name + "/repos"
    my_repo = Repo(url)
    return my_repo.get_repo()


if __name__ == '__main__':

    app.run(debug=True)
