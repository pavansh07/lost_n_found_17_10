# klh_lost_and_found/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.root_redirect, name='root'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add_item/', views.add_item, name='add_item'),
    path('items/', views.item_list, name='item_list'),
    path('lost_items/', views.lost_items, name='lost_items'),
    path('found_items/', views.found_items, name='found_items'),
    path('claim/<int:item_id>/', views.claim_item, name='claim_item'),
    # path('chatbot/', views.chatbot_page, name='chatbot_page'),
    # path('chatbot_api/', views.chatbot_view, name='chatbot_view'),
]

