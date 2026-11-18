import csv, io
from app.config import HEADERS, LIMIT
from app.errors import DomainError
from app.reasons import isolate
def decode(raw):
    for encoding in ('utf-8-sig','gb18030'):
        try: return raw.decode(encoding)
        except UnicodeDecodeError: pass
    raise DomainError('ENCODING','无法识别文件编码')
def read_rows(ctx):
    text=ctx['text'].lstrip('\ufeff')
    if not text: raise DomainError('EMPTY','输入为空')
    reader=csv.reader(io.StringIO(text, newline=''), strict=True)
    try: head=next(reader,None)
    except csv.Error: raise DomainError('STRUCTURE','表头损坏')
    if head is None: raise DomainError('BLANK','文件仅有空行')
    head=[x.strip() for x in head]
    if set(head)!=set(HEADERS) or len(head)!=len(HEADERS):
        raise DomainError('HEADER','字段缺失或重复')
    rows=[];ctx['input_count']=0;ctx['blank_count']=0;ctx['header_count']=0
    try:
        for cells in reader:
            if len(rows)+len(ctx['quarantine']) >= LIMIT: raise DomainError('LIMIT','文件超过一万行')
            if not cells or all(not x.strip() for x in cells): ctx['blank_count']+=1;continue
            if cells==head: ctx['header_count']+=1;continue
            ctx['input_count']+=1
            if len(cells)!=len(head):
                isolate(ctx,{'行号':reader.line_num,'原值':'|'.join(cells)},'COLUMNS','列数不符');continue
            rows.append({**dict(zip(head,[x.strip() for x in cells])), '行号':reader.line_num})
    except csv.Error: raise DomainError('STRUCTURE','引号未闭合或记录截断')
    if not rows and not ctx['quarantine']: raise DomainError('HEADER_ONLY' if not ctx['blank_count'] else 'BLANK','文件没有业务记录')
    ctx['rows']=rows
    return rows
