from django.http import HttpResponse
import json


class PopupHttpResponse(HttpResponse):
    """
    Custom HTTP response class for rendering pop-up messages.

    :param success: A boolean indicating whether the action was successful or not. Default is True.
    :param title: The title of the pop-up message. Default is 'Information'.
    :param message: The message content of the pop-up. Default is an empty string.
    """
    def __init__(self, success: bool = True, title: str = 'Information', message: str = ''):
        super().__init__(status=204, headers={
            'HX-Trigger': json.dumps({
                'popup': {
                    'success': success,
                    'title': title,
                    'message': message
                }
            })
        })
