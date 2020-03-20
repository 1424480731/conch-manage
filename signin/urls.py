from django.urls import path,include
from signin import views
app_name = 'signin'
urlpatterns = [
    path('login_out/',views.login_out,name='login_out')
]
