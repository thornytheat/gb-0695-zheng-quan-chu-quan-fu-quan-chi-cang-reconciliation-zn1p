from flask import Flask, request, jsonify, Response
import csv,io
from app.errors import DomainError
from app.reader import decode
from app.pipeline import calculate
from app.store import save, latest, history, review, get_run
from app.web import bp as web

from app.modules.m1_receiving.handler import bp as bp1
from app.modules.m2_mapping.handler import bp as bp2
from app.modules.m3_registry.handler import bp as bp3
from app.modules.m4_factors.handler import bp as bp4
from app.modules.m5_holdings.handler import bp as bp5
from app.modules.m6_cash.handler import bp as bp6
from app.modules.m7_revisions.handler import bp as bp7
app=Flask(__name__)
app.config['MAX_CONTENT_LENGTH']=5*1024*1024
app.json.ensure_ascii=False
@app.template_filter('display')
def display(value):
    import re
    from decimal import Decimal
    text=str(value)
    if re.fullmatch(r'-?[0-9]+\.[0-9]+',text):
        return format(Decimal(text),'.4f').rstrip('0').rstrip('.')
    return text
app.register_blueprint(web)
app.register_blueprint(bp1)
app.register_blueprint(bp2)
app.register_blueprint(bp3)
app.register_blueprint(bp4)
app.register_blueprint(bp5)
app.register_blueprint(bp6)
app.register_blueprint(bp7)
@app.before_request
def validate_request_object():
    if request.method!='POST': return None
    if request.files:
        if request.path!='/api/run' or 'file' not in request.files:
            raise DomainError('REQUEST','上传必须使用file字段',400)
        return None
    if not request.is_json:
        raise DomainError('REQUEST','请求须为JSON对象或CSV文件',400)
    if not isinstance(request.get_json(silent=True),dict):
        raise DomainError('REQUEST','请求内容必须为JSON对象',400)
@app.errorhandler(DomainError)
def domain_error(error): return jsonify({'code':error.code,'message':error.message}),error.status
@app.errorhandler(413)
def too_big(error): return jsonify({'code':'LIMIT','message':'文件超过5MB'}),413
@app.route('/health')
def health(): return {'status':'ok'}
@app.route('/api/run',methods=['POST'])
def run():
    if request.files:
        raw=request.files['file'].read();text=decode(raw)
    else:
        payload=request.get_json(silent=True) or {};text=payload.get('csv')
    return jsonify(save(calculate(text)))
@app.route('/api/runs/<ident>')
def run_detail(ident): return jsonify(get_run(ident))
@app.route('/api/history')
def runs(): return jsonify(history())
@app.route('/api/review',methods=['POST'])
def decide():
    body=request.get_json(silent=True) or {}
    try: version=int(body.get('revision',0))
    except (ValueError,TypeError): raise DomainError('VERSION','版本必须为整数')
    return jsonify(review(body.get('id'),version,body.get('decision')))
@app.route('/api/evidence.csv')
def evidence():
    result=get_run(request.args['run_id']) if request.args.get('run_id') else (latest() or save(calculate()));out=io.StringIO(newline='')
    rows=[]
    for index,stage in result['stages'].items():
        rows.extend({'阶段':index,**r} for r in stage['rows'])
    rows.extend({'阶段':'隔离',**r} for r in result['quarantine'])
    fields=list(dict.fromkeys(['阶段','run_id','规则版本']+[k for r in rows for k in r]))
    writer=csv.DictWriter(out,fieldnames=fields);writer.writeheader()
    for row in rows: writer.writerow({'run_id':result['manifest']['run_id'],'规则版本':result['manifest']['rule_version'],**row})
    return Response('\ufeff'+out.getvalue(),mimetype='text/csv',headers={'Content-Disposition':'attachment; filename=evidence.csv'})
if __name__=='__main__': app.run(host='0.0.0.0',port=8000)
