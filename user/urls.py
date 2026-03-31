from django.urls import path
from .views import signup_view
from .views import login_view
from .views import logout_view
from .views import home_view
from .views import password_reset_view

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('logout/', logout_view, name='logout'),
    path('password-reset/', password_reset_view, name='password_reset'),
]