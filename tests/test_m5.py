from app.domain import entitlement,allocate_cents
from decimal import Decimal
def test_largest_remainder_conservation(): # TRAP-24
    assert allocate_cents({'a':Decimal('0.005'),'b':Decimal('0.005'),'c':Decimal('0.005')})=={'a':Decimal('.01'),'b':Decimal('.01'),'c':Decimal(0)}
def test_fractional_shares_separate():
    e=entitlement({'shares':'101'},{'bonus':'0.1','rights':'0.05','cash':'0.13','rights_price':'5'});assert e['new_shares']==116 and e['fraction']==Decimal('.15')
def test_current_bonus_applied(ctx):assert ctx['holdings'][0]['新股份']=='127'
def test_dividend_precision(ctx):assert ctx['holdings'][0]['分红_CNY']=='13.26'
def test_subscription_cost(ctx):assert ctx['holdings'][0]['认配支付_CNY']=='25.50'
def test_zero_entitlement():assert entitlement({'shares':'0'},{'bonus':'0.1','rights':'0.05','cash':'0.13','rights_price':'5'})['cash']==0
def test_large_shares_no_float():assert entitlement({'shares':'9007199254740993'},{'bonus':'1','rights':'0','cash':'0','rights_price':'0'})['new_shares']==Decimal('18014398509481986')

