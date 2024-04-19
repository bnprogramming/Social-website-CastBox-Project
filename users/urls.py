from django.urls import path
from users.views import UserRegisterView, UserLoginView, UserLogoutView, UserEditProfileView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register_page'),
    path('login', UserLoginView.as_view(), name='login_page'),
    path('logout', UserLogoutView.as_view(), name='logout_page'),
    path('user-edit-profile/', UserEditProfileView.as_view(), name='edit_profile_view'),
]