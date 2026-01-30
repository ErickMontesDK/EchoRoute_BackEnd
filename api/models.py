from django.db import models

# Create your models here.
class Client(models.Model):
    no_client = models.IntegerField()
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    # observations = models.TextField() #TODO: Not implemented yet


class Visit(models.Model):
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    deliver = models.ForeignKey('users.User', on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now_add=True)
    latitude_registered = models.FloatField()
    longitude_registered = models.FloatField()
    flag = models.BooleanField(default=False)
    # sale = models.BooleanField(default=False) #TODO: Not implemented yet









    

    
    