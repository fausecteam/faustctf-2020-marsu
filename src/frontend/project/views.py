import json
from pprint import pprint
import requests
import misaka
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required

from django import forms

from .models import *
from .forms import NewProjectForm

# Create your views here.
def index(request):
    pass


@login_required
def view_project(request, project):
    proj = Project.objects.get(pk=project)
    if not request.user in proj.users.all():
        return HttpResponse('UNAUTHORIZED', status=401)

    pads = []
    for pad in proj.pad_set.all():
        pads.append(misaka.html(pad.markdown))

    return render(request, 'project/view.xml', {'project': proj,
                                                'pads': pads})


@ensure_csrf_cookie
@login_required
def create(request):
    if request.method == 'POST':
        form = NewProjectForm(request.POST)
        if not form.is_valid():
            return render(request, 'project/create.xml', {'form': form})

        # TODO Step 2: confirm inviting new people
        proj = Project()
        proj.title = form.cleaned_data['title']
        proj.save()
        proj.users.add(request.user)
        proj.save()
        for pk in form.cleaned_data['pad']:
            pad = Pad.objects.get(pk=pk)
            pad.project.add(proj)
            pad.save()

        return HttpResponseRedirect(reverse('project:view', args=(proj.id,)))
    else:
        form = NewProjectForm()
        return render(request, 'project/create.xml', {'form': form})


@login_required
def create_pad(request):
    data = json.loads(request.body)
    pad = Pad.from_markdown(request, '%(name)s\n=====\n\n' % data)
    pad.save()
    return HttpResponse(json.dumps({'url': pad.url, 'pk': pad.id}))


@login_required
def add_pad(request):
    data = json.loads(request.body)
    pad = Pad(url=data['url'])
    pad.save()
    return HttpResponse(json.dumps({'url': pad.url, 'pk': pad.id}))


def newpad(request):
    newpad = requests.post('https://codimd.faui2k.cloud/new', data='test', headers={'Content-Type': 'text/markdown'})
    url = newpad.url
