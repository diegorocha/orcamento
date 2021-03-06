# coding: utf-8
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from compras.models import ListaCompras
from orcamento.models import Orcamento


class PermissionRequired(PermissionRequiredMixin):
    raise_exception = True
    permission_denied_message = "Você não tem permissão para acessar esse conteúdo"

    def get_permission_required(self):
        if not self.permission_required:
            return ()  # Default é não precisar de nenhuma permissão
        return super(PermissionRequired, self).get_permission_required()

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            self.raise_exception = False
        return super(PermissionRequired, self).handle_no_permission()


class BaseViewMixin(LoginRequiredMixin, PermissionRequired):
    pass


