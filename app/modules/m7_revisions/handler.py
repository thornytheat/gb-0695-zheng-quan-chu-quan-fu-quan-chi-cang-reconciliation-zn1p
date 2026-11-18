from flask import Blueprint, request, jsonify
from app.pipeline import calculate
from app.numeric import serial
bp=Blueprint('m7',__name__)
@bp.route('/api/m7', methods=['GET','POST'])
def module_7():
    payload=request.get_json(silent=True) or {}
    result=calculate(payload.get('csv'), stop=7)
    return jsonify(serial(result['stages']['7']))
