from django.shortcuts import render


def no_view(request, title='', message=''):
    """
    Renders a view indicating that there is no data to display.

    :param request: The HTTP request.
    :param title: The title of the view. Default is an empty string.
    :param message: The message content of the view. Default is 'There is nothing to show'.
    :return: HttpResponse object rendering the view.
    """
    context = {
        'title': title or 'No Data',
        'message': message or 'There is nothing to show'
    }
    return render(request, 'popup/layout/nothing.html', context)
