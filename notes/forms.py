from couchdbkit.ext.django.forms import *
from django import forms
from django.conf import settings

from notes.models import Note
from notes.widgets import CommaSeparatedList

class NoteForm(DocumentForm):
    """Form to create a note.
    
    """
    
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


class NoteEditForm(DocumentForm):
    """Form to edit a note.
    This one is a bit different of the creation form, because we need to now
    if the saved revision must become the new head, and some others differents 
    things.
    
    """
    
    title = forms.CharField()
    content = forms.CharField(
        widget=forms.widgets.Textarea(attrs={'class': 'span-18'})
    )
    
    tags = forms.CharField()
#    is_head = forms. 
#    format = forms.ChoiceField(choices=settings.NOTES_FORMATS)
    
    def clean_tags(self):
        """Convert a comma separated list to a python list.
        
        """
        return [unicode(tag.strip()) for tag in self.cleaned_data['tags'].split(',')]
    
    class Meta:
        document = Note
