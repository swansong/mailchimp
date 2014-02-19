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
            return HttpResponseRedirect('/newsletter/' + item_pk + '/view/')
    
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
    return HttpResponse('This is the home view')
