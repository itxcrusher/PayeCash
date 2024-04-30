from django.urls import path
from .views import SignUpView

app_name = 'register'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
]
