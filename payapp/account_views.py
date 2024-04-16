# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import PasswordChangeForm
# from .forms import EditUserProfileForm
# from popup.popup import PopupHttpResponse
# from notificationapp.utils.notifications import get_notifications_for_user
# from django.contrib import messages
#
#
# @login_required(login_url='login')
# def profile(request):
#     notifications = get_notifications_for_user(request.user.id)
#     return render(request, 'account/index.html', {'count': len(notifications)})
#
#
# @login_required(login_url='login')
# def edit_profile(request):
#     form = EditUserProfileForm(request.user)
#
#     if request.method == 'POST':
#         form = EditUserProfileForm(request.user, request.POST)
#         if form.is_valid():
#             new_user = form.save()
#             return PopupHttpResponse(True, 'User Profile Changed', 'Your profile has been successfully changed.')
#
#     context = {
#         'form': form,
#         'user': request.user
#     }
#     return render(request, 'account/partials/edit-profile.html', context)
#
#
# @login_required(login_url='login')
# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('login')  # Redirect to success page
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = PasswordChangeForm(request.user)
#     return render(request, 'account/partials/change_password.html', {'form': form})
