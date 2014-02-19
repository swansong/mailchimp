from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from newsletter.models import *
from newsletter.forms import *
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
import datetime

@login_required
def edit_item(request, item_pk):
    """this is where we edit a block item in the newsletter
    """
    try:
        date_to_publish = request.GET['date_to_publish']
    except:
        today = datetime.date.today()
        date_to_publish = today.isoformat()
    item, created = NewsItem.objects.get_or_create(pk=item_pk, defaults={'date_to_publish': date_to_publish})
    
    if request.POST:
        form = NewsItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/newsletter/' + item_pk + '/')
    
    form = NewsItemForm(instance=item)
    args = {
        'request': request,
        'item_pk': item_pk,
        'form': form,
    }
    
    return render(request, 'edit.html', args, context_instance=RequestContext(request))

@login_required
def save_item(request, item_pk):
    """this is where we save edits made to an existing item
       currently disused in favor of using the modelform, but
       this would be where we might do ajaxy direct editing
    """
    return HttpResponse('This is the save item view/logic that would work on item ' + item_pk)

@login_required
def view_item(request, item_pk):
    """this is for viewing a single item
    """
    return HttpResponse('This is where we view item ' + item_pk)

def home(request):
    """this is where I put together the list of items for templating for today's newsletter
    """
    today = datetime.date.today()
    return HttpResponseRedirect("/newsletter/%d/%d/%d/" % (today.year, today.month, today.day))

def view_date(request, year, month, day):
    try:
        date = datetime.date(int(year), int(month), int(day))
    except:
        return HttpResponse('bad date (somehow)')
    items = NewsItem.objects.all().filter(date_to_publish=date).order_by('position')
    sections = {
        1: None,
        2: None,
        3: None,
        4: None,
        5: None,
        6: None,
        0: None,
    }
    for item in items:
        sections[item.position] = item
    args = {
        'sections': sections,
        'date': date.isoformat(),
        'logged_in': request.user.is_authenticated(),
    }
    return render(request, 'newsletter.html', args)

