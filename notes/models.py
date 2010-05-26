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
    date = DateTimeProperty(auto_now_add=True)
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

    # -- Revison Work ----------------------------------------------------------

    def has_revisions(self):
        """Tell us if a note has some revisions.

        """
        return len(self.revisions) > 1

    @property
    def revisions_count(self):
        return len(self.revisions)

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

    def get_revision_id(self, rev_number):
        return "%s-%s" % (rev_number, self.root) if rev_number != 1 else self.root

    def get_by_rev_number(self, rev_number):
        return Note.get(self.get_revision_id(rev_number))
    
    def has_next(self):
        return self.has_revisions() and self.rev_number != self.revisions_count

    def next(self):
        if self.has_next():
            return Note.get(self.next_id())
        return None

    def has_previous(self):
        return not(self.rev_number == 1)

    def previous(self):
        if self.has_previous():
            return Note.get(self.previous_id())
        return None

    def next_id(self):
        if self.has_next():
            return self.get_revision_id(self.rev_number +1)
        return None
    
    def previous_id(self):
        if self.has_previous():
            return self.get_revision_id(self.rev_number -1)
        return None
