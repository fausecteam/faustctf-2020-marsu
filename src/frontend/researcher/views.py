import json

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django import forms
from django.contrib.auth.forms import UsernameField, PasswordChangeForm
from django.contrib.auth.models import User

class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
    

def edit(request):
    if request.method == 'POST':
        form = ProfileChangeForm(request.POST, instance=request.user)
        if not form.is_valid():
            return render(request, 'researcher/edit.xml', {'form': form})

        form.save()
        return HttpResponseRedirect(reverse('researcher:view'))

    else:
        return render(request, 'researcher/edit.xml', {'form': ProfileChangeForm(instance=request.user)})

def password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST, us=request.user  )
        if not form.is_valid():
            return render(request, 'researcher/edit.xml', {'form': form})

        form.save()
        return HttpResponseRedirect(reverse('researcher:view'))

    else:
        return render(request, 'researcher/password.xml', {'form': PasswordChangeForm(user=request.user)})


def get_friends(request):
    people = []

    people.append({'name': 'Felix Klein',
                   'username': 'klein',
                   'mail': 'felix@faui2k9.de'})

    people.append({'name': 'Christoph Egger',
                   'username': 'egger',
                   'mail': 'egger@cs.fau.de'})

    
    return HttpResponse(json.dumps(people))

    
# Create your views here.
