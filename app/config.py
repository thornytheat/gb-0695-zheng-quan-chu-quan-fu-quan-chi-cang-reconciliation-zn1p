from pathlib import Path
RULE_VERSION = "2026.11.18.2"
TITLE = '证券除权复权与持仓对账'
SHORT = 'equity-adjust'
MODULES = ['行动接收', '证券映射', '权益登记', '除权因子', '持仓重算', '现金对账', '修订回放']
HEADERS = ['record', 'kind', 'security', 'alias', 'event_date', 'record_date', 'ex_date', 'price', 'cash', 'bonus', 'rights', 'rights_price', 'shares', 'version', 'reported_cash']
SAMPLE = Path(__file__).resolve().parent.parent / "sample_data" / "operations.csv"
LIMIT = 10000
