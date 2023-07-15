
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "CHAUHAN"
admin.site.site_title = "Essence Admin Portal"
admin.site.index_title = "Welcome to Essence Admin Portal"

from mainapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('checkout/',views.checkoutpage),
    path('contact/',views.contact),
    path('shop/<str:mc>/<str:sc>/<str:br>/',views.shop),
    path('singleproduct/<int:num>/',views.singleproduct),
    path('login/',views.loginpage),
    path('signup/',views.signup),
    path('logout/',views.logoutpage),
    path('profile/',views.profile),
    path('update/',views.updatepage),
    path('add-to-cart/<int:num>/',views.addtocart),
    path('cart/',views.cartpage),
    path('delete-cart/<str:id>/',views.deletecartpage),
    path('update-cart/<str:id>/<str:op>/',views.updatecartpage),
    path('placeorder/',views.placeorder),
    path('confirmation/',views.confirmationpage),
    path('add-to-wishlist/<int:num>/',views.addToWishlistPage),
    path('delete-wishlist/<int:num>/',views.deleteWishlistPage),
    path('forget-1/',views.forgetPasswordPage1),
    path('forget-2/',views.forgetPasswordPage2),
    path('forget-3/',views.forgetPasswordPage3),
    path('paymentSuccess/<str:rppid>/<str:rpoid>/<str:rpsid>/',views.paymentsuccess),
   
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
