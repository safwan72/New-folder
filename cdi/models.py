from django.db import models
from phone_field import PhoneField

class ActiveAdminModel(models.Model):
    app_level = models.CharField(max_length=64)
    model_name = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    base_url = models.CharField(max_length=32)
    is_active = models.BooleanField(default=True)
    icon_name = models.CharField(max_length=255, default='fa fa-building')
    admin = models.BooleanField(default=True)

    def __str__(self):
        return self.model_name

    def create_url(self):
        return self.base_url + '/add/'

    def retrieve_url(self):
        return self.base_url + '/'

    def update_url(self):
        return self.base_url + '/edit/'

    def delete_url(self):
        return self.base_url + '/delete/'


class ActiveCompany(models.Model):
    entry_name = models.CharField(max_length=64)
    email = models.EmailField()
    phone = PhoneField()
    title = models.CharField(max_length=64, null=True, blank=True)
    tagline = models.CharField(max_length=128, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    zip_postal_code = models.CharField(max_length=254)
    about = models.TextField(null=True, blank=True)

    license_key = models.CharField(max_length=25)
    active_period = models.CharField(max_length=30, default='nan')
    domain = models.CharField(max_length=254)

    is_active = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.entry_name
