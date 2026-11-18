from app.reader import read_rows
def apply(ctx):
    rows=read_rows(ctx)
    return {'rows':rows,'metrics':[['行动记录',sum(r['kind']=='action' for r in rows),'条'],['持仓记录',sum(r['kind']=='position' for r in rows),'条'],['输入',ctx['input_count'],'条']]}

