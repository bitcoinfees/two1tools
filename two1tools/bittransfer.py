import sys
import json
import time
import requests

from two1.lib.bitserv.payment_methods import BitTransfer
from two1.lib.wallet import Wallet
from two1.commands.config import Config


def send_bittransfer_cli():
    """CLI wrapper for send_bittransfer.

    sendsats <payee> <amount> [<description>]
    """
    payee_username = sys.argv[1]
    amount = int(sys.argv[2])
    try:
        description = sys.argv[3]
    except IndexError:
        description = ""
    send_bittransfer(payee_username, amount, description).raise_for_status()


def send_bittransfer(payee_username, amount, description=""):
    """Create and redeem a bittransfer."""
    wallet = Wallet()
    username = Config().username
    bittransfer, signature = create_bittransfer(
        wallet, username, payee_username, amount, description)
    return redeem_bittransfer(bittransfer, signature, payee_username)


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


def create_bittransfer(wallet, payer_username, payee_username,
                       amount, description=""):
    """Manually create and sign a bittransfer.

    wallet is a Wallet instance, payer_username is Config().username.
    Refer to BitTransferRequests.make_402_payment.
    """

    bittransfer = json.dumps({
        'payer': payer_username,
        'payee_username': payee_username,
        'amount': amount,
        'timestamp': time.time(),
        'description': description
    })
    signature = wallet.sign_message(bittransfer)
    return bittransfer, signature


def redeem_bittransfer(bittransfer, signature, payee_username):
    """Apply the result of create_bittransfer to effect the transfer.

    Refer to BitTransfer.redeem_payment.
    """
    verification_url = BitTransfer.verification_url.format(payee_username)
    return requests.post(verification_url,
                         data=json.dumps({'bittransfer': bittransfer,
                                          'signature': signature}),
                         headers={'content-type': 'application/json'})
