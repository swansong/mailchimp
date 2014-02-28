from django.shortcuts import render
from django.shortcuts import render_to_response
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
        form = NewsItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            item_date = item.date_to_publish
            return HttpResponseRedirect('/newsletter/%d/%d/%d/' % (item_date.year, item_date.month, item_date.day))
    
    form = NewsItemForm(instance=item)
    args = {
        'request': request,
        'item_pk': item_pk,
        'form': form,
    }
    
    return render(request, 'edit.html', args, context_instance=RequestContext(request))

@login_required
def new_item(request):
    """this is where we save edits made to an existing item
       currently disused in favor of using the modelform, but
       this would be where we might do ajaxy direct editing
    """
    try:
        """this logic here is for filling from the view_date view's
           output.  If a new item needs to be made from there, it
           will have these GET parameters
        """
        date_to_publish = datetime.datetime.strptime(request.GET['date_to_publish'], "%Y-%m-%d").date()
        position = int(request.GET['position'])
        new_item = NewsItem(date_to_publish=date_to_publish, position=position)
    except:
        """in case someone url hacks here, or if we want to just make
           a 'create new' button somewhere
        """
        new_item = NewsItem()
    new_item.save()
    return HttpResponseRedirect('/newsletter/%d/edit/' % (new_item.pk))

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
    """this is the future, past, and present newsletter view.  It allows people to view past and
       present newsletters without authentication, but future newsletters are for authenticated
       users only
    """
    logged_in = request.user.is_authenticated()

    try:
        date = datetime.date(int(year), int(month), int(day))
    except:
        return HttpResponse('bad date (somehow)')
    
    if date > datetime.date.today() and not logged_in:
        return HttpResponse('this newsletter has yet to be published')

    items = NewsItem.objects.all().filter(date_to_publish=date).order_by('position')
    left_sections = {
        0: None,
        1: None,
        2: None,
    }
    right_sections = {
        3: None,
        4: None,
        5: None,
    }
    extras = []
    
    for item in items:
        item_position = item.position
        if item_position < 3:
            left_sections[item.position] = item
        elif item_position <= 5:
            right_sections[item.position] = item
        else:
            extras.append(item)

    args = {
        'left_sections': left_sections,
        'right_sections': right_sections,
        'extras': extras,
        'date': date.isoformat(),
        'logged_in': logged_in,
    }
    return render(request, 'newsletter.html', args)

def rss(request):
    date = datetime.date.today()
    items = NewsItem.objects.all().filter(date_to_publish=date).order_by('position')
    left_sections = {
        0: None,
        1: None,
        2: None,
    }
    right_sections = {
        3: None,
        4: None,
        5: None,
    }
    
    for item in items:
        item_position = item.position
        if item_position < 3:
            left_sections[item.position] = item
        elif item_position <= 5:
            right_sections[item.position] = item

    args = {
        'left_sections': left_sections,
        'right_sections': right_sections,
        'date': date.isoformat(),
    }
    return render_to_response('rss.xml', args, mimetype='text/xml')
