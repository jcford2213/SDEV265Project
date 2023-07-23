from django.contrib import admin
from django.urls import path
from stocks import views as stocks_view
from users import views as user_view



urlpatterns = [
    path('admin/', admin.site.urls),
    path('stocks/', stocks_view.returnTickerData),
    path('users/signup_user/', user_view.signup_user),
    path('users/login_user/', user_view.login_user),
    path('users/add_stock/', user_view.add_stock),
    path('users/remove_stock/', user_view.remove_stock)

]


