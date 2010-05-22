from couchdbkit.ext.django.schema import *
from datetime import datetime
from django.template.defaultfilters import slugify

class Note(Document):
    """Represents Note documents and revision documents.
    
    """
    title = StringProperty(required=True)
    content = StringProperty(required=True)
    tags = ListProperty()
#    content_format = StringProperty()
    doc_type = 'http://dropit.notmyidea.org/note'
    date = DateTimeProperty(auto_now=True)
    is_head = BooleanProperty()
    root_note = StringProperty()

    def __unicode__():
        return self.title+":\n"+self.content

    def save_as_new(self):
        self._id = slugify(self.title)
        self.is_head = True
        return super(Note, self).save()
   
    @staticmethod
    def get_note(id, rev_id=None):
        """Retreive a note by it's id plus the rev_id if one is provided.
        
        """
        return Note.get(id)

    @property
    def root(self):
        """*always* returns the parent note id.

        """
        if self.is_head and self.root_note:
            return self.root_note
        else:
            return self._id

    def has_revisions(self):
        """Tell us if a note has some revisions.

        """
        return len(self.revisions) > 1

    @property
    def revisions(self):
        """Return all revisions for a specific note.

        For this, we use a map/reduce view. The map returns all revisions, the
        reduce filter to just return the one attached to the specific note we 
        want

        """
        if not hasattr(self, '_revisions'):
            self._revisions = Note.view('notes/history', startkey=[self.root], endkey=[self.root, []])
        return self._revisions
