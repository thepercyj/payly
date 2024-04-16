from django.shortcuts import render


def no_view(request, title='', message=''):
    context = {
        'title': title or 'No Data',
        'message': message or 'There is nothing to show'
    }
    return render(request, 'popup/layout/nothing.html', context)
