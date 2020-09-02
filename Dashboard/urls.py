from django.urls import path
from . import views


urlpatterns = [
    
   path('', views.dashboard, name="dashboard"), 
   path('about', views.about, name="about"), 
   path('research', views.research, name="research"), 
   path('featured_story', views.featured_story, name="featured_story"), 
   path('<int:post_id>/delete', views.delete, name="delete"),
   path('post_message', views.post_mess, name="post_mess"),
   path('add_comment/<int:id>', views.post_comment, name="post_comment"),
   path('like/<int:id>', views.add_like, name="add_like"),
   path('delete/<int:id>', views.delete_comment, name="delete_comment"),
   path('delete_chassis/<int:car_id>', views.delete_chassis, name="delete_chassis"),
   path('add_chassis/<int:car_id>', views.add_chassis, name="add_chassis"),
   path('chassis_page/<int:car_id>', views.chassis_page, name="chassis_page"),
   path('message_board/', views.message_board, name="message_board"),
   path('message_page/<int:id>', views.message_page, name="message_page"),
   path('user_profile/<int:id>', views.user_profile, name="user_profile"),
   path('edit_profile/<int:id>', views.edit_profile, name="edit_profile"),
   path('edit_chassis/<int:id>', views.edit_chassis, name="edit_chassis"),
   path('contact/', views.contact, name="contact"),
   
   
   
    
]