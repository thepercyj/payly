class TransferException(BaseException):
    """
    Custom exception class for transfer-related errors.
    """
    message = None

    def __init__(self, message: str, *args: object) -> None:
        """
        Initialize TransferException with the provided message.

        :param message: Error message describing the transfer exception.
        :param args: Additional arguments for the exception.
        """
        self.message = message

        super().__init__(*args)


class TransactionFailedException(TransferException):
    """
    Custom exception class for transaction failure.
    """
    transaction_id = None

    def __init__(self, transaction_id: str, message: str, *args: object) -> None:
        """
        Initialize TransactionFailedException with the provided transaction ID and message.

        :param transaction_id: ID of the transaction.
        :param message: Error message describing the transaction failure.
        :param args: Additional arguments for the exception.
        """
        self.message = message
        self.transaction_id = transaction_id
        super().__init__(*args)
