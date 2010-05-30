from couchdbkit.ext.django.forms import *
from django import forms
from django.conf import settings

from notes.models import Note
from notes.widgets import CommaSeparatedList

class NoteForm(DocumentForm):
    title = forms.CharField()
    content = forms.CharField(
        widget=forms.widgets.Textarea(attrs={'class': 'span-18'})
    )
    
    tags =  forms.CharField(widget=CommaSeparatedList())
#    format = forms.ChoiceField(choices=settings.NOTES_FORMATS)
    
    def clean_tags(self):
        """Convert a comma separated list to a python list.
        
        """
        return [unicode(tag.strip()) for tag in self.cleaned_data['tags'].split(',')]
    
    class Meta:
        document = Note

