from django.db import models
from django.conf import settings
from django.dispatch import receiver
# from django.db.models.signals import post_init

# Create your models here.

class User(models.Model):
    UserID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    Email = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return str(self.UserID)

# @receiver(post_init, sender=User)
# def my_handler(sender, **kwargs):
#     if sender.slug == '':
#         print('post save callback')

class BTCWallet(models.Model):
    UserID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    BTC = models.CharField(max_length=100, primary_key=True)

    

    def __str__(self):
        return str(self.UserID)

class ETHWallet(models.Model):
    UserID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ETH = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return str(self.UserID)

class LTCWallet(models.Model):
    UserID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    LTC = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return str(self.UserID)