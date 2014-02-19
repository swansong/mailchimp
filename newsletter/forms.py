from django import forms
from newsletter.models import *
from django.forms import ModelForm

class NewsItemForm(ModelForm):
    POSITION_CHOICES = [(0, '0 (Top Left)'), (1, '1 (Middle Left)'), (2, '2 (Bottom Left)'), (3, '3 (Top Right)'), (4, '4 (Middle Right)'), (5, '5 (Bottom Right)')]
    title = forms.CharField(max_length=96, required=False)
    content = forms.CharField(max_length=256, widget=forms.Textarea, required=True)
    date_to_publish = forms.DateField(required=True)
    position = forms.ChoiceField(widget=forms.RadioSelect, choices=POSITION_CHOICES, required=True)

    def save(self, *args, **kwargs):
        instance = ModelForm.save(self, *args, **kwargs)
        return instance

    class Meta:
        model = NewsItem
        fields = (
            'title',
            'content',
            'date_to_publish',
            'position',
        )
        exclude = ('create_date',)
