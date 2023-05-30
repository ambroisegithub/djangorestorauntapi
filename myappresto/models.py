from django.db import models
 
# Create your models here.

# relational serializer
class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255)
    
    def __str__(self) ->  str:
        return self.title
 
class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    invertory = models.SmallIntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT,default=1)
    def __str__(self) ->  str:
        return self.title  
    

         
class MenuItem1(models.Model):
    Title = models.CharField(max_length=255)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Invertory = models.SmallIntegerField()
        