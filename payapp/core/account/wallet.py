from walletapp.models import Wallet


def wallet_profile_id(userid):
    """
    Retrieves the wallet associated with the given user ID.

    :param userid: int
        The ID of the user whose wallet is to be retrieved.
    :type userid: int
    :return: Wallet
        The wallet associated with the given user ID.
    """
    wallet = Wallet.objects.get(user_id=userid)
    return wallet
