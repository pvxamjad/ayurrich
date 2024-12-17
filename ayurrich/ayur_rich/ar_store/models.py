from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"




class ProductRegistration(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="products")
    # second_image =models.ImageField(upload_to="products",null=True)
    # third_image =models.ImageField(upload_to="products",null=True)
    description = models.CharField(max_length=500)
    health_benefits = models.CharField(max_length=500,null=True)
    quantity = models.IntegerField(null=False,blank=False)
    category = models.ForeignKey(Category , on_delete=models.CASCADE,default=1)
    price = models.DecimalField(decimal_places=2,null=False,blank=False,max_digits=10)
    discount_price = models.DecimalField(decimal_places=2,null=False,blank=False,max_digits=10)
    date_added = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.name} - {self.category}"
    

class Contact(models.Model):
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    date_added = models.DateTimeField(auto_now_add=True,blank=True,null=True)


    def __str__(self):
        return f"{self.email} - {self.phone}"



