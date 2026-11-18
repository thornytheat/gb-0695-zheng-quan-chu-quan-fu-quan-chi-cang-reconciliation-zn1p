from flask import Blueprint, request, jsonify
from app.pipeline import calculate
from app.numeric import serial
bp=Blueprint('m2',__name__)
@bp.route('/api/m2', methods=['GET','POST'])
def module_2():
    payload=request.get_json(silent=True) or {}
    result=calculate(payload.get('csv'), stop=2)
    return jsonify(serial(result['stages']['2']))
