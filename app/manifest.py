import hashlib, time
from app.config import RULE_VERSION
def make(text):
    digest=hashlib.sha256(text.encode('utf-8')).hexdigest()
    return {'run_id':hashlib.sha256((RULE_VERSION+':'+digest).encode('utf-8')).hexdigest()[:16], 'sha256':digest, 'rule_version':RULE_VERSION, 'parameters':{}, 'created_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
