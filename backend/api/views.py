from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.utils import json

from .models import Banknote
from .serializers import BanknoteSerializer


success_false = json.dumps({
    "success": False,
})


def amount_recursion(amount_tmp, lst, i, result):
    print(amount_tmp, lst, i, result)
    if amount_tmp == 0 or i > len(lst) - 1:
        return amount_tmp
    else:
        if amount_tmp >= lst[i].get('value') and lst[i].get('quantity'):
            amount_tmp -= lst[i].get('value')
            lst[i]['quantity'] -= 1
            if not len(result) or result[-1].get('value') != lst[i].get('value'):
                result.append({'value': lst[i].get('value'), 'quantity': 0})
            result[-1]['quantity'] += 1
            return amount_recursion(amount_tmp, lst, i, result)
        else:
            return amount_recursion(amount_tmp, lst, i + 1, result)


@api_view(['POST'])
def deposit(request):
    data = json.loads(JSONParser().parse(request))

    banknote = Banknote.objects.filter(currency=data['currency'], value=data['value'])

    if banknote.exists():
        serializer = BanknoteSerializer(banknote, data=data)
    else:
        serializer = BanknoteSerializer(data=data)

    if serializer.is_valid():
        serializer.save()

        resp = json.dumps({
            "success": True,
        })
        return Response(resp, status=status.HTTP_201_CREATED)

    return Response(success_false)


@api_view(['POST'])
def withdraw(request):

    data = json.loads(JSONParser().parse(request))

    currency, amount = data['currency'], data['amount']

    if amount > Banknote.get_amount_currency(currency=currency):
        return Response(success_false)

    banknote_list = list(Banknote.objects.filter(currency=currency).values('id', 'value', 'quantity'))

    result = list()
    amount_tmp = amount_recursion(amount, banknote_list, 0, result)

    if amount_tmp == 0:
        for i in range(len(banknote_list)):
            query = Banknote.objects.get(pk=banknote_list[i].get('id'))
            query.quantity = banknote_list[i].get('quantity')
            query.save()

        resp = json.dumps({
            "success": True,
            "result": result
        })

        return Response(resp, status=status.HTTP_200_OK)
    else:
        return Response(success_false)
