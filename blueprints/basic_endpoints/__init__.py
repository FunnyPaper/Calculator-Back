from flask import Blueprint, request, make_response
from flask_cors import cross_origin
from setup import calculator

# Blueprint to be used by Flask app
blueprint: Blueprint = Blueprint('basic_endpoints', __name__)


@blueprint.route('/evaluate', methods=['POST'])
@cross_origin()
def evaluate():
    """
    Post method for obtaining mathematical equation result

    :return: Response with result if everything was correct or error encountered during evaluation
    """
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
    """
    Forwards used calculator's equation history

    :return: Calculator history
    """
    return calculator.history
