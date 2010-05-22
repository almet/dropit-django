from django.shortcuts import render_to_response as render, redirect
from django.template import RequestContext, loader, Context 
from django.utils.encoding import smart_str, force_unicode

from couchdbkit.ext.django.loading import get_db

from notes.forms import NoteForm 
from notes.models import Note
from utils.shortcuts import get_object_or_404


def list_notes(request):
    """List all notes documents present on the couch DB.

    """
    notes = Note.view('notes/heads')
    return render("list_notes.html", {
        "notes": notes,
    })

def show_note(request, note_id, rev=None):
    """Display a note in detail.

    Here, we work with formats, but it's considered as an advanced feature.
    Formats can be not implemented in others clients.

    """
    # get the note.
    note = get_object_or_404(Note, note_id, rev=rev)
    return render("show_note.html", {
        'note': note,
    })

def add_note(request):
    """Add a note
        - GET request display the form
        - POST request create the note and redirect if the add is successful
    """
    note = None

    if request.POST:
        form = NoteForm(request.POST)
        if form.is_valid():
            # get the new instance from the model, and save it as a new one.
            note = form.save(commit=False)
            note.save_as_new()
            return redirect('notes:list')
    else:
        form = NoteForm()

    return render("add_note.html", {
        "form": form,
        "note": note
    })

def edit_note(request, note_id):
    """Edit a note. This creates a new revision and bump the """
    rev_id = request.POST.get("revid", None)
    
    note = Note.get_note(note_id, rev_id)
    if request.method == "POST":
        form = NoteForm(data=request.POST)
        form.save()
    else:        
        note = get_object_or_404(Note, note_id, rev_id)
        form = NoteForm(initial=note)
    
    return render("edit_note.html", {
        "form": form,
    })

def delete_note(request, note_id):
    """Delete a note and redirect to the list of notes

    """
    pass
