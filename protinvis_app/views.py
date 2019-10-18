from django.shortcuts import render, redirect
from django.views.generic import View

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
            graphJSON = ploter(bound_form.cleaned_data['uniprot_id'], bound_form.cleaned_data['the_dye'])

            if graphJSON.startswith('{'):
                request.session['graphJSON'] = graphJSON
                bound_form.save()
                return redirect(result)
            else:
                error_message = f"{graphJSON} not found"
                bound_form.add_error(field='uniprot_id', error=error_message)
            
        return render(request, self.template, context={'form': bound_form})

def result(request):
    graphJSON = request.session.get('graphJSON')

    if not graphJSON is None:  
        template = 'protinvis_app/result.html'
        return render(request, template, context={'graphJSON': graphJSON})
    
    return redirect('Index')
