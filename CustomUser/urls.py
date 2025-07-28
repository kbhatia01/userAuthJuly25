from django.urls import path

from CustomUser import views
from CustomUser.views import CustomTokenView

urlpatterns = [
    path('user_signup/', views.signup, name='user_signup'),
    path('login/', views.login, name='login'),
    path('token/', CustomTokenView.as_view(), name='token_obtain_pair'),
]