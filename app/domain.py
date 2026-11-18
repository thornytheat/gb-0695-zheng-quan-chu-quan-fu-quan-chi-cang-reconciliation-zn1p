from decimal import Decimal,ROUND_FLOOR,ROUND_HALF_UP
from datetime import date
from app.numeric import number
from app.errors import DomainError
def day(text):
    try:return date.fromisoformat(text)
    except ValueError:raise DomainError('DATE','日期格式无效')
def action_math(a):
    price,cash,bonus,rights,rp=[number(a[k]) for k in ('price','cash','bonus','rights','rights_price')]
    if price<=0 or min(cash,bonus,rights,rp)<0:raise DomainError('ACTION','公司行动数值无效')
    reference=(price-cash+rp*rights)/(1+bonus+rights)
    if reference<=0:raise DomainError('ACTION','除权参考价不为正')
    return reference,reference/price
def allocate_cents(amounts):
    # Aggregate cash is rounded once; rows receive cents by largest remainder.
    target=int(sum(amounts.values(),Decimal(0)).quantize(Decimal('0.01'),rounding=ROUND_HALF_UP)*100)
    floors={key:int((value*100).to_integral_value(rounding=ROUND_FLOOR)) for key,value in amounts.items()}
    order=sorted(amounts,key=lambda key:(-(amounts[key]*100-floors[key]),key))
    for key in order[:target-sum(floors.values())]:floors[key]+=1
    return {key:Decimal(value)/100 for key,value in floors.items()}
def entitlement(position,action):
    shares=number(position['shares']);bonus=number(action['bonus']);rights=number(action['rights'])
    added=shares*(bonus+rights);whole=added.to_integral_value(rounding=ROUND_FLOOR)
    return {'new_shares':shares+whole,'fraction':added-whole,'cash':shares*number(action['cash']),'subscription':shares*rights*number(action['rights_price'])}
