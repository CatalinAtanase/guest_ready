from django.db.models.expressions import Case, When
from django.db.models import Sum, F


CITIES = [
    ('LONDON', 'LONDON'),
    ('PARIS', 'PARIS'),
    ('PORTO', 'PORTO'),
]

COMMISSIONS = {
    'LONDON': 10.0,
    'PARIS': 12.0,
    'PORTO': 9.0,
}

COMMISSIONS_BY_CITY = {
    'commission':
        Sum(
            Case(
                When(location__city='LONDON', then=F(
                    'income') * COMMISSIONS['LONDON'] / 100),
                When(location__city='PARIS', then=F(
                    'income') * COMMISSIONS['PARIS'] / 100),
                When(location__city='PORTO', then=F(
                    'income') * COMMISSIONS['PORTO'] / 100),
            ),
        ),
}
