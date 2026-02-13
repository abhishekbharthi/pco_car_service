from django.urls import path
from .views import login_view, logout_view, mechanic_dashboard

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('mechanic/dashboard/', mechanic_dashboard, name='mechanic_dashboard'),
]
