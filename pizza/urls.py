from django.urls import path
from . import views
app_name = 'pizza'

urlpatterns = [
	path('home/', views.home, name='home'),
	path('create/', views.create_pizza, name='create_pizza'),
	path('index/', views.PizzaIndex.as_view(), name='pizza_index'),
	path('<int:pk>/details/', views.PizzaDetails.as_view(), name='pizza_details'),
	path('index/date_filter/<int:filter>/', views.PizzaIndexFilter.as_view(), name='index_date_filter'),
]