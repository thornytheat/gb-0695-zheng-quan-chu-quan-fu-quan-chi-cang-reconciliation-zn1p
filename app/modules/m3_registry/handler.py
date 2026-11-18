from flask import Blueprint, request, jsonify
from app.pipeline import calculate
from app.numeric import serial
bp=Blueprint('m3',__name__)
@bp.route('/api/m3', methods=['GET','POST'])
def module_3():
    payload=request.get_json(silent=True) or {}
    result=calculate(payload.get('csv'), stop=3)
    return jsonify(serial(result['stages']['3']))
