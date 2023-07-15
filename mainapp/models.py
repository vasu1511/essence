from django.db import models

# Create your models here.
class buyer(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=30)
    username=models.CharField(max_length=50)
    email=models.EmailField(max_length=40)
    phone=models.CharField(max_length=15)
    addressline1=models.CharField(max_length=30)
    addressline2=models.CharField(max_length=30)
    addressline3=models.CharField(max_length=30)
    pin=models.CharField(max_length=10)
    city=models.CharField(max_length=30)
    state=models.CharField(max_length=30)
    pic=models.ImageField(upload_to='user')
    otp=models.IntegerField(default=15111999)

    def __str__(self):
        return self.username+'/'+self.name+'/'+self.email
    

class maincategory(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=30,unique=True)

    def __str__(self):
        return self.name

class subcategory(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=30,unique=True)

    def __str__(self):
        return self.name


class brand(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=30,unique=True)
    pic=models.ImageField(upload_to='brand')

    def __str__(self):
        return self.name


class product(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=30)
    Maincategory=models.ForeignKey("maincategory", on_delete=models.CASCADE)
    Subcategory=models.ForeignKey("subcategory", on_delete=models.CASCADE)
    Brand=models.ForeignKey("brand", on_delete=models.CASCADE)
    color=models.CharField(max_length=20)
    size=models.CharField(max_length=10)
    baseprice=models.IntegerField()
    discount=models.IntegerField()
    finalprice=models.IntegerField()
    stock=models.BooleanField(default=True)
    description=models.TextField(default='THIS IS SAMPLE PRODUCT')
    pic1=models.ImageField(upload_to="product")
    pic2=models.ImageField(upload_to="product")
    pic3=models.ImageField(upload_to="product",default="",blank=True,null=True)
    pic4=models.ImageField(upload_to="product",default="",blank=True,null=True)

    def __str__(self):
        return self.name
    
status=((0,'order placed'),(1,'not packed'),(2,'packed'),(3,'Ready to Ship'),(4,'Shipped'),(5,'Out For Delivery'),(6,'Delivered'),(7,'Cancelled'))
payment=((0,'Pending'),(1,'Done'))
mode=((0,'COD'),(1,'Net Banking'))

class checkout(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(buyer,on_delete=models.CASCADE)
    orderstatus=models.IntegerField(choices=status,default=0)
    paymentmode=models.IntegerField(choices=mode,default=0)
    paymentstatus=models.IntegerField(choices=payment,default=0)
    rppid=models.CharField(max_length=50,default="",null=True,blank=True)
    totalamount=models.IntegerField()
    shippingamount=models.IntegerField()
    finalamount=models.IntegerField()
    time=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class checkoutproducts(models.Model):
    id=models.AutoField(primary_key=True)
    Checkout=models.ForeignKey(checkout,on_delete=models.CASCADE)
    pid=models.IntegerField(default=None)
    name=models.CharField(max_length=50)
    color=models.CharField(max_length=50)
    size=models.CharField(max_length=50)
    price=models.IntegerField()
    qty=models.IntegerField()
    total=models.IntegerField()
    pic=models.CharField(max_length=50)

class Wishlist(models.Model):
    id = models.AutoField(primary_key=True)
    Product = models.ForeignKey(product,on_delete=models.CASCADE)
    user = models.ForeignKey(buyer,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username+" "+self.Product.name

status = ((0,"Active"),(1,"Done"))
class contactUs(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    subject = models.TextField()
    message = models.TextField()
    status = models.IntegerField(choices=status,default=0)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)+" "+self.name+" "+self.email
