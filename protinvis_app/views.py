from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.exceptions import ValidationError

from .forms import ProtInvis_SessionForm
from .create_plot import ploter

class Index(View):
    template = 'protinvis_app/index.html'

    def get(self, request):
        form = ProtInvis_SessionForm()
        return render(request, self.template, context={'form': form})

    def post(self, request):
        bound_form = ProtInvis_SessionForm(request.POST)

        if bound_form.is_valid():
            # new_ps = bound_form.save()
            graphJSON = ploter(bound_form.cleaned_data['uniprot_id'], bound_form.cleaned_data['the_dye'])
            if isinstance(graphJSON, str):
                raise ValidationError(f"{graphJSON} not found")
            request.session['graphJSON'] = graphJSON
            return redirect(result)
        return render(request, self.template, context={'form': bound_form})

def result(request):
    template = 'protinvis_app/result.html'
    graphJSON = request.session.get('graphJSON')
    return render(request, template, context={'graphJSON': graphJSON})
