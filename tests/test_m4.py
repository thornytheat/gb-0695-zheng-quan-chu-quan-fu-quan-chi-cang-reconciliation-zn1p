from app.domain import action_math
from app.numeric import number
from decimal import Decimal
def test_reference_formula():
    a={'price':'10','cash':'1','bonus':'0.2','rights':'0.1','rights_price':'5'};price,factor=action_math(a);assert price==Decimal('9.5')/Decimal('1.3')
def test_factor_precise(): # TRAP-10
    a={'price':'10','cash':'0','bonus':'1','rights':'0','rights_price':'0'};assert action_math(a)==(Decimal(5),Decimal('0.5'))
def test_no_action_identity():assert action_math({'price':'10','cash':'0','bonus':'0','rights':'0','rights_price':'0'})==(Decimal(10),Decimal(1))
def test_sample_factor_rows(ctx):assert len(ctx['stages']['4']['rows'])==19
def test_dividend_not_price_addition():assert action_math({'price':'10','cash':'1','bonus':'0','rights':'0','rights_price':'0'})[0]==9
def test_invalid_action_rejected():
    import pytest
    from app.errors import DomainError
    with pytest.raises(DomainError):action_math({'price':'10','cash':'11','bonus':'0','rights':'0','rights_price':'0'})
def test_current_version_factor(ctx):assert ctx['stages']['4']['rows'][0]['行动版本']=='2'

