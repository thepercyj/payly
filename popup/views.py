from django.shortcuts import render


def empty_view(request, title='', message=''):
    context = {
        'title': title or 'No Data',
        'message': message or 'There is nothing to show'
    }
    return render(request, 'nothing.html', context)
