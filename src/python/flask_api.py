from flask import Flask
from flask import request
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/invoice', methods=['GET', 'POST'])
def send_data():
    if request.method == 'POST':
        response = request.get_json()
        return response
    else : 
        return 'GET'

if __name__ == '__main__':
    app.run(host="0.0.0.0")
