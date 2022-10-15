from django.db import models
from administration_app.models import Admin
# Create your models here.
class Showroom(models.Model):
    license_number=models.CharField(max_length=10)
    created_by=models.ForeignKey(Admin, related_name='showrooms',on_delete=models.CASCADE)
    name=models.CharField(max_length=45)
    email=models.CharField(max_length=45)
    password=models.CharField(max_length=255)
    payment=models.CharField(max_length=45)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
class Brand(models.Model):
    name=models.CharField(max_length=45)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class BrandModel(models.Model):
    brand=models.ForeignKey(Brand,related_name='models',on_delete=models.CASCADE)
    name=models.CharField(max_length=45)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Car(models.Model):
    vin=models.CharField(max_length=17)
    showroom=models.ForeignKey(Showroom,related_name="cars",on_delete=models.CASCADE)
    model=models.ForeignKey(BrandModel,related_name='cars',on_delete=models.CASCADE)
    prod_date=models.DateField()
    color=models.CharField(max_length=45)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    # def delete(self, *args, **kwargs):
    #     self.documents.delete()
    #     super().delete(*args,**kwargs)

class DocumentType(models.Model):
    type=models.CharField(max_length=45)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Document(models.Model):
    car=models.ForeignKey(Car,related_name='documents',on_delete=models.CASCADE)
    type=models.ForeignKey(DocumentType,related_name='documents',on_delete=models.CASCADE)
    doc=models.FileField(upload_to='documents/%Y/%m/%d/')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def delete(self, *args, **kwargs):
        self.doc.delete()
        super().delete(*args,**kwargs)