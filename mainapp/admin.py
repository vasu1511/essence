from django.contrib import admin
from .models import *

     
@admin.register(maincategory)
class maincategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(subcategory)
class subcategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(brand)
class brandAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(product)
class productAdmin(admin.ModelAdmin):
    list_display = ("id", "name","Maincategory","Subcategory","Brand","color","size","baseprice","discount","finalprice","stock","pic1","pic2","pic3","pic4")

@admin.register(buyer)
class buyerAdmin(admin.ModelAdmin):
    list_display = ("id","name","username","email","phone","addressline1","addressline2","addressline3","pin","city","state")

@admin.register(checkout)
class checkoutAdmin(admin.ModelAdmin):
    list_display = ("id","user","orderstatus","paymentstatus","paymentmode","rppid","totalamount","shippingamount","finalamount","time")


@admin.register(checkoutproducts)
class checkoutproductsAdmin(admin.ModelAdmin):
    list_display = ("id","Checkout","pid","name","color","size","price","qty","total","pic")


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("id", "user","Product")


@admin.register(contactUs)
class contactUsAdmin(admin.ModelAdmin):
    list_display = ("id", "name","email","phone","subject","message","status","date")