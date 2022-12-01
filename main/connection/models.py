from django.db import models
from django.conf import settings

class AccountModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    account_number = models.CharField(max_length=100)




    def __str__(self):
        return self.user.email


class AccountDetail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    acc_id = models.CharField(max_length=100)

    def __str__(self):
        return self.user.email



