from django.urls import path

from . import views

from .views import  PostDetailView

urlpatterns = [

	path('', views.Store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),


	path('mens/', views.Men, name='men'),
	path('women/', views.Women, name='women'),
	path('kids/', views.Kids, name='kids'),
	path('electronic/', views.Electronic, name='electronic'),
	path('mobile/', views.Mobile, name='mobile'),
	path('sports/', views.Sports, name='sports'),

	path('search/', views.Search, name='search'),


	path('register/', views.register, name='register'),
    path('login/', views.userlogin, name='login'),
    path('logout/', views.userlogout, name='logout'),

	path('post/<int:pk>/', views.Productdetails, name='post-detail'),


    ]
