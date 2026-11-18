from app.domain import entitlement,action_math
from app.numeric import fmt
def apply(ctx):
    rows=[]
    for old in ctx['action_history']:
        new=next((a for a in ctx['actions'] if a['canonical']==old['canonical'] and a['ex_date']==old['ex_date']),None)
        if not new or old['version']==new['version']:continue
        for item in ctx['eligible']:
            if item['action']['record']!=new['record']:continue
            p=item['position'];before,after=entitlement(p,old),entitlement(p,new)
            rows.append({'证券':new['canonical'],'持仓记录':p['record'],'旧版本':old['version'],'新版本':new['version'],'新增股份差':str(after['new_shares']-before['new_shares']),'分红差_CNY':fmt(after['cash']-before['cash'],'0.01'),'参考价差_CNY':fmt(action_math(new)[0]-action_math(old)[0])})
    return {'rows':rows,'metrics':[['修订影响',len(rows),'条'],['旧版留存',len(ctx['action_history']),'项'],['当前版本',max((a['version_n'] for a in ctx['actions']),default=0),'']]}

