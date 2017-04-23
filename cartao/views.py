from django.views import generic

from cartao import models
from core.views import BaseViewMixin


class CadastrarCompraCartaoView(BaseViewMixin, generic.TemplateView):
    template_name = 'cadastrar-compra-cartao.html'
