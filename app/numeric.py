from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import unicodedata
from app.errors import DomainError
SENTINELS = {'', '-', 'N/A', 'NULL', '未知'}
def number(value, nullable=False):
    text = unicodedata.normalize('NFKC', str(value)).strip().replace(',', '')
    if text.upper() in SENTINELS:
        if nullable: return None
        raise DomainError('MISSING', '必填数值为空')
    try: result = Decimal(text)
    except InvalidOperation: raise DomainError('NUMBER', '数值格式无效')
    if not result.is_finite(): raise DomainError('NUMBER', '数值必须有限')
    return result
def fmt(value, places='0.0001'):
    return str(Decimal(value).quantize(Decimal(places), rounding=ROUND_HALF_UP))
def serial(value):
    if isinstance(value, Decimal): return str(value)
    if isinstance(value, dict): return {str(k):serial(v) for k,v in value.items()}
    if isinstance(value, (list,tuple)): return [serial(v) for v in value]
    return value
