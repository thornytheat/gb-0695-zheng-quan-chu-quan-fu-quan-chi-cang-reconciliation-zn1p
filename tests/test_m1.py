from app.pipeline import calculate
from app.errors import DomainError
import pytest
def test_sample_records(ctx):assert ctx['input_count']==45
def test_bom_header(raw): # TRAP-02
    assert calculate('\ufeff'+raw)['input_count']==45
def test_input_kinds(ctx):assert {r['kind'] for r in ctx['rows']}=={'action','position'}
def test_empty_rejected():
    with pytest.raises(DomainError):calculate('')
def test_truncated_row(raw):assert any(q['原因码']=='COLUMNS' for q in calculate(raw+'bad,row\n')['quarantine'])
def test_sample_large_id(ctx):assert ctx['rows'][20]['record']=='9007199254741001'
def test_input_row_count(ctx):assert len(ctx['stages']['1']['rows'])==45

