from django.shortcuts import render
from django.http import HttpResponse
from newsletter.models import *

def edit_item(request, item_pk):
    """this is where we edit a block item in the newsletter
    """
    try:
        item = NewsItems.objects.get(pk=item_pk)
        edit_or_create = 'edit'
    except:
        edit_or_create = 'create'
    return HttpResponse('This is the ' + edit_or_create + ' view for item ' + item_pk)

def save_item(request, item_pk):
    """this is where we save edits made to an existing item
    """
    return HttpResponse('This is the save item view/logic that would work on item ' + item_pk)

def view_item(request, item_pk):
    """this is for viewing a single item
    """
    return HttpResponse('This is where we view item ' + item_pk)

def home(request):
    """this is where I put together the list of items for templating for today's newsletter
    """
    return HttpResponse('This is the home view')
