from walletapp.models import Wallet


def wallet_profile_id(userid):
    wallet = Wallet.objects.get(user_id=userid)
    return wallet
