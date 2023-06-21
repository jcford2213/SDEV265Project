from django.contrib import admin
from django.urls import path
from TradePlace import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Dashboard, name='dashboard'),
    path('account/', views.Account, name='account'),
    path('ticker/', views.Ticker, name='ticker'),
]

