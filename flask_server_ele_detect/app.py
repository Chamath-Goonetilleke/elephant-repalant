from flask import Flask
from flask_cors import CORS
from Routes.ElephantDetectRoute import elephant_route

app = Flask(__name__)
CORS(app)
elephant_route(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
