from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home,name='home'),
    path('about/', views.About,name='about'),
    path('sign-up/', views.SignUpView, name='sign-up'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('account-verify/<slug:token>',views.account_verify, name='account_verify')
   
]