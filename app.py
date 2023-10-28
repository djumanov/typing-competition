from flask import Flask, jsonify
from handlers import db


app = Flask(__name__)


@app.route('/results/')
def get_results():
    return jsonify(db.get_all_results())



if __name__ == '__main__':
    app.run(debug=True)

