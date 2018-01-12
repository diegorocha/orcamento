from django.contrib.auth.mixins import LoginRequiredMixin

from compras.models import ListaCompras
from orcamento.models import Orcamento


class BaseViewMixin(LoginRequiredMixin):
    pass


