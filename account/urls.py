from django.urls import path, include
from django.contrib.auth import views as auth_views
# 
from . import views
urlpatterns = [
    # previous login url
    # path('login/', views.user_login, name='login'),
    # login / logout urls
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # # change password urls
    # path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    # path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # # reset password urls
    # path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('ppassword-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # 173 => 200
    path('', include('django.contrib.auth.urls')),
    # تلك Django.contrib.auth.urls هي عناوين url نفسها. مما يعني أنه عند تضمينها ، فإنها تتضمن تلقائيًا بعض
    # عناوين url المضمنة في django على سبيل المثال ، تسجيل الدخول ، التسجيل ، إعادة تعيين كلمة المرور ،
    # تأكيد إعادة تعيين كلمة المرور ، إلخ. وجهات النظر الخاصة.
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    
    # Chapter => 7 following Users
    path('users/', views.user_list, name='user_list'),
    path('user/<username>', views.user_detail, name='user_detail'),
    path('users/follow/', views.user_follow, name='user_follow'),
]