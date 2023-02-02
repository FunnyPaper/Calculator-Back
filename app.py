from flask import Flask
from flask_cors import CORS
from blueprints.basic_endpoints import blueprint as basic_endpoints


if __name__ == "__main__":
    # Initiate Flask app
    app = Flask(__name__)
    app.register_blueprint(basic_endpoints)
    # Cors policy for communication with Angular
    app.config['CORS_HEADERS'] = 'Content-Type'
    cors = CORS(app)
    app.run(debug=True)
