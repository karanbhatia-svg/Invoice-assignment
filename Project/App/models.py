from django.db import models

# Create your models here.
class Invoice(models.Model):
    Invoice = models.AutoField(primary_key=True)
    CustomerName= models.CharField(max_length=100)  
    Date = models.DateField()

class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    description = models.CharField(max_length=100,blank=True,null=True,default="")
    quantity = models.IntegerField(blank=True,null=True)
    unit_price = models.IntegerField(blank=True,null=True)
    price = models.IntegerField(blank=True,null=True)
