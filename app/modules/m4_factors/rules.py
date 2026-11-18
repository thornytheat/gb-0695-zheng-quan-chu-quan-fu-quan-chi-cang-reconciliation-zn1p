from app.domain import action_math
from app.numeric import fmt
def apply(ctx):
    rows=[];factors={}
    for a in ctx['actions']:
        reference,factor=action_math(a);factors[(a['canonical'],a['ex_date'])]={'reference':reference,'factor':factor}
        rows.append({'证券':a['canonical'],'除权日':a['ex_date'],'前收盘_CNY':a['price'],'参考价_CNY':fmt(reference),'复权因子':fmt(factor,'0.00000001'),'行动版本':a['version']})
    ctx['factors']={str(k):v for k,v in factors.items()}
    return {'rows':rows,'metrics':[['参考价',len(rows),'项'],['因子',len(factors),'项'],['冲突隔离',sum(r['原因码']=='CONFLICT' for r in ctx['quarantine']),'条']]}

