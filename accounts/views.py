from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from . forms import ProfileForm
from .models import Profile
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.http import Http404

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'sign_up.html'

def profile(request, user_id):
    profile = get_object_or_404(Profile, user_id=user_id)
    if profile != request.user.profile:
        raise Http404

    if request.method != 'POST':
        form = ProfileForm(instance=profile)
    else:
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile_edit = form.save(commit=False)
            profile_edit.save()
            return redirect('../../../')

    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})
