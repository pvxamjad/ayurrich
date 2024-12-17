from django.contrib import admin
from django.urls import path,include
from . import settings
from django.conf.urls.static import static





urlpatterns = [
    path('ayurrichperadmin/', admin.site.urls),
    path('',include('ar_store.urls')),
    path('cart/',include('ar_cart.urls')),
    path('billing/',include('ar_payment.urls')),
    path('aradmin/',include('ar_admin.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
