from flask import Blueprint, request, jsonify
from app.pipeline import calculate
from app.numeric import serial
bp=Blueprint('m5',__name__)
@bp.route('/api/m5', methods=['GET','POST'])
def module_5():
    payload=request.get_json(silent=True) or {}
    result=calculate(payload.get('csv'), stop=5)
    return jsonify(serial(result['stages']['5']))
