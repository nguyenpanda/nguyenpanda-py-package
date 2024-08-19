class InvalidKaggleAPI(Exception):
    """
    Exception raised when the Kaggle API command provided is invalid.

    Attributes:
        api (str): The API command that caused the exception.
        message (str): Explanation of the error.
    """

    def __init__(self, api: str):
        """
        Initializes the InvalidKaggleAPI exception with the invalid API command.

        Args:
            api (str): The invalid Kaggle API command.
        """
        self.message = (
            'KAGGLE_API_COMMAND must be replaced by an actual API command.\n'
            'Expected pattern: `kaggle datasets download -d <username>/<dataset_name>`.\n'
            f'Provided command: {api}\n'
            'For more information, visit: https://www.kaggle.com/docs/api#interacting-with-datasets'
        )
        super().__init__(self.message)


class KaggleAuthenticationFailed(Exception):
    """
    Exception raised when Kaggle authentication fails.

    Attributes:
        message (str): Explanation of the error.
    """

    def __init__(self):
        """
        Initializes the KaggleAuthenticationFailed exception with a predefined error message.
        """
        self.message = (
            'Kaggle authentication failed. Please check your Kaggle API credentials.\n'
            'For more information, visit: https://www.kaggle.com/docs/api#getting-started-installation-&-authentication'
        )
        super().__init__(self.message)
