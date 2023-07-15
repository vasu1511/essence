from django.shortcuts import render,HttpResponseRedirect
from.models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from essence.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY
import razorpay
from random import randint

# Create your views here.
def home(request):
    data=product.objects.all()
    data=data[::-1]
    data=data[0:10]
    Brand=brand.objects.all()
    Subcategory=subcategory.objects.all()
    Maincategory=maincategory.objects.all()
    return render(request,'index.html',{'data':data,'brand':Brand,'subcategory':Subcategory,'maincategory':Maincategory})

@login_required(login_url='/login/')
def checkoutpage(request):
    user=User.objects.get(username=request.user.username)
    if(user.is_superuser):
        return HttpResponseRedirect('/admin/')
    else:
        Buyer=buyer.objects.get(username=request.user.username)
    total = request.session.get("total",0)
    if(total==0):
        return HttpResponseRedirect("/cart/")
    Brand = brand.objects.all()
    Subcategory = subcategory.objects.all()
    Maincategory = maincategory.objects.all()
    return render(request,"checkout.html",{'data':Buyer,'maincategory':Maincategory,'subcategory':Subcategory,'brand':Brand})

client = razorpay.Client(auth=(RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY))
@login_required(login_url='/login/')
def placeorder(request):
    user=User.objects.get(username=request.user.username)
    if(user.is_superuser):
        return HttpResponseRedirect('/admin/')
    else:
        total=request.session.get('total',0)
        if(total):
            shipping=request.session.get('shipping',0)
            final=request.session.get('final',0)
            Buyer=buyer.objects.get(username=request.user.username)
            Checkout=checkout()
            Checkout.user=Buyer
            Checkout.totalamount=total
            Checkout.shippingamount=shipping
            Checkout.finalamount=final
            Checkout.save()
            cart=request.session.get('cart')
            for key,value in cart.items():
                Checkoutproducts=checkoutproducts()
                Checkoutproducts.Checkout=Checkout
                Checkoutproducts.pid=int(key)
                Checkoutproducts.name=value['name']
                Checkoutproducts.color=value['color']
                Checkoutproducts.size=value['size']
                Checkoutproducts.price=value['price']
                Checkoutproducts.qty=value['qty']
                Checkoutproducts.total=value['total']
                Checkoutproducts.pic=value['pic']
                Checkoutproducts.save()
                #return HttpResponseRedirect('/confirmation/')
            request.session['cart']={}
            request.session['total']=0
            request.session['shipping']=0
            request.session['final']=0
            request.session['cartCount']=0

            mode = request.POST.get("mode")
            if(mode=='COD'):
                return HttpResponseRedirect('/confirmation/')
           
            else:
                orderAmount = Checkout.finalamount*100
                orderCurrency = "INR"
                paymentOrder = client.order.create(dict(amount=orderAmount,currency=orderCurrency,payment_capture=1))
                paymentId = paymentOrder['id']
                Checkout.paymentmode= int(1) #"Net Banking"
                Checkout.save()
                return render(request,"pay.html",{
                    "amount":orderAmount,
                    "api_key":RAZORPAY_API_KEY,
                    "order_id":paymentId,
                    "User":Buyer
                })
        else:
            return HttpResponseRedirect('/cart/')

@login_required(login_url='/login/')
def paymentsuccess(request,rppid,):
    Buyer=buyer.objects.get(username=request.user)
    check=checkout.objects.filter(Buyer=Buyer)
    check=check[::-1]
    check=check[0]
    check.rppid=rppid
    #check.rpoid=rpoid
    #check.rpsid=rpsid
    check.paymentstatus=1
    check.save()
    return HttpResponseRedirect('/confirmation/')


@login_required(login_url="/login/")
def confirmationpage(request):
    username=request.user.username
    if(username):
        try:
            Buyer = buyer.objects.get(username=username)
            subject = 'Order Has Been Placed- Team Essence'
            message = "Thank to Shop With US!!! Your Order Has Been Placed!!! Now You Can Track Your Order in Profile Section"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [Buyer.email, ]
            send_mail( subject, message, email_from, recipient_list )
            Brand = brand.objects.all()
            Subcategory = subcategory.objects.all()
            Maincategory = maincategory.objects.all()
            return render(request,"confirmation.html",{'maincategory':Maincategory,'subcategory':Subcategory,'brand':Brand})
        except: 
            return HttpResponseRedirect("/shop/All/All/All")
    else:
        return HttpResponseRedirect("/shop/All/All/All")

   
def contact(request):
    if(request.method=="POST"):
        c = contactUs()
        c.name = request.POST.get("name")
        c.email = request.POST.get("email")
        c.phone = request.POST.get("phone")
        c.subject = request.POST.get("subject")
        c.message = request.POST.get("message")
        c.save()
        messages.success(request,"Thanks to Share Your Query With Us. Our Team Will Contact You Soon!!!")
    Brand = brand.objects.all()
    Subcategory = subcategory.objects.all()
    Maincategory = maincategory.objects.all()
    return render(request,"contact.html",{'maincategory':Maincategory,'subcategory':Subcategory,'brand':Brand})

def shop(request,mc,sc,br):
    if(mc=='All' and sc=='All' and br=="All"):
        data=product.objects.all()
    elif(mc!='All'and sc=='All' and br=='All'):
        data=product.objects.filter(Maincategory=maincategory.objects.get(name=mc))
    elif(mc=='All'and sc!='All' and br=='All'):
        data=product.objects.filter(Subcategory=subcategory.objects.get(name=sc))
    elif(mc=='All'and sc=='All' and br!='All'):
        data=product.objects.filter(Brand=brand.objects.get(name=br))
    elif(mc!='All'and sc!='All' and br=='All'):
        data=product.objects.filter(Maincategory=maincategory.objects.get(name=mc),Subcategory=subcategory.objects.get(name=sc))

    elif(mc!='All'and sc=='All' and br!='All'):
        data=product.objects.filter(Maincategory=maincategory.objects.get(name=mc),Brand=brand.objects.get(name=br))

    elif(mc=='All'and sc!='All' and br!='All'):
        data=product.objects.filter(Brand=brand.objects.get(name=br),Subcategory=subcategory.objects.get(name=sc))
    else :
        data=product.objects.filter(Maincategory=maincategory.objects.get(name=mc),Brand=brand.objects.get(name=br),Subcategory=subcategory.objects.get(name=sc))
    
    count=len(data)
    data=data[::-1]
    Maincategory=maincategory.objects.all()
    Subcategory=subcategory.objects.all()
    Brand=brand.objects.all()
    return render(request,'shop.html',{'data':data,'maincategory':Maincategory,'subcategory':Subcategory,'brand':Brand,'mc':mc,'sc':sc,'br':br,'count':count})
    #return render(request,'shop.html')

def singleproduct(request,num):
    data=product.objects.get(id=num)
    Brand = brand.objects.all()
    Subcategory = subcategory.objects.all()
    Maincategory = maincategory.objects.all()
    return render(request,'single-product-details.html',{'data':data,'maincategory':Maincategory,'subcategory':Subcategory,'brand':Brand})

def loginpage(request):
    if(request.method=='POST'):
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if(user is not None):
            login(request,user)
            if(user.is_superuser):
                return HttpResponseRedirect('/admin')
            else:
                return HttpResponseRedirect('/profile')
        else:
            messages.error(request,'Invalid Username or Password')
    Brand = brand.objects.all()
    Subcategory = subcategory.objects.all()
    Maincategory = maincategory.objects.all()
    return render(request,'login.html',{'maincategory':Maincategory,'subcategory':Subcategory,'brand':Brand})


 

def signup(request):
    if(request.method=="POST"):
        username=request.POST.get("username")
        name=request.POST.get("name")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        password=request.POST.get("password")
        cpassword=request.POST.get("cpassword")
        if(password==cpassword):
            try:
                user=User(username=username)
                user.set_password(password)
                user.save()
                Buyer=buyer()
                Buyer.name=name
                Buyer.username=username
                Buyer.email=email
                Buyer.phone=phone
                Buyer.password=password
                Buyer.save()
                subject = 'Account is Created- Team Essence'
                message = "Thanks to Create an Account With US!!! Now You can buy our latest and awesome products"
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [Buyer.email, ]
                send_mail( subject, message, email_from, recipient_list )
                return HttpResponseRedirect("/login")
            except:
                messages.error(request,'username already exist')
        else:
            messages.error(request,'password and confirm password does not match')
        Brand=brand.objects.all()
        Subcategory=subcategory.objects.all()
        Maincategory=maincategory.objects.all
        return render(request,"signup.html",{'maincategory':Maincategory,'subcategory':Subcategory,'brand':Brand})

    return render(request,'signup.html')

def logoutpage(request):
    logout(request)
    return HttpResponseRedirect('/login/')

@login_required(login_url="/login/")
def profile(request):
    user=User.objects.get(username=request.user.username)
    if(user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        Buyer=buyer.objects.get(username=request.user.username)
        wishlist = Wishlist.objects.filter(user=Buyer)
        orders = []
        checkouts = checkout.objects.filter(user=Buyer)
        for item in checkouts:
            cp = checkoutproducts.objects.filter(Checkout=item)
            data = {
                'Checkout':item,
                'Checkoutproducts':cp
            }
            orders.append(data)
        Brand = brand.objects.all()
        Subcategory = subcategory.objects.all()
        Maincategory = maincategory.objects.all()
        return render(request,"profile.html",{'data':Buyer,'Wishlist':wishlist,'orders':orders,'maincategory':Maincategory,'subcategory':Subcategory,'brand':Brand})
    #return render(request,'profile.html',{'data':Buyer})

@login_required(login_url="/login/")
def updatepage(request):
    user=User.objects.get(username=request.user.username)
    if(user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        Buyer=buyer.objects.get(username=request.user.username)
        if(request.method=="POST"):
            Buyer.name=request.POST.get("name")
            Buyer.email=request.POST.get("email")
            Buyer.phone=request.POST.get("phone")
            Buyer.addressline1=request.POST.get("addressline1")
            Buyer.addressline2=request.POST.get("addressline2")
            Buyer.addressline3=request.POST.get("addressline3")
            Buyer.pin=request.POST.get("pin")
            Buyer.city=request.POST.get("city")
            Buyer.state=request.POST.get("state")
            if(request.FILES.get("pic")):
                Buyer.pic=request.FILES.get("pic")
            Buyer.save()
            return HttpResponseRedirect("/profile/")
            
    Brand = brand.objects.all()
    Subcategory = subcategory.objects.all()
    Maincategory = maincategory.objects.all()
    return render(request,"update.html",{'data':Buyer,'maincategory':Maincategory,'subcategory':Subcategory,'brand':Brand})
        
def addtocart(request,num):
    p=product.objects.get(id=num)
    cart=request.session.get('cart',None)
    cartCount=request.session.get('cartCount',0)
    if(cart):
        if(str(p.id) in cart):
            item=cart[str(p.id)]
            item['qty']=item['qty']+1
            item['total']=item['total']+p.finalprice
            cart[str(p.id)]=item
        else:
            cart.setdefault(str(p.id),{'name':p.name,'color':p.color,'size':p.size,'price':p.finalprice,'qty':1,'total':p.finalprice,'pic':p.pic1.url})
    else:
        cart={str(p.id):{'name':p.name,'color':p.color,'size':p.size,'price':p.finalprice,'qty':1,'total':p.finalprice,'pic':p.pic1.url}}
    request.session['cart']=cart
    total=0
    for value in cart.values():
        total=total+value['total']
    if(total<1000 and total>0):
        shipping=150
    else:
        shipping=0
    request.session['total']=total
    request.session['shipping']=shipping
    request.session['final']=total+shipping
    request.session['cartCount']=cartCount+1
    return HttpResponseRedirect('/cart/')

def cartpage(request):
    cart=request.session.get('cart',None)
    items=[]
    if(cart):
        for key,value in cart.items():
            value.setdefault('id',key)
            items.append(value)
    total=request.session.get('total',0)
    shipping=request.session.get('shipping',0)
    final=request.session.get('final',0)
    Brand = brand.objects.all()
    Subcategory = subcategory.objects.all()
    Maincategory = maincategory.objects.all()
    return render(request,'cart.html',{'cart':items,'Total':total,'shipping':shipping,'final':final,'maincategory':Maincategory,'subcategory':Subcategory,'brand':Brand})

def deletecartpage(request,id):
    cart=request.session.get('cart',None)
    cartCount=0
    if(cart and id in cart):
        del cart[id]
        request.session['cart']=cart
        total=0
        for value in cart.values():
            total=total+value['total']
            cartCount=cartCount+value['qty']
        if(total<1000 and total>0):
            shipping=150
        else:
            shipping=0
        request.session['total']=total
        request.session['shipping']=shipping
        request.session['final']=total+shipping
        request.session['cartCount']=cartCount
    return HttpResponseRedirect('/cart/')

def updatecartpage(request,id,op):
        cart=request.session.get('cart',None)
        cartCount=request.session.get('cartcount',0)
        if(cart and id in cart):
            item=cart[id]
            if(op=='dec' and item['qty']==1):
                pass
            elif(op=='dec'):
                item['qty']=item['qty']-1
                item['total']=item['total']-item['price']
                cartCount=cartCount+1
            else:
                item['qty']=item['qty']+1
                item['total']=item['total']+item['price']
                cartCount=cartCount+1
            cart[id]=item
            request.session['cart']=cart
            request.session['cartCount']=cartCount
            total=0
            for value in cart.values():
                total=total+value['total']
            if(total<1000 and total>0):
                shipping=150
            else:
                shipping=0
            request.session['total']=total
            request.session['shipping']=shipping
            request.session['final']=total+shipping
        return HttpResponseRedirect('/cart/')



@login_required(login_url='/login/')
def addToWishlistPage(request,num):
    user = User.objects.get(username=request.user.username)
    if(user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        Buyer = buyer.objects.get(username=request.user.username)
        Product = product.objects.get(id=num)
        try:
            wishlist = Wishlist.objects.get(user=Buyer,Product=Product)
        except:
            wish = Wishlist()
            wish.user = Buyer
            wish.Product = Product
            wish.save()
        return HttpResponseRedirect("/profile/")

@login_required(login_url='/login/')
def deleteWishlistPage(request,num):
    user = User.objects.get(username=request.user.username)
    if(user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        Buyer = buyer.objects.get(username=request.user.username)
        try:
            wishlist = Wishlist.objects.get(user=Buyer,id=num)
            wishlist.delete()
        except:
            pass
        return HttpResponseRedirect("/profile/")

def forgetPasswordPage1(request):
    if(request.method=="POST"):
        username = request.POST.get("username")
        try:
            user = User.objects.get(username=username)
            if(user.is_superuser):
                return HttpResponseRedirect("/admin/")
            else:
                request.session['resetuser'] = username
                num = randint(100000,999999)
                Buyer = buyer.objects.get(username=username)
                Buyer.otp = num
                Buyer.save() 
                subject = 'OTP for Password Reset- Team Essence'
                message = "OTP for Password Reset is "+str(num)+"\nNever Share Your OTP With Anyone"
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [Buyer.email, ]
                send_mail( subject, message, email_from, recipient_list )
                return HttpResponseRedirect("/forget-2/")
        except:
            messages.error(request,"Invalid Username")
    Brand = brand.objects.all()
    Subcategory = subcategory.objects.all()
    Maincategory = maincategory.objects.all()
    return render(request,"forget-1.html",{'maincategory':Maincategory,'subcategory':Subcategory,'brand':Brand})

def forgetPasswordPage2(request):
    username = request.session.get("resetuser",None)
    if(request.method=="POST" and username):
        otp = request.POST.get("otp")
        try:
            Buyer = buyer.objects.get(username=username)
            if(Buyer.otp == int(otp)):
                request.session['otp']=otp
                return HttpResponseRedirect("/forget-3/")
            else:
                messages.error(request,"Invalid OTP")                
        except:
            messages.error(request,"Invalid OTP")
    Brand = brand.objects.all()
    Subcategory = subcategory.objects.all()
    Maincategory = maincategory.objects.all()
    return render(request,"forget-2.html",{'maincategory':Maincategory,'subcategory':Subcategory,'brand':Brand})

def forgetPasswordPage3(request):
    otp = request.session.get("otp",None)
    if(otp):
        if(request.method=="POST"):
            resetUser = request.session.get("resetuser",None)
            if(resetUser and otp):
                Buyer = buyer.objects.get(username=resetUser)
                if(int(otp)==Buyer.otp):
                    password = request.POST.get("password")
                    cpassword = request.POST.get("cpassword")
                    if(password!=cpassword):
                        messages.error(request,"Password and Confirm Password Doesn't Matched!!!!")
                    else:
                        user = User.objects.get(username=resetUser)
                        user.set_password(password)
                        user.save()
                        subject = 'Password Reset SuccessFully- Team Essence'
                        message = "Your Password Has Been Reset Successfully Now you can login to Your Account"
                        email_from = settings.EMAIL_HOST_USER
                        recipient_list = [Buyer.email, ]
                        send_mail( subject, message, email_from, recipient_list )
                        del request.session['resetuser']
                        del request.session['otp']
                        return HttpResponseRedirect("/login/")
                else:
                    messages.error(request,"Un-Authorised!!!")                
            else:
                messages.error(request,"Un-Authorised!!!")
                Brand = brand.objects.all()
                Subcategory = subcategory.objects.all()
                Maincategory = maincategory.objects.all()
        return render(request,"forget-3.html",{'maincategory':Maincategory,'subcategory':Subcategory,'brand':Brand})
    else:
        return HttpResponseRedirect("/forget-1/")