from app.modules.m1_receiving.service import execute as stage1
from app.modules.m2_mapping.service import execute as stage2
from app.modules.m3_registry.service import execute as stage3
from app.modules.m4_factors.service import execute as stage4
from app.modules.m5_holdings.service import execute as stage5
from app.modules.m6_cash.service import execute as stage6
from app.modules.m7_revisions.service import execute as stage7
from app.config import SAMPLE
from app.manifest import make
from app.numeric import serial
from time import perf_counter
def calculate(text=None, stop=7):
    started=perf_counter()
    if text is None: text=SAMPLE.read_text(encoding='utf-8-sig')
    if not isinstance(text,str):
        from app.errors import DomainError
        raise DomainError('TYPE','CSV必须是文本')
    ctx={'text':text,'rows':[],'quarantine':[],'stages':{},'manifest':make(text)}
    for stage in STAGES[:stop]: stage(ctx)
    ctx['manifest']['elapsed_ms']=round((perf_counter()-started)*1000,3)
    ctx.pop('text',None)
    return serial(ctx)
STAGES=[stage1,stage2,stage3,stage4,stage5,stage6,stage7]
