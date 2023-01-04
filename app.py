import importlib
import sys
import re
import math
from typing import Callable
from dataclasses import dataclass
from flask import Flask, render_template, request, json
from flask_cors import CORS, cross_origin
from logic.calculator import Calculator, verify_functions, verify_groups
import logic.default_rules as dr

calculator: Calculator
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/evaluate', methods=['POST'])
@cross_origin()
def evaluate():
    try:
        inp = request.get_json()
        return str(calculator.evaluate(inp['expression'], True, **inp['options']))
    except Exception as e:
        print(e)
        return 'ERROR'


@app.route('/history', methods=['GET'])
@cross_origin()
def history():
    return calculator.history


if __name__ == "__main__":
    calculator = Calculator()
    calculator.set_rules(
        function=dr.function,
        separator=dr.separator,
        constant=dr.constant,
        open_bracket=dr.open_bracket,
        close_bracket=dr.close_bracket,
        number=dr.number,
        # fixed length lookbehind (first for visible symbols, second for string start)
        # - can be unary or binary (so both groups have to be more specific about matching)
        ul_operator=dr.ul_operator,
        ul_start_operator=dr.ul_start_operator,
        b_operator=dr.b_operator,
        ur_operator=dr.ur_operator
    )
    calculator.set_validators(
        verify_groups,
        verify_functions
    )
    app.run(debug=True)

