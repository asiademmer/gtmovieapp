from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views

from accounts.views import ResetPassword, ChangePassword

urlpatterns = [
    path('signup', views.signup, name='accounts.signup'),
    path('login/', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),

    path('orders/', views.orders, name='accounts.orders'),

    path('password-reset/', ResetPassword.as_view(template_name='accounts/password_reset.html'), name='password_reset'),

    path('password-reset-sent/', ResetPassword.as_view(template_name='home/index.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),

    path('password-change/', ChangePassword.as_view(), name='password_change'),
]

