from django.shortcuts import redirect
from django.template import RequestContext, loader, Context 
from django.utils.encoding import smart_str, force_unicode
from django.utils.translation import ugettext_lazy as _

from couchdbkit.ext.django.loading import get_db
from couchdbkit.resource import ResourceConflict

from notes.shortcuts import render_to_response as render
from notes.forms import NoteForm 
from notes.models import Note
from utils.shortcuts import get_object_or_404


def list_notes(request):
    """List all notes documents present on the couch DB.

    """
    notes = Note.view('notes/heads') or None
    return render("list_notes.html", {
        "notes": notes,
    }, request)

def show_note(request, note_id):
    # get the note.
    note = get_object_or_404(Note, note_id)
    return render("show_note.html", {
        'note': note,
    }, request)

def add_note(request):
    note = None
    if request.POST:
        form = NoteForm(request.POST)
        if form.is_valid():
            # get the new instance from the model, and save it as a new one.
            try:
                note = form.save(commit=False)
                note.save_as_new()
                return redirect('notes:list')
            except ResourceConflict:
                form.errors['title'] = _("The title must be unique. Please choose another one")
    else:
        form = NoteForm()

    return render("add_note.html", {
        "form": form,
        "note": note
    }, request)

def edit_note(request, note_id):
    """Edit a note. This creates a new revision and bump the head to this new one"""
    # get the old note
    old_note = get_object_or_404(Note, note_id)

    if request.method == "POST":
        # get the new one from the form
        form = NoteForm(data=request.POST)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.save_as_revision_of(old_note)
            return redirect("notes:list")
    else:        
        form = NoteForm(initial=old_note)
    
    return render("edit_note.html", {
        "form": form,
    }, request)

def delete_note(request, note_id):
    """Delete a note and redirect to the list of notes.

    Here, we entierly delete the note and it's revisions.
    DO NOT USE TO JUST REMOVE A REVISION, IT WILL DESTROY ALL INFORMATION
    RELATED TO THIS NOTE.

    """
    note = Note.get_note(note_id)
    notes = Note.view("notes/by_root", startkey=note.root, endkey=[note.root, []])
    for note in notes:
        note.delete()
    return redirect('notes:list')

def show_tag(request, tag_name):
    """Display a list of notes related to a special tag.

    """
    notes = Note.view("notes/by_tag", startkey=tag_name, endkey=tag_name)
    return render("list_notes.html", {
        "tag_name": tag_name,
        "notes": notes,
    }, request)

def list_tags(request):
    """List all tags, with a ponderation, into a tag cloud
    
    """
    tags = Note.view("notes/tags", group=True)
    factor = float(max([int(t['value']) for t in tags])) / 10

    tags = [{
        'key': t['key'], 
        'value': int(round(float(t['value'])/factor))
    } for t in tags]
    return render("list_tags.html", {
        'tags': tags,
    }, request)

