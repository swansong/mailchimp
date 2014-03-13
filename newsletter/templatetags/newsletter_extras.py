from django import template

register = template.Library()

@register.filter
def thumbnailify(image_url, size):
   index = image_url.rfind('.')
   return image_url[:index] + ".%s" % (size) + image_url[index:]
