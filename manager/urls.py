from django.urls import path,include

from manager import views
app_name = 'manager'
urlpatterns = [
    path('plugin', views.plugin,name='plugin'),
    path('data', views.data,name='data'),
    path('run',views.run,name='run'),
    path('stop',views.stop,name='stop'),
    path('area_district',views.area_district,name='area_district'),
    path('search',views.search,name='search')
]
