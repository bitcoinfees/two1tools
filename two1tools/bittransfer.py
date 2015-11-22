import json
from two1.lib.bitserv.payment_methods import BitTransfer


def get_bittransfer(request):
    """Get the bittransfer dict.

    Takes in the Flask request context object. Makes no assumptions about
    the validity of the payment.

    bittransfer dict has the following keys:
    1. payer
    2. payee_address
    3. payee_username
    4. amount
    5. timestamp
    6. description
    """
    try:
        return json.loads(request.headers[BitTransfer.http_payment_data])
    except KeyError:
        return None
