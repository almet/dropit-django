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
    rev_number = IntegerProperty()

    def __unicode__():
        return self.title+":\n"+self.content

    def save_as_new(self):
        """Save the note as a new one.

        """
        self._id = slugify(self.title)
        self.is_head = True
        self.rev_number = 1
        return super(Note, self).save()

    def save_as_revision_of(self, old_note):
        old_note.is_head = False
        old_note.save()
        rev_number = old_note.rev_number + 1
        self._id = "%s-%s" %(rev_number, old_note.root)
        self.is_head = True
        self.rev_number = rev_number
        self.root_note = old_note.root
        return super(Note, self).save()
   
    @staticmethod
    def get_note(id, rev_id=None):
        """Retreive a note by it's id plus the rev_id if one is provided.
        
        """
        return Note.get(id)

    @property
    def root(self):
        """*always* returns the root note id, even if the note is the root one.
        If the note havent a root_note specified, let's suppose it's the root
        one.

        """
        if self.root_note:
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
