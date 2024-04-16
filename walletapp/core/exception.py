class TransferException(BaseException):
    message = None

    def __init__(self, message: str, *args: object) -> None:
        self.message = message

        super().__init__(*args)


class TransactionFailedException(TransferException):
    transaction_id = None

    def __init__(self, transaction_id: str, message: str, *args: object) -> None:
        self.message = message
        self.transaction_id = transaction_id
        super().__init__(*args)
