from django.db import models


CURRENCY_CHOICES = (
    ('RUB', 'Ruble'),
    ('USD', 'US dollar'),
    ('EUR', 'EURO'),
)


class Banknote(models.Model):
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='Ruble',
    )
    value = models.PositiveSmallIntegerField()
    quantity = models.PositiveIntegerField()

    @classmethod
    def get_amount_currency(cls, currency='RUB', value=None):

        if value:
            result = Banknote.objects.filter(currency=currency, value=value)
            if not result.exists():
                return 0
        else:
            result = Banknote.objects.filter(currency=currency)
            if not result.exists():
                return 0

        amount = result.annotate(amount=(models.Avg('value') * models.Avg('quantity'))).aggregate(models.Sum('amount'))

        return int(amount['amount__sum'])

    class Meta:
        unique_together = (('currency', 'value'),)
        ordering = ['currency', '-value']
