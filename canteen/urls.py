"""
URL configuration for canteen project.

The `urlpatterns` list routes URLs to  For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from uapcanteen.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('userprofile/', userprofile, name='userprofile'),
    path('dashboard/', dashboard, name='dashboard'),
    path('trackorder/', trackorder, name='trackorder'),
    path('getmessage/', getmessage, name='getmessage'),
    path('update_order/<int:order_id>/', update_order, name='update_order'),
    path('ownerlogin/', ownerlogin, name='ownerlogin'),
    path('ownerlogout/', ownerlogout, name='ownerlogout'),
    path('breakfast/', breakfast, name='breakfast'),
    path('breakfast/<int:id>/', breakfast_detail, name='breakfast_detail'),
    path('lunch/', lunch, name='lunch'),
    path('lunch/<int:id>/', lunch_detail, name='lunch_detail'),
    path('dinner/', dinner, name='dinner'),
    path('dinner/<int:id>/', dinner_detail, name='dinner_detail'),
    path('upload_breakfast/', upload_breakfast, name='upload_breakfast'),
    path('upload_lunch/', upload_lunch, name='upload_lunch'),
    path('upload_dinner/', upload_dinner, name='upload_dinner'),
    path('add_to_cart/<str:item_type>/<int:item_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('update_quantity/<int:cart_item_id>/<str:action>/', update_quantity, name='update_quantity'),
    path('view_cart/', view_cart, name='view_cart'),
    path('checkout/', checkout, name='checkout'),
    path('proceed_to_checkout/', proceed_to_checkout, name='proceed_to_checkout'),
    path('Purchase/', Purchase, name='Purchase'),
    path('orderconfirm/', orderconfirm, name='orderconfirm'),

    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()