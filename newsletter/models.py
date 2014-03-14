from django.db import models
#from django.core.files.storage import Storage

#class CustomStorageOverride(FileSystemStorage):
#    """this is a custom storage class that will prevent duplicate files from being created
#    """
#    def get_available_name(self, name):
#        return name
#
#    def _save(self, name, content):
#        if self.exists(name):
#            return name
#        else:
#            return super(CustomStorageOverride, self)._save(name, content)


class NewsItem(models.Model):
    """NewsItems contain all the content and date to publish for the newsletter sections
    """
    title = models.CharField(max_length=96, blank=True)
    content = models.TextField(max_length=512, blank=True)
    date_to_publish = models.DateField(null=True)
    create_date = models.DateField(auto_now_add=True)
    position = models.IntegerField(blank=True, null=True, default=0)
    image = models.ImageField(upload_to='img/%Y/%m', null=True, blank=True)

    def __unicode__(self):
        date = self.date_to_publish.isoformat()
        return "%d: %s to be published on %s" % (self.pk, self.title, date)
