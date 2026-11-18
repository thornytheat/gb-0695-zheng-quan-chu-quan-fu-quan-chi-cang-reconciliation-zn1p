from flask import Blueprint, request, jsonify
from app.pipeline import calculate
from app.numeric import serial
bp=Blueprint('m4',__name__)
@bp.route('/api/m4', methods=['GET','POST'])
def module_4():
    payload=request.get_json(silent=True) or {}
    result=calculate(payload.get('csv'), stop=4)
    return jsonify(serial(result['stages']['4']))
