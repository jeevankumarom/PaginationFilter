from django.db import models

# Create your models here.


class categories(models.Model):
    category_name=models.CharField(max_length=100,unique=True)
    date=models.DateTimeField()


class category_list(models.Model):
    cat_id=models.ForeignKey(categories,on_delete=models.CASCADE)
    brand=models.TextField()
    datetime=models.DateTimeField()
    originalprice=models.FloatField(default=0)
    price=models.FloatField(default=0)
    discount=models.CharField(max_length=100)
    rating=models.CharField(max_length=10)