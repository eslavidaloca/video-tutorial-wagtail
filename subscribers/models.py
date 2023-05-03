from django.db import models

# Create your models here.

class Subscribers(models.Model):
    email =  models.CharField(blank=False, null=False, max_length=100, help_text='Direccion de correo')
    full_name = models.CharField(blank=False, null=False, max_length=100, help_text='Nombre completo')
    
    """ String representation of this object """
    def __str__(self) -> str:
        return self.full_name
    
    class Meta:
        verbose_name = "Subscriber"
        verbose_name_plural = "Subscribers"