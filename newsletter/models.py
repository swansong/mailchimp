from django.db import models

# Create your models here.

class NewsItem(models.Model):
    """NewsItems contain all the content and date to publish for the newsletter sections
    """
    title = models.CharField(max_length=96, blank=True)
    content = models.TextField(max_length=256, blank=True)
    date_to_publish = models.DateField(null=True)
    create_date = models.DateField(auto_now_add=True)
    position = models.IntegerField(blank=True)

    def __unicode__(self):
        return(self.pk + ': ' + self.title + ' ' + self.date_to_publish)

class NewsImage(models.Model):
    """NewsImages are the images associated with a NewsItem
    """
    news_item = models.ForeignKey(NewsItem)
    image = models.ImageField(upload_to='static/newsletter/screenshots/', null=True, blank=True)

    def __unicode__(self):
        return(self.pk)
