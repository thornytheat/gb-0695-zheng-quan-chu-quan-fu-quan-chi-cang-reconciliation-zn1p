from app.modules.m3_registry.rules import apply
from copy import deepcopy
def test_registration_day_included(ctx):assert any(p['position']['record']=='9007199254741001' for p in ctx['eligible'])
def test_late_position_excluded(ctx):assert all(p['position']['record']!='LATE' for p in ctx['eligible'])
def test_conflicted_action_no_rights(ctx):assert all(p['position']['security']!='000003' for p in ctx['eligible'])
def test_expected_eligible_count(ctx):assert len(ctx['eligible'])==19
def test_no_actions(ctx):
    c=deepcopy(ctx);c['actions']=[];apply(c);assert c['eligible']==[]
def test_before_registration(ctx):
    c=deepcopy(ctx);c['positions'][0]['event_date']='2026-11-16';apply(c);assert c['eligible'][0]['position']['event_date']=='2026-11-16'
def test_no_implicit_entitlement(ctx):assert sum(r['资格']=='无登记权益' for r in ctx['stages']['3']['rows'])==2


def test_latest_snapshot_prevents_double_entitlement(ctx):
    c=deepcopy(ctx);old={**c['positions'][0],'event_date':'2026-11-16','shares':'50','行号':99};c['positions'].append(old);apply(c)
    selected=[r for r in c['eligible'] if r['position']['record']==old['record']]
    assert len(selected)==1 and selected[0]['position']['shares']=='102'
