from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from ArticleMetadata import get_metadata

from .models import Paper

def index(request):
    return render(request, 'index.xml')

@login_required
def add(request):
    paperdata = get_metadata(request.POST['metaurl'])
    try:
        paper = Paper.from_dict(paperdata)
        paper.save()
    except IntegrityError:
        paper = Paper.objects.get(source=paperdata['importer'], handle=paperdata['uid'])

    paper.user.add(request.user)
        
    return HttpResponseRedirect(reverse('readinglist:detail', args=(paperdata['importer'], paperdata['uid'])))

def detail(request, source, handle):
    paper = get_object_or_404(Paper,
                              source=source,
                              handle=handle)

    return render(request, 'readinglist/detail.xml', {'paper': paper})

@login_required
def listpapers(request, username=None):
    if username is None:
        foruser = request.user
    else:
        foruser = User.objects.get(username=username)

    papers = request.user.paper_set.all()
    
    return render(request, 'readinglist/list.xml', {'papers': papers,
                                                    'users': User.objects.all(),
                                                    'foruser': foruser})
