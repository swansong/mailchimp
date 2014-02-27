from django import forms
from newsletter.models import *
from django.forms import ModelForm
from tinymce.widgets import TinyMCE
from django.utils.safestring import mark_safe
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode
from django.forms.widgets import ClearableFileInput, Input, CheckboxInput

class CustomClearableImageInput(ClearableFileInput):

    def render(self, name, value, attrs=None):
        substitutions = {
            'initial_text': 'Current choice', 
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
            }
        template = '%(input)s'
        substitutions['input'] = Input.render(self, name, value, attrs)

        if value and hasattr(value, "url"):
            template = self.template_with_initial
            substitutions['initial'] = ('<img src="%s" alt="%s"/>'
                                        % (escape(value.url),
                                           escape(force_unicode(value))))
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % substitutions

        return mark_safe(template % substitutions)

class NewsItemForm(ModelForm):
    POSITION_CHOICES = [(0, '0 (Top Left)'), (1, '1 (Middle Left)'), (2, '2 (Bottom Left)'), (3, '3 (Top Right)'), (4, '4 (Middle Right)'), (5, '5 (Bottom Right)'), (6, 'Draft (not published)')]
    title = forms.CharField(max_length=96, required=False)
    content = forms.CharField(max_length=256, widget=TinyMCE(attrs={'cols':60, 'rows':30}), required=True)
    date_to_publish = forms.DateField(required=True)
    position = forms.ChoiceField(widget=forms.RadioSelect, choices=POSITION_CHOICES, required=True)
    image = forms.ImageField(widget=CustomClearableImageInput, required=False)

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
            'image',
        )
        exclude = ('create_date',)
