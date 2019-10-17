from django import forms
from .models import ProtInvis_Session

from .constants import dyes_for_form


class ProtInvis_SessionForm(forms.Form):
    uniprot_id = forms.CharField(max_length=1000)
    the_dye = forms.ChoiceField(choices=dyes_for_form)

    def save(self):
        new_session = ProtInvis_Session.objects.create(
            uniprot_id=self.cleaned_data['uniprot_id'],
            the_dye=self.cleaned_data['the_dye'],
            )
        return new_session
        