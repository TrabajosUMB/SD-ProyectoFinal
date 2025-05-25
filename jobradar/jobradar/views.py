from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class FrontendView(TemplateView):
    template_name = None

    def get_template_names(self):
        template_name = self.kwargs.get('template_name', 'index.html')
        return [template_name]
