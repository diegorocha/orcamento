from model_mommy import mommy
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse


class LoginRequiredMixin(TestCase):
    def setUp(self):
        super(LoginRequiredMixin, self).setUp()
        username = 'admin'
        password = '4dm1n'
        user = User.objects.create_superuser(username=username, password=password, email='')
        token = Token()
        token.user = user
        token.save()
        self.client.login(username=username, password=password)


class ModelViewSetTestCase(APITestCase):
    url_base_name = None
    model_name = None

    def setUp(self):
        self.endpoint = reverse('%s-list' % self.url_base_name) if self.url_base_name else None

    def get_detail_endpoint(self, pk):
        return reverse('%s-detail' % self.url_base_name, args=(pk,)) if self.url_base_name else None

    def create_data(self):
        return {}

    def update_data(self):
        return {}

    def test_list(self):
        if self.model_name:
            mommy.make(self.model_name, _fill_optional=True, _quantity=20)
            count = self.model_name.objects.count()
            response = self.client.get(self.endpoint)
            self.assertEquals(response.status_code, 200)
            data = response.json()
            self.assertEquals(len(data), count)

    def test_create(self):
        if self.model_name:
            response = self.client.post(self.endpoint, self.create_data(), format='json')
            self.assertEquals(response.status_code, 201)
            data = response.json()
            pk = data["id"]
            instance = self.model_name.objects.filter(pk=pk).first()
            self.assertIsNotNone(instance)

    def test_retrieve(self):
        if self.model_name:
            instance = mommy.make(self.model_name, _fill_optional=True)
            response = self.client.get(self.get_detail_endpoint(instance.pk))
            self.assertEquals(response.status_code, 200)
            data = response.json()
            self.assertIsNotNone(data)

    def test_update(self):
        if self.model_name:
            instance = mommy.make(self.model_name, _fill_optional=True)
            detail_endpoint = self.get_detail_endpoint(instance.pk)
            response = self.client.get(detail_endpoint)
            self.assertEquals(response.status_code, 200)
            data = response.json()
            new_data = self.update_data()
            data.update(new_data)
            response = self.client.put(detail_endpoint, data, format='json')
            self.assertEquals(response.status_code, 200)
            updated_instance = self.model_name.objects.get(pk=instance.pk)
            for key, value in new_data.items():
                self.assertEquals(getattr(updated_instance, key), value)

    def test_partial_update(self):
        if self.model_name:
            instance = mommy.make(self.model_name, _fill_optional=True)
            detail_endpoint = self.get_detail_endpoint(instance.pk)
            new_data = self.update_data()
            response = self.client.patch(detail_endpoint, new_data, format='json')
            self.assertEquals(response.status_code, 200)
            updated_instance = self.model_name.objects.get(pk=instance.pk)
            for key, value in new_data.items():
                self.assertEquals(getattr(updated_instance, key), value)

    def test_delete(self):
        if self.model_name:
            instance = mommy.make(self.model_name, _fill_optional=True)
            detail_endpoint = self.get_detail_endpoint(instance.pk)
            response = self.client.delete(detail_endpoint)
            self.assertEquals(response.status_code, 204)
            deleted_instance = self.model_name.objects.filter(pk=instance.pk).first()
            self.assertIsNone(deleted_instance)
