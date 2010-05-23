from django.forms.widgets import TextInput

class CommaSeparatedList(TextInput):
    def render(self, name, value, attrs=None):
        value = ", ".join(value) if value else None
        return super(CommaSeparatedList, self).render(name, value, attrs)
