from flask import Blueprint, request, make_response
from flask_cors import cross_origin
from setup import calculator

blueprint: Blueprint = Blueprint('basic_endpoints', __name__)


@blueprint.route('/evaluate', methods=['POST'])
@cross_origin()
def evaluate():
    try:
        inp = request.get_json()
        calculator.evaluate(inp['expression'], True, **inp['options'])
        return calculator.history[0]["result"]
    except Exception as e:
        print(e)
        resp = make_response(str(e), 500)
        return resp


@blueprint.route('/history', methods=['GET'])
@cross_origin()
def history():
    return calculator.history
