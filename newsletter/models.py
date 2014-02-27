from django.db import models

# Create your models here.

class NewsItem(models.Model):
    """NewsItems contain all the content and date to publish for the newsletter sections
    """
    title = models.CharField(max_length=96, blank=True)
    content = models.TextField(max_length=256, blank=True)
    date_to_publish = models.DateField(null=True)
    create_date = models.DateField(auto_now_add=True)
    position = models.IntegerField(blank=True, null=True, default=0)
    image = models.ImageField(upload_to='uploads/img/', null=True, blank=True)

    def __unicode__(self):
        date = self.date_to_publish.isoformat()
        return "%d: %s to be published on %s" % (self.pk, self.title, date)
