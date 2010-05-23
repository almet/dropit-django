from django.conf.urls.defaults import *

urlpatterns = patterns('notes.views',
    (r'^$', 'list_notes', {}, 'list'),
    (r'^new/$', 'add_note', {}, 'add'),
    (r'show/(?P<note_id>.+)/$', 'show_note', {}, 'show'),
    (r'show/(?P<note_id>.+)/(?P<rev>.+)$', 'show_note', {}, 'show'),
    (r'delete/(?P<note_id>.+)/$', 'delete_note', {}, 'delete'),
    (r'edit/(?P<note_id>.+)/$', 'edit_note', {}, 'edit'),
    (r'tag/(?P<tag_name>.+)/$', 'show_tag', {}, 'tag'),
    (r'tags/$', 'list_tags', {}, 'tags'),
)
