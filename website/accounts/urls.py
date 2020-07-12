from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns =[
    path('reset_password/',
         auth_views.PasswordResetView.as_view(),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(),
         name="password_reset_complete"),
    path('', home,name='home'),
    path('register/', registerPage,name='register'),
    path('login/', loginPage,name='login'),
    path('logout/', logoutUser,name='logout'),
    path('user/', userPage,name='userPage'),
    path('customers/<str:pk_test>/', customers,name='customer'),
    path('products/', products,name='product'),
    path('create/<str:pk_test>/',createOrder,name='createOrder'),
    path('updateorder/<str:pk>/',updateOrder,name='updateorder'),
    path('deleteorder/<str:pk>/',deleteOrder,name='deleteorder'),
    path('account/',accountSettings,name='accounts'),
]



