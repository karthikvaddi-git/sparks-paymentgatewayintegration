from django.db import models

# Create your models here.
class savenature(models.Model):
    name=models.CharField(max_length=1000)
    email=models.EmailField(max_length=200)
    amount=models.CharField(max_length=500)
    phonenumber=models.CharField(max_length=20)
    paymentid=models.CharField(max_length=1000)
    paid=models.BooleanField(default=False)

    def __str__(self):
        return self.email