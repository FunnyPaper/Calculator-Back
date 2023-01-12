from flask import Flask
from flask_cors import CORS
from blueprints.basic_endpoints import blueprint as basic_endpoints

app = Flask(__name__)
app.register_blueprint(basic_endpoints)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)

if __name__ == "__main__":
    app.run(debug=True)
