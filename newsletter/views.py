from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from newsletter.models import *
from newsletter.forms import *
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
import datetime
from django.conf import settings
from PIL import Image
import os.path
import re

SUBSITE = settings.SUBSITE
CDN = settings.CDN


def user_login(request):
    """this view is the login view for the newsletter
    """
    if request.user.is_authenticated():
        try:
            return HttpResponseRedirect(request.GET['next'])
        except:
            return HttpResponseRedirect('%s/newsletter/home/' % (SUBSITE))
    
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    try:
                        return HttpResponseRedirect(request.GET['next'])
                    except:
                        return HttpResponseRedirect('%s/newsletter/home/' % (SUBSITE))
                else:
                    return render('inactive user')
    
    form = LoginForm()

    args = {
        'form': form,
        'SUBSITE': SUBSITE,
    }

    return render(request, 'login.html', args, context_instance=RequestContext(request))

def user_logout(request):
    """log out a user
    """
    logout(request)
    return HttpResponseRedirect('%s/newsletter/home/' % (SUBSITE))


@login_required
def edit_item(request, item_pk):
    """this is where we edit a block item in the newsletter
    """
    item, created = NewsItem.objects.get_or_create(pk=item_pk)
    if created and request.GET:
        try:
            item.date_to_publish = request.GET['date_to_publish']
        except:
            today = datetime.date.today()
            item.date_to_publish = today.isoformat()
    if request.POST:
        form = NewsItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            if request.FILES:

                # these lines figure out in what folder the thumbnails should be saved
                date_iso_list = request.POST['date_to_publish'].split('-')
                directory = '%simg/%s/%s/' % (settings.MEDIA_ROOT, date_iso_list[0], date_iso_list[1])
                if not os.path.exists(directory):
                    # necessary to create proper directory if not in existence.
                    os.makedirs(directory)

                this_image = request.FILES['image']
                name = this_image.name
                import pdb;pdb.set_trace()
                name = name.replace(' ', '_');              #django turn spaces into underscores
                name = re.sub('[\[\]{}()<>:;]', '', name)     #and removes colons from filenames
                imagefile = directory + name                #building where the image and its related thumbnails will live
                index = imagefile.rfind('.')                #figuring out where to append thumbnail
                
                if os.path.isfile(imagefile):
                    """ This is designed to use django's naming scheme to figure out what an image's saved name will be
                        if a file with the same name already exists in the month's folder.  For creating proper thumbnails
                        in the edge case of two different uploaded pictures with the same name.  TODO: make custom storage
                    """
                    tempname = imagefile
                    counter = 0
                    while os.path.isfile(tempname):
                        counter += 1
                        tempname = '%s_%d%s' % (imagefile[:index], counter, imagefile[index:])
                    imagefile = tempname
                    index = imagefile.rfind('.')

                #figure out the content type of the image
                if this_image.content_type == 'image/jpeg':
                    imagetype = 'JPEG'
                if this_image.content_type == 'image/png':
                    imagetype = 'PNG'

                try:
                    """ Open the uploaded file, then create a PIL image from that.  Then create an approprate thumbnail name
                        and size and save it.  Do for large thumbnail then repeat for small
                    """
                    this_image.open()
                    image = Image.open(this_image)
                    large = imagefile[:index] + '.large' + imagefile[index:]
                    if not os.path.isfile(large):
                        image.thumbnail((300, 300), Image.ANTIALIAS)
                        image.save(large, imagetype)
                except Exception as e:
                    return render("could not save large thumbnail")
                try:
                    this_image.open()
                    image = Image.open(this_image)
                    small = imagefile[:index] + '.small' + imagefile[index:]
                    if not os.path.isfile(small):
                        image.thumbnail((260, 260), Image.ANTIALIAS)
                        image.save(small, imagetype)
                except Exception as e:
                    return render("could not save small thumbnail")

                this_image.close()

            form.save()
            
            item_date = item.date_to_publish    #replicated functionality if image is uploaded, but can't assume that is the case
            return HttpResponseRedirect('%s/newsletter/%d/%d/%d/' % (SUBSITE, item_date.year, item_date.month, item_date.day))
    
    form = NewsItemForm(instance=item)
    args = {
        'request': request,
        'item_pk': item_pk,
        'form': form,
        'SUBSITE': SUBSITE,
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
    return HttpResponseRedirect('%s/newsletter/%d/edit/' % (SUBSITE, new_item.pk))

@login_required
def view_item(request, item_pk):
    """this is for viewing a single item
    """
    return HttpResponse('This is where we view item ' + item_pk)

def home(request):
    """this is where I put together the list of items for templating for today's newsletter
    """
    today = datetime.date.today()
    return HttpResponseRedirect("%s/newsletter/%d/%d/%d/" % (SUBSITE, today.year, today.month, today.day))

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
        if item.content:
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
        'SUBSITE': SUBSITE,
        'CDN': CDN,     #included here for when we go live and need a place for people to view the newsletter
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
        if item.content:
            if item_position < 3:
                left_sections[item.position] = item
            elif item_position <= 5:
                right_sections[item.position] = item

    args = {
        'left_sections': left_sections,
        'right_sections': right_sections,
        'date': date.isoformat(),
        'logged_in': False,
        'SUBSITE': SUBSITE,
        'CDN': CDN,
    }
    return render_to_response('rss.xml', args, mimetype='text/xml')
