from app.numeric import number
def test_security_leading_zero(ctx): # TRAP-08
    assert ctx['actions'][0]['canonical']=='000001'
def test_large_id_unchanged(ctx): # TRAP-09
    assert ctx['positions'][0]['record']=='9007199254741001'
def test_fullwidth_decimal(): # TRAP-06
    assert number('１,２３４.５')==number('1234.5')
def test_conflicting_action_removed(ctx): # TRAP-14
    assert all(a['canonical']!='000003' for a in ctx['actions'])
def test_latest_action_chosen(ctx): # TRAP-25
    assert ctx['actions'][0]['version']=='2'
def test_older_action_retained(ctx):assert len(ctx['action_history'])==1
def test_missing_shares_isolated(ctx):assert any(q['原因码']=='MISSING' for q in ctx['quarantine'])

