from rest_framework.response import Response
from rest_framework.decorators import api_view
from decimal import Decimal
from walletapp.core.wallet import convert
from payapp.models import Currency

@api_view(['GET'])
def currency_conversion(request, currency1, currency2, amount):
    """
    Converts an amount from one currency to another.

    :param request: HttpRequest
        The request object containing information about the current HTTP request.
    :type request: HttpRequest
    :param currency1: str
        The source currency code.
    :type currency1: str
    :param currency2: str
        The target currency code.
    :type currency2: str
    :param amount: float
        The amount to be converted.
    :type amount: float
    :return: Response
        JSON response containing the conversion result.
    """
    try:
        # handle not supported currency
        if currency1 not in [currency for currency, _ in Currency.choices] or currency2 not in [currency for currency, _ in Currency.choices]:
            error_data = {
                'success': False,
                'currency1': currency1,
                'currency2': currency2,
                'amount': amount,
                'error': f'unsupported conversion of {currency1} and {currency2}'
            }
            return Response(error_data, status=400)

        # convert amount if everything is right
        converted_amount = convert(Decimal(amount), currency1, currency2)

        data = {
            'success': True,
            'currency1': currency1,
            'currency2': currency2,
            'amount': amount,
            'converted_amount': converted_amount
        }
        return Response(data, status=200)
    except Exception as e:
        error_data = {
            'success': False,
            'currency1': currency1,
            'currency2': currency2,
            'amount': amount,
            'error': str(e)
        }
        return Response(error_data, status=400)