from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import SignupAPIView, ForgotPasswordAPIView, ChangePasswordAPIView, LogoutAPIView,EditProfileView
from . import views

# from .views import CustomPasswordResetView

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot_password'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change_password'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('editprofile/<int:pk>',EditProfileView.as_view(),name='editprofile'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    
    # path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    # path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]




# from django.urls import path
# from . import views

# urlpatterns = [
#     path('signup/', views.signup, name='signup'),
#     path('login/', views.login, name='login'),
#     path('protected/', views.protected_page, name='protected-page'),
# ]