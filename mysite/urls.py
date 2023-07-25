from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from stocks import views as stocks_view
from users import views as users_view



urlpatterns = [
    path('admin/', admin.site.urls),
    path('stocks/', stocks_view.returnTickerData),
    path('user/create/', users_view.user_registration, name='user-create'),
    path('user/get-user/', users_view.get_user, name='user-create'),
    path('user/delete/', users_view.user_deletion, name='user-deletion'),
    path('user/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/get-tracked-stocks/', stocks_view.get_tracked_stocks, name='get-tracked-stocks'),
    path('user/track-stock/', stocks_view.add_tracked_stock, name='track-stock'),
    path('user/untrack-stock/', stocks_view.delete_tracked_stock, name='untrack-stock'),

]


