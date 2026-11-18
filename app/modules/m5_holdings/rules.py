from app.domain import entitlement,allocate_cents
from app.numeric import fmt
def apply(ctx):
    groups={};rows=[]
    for item in ctx['eligible']:groups.setdefault((item['action']['canonical'],item['action']['ex_date']),[]).append(item)
    for key,items in sorted(groups.items()):
        calculations={p['position']['record']:entitlement(p['position'],p['action']) for p in items};cash=allocate_cents({k:v['cash'] for k,v in calculations.items()})
        for item in items:
            p,a=item['position'],item['action'];e=calculations[p['record']]
            rows.append({'持仓记录':p['record'],'证券':p['canonical'],'快照日':p['event_date'],'除权日':a['ex_date'],'原股份':p['shares'],'新股份':str(e['new_shares']),'零碎股':str(e['fraction']),'分红_CNY':fmt(cash[p['record']],'0.01'),'认配支付_CNY':fmt(e['subscription'],'0.01'),'行动版本':a['version'],'行号':p['行号']})
    ctx['holdings']=rows
    return {'rows':rows,'metrics':[['重算持仓',len(rows),'条'],['零碎股记录',sum(r['零碎股']!='0' for r in rows),'条'],['现金分红',str(sum((__import__('decimal').Decimal(r['分红_CNY']) for r in rows),__import__('decimal').Decimal(0))),'CNY']]}

