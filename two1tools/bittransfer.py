import json
import time
import requests

from two1.lib.bitserv.payment_methods import BitTransfer


def get_bittransfer(request):
    """Get the bittransfer header from a request.

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


def create_bittransfer(wallet, payer_username, payee_username, payee_address,
                       amount, description=""):
    """Manually create and sign a bittransfer.

    wallet is a Wallet instance, payer_username is Config().username.
    Refer to BitTransferRequests.make_402_payment.
    """

    bittransfer = json.dumps({
        'payer': payer_username,
        'payee_address': payee_address,
        'payee_username': payee_username,
        'amount': amount,
        'timestamp': time.time(),
        'description': description
    })
    signature = wallet.sign_message(bittransfer)
    return bittransfer, signature


def redeem_bittransfer(bittransfer, signature):
    """Apply the result of create_bittransfer to effect the transfer.

    Refer to BitTransfer.redeem_payment.
    """
    verification_url = BitTransfer.verification_url.format(
        bittransfer['payee_username'])
    try:
        return requests.post(verification_url,
                             data=json.dumps({'bittransfer': bittransfer,
                                              'signature': signature}),
                             headers={'content-type': 'application/json'})
    except requests.ConnectionError:
        pass
