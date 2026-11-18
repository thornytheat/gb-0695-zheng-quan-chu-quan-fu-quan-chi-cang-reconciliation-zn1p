from flask import Blueprint, request, jsonify
from app.pipeline import calculate
from app.numeric import serial
bp=Blueprint('m1',__name__)
@bp.route('/api/m1', methods=['GET','POST'])
def module_1():
    payload=request.get_json(silent=True) or {}
    result=calculate(payload.get('csv'), stop=1)
    return jsonify(serial(result['stages']['1']))
