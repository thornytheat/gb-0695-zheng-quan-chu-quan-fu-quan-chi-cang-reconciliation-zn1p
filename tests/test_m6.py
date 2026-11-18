def test_record_conservation(ctx):assert ctx['balanced'] is True
def test_reconcile_count(ctx):assert len(ctx['cash_reconciliation'])==19
def test_dividend_expected(ctx):assert ctx['cash_reconciliation'][0]['应付_CNY']=='13.26'
def test_sample_channels_match(ctx):assert all(r['结论']=='相符' for r in ctx['cash_reconciliation'])
def test_cash_diff_zero(ctx):assert all(r['差异_CNY'] in ('0.00','-0.00') for r in ctx['cash_reconciliation'])
def test_reported_rounded_for_display(ctx):assert len(ctx['cash_reconciliation'][0]['渠道报送_CNY'].split('.')[1])==2
def test_manifest_has_rule(ctx):assert ctx['manifest']['rule_version']=='2026.11.18.2'

