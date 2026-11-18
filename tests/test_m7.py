from app.modules.m7_revisions.rules import apply
from copy import deepcopy
def test_revision_impact_count(ctx):assert len(ctx['stages']['7']['rows'])==1
def test_share_revision_impact(ctx):assert ctx['stages']['7']['rows'][0]['新增股份差']=='10'
def test_version_transition(ctx):assert ctx['stages']['7']['rows'][0]['旧版本']=='1' and ctx['stages']['7']['rows'][0]['新版本']=='2'
def test_bonus_revision_no_dividend_change(ctx):assert ctx['stages']['7']['rows'][0]['分红差_CNY']=='0.00'
def test_reference_price_revision_negative(ctx):assert ctx['stages']['7']['rows'][0]['参考价差_CNY'].startswith('-')
def test_no_history_no_impact(ctx):
    c=deepcopy(ctx);c['action_history']=[];assert apply(c)['rows']==[]
def test_revision_investor_preserved(ctx):assert ctx['stages']['7']['rows'][0]['持仓记录']=='9007199254741001'

