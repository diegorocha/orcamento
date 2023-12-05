# coding: utf-8
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.urls import reverse
from django.views import generic


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
    def get_admin_url(self):
        if hasattr(self, 'object') and hasattr(self.object, '_meta'):
            return reverse(
                f'admin:{self.object._meta.app_label}_{self.object._meta.model_name}_change',
                args=(self.object.id,),
            )

    def get_context_data(self, **kwargs):
        context = super(BaseViewMixin, self).get_context_data(**kwargs)
        context['admin_url'] = self.get_admin_url()
        return context


class HealthCheckView(generic.View):
    def get(self, request):
        return JsonResponse({"status": "OK"}, status=200)
