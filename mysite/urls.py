from django.contrib import admin
from django.urls import path
from stocks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('stocks/', views.returnGetMessage),
    path('stocks/', views.returnTickerData),
]


