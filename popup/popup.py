from django.http import HttpResponse
import json


class PopupHttpResponse(HttpResponse):
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
